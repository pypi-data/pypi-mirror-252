import hashlib
import json
import os
import pickle
import shutil
import string
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from office365.sharepoint.client_context import (
    ClientContext,
    ClientCredential,
    UserCredential,
)
from pytrie import StringTrie
from requests.models import Response
from simple_salesforce import Salesforce
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.engine.base import Connection as sqlConn
from thirdai import bolt
from thirdai.data import get_udt_col_types
from thirdai.dataset.data_source import PyDataSource

from .connectors import SalesforceConnector, SharePointConnector, SQLConnector
from .constraint_matcher import ConstraintMatcher, ConstraintValue, Filter, to_filters
from .parsing_utils import doc_parse, pdf_parse, sliding_pdf_parse, url_parse
from .utils import hash_file, hash_string, requires_condition


class Reference:
    pass


def _raise_unknown_doc_error(element_id: int):
    raise ValueError(f"Unable to find document that has id {element_id}.")


class Document:
    @property
    def size(self) -> int:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def hash(self) -> str:
        sha1 = hashlib.sha1()
        sha1.update(bytes(self.name, "utf-8"))
        for i in range(self.size):
            sha1.update(bytes(self.reference(i).text, "utf-8"))
        return sha1.hexdigest()

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        raise NotImplementedError()

    def all_entity_ids(self) -> List[int]:
        raise NotImplementedError()

    def filter_entity_ids(self, filters: Dict[str, Filter]):
        return self.all_entity_ids()

    def id_map(self) -> Optional[Dict[str, int]]:
        return None

    # This attribute allows certain things to be saved or not saved during
    # the pickling of a savable_state object. For example, if we set this
    # to True for CSV docs, we will save the actual csv file in the pickle.
    # Utilize this property in save_meta and load_meta of document objs.
    @property
    def save_extra_info(self) -> bool:
        return self._save_extra_info

    @save_extra_info.setter
    def save_extra_info(self, value: bool):
        self._save_extra_info = value

    def reference(self, element_id: int) -> Reference:
        raise NotImplementedError()

    def strong_text(self, element_id: int) -> str:
        return self.reference(element_id).text

    def weak_text(self, element_id: int) -> str:
        return self.reference(element_id).text

    def context(self, element_id: int, radius: int) -> str:
        window_start = max(0, element_id - radius)
        window_end = min(self.size, element_id + radius + 1)
        return " \n".join(
            [self.reference(elid).text for elid in range(window_start, window_end)]
        )

    def save_meta(self, directory: Path):
        pass

    def load_meta(self, directory: Path):
        pass

    def row_iterator(self):
        for i in range(self.size):
            yield DocumentRow(
                element_id=i,
                strong=self.strong_text(i),
                weak=self.weak_text(i),
            )

    def save(self, directory: str):
        dirpath = Path(directory)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        with open(dirpath / f"doc.pkl", "wb") as pkl:
            pickle.dump(self, pkl)
        os.mkdir(dirpath / "meta")
        self.save_meta(dirpath / "meta")

    @staticmethod
    def load(directory: str):
        dirpath = Path(directory)
        with open(dirpath / f"doc.pkl", "rb") as pkl:
            obj = pickle.load(pkl)
        obj.load_meta(dirpath / "meta")
        return obj


class Reference:
    def __init__(
        self,
        document: Document,
        element_id: int,
        text: str,
        source: str,
        metadata: dict,
        upvote_ids: List[int] = None,
    ):
        self._id = element_id
        self._upvote_ids = upvote_ids if upvote_ids is not None else [element_id]
        self._text = text
        self._source = source
        self._metadata = metadata
        self._context_fn = lambda radius: document.context(element_id, radius)
        self._score = 0

    @property
    def id(self):
        return self._id

    @property
    def upvote_ids(self):
        return self._upvote_ids

    @property
    def text(self):
        return self._text

    @property
    def source(self):
        return self._source

    @property
    def metadata(self):
        return self._metadata

    @property
    def score(self):
        return self._score

    def context(self, radius: int):
        return self._context_fn(radius)

    def __eq__(self, other):
        if isinstance(other, Reference):
            return (
                self.id == other.id
                and self.text == other.text
                and self.source == other.source
            )
        return False


class DocumentRow:
    def __init__(self, element_id: int, strong: str, weak: str):
        self.id = element_id
        self.strong = strong
        self.weak = weak


DocAndOffset = Tuple[Document, int]


class DocumentDataSource(PyDataSource):
    def __init__(self, id_column, strong_column, weak_column):
        PyDataSource.__init__(self)
        self.documents: List[DocAndOffset] = []
        for col in [id_column, strong_column, weak_column]:
            if '"' in col or "," in col:
                raise RuntimeError(
                    "DocumentDataSource columns cannot contain '\"' or ','"
                )
        self.id_column = id_column
        self.strong_column = strong_column
        self.weak_column = weak_column
        self._size = 0
        self.restart()

    def add(self, document: Document, start_id: int):
        self.documents.append((document, start_id))
        self._size += document.size

    def row_iterator(self):
        for doc, start_id in self.documents:
            for row in doc.row_iterator():
                row.id = row.id + start_id
                yield row

    @property
    def size(self):
        return self._size

    def _csv_line(self, element_id: str, strong: str, weak: str):
        csv_strong = '"' + strong.replace('"', '""') + '"'
        csv_weak = '"' + weak.replace('"', '""') + '"'
        return f"{element_id},{csv_strong},{csv_weak}"

    def _get_line_iterator(self):
        # First yield the header
        yield f"{self.id_column},{self.strong_column},{self.weak_column}"
        # Then yield rows
        for row in self.row_iterator():
            yield self._csv_line(element_id=row.id, strong=row.strong, weak=row.weak)

    def resource_name(self) -> str:
        return "Documents:\n" + "\n".join([doc.name for doc, _ in self.documents])

    def save(self, path: Path, save_interval=100_000):
        """
        DocumentDataSource is agnostic to the documents that are a part of it as the line_iterator is agnostic to the kind of document and returns data in a specific format. Hence, to serialize DocumentDataSource, we do not need to serialize the documents but rather, dump the lines yielded by the line iterator into a CSV. This makes the saving and loading logic simpler.
        """
        path.mkdir(exist_ok=True, parents=True)
        number_lines_in_buffer = 0
        with open(path / "source.csv", "w") as f:
            for line in self._get_line_iterator():
                f.write(line + "\n")
                number_lines_in_buffer += 1
            if number_lines_in_buffer > save_interval:
                f.flush()
                number_lines_in_buffer = 0

        with open(path / "arguments.json", "w") as f:
            json.dump(
                {
                    "id_column": self.id_column,
                    "strong_column": self.strong_column,
                    "weak_column": self.weak_column,
                },
                f,
                indent=4,
            )
        self.restart()

    @staticmethod
    def load(path: Path):
        with open(path / "arguments.json", "r") as f:
            args = json.load(f)

        csv_document = CSV(
            path=path / "source.csv",
            id_column=args["id_column"],
            strong_columns=[args["strong_column"]],
            weak_columns=[args["weak_column"]],
            has_offset=True,
        )
        data_source = DocumentDataSource(**args)
        data_source.add(csv_document, start_id=0)
        return data_source


class IntroAndTrainDocuments:
    def __init__(self, intro: DocumentDataSource, train: DocumentDataSource) -> None:
        self.intro = intro
        self.train = train


