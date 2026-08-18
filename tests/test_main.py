import pandas as pd
import pytest

from src.main import load_csv


def test_load_csv_reads_valid_file(tmp_path):
    csv_file = tmp_path / "valid.csv"

    csv_file.write_text(
        "nome,valor\nA,10\nB,20\n"
    )

    dataframe = load_csv(csv_file)

    assert isinstance(
        dataframe,
        pd.DataFrame,
    )

    assert len(dataframe) == 2
    assert list(dataframe.columns) == [
        "nome",
        "valor",
    ]


def test_load_csv_rejects_missing_file(
    tmp_path,
):
    csv_file = (
        tmp_path / "missing.csv"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        load_csv(csv_file)


def test_load_csv_rejects_empty_file(
    tmp_path,
):
    csv_file = tmp_path / "empty.csv"

    csv_file.write_text("")

    with pytest.raises(
        ValueError,
        match="empty",
    ):
        load_csv(csv_file)


def test_load_csv_rejects_header_only_file(
    tmp_path,
):
    csv_file = (
        tmp_path / "header-only.csv"
    )

    csv_file.write_text(
        "nome,valor\n"
    )

    with pytest.raises(
        ValueError,
        match="no data rows",
    ):
        load_csv(csv_file)
