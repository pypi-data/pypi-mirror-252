from __future__ import annotations

import random
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from thirdai import bolt, data

from .documents import DocumentDataSource
from .mach_defaults import acc_to_stop, metric_to_track
from .supervised_datasource import SupDataSource
from .trainer.checkpoint_config import CheckpointConfig
from .trainer.training_progress_manager import (
    TrainingProgressCallback,
    TrainingProgressManager,
)
from .utils import clean_text, pickle_to

InferSamples = List
Predictions = Sequence
TrainLabels = List
TrainSamples = List


# This class can be constructed by clients that use neural_db.
# The object can then be passed into Model.index_documents(), and if
# the client calls CancelState.cancel() on the object, training will halt.
class CancelState:
    def __init__(self, canceled=False):
        self.canceled = canceled

    def cancel(self):
        self.canceled = True

    def uncancel(self):
        self.canceled = False

    def is_canceled(self):
        return self.canceled


class Model:
    def get_model(self) -> bolt.UniversalDeepTransformer:
        raise NotImplementedError()

    def index_documents(
        self,
        intro_documents: DocumentDataSource,
        train_documents: DocumentDataSource,
        should_train: bool,
        fast_approximation: bool = True,
        num_buckets_to_sample: Optional[int] = None,
        on_progress: Callable = lambda **kwargs: None,
        cancel_state: CancelState = None,
        max_in_memory_batches: int = None,
        override_number_classes: int = None,
        variable_length: Optional[
            data.transformations.VariableLengthConfig
        ] = data.transformations.VariableLengthConfig(),
        checkpoint_config: CheckpointConfig = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError()

    def forget_documents(self) -> None:
        raise NotImplementedError()

    def delete_entities(self, entities) -> None:
        raise NotImplementedError()

    @property
    def searchable(self) -> bool:
        raise NotImplementedError()

    def get_query_col(self) -> str:
        raise NotImplementedError()

    def set_n_ids(self, n_ids: int):
        raise NotImplementedError()

    def get_id_col(self) -> str:
        raise NotImplementedError()

    def get_id_delimiter(self) -> str:
        raise NotImplementedError()

    def infer_samples_to_infer_batch(self, samples: InferSamples):
        query_col = self.get_query_col()
        return [{query_col: clean_text(text)} for text in samples]

    def infer_buckets(
        self, samples: InferSamples, n_results: int, **kwargs
    ) -> Predictions:
        raise NotImplementedError()

    def infer_labels(
        self,
        samples: InferSamples,
        n_results: int,
        **kwargs,
    ) -> Predictions:
        raise NotImplementedError()

    def score(
        self, samples: InferSamples, entities: List[List[int]], n_results: int = None
    ) -> Predictions:
        raise NotImplementedError()

    def save_meta(self, directory: Path) -> None:
        raise NotImplementedError()

    def load_meta(self, directory: Path):
        raise NotImplementedError()

    def associate(
        self,
        pairs: List[Tuple[str, str]],
        n_buckets: int,
        n_association_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        raise NotImplementedError()

    def upvote(
        self,
        pairs: List[Tuple[str, int]],
        n_upvote_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        raise NotImplementedError()

    def retrain(
        self,
        balancing_data: DocumentDataSource,
        source_target_pairs: List[Tuple[str, str]],
        n_buckets: int,
        learning_rate: float,
        epochs: int,
    ):
        raise NotImplementedError()

    def train_on_supervised_data_source(
        self,
        supervised_data_source: SupDataSource,
        learning_rate: float,
        epochs: int,
        batch_size: Optional[int],
        max_in_memory_batches: Optional[int],
        metrics: List[str],
        callbacks: List[bolt.train.callbacks.Callback],
    ):
        raise NotImplementedError()


class EarlyStopWithMinEpochs(bolt.train.callbacks.Callback):
    def __init__(
        self,
        min_epochs,
        tracked_metric,
        metric_threshold,
    ):
        super().__init__()

        self.epoch_count = 0
        self.min_epochs = min_epochs
        self.tracked_metric = tracked_metric
        self.metric_threshold = metric_threshold

    def on_epoch_end(self):
        self.epoch_count += 1

        if (
            self.epoch_count > self.min_epochs
            and self.history[f"train_{self.tracked_metric}"][-1] > self.metric_threshold
        ):
            self.train_state.stop_training()


class ProgressUpdate(bolt.train.callbacks.Callback):
    def __init__(
        self,
        max_epochs,
        progress_callback_fn,
    ):
        super().__init__()

        self.batch_count = 0
        self.max_epochs = max_epochs
        self.progress_callback_fn = progress_callback_fn

    def on_batch_end(self):
        self.batch_count += 1

        # We update progress every other batch because otherwise the updates are
        # too fast for frontend components to display these changes.
        if self.batch_count % 2:
            batch_progress = self.batch_count / self.train_state.batches_in_dataset()
            progress = batch_progress / self.max_epochs

            # TODO revisit this progress bar update
            # This function (sqrt) increases faster at the beginning
            progress = progress ** (1.0 / 2)
            self.progress_callback_fn(progress)


class FreezeHashTable(bolt.train.callbacks.Callback):
    def __init__(
        self,
        freeze_before_train,
        freeze_after_epoch,
        tracked_metric,
        metric_threshold,
    ):
        super().__init__()

        self.epoch_count = 0
        self.freeze_after_epoch = freeze_after_epoch
        self.tracked_metric = tracked_metric
        self.metric_threshold = metric_threshold
        self.freeze_before_train = freeze_before_train

    def on_train_start(self):
        if self.freeze_before_train:
            self.model.freeze_hash_tables()

    def on_epoch_end(self):
        self.epoch_count += 1
        if self.freeze_before_train:
            return
        if (self.epoch_count == self.freeze_after_epoch) or (
            self.history[f"train_{self.tracked_metric}"][-1] > self.metric_threshold
        ):
            self.model.freeze_hash_tables()


class CancelTraining(bolt.train.callbacks.Callback):
    def __init__(self, cancel_state):
        super().__init__()
        self.cancel_state = cancel_state

    def on_batch_end(self):
        if self.cancel_state is not None and self.cancel_state.is_canceled():
            self.train_state.stop_training()


def unsupervised_train_on_docs(
    model,
    documents: DocumentDataSource,
    min_epochs: int,
    max_epochs: int,
    metric: str,
    learning_rate: float,
    batch_size: int,
    acc_to_stop: float,
    on_progress: Callable,
    freeze_before_train: bool,
    freeze_after_epoch: int,
    freeze_after_acc: float,
    cancel_state: CancelState,
    max_in_memory_batches: int,
    variable_length: Optional[
        data.transformations.VariableLengthConfig
    ] = data.transformations.VariableLengthConfig(),
    training_progress_callback: Optional[TrainingProgressCallback] = None,
    **kwargs,
):
    documents.restart()

    early_stop_callback = EarlyStopWithMinEpochs(
        min_epochs=min_epochs,
        tracked_metric=metric,
        metric_threshold=acc_to_stop,
    )

    progress_callback = ProgressUpdate(
        max_epochs=max_epochs,
        progress_callback_fn=on_progress,
    )

    cancel_training_callback = CancelTraining(cancel_state=cancel_state)

    freeze_hashtable_callback = FreezeHashTable(
        freeze_before_train=freeze_before_train,
        freeze_after_epoch=freeze_after_epoch,
        tracked_metric=metric,
        metric_threshold=freeze_after_acc,
    )

    callbacks = [
        early_stop_callback,
        progress_callback,
        cancel_training_callback,
        freeze_hashtable_callback,
    ]

    if training_progress_callback:
        callbacks.append(training_progress_callback)

    model.cold_start_on_data_source(
        data_source=documents,
        strong_column_names=[documents.strong_column],
        weak_column_names=[documents.weak_column],
        batch_size=batch_size,
        learning_rate=learning_rate,
        epochs=max_epochs,
        metrics=[metric],
        callbacks=callbacks,
        max_in_memory_batches=max_in_memory_batches,
        variable_length=variable_length,
    )


def make_balancing_samples(documents: DocumentDataSource):
    samples = [
        (". ".join([row.strong, row.weak]), [row.id])
        for row in documents.row_iterator()
    ]
    if len(samples) > 25000:
        samples = random.sample(samples, k=25000)
    return samples


class Mach(Model):
    def __init__(
        self,
        id_col="DOC_ID",
        id_delimiter=" ",
        query_col="QUERY",
        fhr=50_000,
        embedding_dimension=2048,
        extreme_output_dim=50_000,
        extreme_num_hashes=8,
        tokenizer="char-4",
        hidden_bias=False,
        model_config=None,
    ):
        self.id_col = id_col
        self.id_delimiter = id_delimiter
        self.tokenizer = tokenizer
        self.query_col = query_col
        self.fhr = fhr
        self.embedding_dimension = embedding_dimension
        self.extreme_output_dim = extreme_output_dim
        self.extreme_num_hashes = extreme_num_hashes
        self.hidden_bias = hidden_bias
        self.n_ids = 0
        self.model = None
        self.balancing_samples = []
        self.model_config = model_config

    def set_mach_sampling_threshold(self, threshold: float):
        if self.model is None:
            raise Exception(
                "Cannot set Sampling Threshold for a model that has not been"
                " initialized"
            )
        self.model.set_mach_sampling_threshold(threshold)

    def reset_model(self, new_model: Mach):
        self.id_col = new_model.id_col
        self.id_delimiter = new_model.id_delimiter
        self.tokenizer = new_model.tokenizer
        self.query_col = new_model.query_col
        self.fhr = new_model.fhr
        self.embedding_dimension = new_model.embedding_dimension
        self.extreme_output_dim = new_model.extreme_output_dim
        self.extreme_num_hashes = new_model.extreme_num_hashes
        self.hidden_bias = new_model.hidden_bias
        self.n_ids = new_model.n_ids
        self.model = new_model.model
        self.balancing_samples = new_model.balancing_samples
        self.model_config = new_model.model_config

    def save(self, path: Path):
        pickle_to(self, filepath=path)

    def get_model(self) -> bolt.UniversalDeepTransformer:
        return self.model

    def set_model(self, model):
        self.model = model

    def save_meta(self, directory: Path):
        pass

    def load_meta(self, directory: Path):
        pass

    def set_n_ids(self, n_ids: int):
        self.n_ids = n_ids

    def get_query_col(self) -> str:
        return self.query_col

    def get_id_col(self) -> str:
        return self.id_col

    def get_id_delimiter(self) -> str:
        return self.id_delimiter

    def introduce_documents(
        self,
        intro_documents: DocumentDataSource,
        fast_approximation: bool,
        num_buckets_to_sample: Optional[int],
        override_number_classes: int,
    ):
        if intro_documents.id_column != self.id_col:
            raise ValueError(
                f"Model configured to use id_col={self.id_col}, received document with"
                f" id_col={intro_documents.id_column}"
            )

        if self.model is None:
            self.id_col = intro_documents.id_column
            self.model = self.model_from_scratch(
                intro_documents, number_classes=override_number_classes
            )
        else:
            if intro_documents.size > 0:
                doc_id = intro_documents.id_column
                if doc_id != self.id_col:
                    raise ValueError(
                        f"Document has a different id column ({doc_id}) than the model"
                        f" configuration ({self.id_col})."
                    )

                num_buckets_to_sample = num_buckets_to_sample or int(
                    self.model.get_index().num_hashes() * 2.0
                )

                self.model.introduce_documents_on_data_source(
                    data_source=intro_documents,
                    strong_column_names=[intro_documents.strong_column],
                    weak_column_names=[intro_documents.weak_column],
                    fast_approximation=fast_approximation,
                    num_buckets_to_sample=num_buckets_to_sample,
                )
        self.n_ids += intro_documents.size

    def index_documents_impl(
        self,
        training_progress_manager: TrainingProgressManager,
        on_progress: Callable = lambda **kwargs: None,
        cancel_state: CancelState = None,
    ):
        intro_documents = training_progress_manager.intro_source
        train_documents = training_progress_manager.train_source

        if not training_progress_manager.is_insert_completed:
            self.introduce_documents(
                intro_documents=intro_documents,
                **training_progress_manager.introduce_arguments(),
            )
            training_progress_manager.insert_complete()

        if not training_progress_manager.is_training_completed:
            train_arguments = training_progress_manager.training_arguments()
            unsupervised_train_on_docs(
                model=self.model,
                documents=train_documents,
                metric=metric_to_track,
                acc_to_stop=acc_to_stop,
                on_progress=on_progress,
                cancel_state=cancel_state,
                training_progress_callback=TrainingProgressCallback(
                    training_progress_manager=training_progress_manager
                ),
                **train_arguments,
            )
            training_progress_manager.training_complete()

    def resume(
        self,
        on_progress: Callable,
        cancel_state: CancelState,
        checkpoint_config: CheckpointConfig,
    ):
        # This will load the datasources, model, training config and upload the current model with the loaded one. This updates the underlying UDT MACH of the current model with the one from the checkpoint along with other class attributes.
        training_progress_manager = TrainingProgressManager.from_checkpoint(
            self, checkpoint_config=checkpoint_config
        )

        self.index_documents_impl(
            training_progress_manager=training_progress_manager,
            on_progress=on_progress,
            cancel_state=cancel_state,
        )

    def index_from_start(
        self,
        intro_documents: DocumentDataSource,
        train_documents: DocumentDataSource,
        should_train: bool,
        fast_approximation: bool = True,
        num_buckets_to_sample: Optional[int] = None,
        on_progress: Callable = lambda **kwargs: None,
        cancel_state: CancelState = None,
        max_in_memory_batches: int = None,
        override_number_classes: int = None,
        variable_length: Optional[
            data.transformations.VariableLengthConfig
        ] = data.transformations.VariableLengthConfig(),
        checkpoint_config: CheckpointConfig = None,
        **kwargs,
    ):
        """
        override_number_classes : The number of classes for the Mach model

        Note: Given the datasources for introduction and training, we initialize a Mach model that has number_classes set to the size of introduce documents. But if we want to use this Mach model in our mixture of Models, this will not work because each Mach will be initialized with number of classes equal to the size of the datasource shard. Hence, we add override_number_classes parameters which if set, will initialize Mach Model with number of classes passed by the Mach Mixture.
        """

        training_progress_manager = TrainingProgressManager.from_scratch(
            model=self,
            intro_documents=intro_documents,
            train_documents=train_documents,
            should_train=should_train,
            fast_approximation=fast_approximation,
            num_buckets_to_sample=num_buckets_to_sample,
            max_in_memory_batches=max_in_memory_batches,
            override_number_classes=override_number_classes,
            variable_length=variable_length,
            checkpoint_config=checkpoint_config,
            **kwargs,
        )

        training_progress_manager.make_preindexing_checkpoint()
        self.index_documents_impl(
            training_progress_manager=training_progress_manager,
            on_progress=on_progress,
            cancel_state=cancel_state,
        )

    def add_balancing_samples(self, documents: DocumentDataSource):
        samples = make_balancing_samples(documents)
        self.balancing_samples += samples
        if len(self.balancing_samples) > 25000:
            self.balancing_samples = random.sample(self.balancing_samples, k=25000)

    def delete_entities(self, entities) -> None:
        for entity in entities:
            self.get_model().forget(entity)

    def model_from_scratch(
        self, documents: DocumentDataSource, number_classes: int = None
    ):
        return bolt.UniversalDeepTransformer(
            data_types={
                self.query_col: bolt.types.text(tokenizer=self.tokenizer),
                self.id_col: bolt.types.categorical(delimiter=self.id_delimiter),
            },
            target=self.id_col,
            n_target_classes=(
                documents.size if number_classes is None else number_classes
            ),
            integer_target=True,
            options={
                "extreme_classification": True,
                "extreme_output_dim": self.extreme_output_dim,
                "fhr": self.fhr,
                "embedding_dimension": self.embedding_dimension,
                "extreme_num_hashes": self.extreme_num_hashes,
                "hidden_bias": self.hidden_bias,
                "rlhf": True,
            },
            model_config=self.model_config,
        )

    def forget_documents(self) -> None:
        if self.model is not None:
            self.model.clear_index()
        self.n_ids = 0
        self.balancing_samples = []

    @property
    def searchable(self) -> bool:
        return self.n_ids != 0

    def infer_labels(
        self,
        samples: InferSamples,
        n_results: int,
        **kwargs,
    ) -> Predictions:
        infer_batch = self.infer_samples_to_infer_batch(samples)
        self.model.set_decode_params(min(self.n_ids, n_results), min(self.n_ids, 100))
        return self.model.predict_batch(infer_batch)

    def score(
        self, samples: InferSamples, entities: List[List[int]], n_results: int = None
    ) -> Predictions:
        infer_batch = self.infer_samples_to_infer_batch(samples)
        return self.model.score_batch(infer_batch, classes=entities, top_k=n_results)

    def infer_buckets(
        self, samples: InferSamples, n_results: int, **kwargs
    ) -> Predictions:
        infer_batch = self.infer_samples_to_infer_batch(samples)
        predictions = [
            self.model.predict_hashes(sample)[:n_results] for sample in infer_batch
        ]
        return predictions

    def _format_associate_samples(self, pairs: List[Tuple[str, str]]):
        return [(clean_text(source), clean_text(target)) for source, target in pairs]

    def associate(
        self,
        pairs: List[Tuple[str, str]],
        n_buckets: int,
        n_association_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        self.model.associate(
            source_target_samples=self._format_associate_samples(pairs),
            n_buckets=n_buckets,
            n_association_samples=n_association_samples,
            n_balancing_samples=n_balancing_samples,
            learning_rate=learning_rate,
            epochs=epochs,
        )

    def upvote(
        self,
        pairs: List[Tuple[str, int]],
        n_upvote_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        samples = [(clean_text(text), label) for text, label in pairs]

        self.model.upvote(
            source_target_samples=samples,
            n_upvote_samples=n_upvote_samples,
            n_balancing_samples=n_balancing_samples,
            learning_rate=learning_rate,
            epochs=epochs,
        )

    def retrain(
        self,
        balancing_data: DocumentDataSource,
        source_target_pairs: List[Tuple[str, str]],
        n_buckets: int,
        learning_rate: float,
        epochs: int,
    ):
        self.model.associate_cold_start_data_source(
            balancing_data=balancing_data,
            strong_column_names=[balancing_data.strong_column],
            weak_column_names=[balancing_data.weak_column],
            source_target_samples=self._format_associate_samples(source_target_pairs),
            n_buckets=n_buckets,
            n_association_samples=1,
            learning_rate=learning_rate,
            epochs=epochs,
            metrics=["hash_precision@5"],
            options=bolt.TrainOptions(),
        )

    def __setstate__(self, state):
        if "model_config" not in state:
            # Add model_config field if an older model is being loaded.
            state["model_config"] = None
        self.__dict__.update(state)

    def train_on_supervised_data_source(
        self,
        supervised_data_source: SupDataSource,
        learning_rate: float,
        epochs: int,
        batch_size: Optional[int],
        max_in_memory_batches: Optional[int],
        metrics: List[str],
        callbacks: List[bolt.train.callbacks.Callback],
    ):
        self.model.train_on_data_source(
            data_source=supervised_data_source,
            learning_rate=learning_rate,
            epochs=epochs,
            batch_size=batch_size,
            max_in_memory_batches=max_in_memory_batches,
            metrics=metrics,
            callbacks=callbacks,
        )
