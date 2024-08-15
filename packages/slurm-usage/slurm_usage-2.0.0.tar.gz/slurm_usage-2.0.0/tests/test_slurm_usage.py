import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from slurm_usage import (
    combine_statuses,
    main,
    process_data,
    parse_squeue,
    summarize_status,
)

# Mock squeue output (adjusted to match the expected format)
squeue_mock_output = """USER/ST/NODES/PARTITION/CPUS/NODELIST/OVER_SUBSCRIBE
bas.nijholt/PD/1/mypartition-10/32/node01/NO
bas.nijholt/R/2/mypartition-20/64/node02/USER
user2/R/1/mypartition-10/16/node03/OK"""


@pytest.fixture()
def mock_subprocess_output():
    with patch("subprocess.getoutput", return_value=squeue_mock_output) as mock_output:
        yield mock_output


def test_parse_squeue(mock_subprocess_output) -> None:
    output = parse_squeue()
    assert len(output) == 3  # Based on the mocked output
    assert output[0].user == "bas.nijholt"
    assert output[0].status == "PD"
    assert output[0].nodes == 1
    assert output[0].partition == "mypartition-10"
    assert output[0].cpus == 32
    assert output[0].node == "node01"
    assert output[0].oversubscribe == "NO"


def test_process_data(mock_subprocess_output) -> None:
    output = parse_squeue()
    data, total_partition, totals = process_data(output, "nodes")

    assert data["bas.nijholt"]["mypartition-10"]["PD"] == 1
    assert data["bas.nijholt"]["mypartition-20"]["R"] == 1
    assert data["user2"]["mypartition-10"]["R"] == 1

    assert total_partition["mypartition-10"]["PD"] == 1
    assert total_partition["mypartition-20"]["R"] == 1

    assert totals["PD"] == 1
    assert totals["R"] == 2


def test_summarize_status() -> None:
    status_dict = {"R": 3, "PD": 1}
    summary = summarize_status(status_dict)
    assert summary == "R=3 / PD=1"


def test_combine_statuses() -> None:
    statuses = {"mypartition-10": {"R": 2, "PD": 1}, "mypartition-20": {"R": 1}}
    combined = combine_statuses(statuses)
    assert combined == {"R": 3, "PD": 1}


@patch("getpass.getuser", return_value="bas.nijholt")
def test_main(mock_getuser, mock_subprocess_output) -> None:
    with patch("rich.console.Console.print") as mock_print:
        main()
        assert mock_print.called
