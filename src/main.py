import argparse
from pathlib import Path

import pandas as pd

from src.analyzer import DatasetAnalyzer
from src.report import ExcelReportGenerator


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Excel reports from CSV files."
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

    return parser.parse_args()


def main():
    args = parse_arguments()

    csv_path = Path(args.csv_file)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)

    analyzer = DatasetAnalyzer(dataframe)
    analysis = analyzer.analyze()

    print(f"Rows: {analysis.rows}")
    print(f"Columns: {analysis.columns}")
    print(f"Numeric: {analysis.numeric_columns}")
    print(f"Categorical: {analysis.categorical_columns}")
    print(f"Datetime: {analysis.datetime_columns}")

    generator = ExcelReportGenerator(dataframe)
    generator.generate(args.output)

    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
