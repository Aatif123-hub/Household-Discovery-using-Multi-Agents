import pandas as pd

class Parsers:
    @staticmethod
    def csv_parser(csv_files):
        dataframes = []
        for csv_file in csv_files:
            try:
                dataframes.append(pd.read_csv(csv_file))
            except Exception as e:
                raise Exception(f"Failed to read the CSV file: {csv_file}. Error: {e}")
        return pd.concat(dataframes, ignore_index=False)

    @staticmethod
    def xlsx_parser(xlsx_files):
        dataframes = []
        for xlsx_file in xlsx_files:
            try:
                dataframes.append(pd.read_excel(xlsx_file))
            except Exception as e:
                raise Exception(f"Failed to read the XLSX file: {xlsx_file}. Error: {e}")
        return pd.concat(dataframes, ignore_index=False)
