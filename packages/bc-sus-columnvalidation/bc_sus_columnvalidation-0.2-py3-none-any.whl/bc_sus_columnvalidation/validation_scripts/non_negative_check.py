import pandas as pd

def non_negative_check(excel_file, sheet_name, column_name):
    """
    Check if all values in the specified column are non-negative.

    :param excel_file: Path to the Excel file
    :param sheet_name: Name of the sheet
    :param column_name: Name of the column to check
    :return: A dictionary containing rows which failed the check
    """
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Convert the column to numeric, coercing errors to NaN
    numeric_column = pd.to_numeric(df[column_name], errors='coerce')

    # Find rows where the value is less than zero
    failed_rows = numeric_column[numeric_column < 0].index.tolist()
    return {'rows_which_failed': [row + 2 for row in failed_rows]}  # Adjusting for Excel indexing
