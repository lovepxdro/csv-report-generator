from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


class ExcelReportGenerator:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def generate(self, output_path: str) -> None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        self.df.to_excel(
            output,
            index=False,
            sheet_name="Dados",
        )

        workbook = load_workbook(output)
        worksheet = workbook["Dados"]

        self._format_header(worksheet)
        self._adjust_column_widths(worksheet)
        self._configure_table_view(worksheet)

        workbook.save(output)

    @staticmethod
    def _format_header(worksheet) -> None:
        fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78",
        )

        font = Font(
            color="FFFFFF",
            bold=True,
        )

        for cell in worksheet[1]:
            cell.fill = fill
            cell.font = font
            cell.alignment = Alignment(horizontal="center")

    @staticmethod
    def _adjust_column_widths(worksheet) -> None:
        for column_cells in worksheet.columns:
            max_length = 0

            column_letter = get_column_letter(column_cells[0].column)

            for cell in column_cells:
                if cell.value is None:
                    continue

                max_length = max(
                    max_length,
                    len(str(cell.value)),
                )

            worksheet.column_dimensions[column_letter].width = min(
                max_length + 2,
                50,
            )

    @staticmethod
    def _configure_table_view(worksheet) -> None:
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
