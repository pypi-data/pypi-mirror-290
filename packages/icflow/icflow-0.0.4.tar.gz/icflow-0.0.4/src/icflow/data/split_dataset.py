"""
This module has functionaly for handling datasets that feed into
models.
"""

from pathlib import Path
import logging

from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler

from icflow.utils.runtime import RuntimeContext

from .dataset import BaseDataset

logger = logging.getLogger(__name__)


class SplitDataset(BaseDataset):
    """
    A dataset supporting splits into parts, e.g 'test', 'train', 'val'
    """

    def __init__(
        self,
        path: Path,
        batch_size: int,
        name: str = "",
        archive_name: str = "",
        hostname: str = "",
    ):
        super().__init__(path, name, archive_name, hostname)

        self.batch_size = batch_size
        self.splits: dict = {}
        self.dataloaders: dict = {}
        self.samplers: dict = {}
        self.transform = None
        self.num_classes: int = 0
        self.is_loaded = False

    def load(
        self,
        splits: list[str] | None = None,
        runtime_ctx: RuntimeContext = RuntimeContext(),
    ):
        """
        Load the dataset from the supplied path
        """

        if self.is_loaded:
            return

        if not splits:
            splits = ["train", "val", "test"]

        logger.info("Loading dataset from %s", self.path)
        if not self.path.exists():
            raise RuntimeError(f"Provided dataset path {self.path} not found")

        for split in splits:
            self.splits[split] = self.load_torch_dataset(split)
        if self.splits:
            self.num_classes = list(self.splits.values())[0].num_classes

        self.setup_dataloaders(runtime_ctx)

        self.is_loaded = True
        logger.info(
            "Finished loading dataset with %d dataloaders", len(self.splits.keys())
        )

    def load_torch_dataset(self, stage: str) -> Dataset:
        """
        Stub method to load a PyTorch dataset
        """
        raise NotImplementedError()

    def get_data(self, split: str) -> Dataset:
        return self.splits[split]

    def get_dataloader(self, split: str) -> DataLoader:
        return self.dataloaders[split]

    def get_num_batches(self, split: str) -> int:
        return len(self.dataloaders[split])

    def set_sampler_epoch(self, epoch: int):
        for sampler in self.samplers.values():
            sampler.set_epoch(epoch)

    def on_epoch_start(self, epoch_idx: int):
        self.set_sampler_epoch(epoch_idx)

    def setup_dataloaders(self, runtime_ctx: RuntimeContext):
        """
        Given the datasets generate suitable dataloaders,
        and if running in a multi-gpu context suitable samplers.
        """

        logger.info("Setting up dataloaders")
        sampler_splits = []
        if runtime_ctx.is_multigpu:
            sampler_splits = ["train", "validation"]
            logger.info("Running in multigpu mode - setting up Samplers")
            for split in sampler_splits:
                self.samplers[split] = DistributedSampler(
                    self.splits[split],
                    num_replicas=runtime_ctx.world_size,
                    rank=runtime_ctx.global_rank,
                )

        for key, value in self.splits.items():
            self.dataloaders[key] = DataLoader(
                dataset=value,
                batch_size=self.batch_size,
                shuffle=True,
                sampler=self.samplers[key] if key in sampler_splits else None,
                num_workers=runtime_ctx.num_workers,
            )
