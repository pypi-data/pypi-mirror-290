import requests
from io import BytesIO
import pandas as pd


class Client:
    URL = "https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls"

    def __init__(self) -> None:
        self.data = None

    def get_national_holidays(self):
        try:
            response = requests.get(self.URL)
            response.raise_for_status()

            excel_file = BytesIO(response.content)
            self.data = pd.read_excel(excel_file)

            self.data["Data"] = pd.to_datetime(
                self.data["Data"], format="%Y-%m-%d", errors="coerce"
            )
            self.data = self.data.dropna(subset=["Data"])

            self.data["Data"] = self.data["Data"].dt.date
            return self.data
        except requests.RequestException as req_err:
            print(f"Request error: {req_err}")
        except pd.errors.ParserError as parse_err:
            print(f"Parsing error: {parse_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
