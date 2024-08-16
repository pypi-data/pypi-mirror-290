import logging
import json

import torch

logger = logging.getLogger(__name__)


class ComputeDevice:
    """
    This represents a compute device, such as a GPU or CPU
    """

    def __init__(self, local_rank: int = 0) -> None:
        self.handle = None
        self.local_rank = local_rank
        self.name = "cpu"

    def load(self):
        if torch.cuda.is_available():
            self.name = f"cuda:{self.local_rank}"
        logger.info("Loading torch device %s", self.name)
        self.handle = torch.device(self.name)

    def serialize(self):
        return {"name", self.name, "rank", self.local_rank}

    def __str__(self):
        return json.dumps(self.serialize())
