from pathlib import Path

from .metrics import MetricsCalculator
from .stopping_criteria import StoppingCriterion


class MachineLearningModel:
    """
    Simple representation of a machine learning model, collects model related
    things like the optimizer and metrics calculator together.
    """

    def __init__(
        self,
        model,
        device,
        metrics_calculator: MetricsCalculator,
        optimizer=None,
        stopping_criterion: StoppingCriterion | None = None,
    ) -> None:

        self.model = model
        self.device = device
        self.metrics = metrics_calculator
        self.optimizer = optimizer
        self.stopping = stopping_criterion

    def send_to_device(self) -> None:
        """
        Send the model to the compute device
        """

    def to_device(self, batch):
        """
        Send the batch to the compute device
        """
        return batch

    def on_before_epochs(self, is_distributed: bool = False):
        """
        Called right before starting the epoch loop
        """
        self.send_to_device()
        if is_distributed:
            self.set_as_distributed()
        self.metrics.on_before_epochs()

    def on_epoch_start(self):
        """
        Called at the beginnging of an epoch
        """
        self.metrics.on_epoch_start()
        if self.stopping:
            self.stopping.on_epoch_start()
        self.model.train()

    def on_epoch_end(self) -> tuple[bool, bool]:
        """
        Called at the end of an epoch
        """

        self.metrics.on_epoch_end()

        if self.stopping:
            return self.stopping.on_epoch_end(self.metrics.cache)
        return False, False

    def on_validation_start(self):
        """
        Called at the start of the validation stage, before
        any batches are loaded
        """
        self.metrics.on_validation_start()
        self.model.eval()
        if self.stopping:
            self.stopping.on_validation_start()

    def on_batch_start(self):
        self.metrics.on_batch_start()
        if self.stopping:
            self.stopping.on_batch_start()

    def on_batch_end(self, prediction, ground_truth):
        """
        Call at the end of a batch, when the prediction has
        been made
        """
        self.metrics.on_batch_end(prediction, ground_truth)
        if self.stopping:
            return self.stopping.on_batch_end()
        return False

    def on_before_infer(self):
        """
        Called before doing inference
        """
        self.metrics.on_before_infer()
        if self.stopping:
            self.stopping.on_before_infer()
        self.send_to_device()

    def load(self, path: Path):
        """
        Load the model from the given path
        """
        raise NotImplementedError()

    def set_as_distributed(self) -> None:
        """
        Indicate that we are running in a distributed setting
        """

    def predict(self, inputs):
        """
        Preduct a result from the model
        """

        return self.model(inputs)

    def calculate_loss(self, prediction, ground_truth):
        """
        Evaluate the loss function
        """
        return self.metrics.calculate_loss(prediction, ground_truth)

    def save(self, path: Path):
        """
        Save the model to disk
        """
        raise NotImplementedError()
