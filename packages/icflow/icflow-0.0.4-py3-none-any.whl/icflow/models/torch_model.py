import logging
from pathlib import Path

import torch

from .metrics import MetricsCalculator
from .stopping_criteria import StoppingCriterion
from .machine_learning_model import MachineLearningModel


class TorchModel(MachineLearningModel):
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

        super().__init__(
            model, device, metrics_calculator, optimizer, stopping_criterion
        )

        self.is_sent_to_device: bool = False

    def send_to_device(self) -> None:
        """
        Send the model to the compute device
        """

        if not self.is_sent_to_device:
            self.model.to(self.device)
            self.is_sent_to_device = True

    def to_device(self, batch):
        return batch.to(self.device)

    def load(self, path: Path):
        """
        Load the model from the given path
        """

        self.model = torch.load(path)

    def set_as_distributed(self) -> None:
        """
        Indicate that we are running in a distributed setting
        """

        self.model = torch.nn.parallel.DistributedDataParallel(self.model)

    def load_model(self):
        logging.info("Loading model")
        """
        # device = "mps" if torch.cuda.is_available() else "cpu"
        if self.target_device == "cuda" and torch.cuda.is_available():
            self.device = torch.device("cuda")
            logging.info("Loading on GPU")
        else:
            self.device = torch.device("cpu")
            logging.info("Loading on CPU")

        if self.name == "resnet18":
            logging.info("Loading resnet model")
            self.model = torch_models.resnet18(
                weights=torch_models.ResNet18_Weights.DEFAULT
            )
            self.model.fc = nn.Linear(self.model.fc.in_features, self.num_classes)
        elif self.name == "mobilenet_v2":
            logging.info("Loading mobilenet_v2 model")
            self.model = torch_models.mobilenet_v2(
                weights=torch_models.MobileNet_V2_Weights.DEFAULT
            )
            self.model.classifier[1] = nn.Linear(
                self.model.classifier[1].in_features, self.num_classes
            )
        elif self.name == "deeplabv3":
            self.model = smp.DeepLabV3Plus(classes=self.num_classes)
        else:
            raise RuntimeError(f"Model name {self.name} not supported")

        self.model = self.model.to(self.device)
        self.loss_func = nn.CrossEntropyLoss()

        optimizer_name = self.optimizer_settings["name"]
        if optimizer_name == "sgd":
            learning_rate = self.optimizer_settings["learning_rate"]
            momentum = self.optimizer_settings["momentum"]
            self.optimizer = optim.SGD(
                self.model.parameters(), lr=learning_rate, momentum=momentum
            )
        elif optimizer_name == "adam":
            learning_rate = self.optimizer_settings["learning_rate"]
            torch.optim.Adam(params=self.model.parameters(), lr=learning_rate)
        else:
            raise RuntimeError(f"Unsupported optimizer name {optimizer_name}")
        """
        logging.info("Finished Loading model")

    def save(self, path):
        torch.save(self.model.state_dict(), path)
