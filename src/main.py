import argparse
import sys
from pathlib import Path

import pandas as pd

from src.analyzer import DatasetAnalyzer
from src.report import ExcelReportGenerator


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Generate adaptive Excel reports "
            "and dashboards from CSV files."
        )
    )

    parser.add_argument(
        "csv_file",
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--output",
        default="output/report.xlsx",
        help="Path to the generated Excel file.",
    )

    parser.add_argument(
        "--mode",
        choices=["report", "dashboard"],
        default="report",
        help="Generation mode.",
    )

    return parser.parse_args()


def load_csv(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {csv_path}"
        )

    if not csv_path.is_file():
        raise ValueError(
            f"Input path is not a file: {csv_path}"
        )

    try:
        dataframe = pd.read_csv(csv_path)

    except pd.errors.EmptyDataError as error:
        raise ValueError(
            "The CSV file is empty."
        ) from error

    except pd.errors.ParserError as error:
        raise ValueError(
            "The CSV file could not be parsed."
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            "The CSV encoding could not be decoded."
        ) from error

    if dataframe.empty:
        raise ValueError(
            "The CSV contains no data rows."
        )

    if len(dataframe.columns) == 0:
        raise ValueError(
            "The CSV contains no columns."
        )

    return dataframe


def main() -> int:
    args = parse_arguments()

    try:
        csv_path = Path(args.csv_file)

        dataframe = load_csv(csv_path)

        analyzer = DatasetAnalyzer(dataframe)
        analysis = analyzer.analyze()

        typed_dataframe = analyzer.get_dataframe()

        print(f"Rows: {analysis.rows}")
        print(f"Columns: {analysis.columns}")
        print(f"Numeric: {analysis.numeric_columns}")
        print(f"Categorical: {analysis.categorical_columns}")
        print(f"Datetime: {analysis.datetime_columns}")
        print(f"Mode: {args.mode}")
        print(f"Profile: {analysis.profile_type}")
        print(
            f"Primary metric: "
            f"{analysis.primary_metric}"
        )

        generator = ExcelReportGenerator(
            typed_dataframe,
            analysis,
            include_dashboard=(
                args.mode == "dashboard"
            ),
        )

        generator.generate(args.output)

        print(
            f"Report generated: {args.output}"
        )

        return 0

    except (
        FileNotFoundError,
        ValueError,
    ) as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )

        return 1

    except PermissionError:
        print(
            "Error: permission denied while "
            "reading or writing a file.",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
