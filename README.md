# PyTestRailReporter

[![PyPI version](about:sanitized)](https://badge.fury.io/py/pytest-testrail)

[![License: MIT](about:sanitized)](https://opensource.org/licenses/MIT)

[![Poetry](about:sanitized)](https://python-poetry.org/)

**Seamless TestRail Integration for Pytest**

PyTestRailReporter is a pytest plugin designed to bridge the gap between your pytest test runs and TestRail, the test case management system. This plugin automates the process of reporting your test results to TestRail, streamlining your testing workflow and improving collaboration.

## Key Features

  * **Automated Results Reporting**: Automatically send test results to TestRail, eliminating manual updates.
  * **Test Case Mapping**: Link pytest functions to TestRail test cases using the `@pytest.mark.testrail_cases` marker.
  * **Flexible Configuration**: Configure TestRail connection settings via command-line options or a YAML configuration file.
  * **Asynchronous Reporting**: Upload test results in the background to minimize test execution time.
  * **Robustness**: Handles TestRail API limits and network issues with retries and exponential backoff.
  * **Poetry Support**: Uses Poetry for dependency management and project packaging.

## Installation

Install using Poetry:

```bash
poetry add pytest-testrail
```

## Usage

### Configure TestRail Connection

#### Command-line options

```python
pytest --testrail-url <your_testrail_url> \
       --testrail-user <your_testrail_user> \
       --testrail-password <your_testrail_password> \
       --testrail-project-id <your_testrail_project_id> \
       --testrail-run-name "<your_testrail_run_name>"
```

#### YAML Configuration (testrail_config.yaml)
```
url: <your_testrail_url>
user: <your_testrail_user>
password: <your_testrail_password>
project_id: <your_testrail_project_id>
run_name: "<your_testrail_run_name>"
```

Then, run pytest:
```python
pytest --testrail-config testrail_config.yaml
```

Link Tests to TestRail CasesUse the @pytest.mark.testrail_cases marker to associate pytest test functions with TestRail case IDs:

```python
import pytest

@pytest.mark.testrail_cases(["C123", "C456"])
def test_my_function():
    assert True
```

### Run Tests and Report Results
Run your pytest tests.  PyTestRailReporter will automatically send the results to TestRail.
```python
poetry run pytest
```

## Example

```python
import pytest

@pytest.mark.testrail_cases(["C101", "C102"])
def test_user_login():
    # Simulate user login
    user_logged_in = True
    assert user_logged_in

@pytest.mark.testrail_cases(["C205"])
def test_product_page_load():
    # Simulate loading a product page
    page_loaded = True
    assert page_loaded, "Product page should load successfully"

```

## Contributing

Contributions