class DocumentManager:
    def __init__(self, id_column, strong_column, weak_column) -> None:
        self.id_column = id_column
        self.strong_column = strong_column
        self.weak_column = weak_column

        # After python 3.8, we don't need to use OrderedDict as Dict is ordered by default
        self.registry: OrderedDict[str, DocAndOffset] = OrderedDict()
        self.source_id_prefix_trie = StringTrie()
        self.constraint_matcher = ConstraintMatcher[DocAndOffset]()

    def _next_id(self):
        if len(self.registry) == 0:
            return 0
        doc, start_id = next(reversed(self.registry.values()))
        return start_id + doc.size

    def add(self, documents: List[Document]):
        intro = DocumentDataSource(self.id_column, self.strong_column, self.weak_column)
        train = DocumentDataSource(self.id_column, self.strong_column, self.weak_column)
        for doc in documents:
            doc_hash = doc.hash
            if doc_hash not in self.registry:
                start_id = self._next_id()
                doc_and_id = (doc, start_id)
                self.registry[doc_hash] = doc_and_id
                self.source_id_prefix_trie[doc_hash] = doc_hash
                intro.add(doc, start_id)
                self.constraint_matcher.index(
                    item=(doc, start_id), constraints=doc.matched_constraints
                )
            doc, start_id = self.registry[doc_hash]
            train.add(doc, start_id)

        return IntroAndTrainDocuments(intro=intro, train=train), [
            doc.hash for doc in documents
        ]

    def delete(self, source_id):
        # TODO(Geordie): Error handling
        doc, offset = self.registry[source_id]
        deleted_entities = [offset + entity_id for entity_id in doc.all_entity_ids()]
        del self.registry[source_id]
        del self.source_id_prefix_trie[source_id]
        self.constraint_matcher.delete((doc, offset), doc.matched_constraints)
        return deleted_entities

    def entity_ids_by_constraints(self, constraints: Dict[str, Any]):
        filters = to_filters(constraints)
        return [
            start_id + entity_id
            for doc, start_id in self.constraint_matcher.match(filters)
            for entity_id in doc.filter_entity_ids(filters)
        ]

    def sources(self):
        return {doc_hash: doc for doc_hash, (doc, _) in self.registry.items()}

    def match_source_id_by_prefix(self, prefix: str) -> Document:
        if prefix in self.registry:
            return [prefix]
        return self.source_id_prefix_trie.values(prefix)

    def source_by_id(self, source_id: str):
        return self.registry[source_id]

    def clear(self):
        self.registry = OrderedDict()
        self.source_id_prefix_trie = StringTrie()

    def _get_doc_and_start_id(self, element_id: int):
        for doc, start_id in reversed(self.registry.values()):
            if start_id <= element_id:
                return doc, start_id

        _raise_unknown_doc_error(element_id)

    def reference(self, element_id: int):
        doc, start_id = self._get_doc_and_start_id(element_id)
        doc_ref = doc.reference(element_id - start_id)
        doc_ref._id = element_id
        doc_ref._upvote_ids = [start_id + uid for uid in doc_ref._upvote_ids]
        return doc_ref

    def context(self, element_id: int, radius: int):
        doc, start_id = self._get_doc_and_start_id(element_id)
        return doc.context(element_id - start_id, radius)

    def get_data_source(self) -> DocumentDataSource:
        data_source = DocumentDataSource(
            id_column=self.id_column,
            strong_column=self.strong_column,
            weak_column=self.weak_column,
        )

        for doc, start_id in self.registry.values():
            data_source.add(document=doc, start_id=start_id)

        return data_source

    def save_meta(self, directory: Path):
        for i, (doc, _) in enumerate(self.registry.values()):
            subdir = directory / str(i)
            os.mkdir(subdir)
            doc.save_meta(subdir)

    def load_meta(self, directory: Path):
        for i, (doc, _) in enumerate(self.registry.values()):
            subdir = directory / str(i)
            doc.load_meta(subdir)

        if not hasattr(self, "doc_constraints"):
            self.constraint_matcher = ConstraintMatcher[DocAndOffset]()
            for item in self.registry.values():
                self.constraint_matcher.index(item, item[0].matched_constraints)


def safe_has_offset(this):
    """Checks the value of the "has_offset" attribute of a class.
    Defaults to False when the attribute does not exist.
    This function is needed for backwards compatibility reasons.
    """
    if hasattr(this, "has_offset"):
        return this.has_offset
    return False


