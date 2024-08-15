#!/usr/bin/env python
"""Command to list the current cluster usage per user.
Part of the [slurm-usage](https://github.com/basnijholt/slurm-usage) library.
"""

from __future__ import annotations

import subprocess
from collections import defaultdict
from functools import lru_cache
from getpass import getuser
from typing import NamedTuple

from rich.console import Console
from rich.table import Table


class SlurmJob(NamedTuple):
    user: str
    status: str
    nodes: int
    partition: str
    cpus: int
    node: str
    oversubscribe: str

    @classmethod
    def from_line(cls, line: str) -> SlurmJob:
        user, status, nodes, partition, cpus, node, oversubscribe = line.split("/")
        return cls(user, status, int(nodes), partition, int(cpus), node, oversubscribe)


def parse_squeue() -> list[SlurmJob]:
    cmd = "squeue -ro '%u/%t/%D/%P/%C/%N/%h'"
    try:
        output = subprocess.getoutput(cmd).split("\n")[1:]  # Get the output and skip the header
        return [SlurmJob.from_line(line) for line in output]
    except Exception as e:
        print(f"Error fetching squeue output: {e}")
        return []


@lru_cache(maxsize=None)
def total_cpus_in_node(node_name: str) -> int | float:
    cmd = f"scontrol show node {node_name}"
    output = subprocess.getoutput(cmd)

    for line in output.splitlines():
        if "CPUTot" in line:
            return int(line.split("CPUTot=")[1].split()[0])

    return float("nan")


def process_data(
    output: list[SlurmJob], cpus_or_nodes: str
) -> tuple[
    dict[str, dict[str, dict[str, int]]],
    dict[str, dict[str, int]],
    dict[str, int],
]:
    data: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    total_partition: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    totals: dict[str, int] = defaultdict(int)

    # Track which nodes have been counted for each user
    counted_nodes = defaultdict(set)

    for s in output:
        if s.oversubscribe in ["NO", "USER"]:  # --exclusive or --exclusive=user
            if s.node not in counted_nodes[s.user]:
                if cpus_or_nodes == "nodes":
                    n = 1  # Count the node itself
                else:
                    n = total_cpus_in_node(s.node)  # Count all cpus in the node
                # Mark this node as counted for this user
                counted_nodes[s.user].add(s.node)
            else:
                continue  # Skip this job to prevent double-counting
        else:
            n = s.nodes if cpus_or_nodes == "nodes" else s.cpus

        data[s.user][s.partition][s.status] += n
        total_partition[s.partition][s.status] += n
        totals[s.status] += n

    return data, total_partition, totals


def summarize_status(d: dict[str, int]) -> str:
    return " / ".join([f"{status}={n}" for status, n in d.items()])


def combine_statuses(d: dict[str, dict[str, int]]) -> dict[str, int]:
    tot = defaultdict(int)
    for dct in d.values():
        for status, n in dct.items():
            tot[status] += n
    return dict(tot)


def main() -> None:
    output = parse_squeue()
    me = getuser()
    for which in ["cpus", "nodes"]:
        data, total_partition, totals = process_data(output, which)
        table = Table(title=f"SLURM statistics [b]{which}[/]", show_footer=True)
        partitions = sorted(total_partition.keys())
        table.add_column("User", f"{len(data)} users", style="cyan")
        for partition in partitions:
            tot = summarize_status(total_partition[partition])
            table.add_column(partition, tot, style="magenta")
        table.add_column("Total", summarize_status(totals), style="magenta")

        for user, _stats in sorted(data.items()):
            kw = {"style": "bold italic"} if user == me else {}
            partition_stats = [summarize_status(_stats[p]) if p in _stats else "-" for p in partitions]
            table.add_row(
                user,
                *partition_stats,
                summarize_status(combine_statuses(_stats)),
                **kw,
            )
        console = Console()
        console.print(table, justify="center")


if __name__ == "__main__":
    main()
