
# Brazil National Days

`brazil_national_days` is a package designed to simplify the retrieval and management of Brazilian national holidays. The package provides an easy-to-use interface for downloading, parsing, and querying holiday data directly from the ANBIMA website. This package can be used to check for national holidays, obtain the dates and names of holidays, and determine whether a specific date is a holiday.
## Installation

To install the package, you can use pip:

```bash
    pip install brazil_national_days
```
    
## Use

Here is a basic example of how to use the brazil_national_days package:

### 1. Import the Package

```python
from brazil_national_days import Controller
```

### 2. Instantiate the Controller
```python
controller = Controller()
```
### 3. Use the Controller
```python
# Get all weekdays corresponding to national holidays
national_days = controller.get_national_days()

# Get all national holiday dates
national_dates = controller.get_national_dates()

# Get all national holiday names
national_holidays = controller.get_national_holidays()

# Get weekdays by a specific holiday name
holiday_name = "Carnaval"
holiday_days = controller.get_national_days_by_holiday(holiday_name)

# Get dates by a specific holiday name
holiday_dates = controller.get_national_dates_by_holiday(holiday_name)

# Check if a specific date is a holiday
date_to_check = "2024-02-12"
is_holiday = controller.is_holiday(date_to_check)
```
## Class and Method Details

### Clients
This class is used to fetch and prepare the holiday data.

#### Attributes:
* `URL (str)`: The URL to the ANBIMA Excel file containing the national holidays.
* `data (pd.DataFrame)`: A DataFrame that holds the processed holiday data.
#### Methods:
* `get_national_holidays() -> pd.DataFrame`: Downloads the Excel file from the provided URL, processes the data, and returns it as a pandas DataFrame. The dates are converted to `datetime.date` objects. If an error occurs during the request or parsing, the method handles the exceptions and returns `None`.
### Controller
This class provides methods to interact with the holiday data fetched by the Client.

#### Attributes:
* `__data (pd.DataFrame)`: A private attribute that stores the national holiday data fetched by the `Client`.
#### Methods:
* `get_national_days() -> list:` Returns a list of weekdays corresponding to all national holidays.
* `get_national_dates() -> list:` Returns a list of dates for all national holidays.
* `get_national_holidays() -> list:` Returns a list of names of all national holidays.
* `get_national_days_by_holiday(holiday: str) -> pd.Series:` Returns a Series of weekdays for a specific holiday.
* `get_national_dates_by_holiday(holiday: str) -> pd.Series:` Returns a Series of dates for a specific holiday.
* `is_holiday(date: Union[str, datetime.date]) -> bool:` Checks if a given date is a national holiday. Accepts both string `("YYYY-MM-DD")` and `datetime.date` objects.
## Error Handling

The package is designed to handle various errors, such as:

* Network issues when fetching the data.
* Parsing errors with the Excel file.
* Incorrect date formats when checking holidays.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. All contributions are welcome!


## Licença

MIT License

Copyright (c) [2024] [Leonardo Alves Francisco]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