class CSV(Document):
    """
    A document containing the rows of a csv file.

    Args:
        path (str): The path to the csv file.
        id_column (Optional[str]). Optional, defaults to None. If provided then the
            ids in this column are used to identify the rows in NeuralDB. If not provided
            then ids are assigned.
        strong_columns (Optional[List[str]]): Optional, defaults to None. This argument
            can be used to provide NeuralDB with information about which columns are
            likely to contain the strongest signal in matching with a given query. For
            example this could be something like the name of a product.
        weak_columns (Optional[List[str]]): Optional, defaults to None. This argument
            can be used to provide NeuralDB with information about which columns are
            likely to contain weaker signals in matching with a given query. For
            example this could be something like the description of a product.
        reference_columns (Optional[List[str]]): Optional, defaults to None. If provided
            the specified columns are returned by NeuralDB as responses to queries. If
            not specifed all columns are returned.
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def valid_id_column(column):
        return (
            (len(column.unique()) == len(column))
            and (column.min() == 0)
            and (column.max() == len(column) - 1)
        )

    def __init__(
        self,
        path: str,
        id_column: Optional[str] = None,
        strong_columns: Optional[List[str]] = None,
        weak_columns: Optional[List[str]] = None,
        reference_columns: Optional[List[str]] = None,
        save_extra_info=True,
        metadata={},
        index_columns=[],
        has_offset=False,
    ) -> None:
        self.df = pd.read_csv(path)

        # This variable is used to check whether the id's in the CSV are supposed to start with 0 or with some custom offset. We need the latter when we shard the datasource.
        self.has_offset = has_offset

        if reference_columns is None:
            reference_columns = list(self.df.columns)

        self.orig_to_assigned_id = None
        self.id_column = id_column
        orig_id_column = id_column
        if self.id_column and (
            has_offset or CSV.valid_id_column(self.df[self.id_column])
        ):
            self.df = self.df.sort_values(self.id_column)
        else:
            self.id_column = "thirdai_index"
            self.df[self.id_column] = range(self.df.shape[0])
            if orig_id_column:
                self.orig_to_assigned_id = {
                    row[orig_id_column]: row[self.id_column]
                    for _, row in self.df.iterrows()
                }

        if strong_columns is None and weak_columns is None:
            # autotune column types
            text_col_names = []
            try:
                for col_name, udt_col_type in get_udt_col_types(path).items():
                    if type(udt_col_type) == type(bolt.types.text()):
                        text_col_names.append(col_name)
            except:
                text_col_names = list(self.df.columns)
                text_col_names.remove(self.id_column)
                if orig_id_column:
                    text_col_names.remove(orig_id_column)
                self.df[text_col_names] = self.df[text_col_names].astype(str)
            strong_columns = []
            weak_columns = text_col_names
        elif strong_columns is None:
            strong_columns = []
        elif weak_columns is None:
            weak_columns = []

        for col in strong_columns + weak_columns:
            self.df[col] = self.df[col].fillna("")

        # So we can do df.loc[]
        self.df = self.df.set_index(self.id_column)

        self.path = Path(path)
        self.strong_columns = strong_columns
        self.weak_columns = weak_columns
        self.reference_columns = [
            col for col in reference_columns if col != self.df.index.name
        ]
        self._save_extra_info = save_extra_info
        self.doc_metadata = metadata
        self.doc_metadata_keys = set(self.doc_metadata.keys())
        self.indexed_columns = index_columns
        # Add column names to hash metadata so that CSVs with different
        # hyperparameters are treated as different documents. Otherwise, this
        # may break training.
        self._hash = hash_file(
            path,
            metadata="csv-"
            + str(self.id_column)
            + str(sorted(self.strong_columns))
            + str(sorted(self.weak_columns))
            + str(sorted(self.reference_columns))
            + str(sorted(self.indexed_columns))
            + str(sorted(list(self.doc_metadata.items()))),
        )

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def size(self) -> int:
        return len(self.df)

    @property
    def name(self) -> str:
        return self.path.name

    @requires_condition(
        check_func=lambda self: not safe_has_offset(self),
        method_name="matched_constraints",
        method_class="CSV(Document)",
        condition_unmet_string=" when there is an offset in the CSV document",
    )
    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        metadata_constraints = {
            key: ConstraintValue(value) for key, value in self.doc_metadata.items()
        }
        indexed_column_constraints = {
            key: ConstraintValue(is_any=True) for key in self.indexed_columns
        }
        return {**metadata_constraints, **indexed_column_constraints}

    def all_entity_ids(self) -> List[int]:
        return self.df.index.to_list()

    def filter_entity_ids(self, filters: Dict[str, Filter]):
        df = self.df
        row_filters = {
            k: v for k, v in filters.items() if k not in self.doc_metadata_keys
        }
        for column_name, filterer in row_filters.items():
            if column_name not in self.df.columns:
                return []
            df = filterer.filter_df_column(df, column_name)
        return df.index.to_list()

    def id_map(self) -> Optional[Dict[str, int]]:
        return self.orig_to_assigned_id

    def strong_text_from_row(self, row) -> str:
        return " ".join(getattr(row, col) for col in self.strong_columns)

    def strong_text(self, element_id: int) -> str:
        row = self.df.loc[element_id]
        return self.strong_text_from_row(row)

    def weak_text_from_row(self, row) -> str:
        return " ".join(getattr(row, col) for col in self.weak_columns)

    def weak_text(self, element_id: int) -> str:
        row = self.df.loc[element_id]
        return self.weak_text_from_row(row)

    def row_iterator(self):
        for row in self.df.itertuples():
            yield DocumentRow(
                element_id=row.Index,
                strong=self.strong_text_from_row(row),
                weak=self.weak_text_from_row(row),
            )

    @requires_condition(
        check_func=lambda self: not safe_has_offset(self),
        method_name="reference",
        method_class="CSV(Document)",
        condition_unmet_string=" when there is an offset in the CSV document",
    )
    def reference(self, element_id: int) -> Reference:
        if element_id >= len(self.df):
            _raise_unknown_doc_error(element_id)
        row = self.df.loc[element_id]
        text = "\n\n".join([f"{col}: {row[col]}" for col in self.reference_columns])
        return Reference(
            document=self,
            element_id=element_id,
            text=text,
            source=str(self.path.absolute()),
            metadata={**row.to_dict(), **self.doc_metadata},
        )

    def context(self, element_id: int, radius) -> str:
        rows = self.df.loc[
            max(0, element_id - radius) : min(len(self.df), element_id + radius + 1)
        ]

        return " ".join(
            [
                "\n\n".join([f"{col}: {row[col]}" for col in self.reference_columns])
                for _, row in rows.iterrows()
            ]
        )

    def __getstate__(self):
        state = self.__dict__.copy()

        # Remove the path attribute because it is not cross platform compatible
        del state["path"]

        # Save the filename so we can load it with the same name
        state["doc_name"] = self.name

        # End pickling functionality here to support old directory checkpoint save
        return state

    def __setstate__(self, state):
        # Add new attributes to state for older document object version backward compatibility
        if "_save_extra_info" not in state:
            state["_save_extra_info"] = True

        self.__dict__.update(state)

    @requires_condition(
        check_func=lambda self: not safe_has_offset(self),
        method_name="save_meta",
        method_class="CSV(Document)",
        condition_unmet_string=" when there is an offset in the CSV document",
    )
    def save_meta(self, directory: Path):
        # Let's copy the original CSV file to the provided directory
        if self.save_extra_info:
            shutil.copy(self.path, directory)

    @requires_condition(
        check_func=lambda self: not safe_has_offset(self),
        method_name="load_meta",
        method_class="CSV(Document)",
        condition_unmet_string=" when there is an offset in the CSV document",
    )
    def load_meta(self, directory: Path):
        # Since we've moved the CSV file to the provided directory, let's make
        # sure that we point to this CSV file.
        if hasattr(self, "doc_name"):
            self.path = directory / self.doc_name
        else:
            # this else statement handles the deprecated attribute "path" in self, we can remove this soon
            self.path = directory / self.path.name

        if not hasattr(self, "doc_metadata"):
            self.doc_metadata = {}
        if not hasattr(self, "doc_metadata_keys"):
            self.doc_metadata_keys = set()
        if not hasattr(self, "indexed_columns"):
            self.indexed_columns = []
        if not hasattr(self, "orig_to_assigned_id"):
            self.orig_to_assigned_id = None
        if not hasattr(self, "has_offset"):
            self.has_offset = False

        # So we can do df.loc[]
        if self.df.index.name != self.id_column:
            self.df = self.df.set_index(self.id_column)
            self.reference_columns = [
                col for col in self.reference_columns if col != self.id_column
            ]


# Base class for PDF, DOCX and Unstructured classes because they share the same logic.
class Extracted(Document):
    def __init__(
        self, path: str, save_extra_info=True, metadata={}, strong_column=None
    ):
        path = str(path)
        self.df = self.process_data(path)
        self.hash_val = hash_file(path, metadata="extracted-" + str(metadata))
        self._save_extra_info = save_extra_info

        self.path = Path(path)
        self.doc_metadata = metadata
        self.strong_column = strong_column
        if self.strong_column and self.strong_column not in self.df.columns:
            raise RuntimeError(
                f"Strong column '{self.strong_column}' not found in the dataframe."
            )

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        raise NotImplementedError()

    @property
    def hash(self) -> str:
        return self.hash_val

    @property
    def size(self) -> int:
        return len(self.df)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        return {key: ConstraintValue(value) for key, value in self.doc_metadata.items()}

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def strong_text(self, element_id: int) -> str:
        return (
            ""
            if not self.strong_column
            else self.df[self.strong_column].iloc[element_id]
        )

    def weak_text(self, element_id: int) -> str:
        return self.df["para"].iloc[element_id]

    def show_fn(text, source, **kwargs):
        return text

    def reference(self, element_id: int) -> Reference:
        if element_id >= len(self.df):
            _raise_unknown_doc_error(element_id)
        return Reference(
            document=self,
            element_id=element_id,
            text=self.df["display"].iloc[element_id],
            source=str(self.path.absolute()),
            metadata={**self.df.iloc[element_id].to_dict(), **self.doc_metadata},
        )

    def context(self, element_id, radius) -> str:
        if not 0 <= element_id or not element_id < self.size:
            raise ("Element id not in document.")

        rows = self.df.iloc[
            max(0, element_id - radius) : min(len(self.df), element_id + radius + 1)
        ]
        return "\n".join(rows["para"])

    def __getstate__(self):
        state = self.__dict__.copy()

        # Remove filename attribute because this is a deprecated attribute for Extracted
        if "filename" in state:
            del state["filename"]

        # In older versions of neural_db, we accidentally stored Path objects in the df.
        # This changes those objects to a string, because PosixPath can't be loaded in Windows
        def path_to_str(element):
            if isinstance(element, Path):
                return element.name
            return element

        state["df"] = state["df"].applymap(path_to_str)

        # Remove the path attribute because it is not cross platform compatible
        del state["path"]

        # Save the filename so we can load it with the same name
        state["doc_name"] = self.name

        return state

    def __setstate__(self, state):
        # Add new attributes to state for older document object version backward compatibility
        if "_save_extra_info" not in state:
            state["_save_extra_info"] = True
        if "filename" in state:
            state["path"] = state["filename"]

        self.__dict__.update(state)

    def save_meta(self, directory: Path):
        # Let's copy the original file to the provided directory
        if self.save_extra_info:
            shutil.copy(self.path, directory)

    def load_meta(self, directory: Path):
        # Since we've moved the file to the provided directory, let's make
        # sure that we point to this file.
        if hasattr(self, "doc_name"):
            self.path = directory / self.doc_name
        else:
            # this else statement handles the deprecated attribute "path" in self, we can remove this soon
            self.path = directory / self.path.name

        if not hasattr(self, "doc_metadata"):
            self.doc_metadata = {}

        if not hasattr(self, "strong_column"):
            self.strong_column = None


def process_pdf(path: str) -> pd.DataFrame:
    elements, success = pdf_parse.process_pdf_file(path)

    if not success:
        raise ValueError(f"Could not read PDF file: {path}")

    elements_df = pdf_parse.create_train_df(elements)

    return elements_df


def process_docx(path: str) -> pd.DataFrame:
    elements, success = doc_parse.get_elements(path)

    if not success:
        raise ValueError(f"Could not read DOCX file: {path}")

    elements_df = doc_parse.create_train_df(elements)

    return elements_df


class PDF(Extracted):
    """
    Parses a PDF document into chunks of text that can be indexed by NeuralDB.

    Args:
        path (str): path to PDF file
        chunk_size (int): The number of words in each chunk of text. Defaults to 100
        stride (int): The number of words between each chunk of text. When stride <
            chunk_size, the text chunks overlap. When stride = chunk_size, the
            text chunks do not overlap. Defaults to 40 so adjacent chunks have a
            60% overlap.
        emphasize_first_words (int): The number of words at the beginning of the
            document to be passed into NeuralDB as a strong signal. For example,
            if your document starts with a descriptive title that is 3 words long,
            then you can set emphasize_first_words to 3 so that NeuralDB captures
            this strong signal. Defaults to 0.
        ignore_header_footer (bool): whether the parser should remove headers and
            footers. Defaults to True; headers and footers are removed by
            default.
        ignore_nonstandard_orientation (bool): whether the parser should remove lines
            of text that have a nonstandard orientation, such as margins that
            are oriented vertically. Defaults to True; lines with nonstandard
            orientation are removed by default.
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def __init__(
        self,
        path: str,
        version: str = "v1",
        chunk_size=100,
        stride=40,
        emphasize_first_words=0,
        ignore_header_footer=True,
        ignore_nonstandard_orientation=True,
        metadata={},
    ):
        self.version = version

        if version == "v1":
            super().__init__(path=path, metadata=metadata)
            return

        if version != "v2":
            raise ValueError(
                f"Received invalid version '{version}'. Choose between 'v1' and 'v2'"
            )

        self.chunk_size = chunk_size
        self.stride = stride
        self.emphasize_first_words = emphasize_first_words
        self.ignore_header_footer = ignore_header_footer
        self.ignore_nonstandard_orientation = ignore_nonstandard_orientation
        # Add pdf version, chunk size, and stride metadata. The metadata will be
        # incorporated in the document hash so that the same PDF inserted with
        # different hyperparameters are treated as different documents.
        # Otherwise, this may break training.
        super().__init__(
            path=path,
            metadata={
                **metadata,
                "__version__": "v2",
                "__chunk_size__": chunk_size,
                "__stride__": stride,
            },
            strong_column="emphasis",
        )

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        if not hasattr(self, "version") or self.version == "v1":
            return process_pdf(path)
        return sliding_pdf_parse.make_df(
            path,
            self.chunk_size,
            self.stride,
            self.emphasize_first_words,
            self.ignore_header_footer,
            self.ignore_nonstandard_orientation,
        )

    @staticmethod
    def highlighted_doc(reference: Reference):
        old_highlights = pdf_parse.highlighted_doc(reference.source, reference.metadata)
        if old_highlights:
            return old_highlights
        return sliding_pdf_parse.highlighted_doc(reference.source, reference.metadata)


