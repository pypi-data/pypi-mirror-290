from client import Client
import pandas as pd


class Controller:
    def __init__(self) -> None:
        self.__data = Client().get_national_holidays()

    def get_national_days(self):
        return self.__data["Dia da Semana"].tolist()

    def get_national_dates(self):
        return self.__data["Data"].tolist()

    def get_national_holidays(self):
        return self.__data["Feriado"].tolist()

    def get_national_days_by_holiday(self, holiday):
        return self.__data[self.__data["Feriado"] == holiday]["Dia da Semana"]

    def get_national_dates_by_holiday(self, holiday):
        return self.__data[self.__data["Feriado"] == holiday]["Data"]

    def is_holiday(self, date):
        if isinstance(date, str):
            try:
                date = pd.to_datetime(date, format="%Y-%m-%d").date()
            except ValueError:
                return False

        return date in self.__data["Data"].values
