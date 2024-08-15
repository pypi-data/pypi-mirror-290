"""
This module has functionality to support running in
a distributeed context
"""

import os
import socket
import logging
import copy

import torch
import torch.distributed as dist

logger = logging.getLogger(__name__)


class RuntimeContext:
    """
    This holds runtime information for the session, which is mostly
    useful in a distributed setting.
    """

    def __init__(
        self,
        node_id: int = 0,
        num_nodes: int = 1,
        gpus_per_node: int = 1,
        local_rank: int = 0,
    ) -> None:

        self.local_rank = local_rank
        self.is_multigpu: bool = gpus_per_node > 1
        self.num_workers: int = 1
        self.world_size: int = gpus_per_node * num_nodes
        self.global_rank: int = node_id * gpus_per_node + local_rank
        self.dist_backend = "nccl"

    def init(self) -> None:
        """
        If we're running in a multigpu context set up the process group
        """

        logger.info(
            "Starting runtime: world size %s, local rank %s, global rank %s",
            self.world_size,
            self.local_rank,
            self.global_rank,
        )

        if not self.is_multigpu:
            return

        logger.info("Starting torch dist process group")
        dist.init_process_group(
            backend=self.dist_backend, world_size=self.world_size, rank=self.global_rank
        )

    def is_master_process(self) -> bool:
        """
        Return true if this process has zero global rank
        """
        return self.global_rank == 0

    def sync_dict(self, input_dict: dict, device) -> dict:
        """
        If we are running in on multiple gpus sync dict across devices
        """

        if not self.is_multigpu:
            return input_dict

        dict_copy = copy.deepcopy(input_dict)
        dist.barrier()

        for outer_key, outer_value in dict_copy.items():
            for key, value in outer_value.items():
                value_tensor = torch.tensor(value, device=device)
                dist.all_reduce(value_tensor, op=dist.ReduceOp.AVG)
                input_dict[outer_key][key] = value_tensor
        return input_dict


def run(rank, size, hostname):
    print(f"I am {rank} of {size} in {hostname}")


def init_processes(my_rank, world_size, hostname, fn, backend):

    os.environ["MASTER_ADDR"] = os.environ["SLURM_LAUNCH_NODE_IPADDR"]
    os.environ["MASTER_PORT"] = "8933"

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("my ip: ", ip_address)
    fn(my_rank, world_size, hostname)

    dist.init_process_group(
        backend, init_method="env://", rank=my_rank, world_size=world_size
    )
    print("Initialized Rank:", dist.get_rank())


if __name__ == "__main__":
    world_size = int(os.environ["SLURM_NPROCS"])
    my_rank = int(os.environ["SLURM_PROCID"])

    hostname = socket.gethostname()

    init_processes(my_rank, world_size, hostname, run, backend="nccl")