class DOCX(Extracted):
    def __init__(self, path: str, metadata={}):
        super().__init__(path=path, metadata=metadata)

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        return process_docx(path)


class Unstructured(Extracted):
    def __init__(
        self, path: Union[str, Path], save_extra_info: bool = True, metadata={}
    ):
        super().__init__(path=path, save_extra_info=save_extra_info, metadata=metadata)

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        if path.endswith(".pdf") or path.endswith(".docx"):
            raise NotImplementedError(
                "For PDF and DOCX FileTypes, use neuraldb.PDF and neuraldb.DOCX "
            )
        elif path.endswith(".pptx"):
            from .parsing_utils.unstructured_parse import PptxParse

            self.parser = PptxParse(path)

        elif path.endswith(".txt"):
            from .parsing_utils.unstructured_parse import TxtParse

            self.parser = TxtParse(path)

        elif path.endswith(".eml"):
            from .parsing_utils.unstructured_parse import EmlParse

            self.parser = EmlParse(path)

        else:
            raise Exception(f"File type is not yet supported")

        elements, success = self.parser.process_elements()

        if not success:
            raise ValueError(f"Could not read file: {path}")

        return self.parser.create_train_df(elements)


class URL(Document):
    """
    A URL document takes the data found at the provided URL (or in the provided reponse)
    and creates entities that can be inserted into NeuralDB.

    Args:
        url (str): The URL where the data is located.
        url_response (Reponse): Optional, defaults to None. If provided then the
            data in the response is used to create the entities, otherwise a get request
            is sent to the url.
        title_is_strong (bool): Optional, defaults to False. If true then the title is
            used as a strong signal for NeuralDB.
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def __init__(
        self,
        url: str,
        url_response: Response = None,
        save_extra_info: bool = True,
        title_is_strong: bool = False,
        metadata={},
    ):
        self.url = url
        self.df = self.process_data(url, url_response)
        self.hash_val = hash_string(url + str(metadata))
        self._save_extra_info = save_extra_info
        self._strong_column = "title" if title_is_strong else "text"
        self.doc_metadata = metadata

    def process_data(self, url, url_response=None) -> pd.DataFrame:
        # Extract elements from each file
        elements, success = url_parse.process_url(url, url_response)

        if not success or not elements:
            raise ValueError(f"Could not retrieve data from URL: {url}")

        elements_df = url_parse.create_train_df(elements)

        return elements_df

    @property
    def hash(self) -> str:
        return self.hash_val

    @property
    def size(self) -> int:
        return len(self.df)

    @property
    def name(self) -> str:
        return self.url

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        return {key: ConstraintValue(value) for key, value in self.doc_metadata.items()}

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def strong_text(self, element_id: int) -> str:
        return self.df[self._strong_column if self._strong_column else "text"].iloc[
            element_id
        ]

    def weak_text(self, element_id: int) -> str:
        return self.df["text"].iloc[element_id]

    def reference(self, element_id: int) -> Reference:
        if element_id >= len(self.df):
            _raise_unknown_doc_error(element_id)
        return Reference(
            document=self,
            element_id=element_id,
            text=self.df["display"].iloc[element_id],
            source=self.url,
            metadata=(
                {"title": self.df["title"].iloc[element_id], **self.doc_metadata}
                if "title" in self.df.columns
                else self.doc_metadata
            ),
        )

    def context(self, element_id, radius) -> str:
        if not 0 <= element_id or not element_id < self.size:
            raise ("Element id not in document.")
        rows = self.df.iloc[
            max(0, element_id - radius) : min(len(self.df), element_id + radius + 1)
        ]
        return "\n".join(rows["text"])

    def load_meta(self, directory: Path):
        if not hasattr(self, "doc_metadata"):
            self.doc_metadata = {}


class DocumentConnector(Document):
    @property
    def hash(self) -> str:
        raise NotImplementedError()

    @property
    def meta_table(self) -> Optional[pd.DataFrame]:
        """
        It stores the mapping from id_in_document to meta_data of the document. It could be used to fetch the minimal document result if the connection is lost.
        """
        raise NotImplementedError()

    @property
    def meta_table_id_col(self) -> str:
        return "id_in_document"

    def _get_connector_object_name(self):
        raise NotImplementedError()

    def get_strong_columns(self):
        raise NotImplementedError()

    def get_weak_columns(self):
        raise NotImplementedError()

    def row_iterator(self):
        id_in_document = 0
        for current_chunk in self.chunk_iterator():
            for idx in range(len(current_chunk)):
                yield DocumentRow(
                    element_id=id_in_document,
                    strong=self.strong_text_from_chunk(
                        id_in_chunk=idx, chunk=current_chunk
                    ),  # Strong text from (idx)th row of the current_chunk
                    weak=self.weak_text_from_chunk(
                        id_in_chunk=idx, chunk=current_chunk
                    ),  # Weak text from (idx)th row of the current_chunk
                )
                id_in_document += 1

    def chunk_iterator(self) -> pd.DataFrame:
        raise NotImplementedError()

    def strong_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_strong_columns()])
        except Exception as e:
            return ""

    def weak_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_weak_columns()])
        except Exception as e:
            return ""

    def reference(self, element_id: int) -> Reference:
        raise NotImplementedError()

    def context(self, element_id, radius) -> str:
        if not 0 <= element_id or not element_id < self.size:
            raise ("Element id not in document.")

        reference_texts = [
            self.reference(i).text
            for i in range(
                max(0, element_id - radius), min(self.size, element_id + radius + 1)
            )
        ]
        return "\n".join(reference_texts)

    def save_meta(self, directory: Path):
        # Save the index table
        if self.save_extra_info and self.meta_table is not None:
            self.meta_table.to_csv(
                path_or_buf=directory / (self.name + ".csv"), index=False
            )

    def __getstate__(self):
        # Document Connectors are expected to remove their connector(s) object
        state = self.__dict__.copy()

        del state[self._get_connector_object_name()]

        return state


class SQLDatabase(DocumentConnector):
    """
    class for handling SQL database connections and data retrieval for training the neural_db model

    This class encapsulates functionality for connecting to an SQL database, executing SQL queries, and retrieving
    data for use in training the model.

    NOTE: It is being expected that the table will remain static in terms of both rows and columns.
    """

    def __init__(
        self,
        engine: sqlConn,
        table_name: str,
        id_col: str,
        strong_columns: Optional[List[str]] = None,
        weak_columns: Optional[List[str]] = None,
        reference_columns: Optional[List[str]] = None,
        chunk_size: int = 10_000,
        save_extra_info: bool = False,
        metadata: dict = {},
    ) -> None:
        self.table_name = table_name
        self.id_col = id_col
        self.strong_columns = strong_columns
        self.weak_columns = weak_columns
        self.reference_columns = reference_columns
        self.chunk_size = chunk_size
        self._save_extra_info = save_extra_info
        self.doc_metadata = metadata

        self._connector = SQLConnector(
            engine=engine,
            table_name=self.table_name,
            id_col=self.id_col,
            chunk_size=self.chunk_size,
        )
        self.total_rows = self._connector.total_rows()
        if not self.total_rows > 0:
            raise FileNotFoundError("Empty table")

        self.database_name = engine.url.database
        self.url = str(engine.url)
        self.engine_uq = self.url + f"/{self.table_name}"
        self._hash = hash_string(string=self.engine_uq)

        # Integrity checks
        self.assert_valid_id()
        self.assert_valid_columns()

        # setting the columns in the conector object
        self._connector.columns = list(set(self.strong_columns + self.weak_columns))

    @property
    def name(self):
        return self.database_name + "-" + self.table_name

    @property
    def hash(self):
        return self._hash

    @property
    def size(self) -> int:
        # It is verfied by the uniqueness assertion of the id column.
        return self.total_rows

    def setup_connection(self, engine: sqlConn):
        """
        This is a helper function to re-establish the connection upon loading the
        saved ndb model containing this SQLDatabase document.

        Args:
            engine: SQLAlchemy Connection object
                    NOTE: Provide the same connection object.

        NOTE: Same table would be used to establish connection
        """
        try:
            # The idea is to check for the connector object existence
            print(
                "Connector object already exists with url:"
                f" {self._connector.get_engine_url()}"
            )
        except AttributeError as e:
            assert engine.url.database == self.database_name
            assert str(engine.url) == self.url
            self._connector = SQLConnector(
                engine=engine,
                table_name=self.table_name,
                id_col=self.id_col,
                columns=list(set(self.strong_columns + self.weak_columns)),
                chunk_size=self.chunk_size,
            )

    def _get_connector_object_name(self):
        return "_connector"

    def get_strong_columns(self):
        return self.strong_columns

    def get_weak_columns(self):
        return self.weak_columns

    def get_engine(self):
        try:
            return self._connector._engine
        except AttributeError as e:
            raise AttributeError("engine is not available")

    @property
    def meta_table(self) -> Optional[pd.DataFrame]:
        return None

    def strong_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_strong_columns()])
        except Exception as e:
            return ""

    def weak_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_weak_columns()])
        except Exception as e:
            return ""

    def chunk_iterator(self) -> pd.DataFrame:
        return self._connector.chunk_iterator()

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def reference(self, element_id: int) -> Reference:
        if element_id >= self.size:
            _raise_unknown_doc_error(element_id)

        try:
            reference_texts = self._connector.execute(
                query=(
                    f"SELECT {','.join(self.reference_columns)} FROM"
                    f" {self.table_name} WHERE {self.id_col} = {element_id}"
                )
            ).fetchone()

            text = "\n\n".join(
                [
                    f"{col_name}: {col_text}"
                    for col_name, col_text in zip(
                        self.reference_columns, reference_texts
                    )
                ]
            )

        except Exception as e:
            text = (
                f"Unable to connect to database, Referenced row with {self.id_col}:"
                f" {element_id} "
            )

        return Reference(
            document=self,
            element_id=element_id,
            text=text,
            source=str(self.engine_uq),
            metadata={
                "Database": self.database_name,
                "Table": self.table_name,
                **self.doc_metadata,
            },
        )

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        """
        This method is called when the document is being added to a DocumentManager in order to build an index for constrained search.
        """
        return {key: ConstraintValue(value) for key, value in self.doc_metadata.items()}

    def assert_valid_id(self):
        all_cols = self._connector.cols_metadata()

        id_col_meta = list(filter(lambda col: col["name"] == self.id_col, all_cols))
        if len(id_col_meta) == 0:
            raise AttributeError("id column not present in the table")
        elif not isinstance(id_col_meta[0]["type"], Integer):
            raise AttributeError("id column needs to be of type Integer")

        primary_keys = self._connector.get_primary_keys()
        if len(primary_keys) > 1:
            raise AttributeError("Composite primary key is not allowed")
        elif len(primary_keys) == 0 or primary_keys[0] != self.id_col:
            raise AttributeError(f"{self.id_col} needs to be a primary key")

        min_id = self._connector.execute(
            query=f"SELECT MIN({self.id_col}) FROM {self.table_name}"
        ).fetchone()[0]

        max_id = self._connector.execute(
            query=f"SELECT MAX({self.id_col}) FROM {self.table_name}"
        ).fetchone()[0]

        if min_id != 0 or max_id != self.size - 1:
            raise AttributeError(
                f"id column needs to be unique from 0 to {self.size - 1}"
            )

    def assert_valid_columns(self):
        all_cols = self._connector.cols_metadata()

        columns_set = set([col["name"] for col in all_cols])

        # Checking for strong, weak and reference columns (if provided) to be present in column list of the table
        if (self.strong_columns is not None) and (
            not set(self.strong_columns).issubset(columns_set)
        ):
            raise AttributeError(
                f"Strong column(s) doesn't exists in the table '{self.table_name}'"
            )
        if (self.weak_columns is not None) and (
            not set(self.weak_columns).issubset(columns_set)
        ):
            raise AttributeError(
                f"Weak column(s) doesn't exists in the table '{self.table_name}'"
            )
        if (self.reference_columns is not None) and (
            not set(self.reference_columns).issubset(columns_set)
        ):
            raise AttributeError(
                f"Reference column(s) doesn't exists in the table '{self.table_name}'"
            )

        # Checking for strong and weak column to have the correct column type
        for col in all_cols:
            if (
                self.strong_columns is not None
                and col["name"] in self.strong_columns
                and not isinstance(col["type"], String)
            ):
                raise AttributeError(
                    f"strong column '{col['name']}' needs to be of type String"
                )
            elif (
                self.weak_columns is not None
                and col["name"] in self.weak_columns
                and not isinstance(col["type"], String)
            ):
                raise AttributeError(
                    f"weak column '{col['name']}' needs to be of type String"
                )

        if self.strong_columns is None and self.weak_columns is None:
            self.strong_columns = []
            self.weak_columns = []
            for col in all_cols:
                if isinstance(col["type"], String):
                    self.weak_columns.append(col["name"])
        elif self.strong_columns is None:
            self.strong_columns = []
        elif self.weak_columns is None:
            self.weak_columns = []

        if self.reference_columns is None:
            self.reference_columns = list(columns_set)


class SharePoint(DocumentConnector):
    """
    Class for handling sharepoint connection, retrieving documents, processing and training the neural_db model

    Args:
        ctx (ClientContext): A ClientContext object for SharePoint connection.
        library_path (str): The server-relative directory path where documents
            are stored. Default: 'Shared Documents'
        chunk_size (int): The maximum amount of data (in bytes) that can be fetched
            at a time. (This limit may not apply if there are no files within this
            range.) Default: 10MB
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def __init__(
        self,
        ctx: ClientContext,
        library_path: str = "Shared Documents",
        chunk_size: int = 10485760,
        save_extra_info: bool = False,
        metadata: dict = {},
    ) -> None:
        # Executing a dummy query to check for the authentication for the ctx object
        try:
            SharePoint.dummy_query(ctx=ctx)
        except Exception as e:
            raise Exception("Invalid ClientContext Object. Error: " + str(e))

        self._connector = SharePointConnector(
            ctx=ctx, library_path=library_path, chunk_size=chunk_size
        )
        self.library_path = library_path
        self.chunk_size = chunk_size
        self._save_extra_info = save_extra_info
        self.doc_metadata = metadata

        self.strong_column = "strong_text"
        self.weak_column = "weak_text"
        self.build_meta_table()
        self._name = (
            self._connector.site_name + "-" + (self.library_path).replace(" ", "_")
        )
        self.url = self._connector.url
        self._source = self.url + "/" + library_path
        self._hash = hash_string(self._source)

    @property
    def size(self) -> int:
        return len(self.meta_table)

    @property
    def name(self) -> str:
        return self._name

    @property
    def hash(self) -> str:
        return self._hash

    def setup_connection(self, ctx: ClientContext):
        """
        This is a helper function to re-establish the connection upon loading the saved ndb model containing this Sharepoint document.

        Args:
            engine: SQLAlchemy Connection object. NOTE: Provide the same connection object.
        NOTE: Same library path would be used
        """
        try:
            # The idea is to check for the connector object existence
            print(f"Connector object already exists with url: {self._connector.url}")
        except AttributeError as e:
            assert self.url == ctx.web.get().execute_query().url
            self._connector = SharePointConnector(
                ctx=ctx, library_path=self.library_path, chunk_size=self.chunk_size
            )

    def get_strong_columns(self):
        return [self.strong_column]

    def get_weak_columns(self):
        return [self.weak_column]

    def build_meta_table(self):
        num_files = self._connector.num_files()

        print(f"Found {num_files} supported files")
        self._meta_table = pd.DataFrame(
            columns=[
                "internal_doc_id",
                "server_relative_url",
                "page",
            ]
        )
        self._meta_table = pd.concat(
            [
                current_chunk.drop(
                    columns=self.get_strong_columns() + self.get_weak_columns()
                )
                for current_chunk in self.chunk_iterator()
            ],
            ignore_index=True,
        )

        self._meta_table[self.meta_table_id_col] = range(len(self._meta_table))
        self._meta_table.set_index(keys=self.meta_table_id_col, inplace=True)

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        """
        Each constraint will get applied to each supported document on the sharepoint. This method is called when the document is being added to a DocumentManager in order to build an index for constrained search.
        """
        return {key: ConstraintValue(value) for key, value in self.doc_metadata.items()}

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def reference(self, element_id: int) -> Reference:
        if element_id >= self.size:
            _raise_unknown_doc_error(element_id)

        filename = self.meta_table.iloc[element_id]["server_relative_url"].split(
            sep="/"
        )[-1]
        return Reference(
            document=self,
            element_id=element_id,
            text=f"filename: {filename}"
            + (
                f", page no: {self.meta_table.iloc[element_id]['page']}"
                if self.meta_table.iloc[element_id]["page"] is not None
                else ""
            ),
            source=self._source + "/" + filename,
            metadata={
                **self.meta_table.loc[element_id].to_dict(),
                **self.doc_metadata,
            },
        )

    @property
    def meta_table(self) -> Optional[pd.DataFrame]:
        return self._meta_table

    def chunk_iterator(self) -> pd.DataFrame:
        chunk_df = pd.DataFrame(
            columns=[
                self.strong_column,
                self.weak_column,
                "internal_doc_id",
                "server_relative_url",
                "page",
            ]
        )

        for file_dict in self._connector.chunk_iterator():
            chunk_df.drop(chunk_df.index, inplace=True)
            temp_dfs = []
            for server_relative_url, filepath in file_dict.items():
                if filepath.endswith(".pdf"):
                    doc = PDF(path=filepath, metadata=self.doc_metadata)
                elif filepath.endswith(".docx"):
                    doc = DOCX(path=filepath, metadata=self.doc_metadata)
                else:
                    doc = Unstructured(
                        path=filepath,
                        save_extra_info=self._save_extra_info,
                        metadata=self.doc_metadata,
                    )

                df = doc.df
                temp_df = pd.DataFrame(
                    columns=chunk_df.columns.tolist(), index=range(doc.size)
                )
                strong_text, weak_text, internal_doc_id, page = zip(
                    *[
                        (
                            doc.strong_text(i),
                            doc.weak_text(i),
                            i,
                            doc.reference(i).metadata.get("page", None),
                        )
                        for i in range(doc.size)
                    ]
                )
                temp_df[self.strong_column] = strong_text
                temp_df[self.weak_column] = weak_text
                temp_df["internal_doc_id"] = internal_doc_id
                temp_df["server_relative_url"] = [server_relative_url] * len(df)
                temp_df["page"] = page

                temp_dfs.append(temp_df)

            chunk_df = pd.concat(temp_dfs, ignore_index=True)
            yield chunk_df

    def _get_connector_object_name(self):
        return "_connector"

    @staticmethod
    def dummy_query(ctx: ClientContext):
        # Authenticatiion fails if this dummy query execution fails
        ctx.web.get().execute_query()

    @staticmethod
    def setup_clientContext(
        base_url: str, credentials: Dict[str, str]
    ) -> ClientContext:
        """
        Method to create a ClientContext object given base_url and credentials in the form (username, password) OR (client_id, client_secret)
        """
        ctx = None
        try:
            if all([cred in credentials.keys() for cred in ("username", "password")]):
                user_credentials = UserCredential(
                    user_name=credentials["username"], password=credentials["password"]
                )
                ctx = ClientContext(base_url=base_url).with_credentials(
                    user_credentials
                )
            SharePoint.dummy_query(ctx=ctx)
        except Exception as userCredError:
            try:
                if all(
                    [
                        cred in credentials.keys()
                        for cred in ("client_id", "client_secret")
                    ]
                ):
                    client_credentials = ClientCredential(
                        client_id=credentials["client_id"],
                        client_secret=credentials["client_secret"],
                    )
                    ctx = ClientContext(base_url=base_url).with_credentials(
                        client_credentials
                    )
                    SharePoint.dummy_query(ctx=ctx)
            except Exception as clientCredError:
                pass

        if ctx:
            return ctx
        raise AttributeError("Incorrect or insufficient credentials")


class SalesForce(DocumentConnector):
    """
    Class for handling the Salesforce object connections and data retrieval for
    training the neural_db model

    This class encapsulates functionality for connecting to an object, executing
    Salesforce Object Query Language (SOQL) queries, and retrieving

    NOTE: Allow the Bulk API access for the provided object. Also, it is being
    expected that the table will remain static in terms of both rows and columns.
    """

    def __init__(
        self,
        instance: Salesforce,
        object_name: str,
        id_col: str,
        strong_columns: Optional[List[str]] = None,
        weak_columns: Optional[List[str]] = None,
        reference_columns: Optional[List[str]] = None,
        save_extra_info: bool = True,
        metadata: dict = {},
    ) -> None:
        self.object_name = object_name
        self.id_col = id_col
        self.strong_columns = strong_columns
        self.weak_columns = weak_columns
        self.reference_columns = reference_columns
        self._save_extra_info = save_extra_info
        self.doc_metadata = metadata
        self._connector = SalesforceConnector(
            instance=instance, object_name=object_name
        )

        self.total_rows = self._connector.total_rows()
        if not self.total_rows > 0:
            raise FileNotFoundError("Empty Object")
        self._hash = hash_string(self._connector.sf_instance + self._connector.base_url)
        self._source = self._connector.sf_instance + self.object_name

        # Integrity_checks
        self.assert_valid_id()
        self.assert_valid_fields()

        # setting the columns in the connector object
        self._connector._fields = [self.id_col] + list(
            set(self.strong_columns + self.weak_columns)
        )

    @property
    def name(self) -> str:
        return self.object_name

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def size(self) -> int:
        return self.total_rows

    def setup_connection(self, instance: Salesforce):
        """
        This is a helper function to re-establish the connection upon loading a saved ndb model containing this SalesForce document.

        Args:
            instance: Salesforce instance. NOTE: Provide the same connection object.

        NOTE: Same object name would be used to establish connection
        """
        try:
            # The idea is to check for the connector object existence
            print(
                f"Connector object already exists with url: {self._connector.base_url}"
            )
        except AttributeError as e:
            assert self.hash == hash_string(instance.sf_instance + instance.base_url)
            self._connector = SalesforceConnector(
                instance=instance,
                object_name=self.object_name,
                fields=[self.id_col]
                + list(set(self.strong_columns + self.weak_columns)),
            )

    def _get_connector_object_name(self):
        return "_connector"

    def row_iterator(self):
        for current_chunk in self.chunk_iterator():
            for idx in range(len(current_chunk)):
                """
                * Since we are not able to retrieve the rows in sorted order, we have to do this so that (id, strong_text, weak_text) gets mapped correctly.
                * We cannot sort because the id_col needs to be of type 'autoNumber' which is a string. Neither we can do 'SELECT row FROM object_name ORDER BY LEN(id_col), id_col' because there is no LEN function in SOQL (by default). Owner of the object have to create a formula LEN() to use such query.
                """
                yield DocumentRow(
                    element_id=int(current_chunk.iloc[idx][self.id_col]),
                    strong=self.strong_text_from_chunk(
                        id_in_chunk=idx, chunk=current_chunk
                    ),  # Strong text from (idx)th row of the current_chunk
                    weak=self.weak_text_from_chunk(
                        id_in_chunk=idx, chunk=current_chunk
                    ),  # Weak text from (idx)th row of the current_chunk
                )

    def get_strong_columns(self):
        return self.strong_columns

    def get_weak_columns(self):
        return self.weak_columns

    @property
    def meta_table(self) -> Optional[pd.DataFrame]:
        return None

    def strong_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_strong_columns()])
        except Exception as e:
            return ""

    def weak_text_from_chunk(self, id_in_chunk: int, chunk: pd.DataFrame) -> str:
        try:
            row = chunk.iloc[id_in_chunk]
            return " ".join([str(row[col]) for col in self.get_weak_columns()])
        except Exception as e:
            return ""

    def chunk_iterator(self) -> pd.DataFrame:
        return self._connector.chunk_iterator()

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def reference(self, element_id: int) -> Reference:
        if element_id >= self.size:
            _raise_unknown_doc_error(element_id)

        try:
            result = self._connector.execute(
                query=(
                    f"SELECT {','.join(self.reference_columns)} FROM"
                    f" {self.object_name} WHERE {self.id_col} = '{element_id}'"
                )
            )["records"][0]
            del result["attributes"]
            text = "\n\n".join(
                [f"{col_name}: {col_text}" for col_name, col_text in result.items()]
            )

        except Exception as e:
            text = (
                "Unable to connect to the object instance, Referenced row with"
                f" {self.id_col}: {element_id} "
            )

        return Reference(
            document=self,
            element_id=element_id,
            text=text,
            source=self._source,
            metadata={
                "object_name": self.object_name,
                **self.doc_metadata,
            },
        )

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        """
        This method is called when the document is being added to a DocumentManager in order to build an index for constrained search.
        """
        return {key: ConstraintValue(value) for key, value in self.doc_metadata.items()}

    def assert_valid_id(self):
        all_fields = self._connector.field_metadata()

        all_field_name = [field["name"] for field in all_fields]

        if self.id_col not in all_field_name:
            raise AttributeError("Id Columns is not present in the object")

        # Uniqueness or primary constraint
        id_field_meta = list(
            filter(lambda field: field["name"] == self.id_col, all_fields)
        )
        if len(id_field_meta) == 0:
            raise AttributeError("id col not present in the object")
        id_field_meta = id_field_meta[0]

        """
        Reason behinds using AutoNumber as the id column type:

            1. Salesforce doesn't have typical table constraints. Object in a salesforce (or table in conventional sense) uses an alpha-numeric string as a primary key.
            2. Salesforce doesn't have a pure integer field. It have one in which we can set the decimal field of the double data-type to 0 but it is only for display purpose.
            3. Only option left is one Auto-number field that can be used but it limits some options.
        """
        if not id_field_meta["autoNumber"]:
            raise AttributeError("id col must be of type Auto-Number")
        else:
            # id field is auto-incremented string. Have to check for the form of A-{0}

            result = self._connector.execute(
                query=f"SELECT {self.id_col} FROM {self.object_name} LIMIT 1"
            )
            value: str = result["records"][0][self.id_col]
            if not value.isdigit():
                raise AttributeError("id column needs to be of the form \{0\}")

        expected_min_row_id = 0
        min_id = self._connector.execute(
            query=(
                f"SELECT {self.id_col} FROM {self.object_name} WHERE {self.id_col} ="
                f" '{expected_min_row_id}'"
            )
        )

        # This one is not required probably because user can't put the auto-number field mannually.
        # User just can provide the start of the auto-number so if the min_id is 0, then max_id should be size - 1
        expected_max_row_id = self.size - 1
        max_id = self._connector.execute(
            query=(
                f"SELECT {self.id_col} FROM {self.object_name} WHERE {self.id_col} ="
                f" '{expected_max_row_id}'"
            )
        )

        if not (min_id["totalSize"] == 1 and max_id["totalSize"] == 1):
            raise AttributeError(
                f"id column needs to be unique from 0 to {self.size - 1}"
            )

    def assert_valid_fields(
        self, supported_text_types: Tuple[str] = ("string", "textarea")
    ):
        all_fields = self._connector.field_metadata()
        self.assert_field_inclusion(all_fields)
        self.assert_field_type(all_fields, supported_text_types)
        self.default_fields(all_fields, supported_text_types)

    def assert_field_inclusion(self, all_fields: List[OrderedDict]):
        fields_set = set([field["name"] for field in all_fields])

        # Checking for strong, weak and reference columns (if provided) to be present in column list of the table
        column_name_error = (
            "Remember if it is a custom column, salesforce requires it to be appended"
            " with __c."
        )
        if (self.strong_columns is not None) and (
            not set(self.strong_columns).issubset(fields_set)
        ):
            raise AttributeError(
                f"Strong column(s) doesn't exists in the object. {column_name_error}"
            )
        if (self.weak_columns is not None) and (
            not set(self.weak_columns).issubset(fields_set)
        ):
            raise AttributeError(
                f"Weak column(s) doesn't exists in the object. {column_name_error}"
            )
        if (self.reference_columns is not None) and (
            not set(self.reference_columns).issubset(fields_set)
        ):
            raise AttributeError(
                f"Reference column(s) doesn't exists in the object. {column_name_error}"
            )

    def assert_field_type(
        self, all_fields: List[OrderedDict], supported_text_types: Tuple[str]
    ):
        # Checking for strong and weak column to have the correct column type
        for field in all_fields:
            if (
                self.strong_columns is not None
                and field["name"] in self.strong_columns
                and field["type"] not in supported_text_types
            ):
                raise AttributeError(
                    f"Strong column '{field['name']}' needs to be type from"
                    f" {supported_text_types}"
                )
            if (
                self.weak_columns is not None
                and field["name"] in self.weak_columns
                and field["type"] not in supported_text_types
            ):
                raise AttributeError(
                    f"Weak column '{field['name']}' needs to be type"
                    f" {supported_text_types}"
                )

    def default_fields(
        self, all_fields: List[OrderedDict], supported_text_types: Tuple[str]
    ):
        if self.strong_columns is None and self.weak_columns is None:
            self.strong_columns = []
            self.weak_columns = []
            for field in all_fields:
                if field["type"] in supported_text_types:
                    self.weak_columns.append(field["name"])
        elif self.strong_columns is None:
            self.strong_columns = []
        elif self.weak_columns is None:
            self.weak_columns = []

        if self.reference_columns is None:
            self.reference_columns = [self.id_col]
            for field in all_fields:
                if field["type"] in supported_text_types:
                    self.reference_columns.append(field["name"])


class SentenceLevelExtracted(Extracted):
    """Parses a document into sentences and creates a NeuralDB entry for each
    sentence. The strong column of the entry is the sentence itself while the
    weak column is the paragraph from which the sentence came. A NeuralDB
    reference produced by this object displays the paragraph instead of the
    sentence to increase recall.
    """

    def __init__(self, path: str, save_extra_info: bool = True, metadata={}):
        self.path = Path(path)
        self.df = self.parse_sentences(self.process_data(path))
        self.hash_val = hash_file(
            path, metadata="sentence-level-extracted-" + str(metadata)
        )
        self.para_df = self.df["para"].unique()
        self._save_extra_info = save_extra_info
        self.doc_metadata = metadata

    def not_just_punctuation(sentence: str):
        for character in sentence:
            if character not in string.punctuation and not character.isspace():
                return True
        return False

    def get_sentences(paragraph: str):
        return [
            sentence
            for sentence in sent_tokenize(paragraph)
            if SentenceLevelExtracted.not_just_punctuation(sentence)
        ]

    def parse_sentences(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df["sentences"] = df["para"].apply(SentenceLevelExtracted.get_sentences)

        num_sents_cum_sum = np.cumsum(df["sentences"].apply(lambda sents: len(sents)))
        df["id_offsets"] = np.zeros(len(df))
        df["id_offsets"][1:] = num_sents_cum_sum[:-1]
        df["id_offsets"] = df["id_offsets"].astype(int)

        def get_ids(record):
            id_offset = record["id_offsets"]
            n_sents = len(record["sentences"])
            return list(range(id_offset, id_offset + n_sents))

        df = pd.DataFrame.from_records(
            [
                {
                    "sentence": sentence,
                    "para_id": para_id,
                    "sentence_id": i + record["id_offsets"],
                    "sentence_ids_in_para": get_ids(record),
                    **record,
                }
                for para_id, record in enumerate(df.to_dict(orient="records"))
                for i, sentence in enumerate(record["sentences"])
            ]
        )

        df.drop("sentences", axis=1, inplace=True)
        df.drop("id_offsets", axis=1, inplace=True)
        return df

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        raise NotImplementedError()

    @property
    def hash(self) -> str:
        return self.hash_val

    @property
    def size(self) -> int:
        return len(self.df)

    def get_strong_columns(self):
        return ["sentence"]

    @property
    def name(self) -> str:
        return self.path.name if self.path else None

    def strong_text(self, element_id: int) -> str:
        return self.df["sentence"].iloc[element_id]

    def weak_text(self, element_id: int) -> str:
        return self.df["para"].iloc[element_id]

    def show_fn(text, source, **kwargs):
        return text

    def reference(self, element_id: int) -> Reference:
        if element_id >= len(self.df):
            _raise_unknown_doc_error(element_id)
        return Reference(
            document=self,
            element_id=element_id,
            text=self.df["display"].iloc[element_id],
            source=str(self.path.absolute()),
            metadata={**self.df.iloc[element_id].to_dict(), **self.doc_metadata},
            upvote_ids=self.df["sentence_ids_in_para"].iloc[element_id],
        )

    def context(self, element_id, radius) -> str:
        if not 0 <= element_id or not element_id < self.size:
            raise ("Element id not in document.")

        para_id = self.df.iloc[element_id]["para_id"]

        rows = self.para_df[
            max(0, para_id - radius) : min(len(self.para_df), para_id + radius + 1)
        ]
        return "\n\n".join(rows)

    def save_meta(self, directory: Path):
        # Let's copy the original file to the provided directory
        if self.save_extra_info:
            shutil.copy(self.path, directory)

    def load_meta(self, directory: Path):
        # Since we've moved the file to the provided directory, let's make
        # sure that we point to this file.
        if hasattr(self, "doc_name"):
            self.path = directory / self.doc_name
        else:
            # deprecated, self.path should not be in self
            self.path = directory / self.path.name

        if not hasattr(self, "doc_metadata"):
            self.doc_metadata = {}


class SentenceLevelPDF(SentenceLevelExtracted):
    """
    Parses a document into sentences and creates a NeuralDB entry for each
    sentence. The strong column of the entry is the sentence itself while the
    weak column is the paragraph from which the sentence came. A NeuralDB
    reference produced by this object displays the paragraph instead of the
    sentence to increase recall.

    Args:
        path (str): The path to the pdf file.
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def __init__(self, path: str, metadata={}):
        super().__init__(path=path, metadata=metadata)

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        return process_pdf(path)


class SentenceLevelDOCX(SentenceLevelExtracted):
    """
    Parses a document into sentences and creates a NeuralDB entry for each
    sentence. The strong column of the entry is the sentence itself while the
    weak column is the paragraph from which the sentence came. A NeuralDB
    reference produced by this object displays the paragraph instead of the
    sentence to increase recall.

    Args:
        path (str): The path to the docx file.
        metadata (Dict[str, Any]): Optional, defaults to {}. Specifies metadata to
            associate with entities from this file. Queries to NeuralDB can provide
            constrains to restrict results based on the metadata.
    """

    def __init__(self, path: str, metadata={}):
        super().__init__(path=path, metadata=metadata)

    def process_data(
        self,
        path: str,
    ) -> pd.DataFrame:
        return process_docx(path)


class InMemoryText(Document):
    """
    A wrapper around a batch of texts and their metadata to fit it in the
    NeuralDB Document framework.

    Args:
        name (str): A name for the batch of texts.
        texts (List[str]): A batch of texts.
        metadatas (List[Dict[str, Any]]): Optional. Metadata for each text.
        global_metadata (Dict[str, Any]): Optional. Metadata for the whole batch
        of texts.
    """

    def __init__(
        self,
        name: str,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
        global_metadata=None,
    ):
        self._name = name
        self.df = pd.DataFrame({"texts": texts})
        self.metadata_columns = []
        if metadatas:
            metadata_df = pd.DataFrame.from_records(metadatas)
            self.df = pd.concat([self.df, metadata_df], axis=1)
            self.metadata_columns = metadata_df.columns
        self.hash_val = hash_string(str(texts) + str(metadatas))
        self.global_metadata = global_metadata or {}

    @property
    def hash(self) -> str:
        return self.hash_val

    @property
    def size(self) -> int:
        return len(self.df)

    @property
    def name(self) -> str:
        return self._name

    @property
    def matched_constraints(self) -> Dict[str, ConstraintValue]:
        metadata_constraints = {
            key: ConstraintValue(value) for key, value in self.global_metadata.items()
        }
        indexed_column_constraints = {
            key: ConstraintValue(is_any=True) for key in self.metadata_columns
        }
        return {**metadata_constraints, **indexed_column_constraints}

    def all_entity_ids(self) -> List[int]:
        return list(range(self.size))

    def filter_entity_ids(self, filters: Dict[str, Filter]):
        df = self.df
        row_filters = {
            k: v for k, v in filters.items() if k not in self.global_metadata.keys()
        }
        for column_name, filterer in row_filters.items():
            if column_name not in self.df.columns:
                return []
            df = filterer.filter_df_column(df, column_name)
        return df.index.to_list()

    def strong_text(self, element_id: int) -> str:
        return ""

    def weak_text(self, element_id: int) -> str:
        return self.df["texts"].iloc[element_id]

    def reference(self, element_id: int) -> Reference:
        if element_id >= len(self.df):
            _raise_unknown_doc_error(element_id)
        return Reference(
            document=self,
            element_id=element_id,
            text=self.df["texts"].iloc[element_id],
            source=self._name,
            metadata={**self.df.iloc[element_id].to_dict(), **self.global_metadata},
        )

    def context(self, element_id, radius) -> str:
        # We don't return neighboring texts because they are not necessarily
        # related.
        return self.df["texts"].iloc[element_id]

    def save_meta(self, directory: Path):
        pass

    def load_meta(self, directory: Path):
        pass
