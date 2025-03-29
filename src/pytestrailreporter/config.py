# src/pytestrailreporter/config.py
import yaml
import pytest
import logging

def load_config(config):
    """Loads TestRail configuration from YAML or CLI options."""
    if config.getoption("--testrail-config"):
        config_path = config.getoption("--testrail-config")
        try:
            with open(config_path, 'r') as file:
                testrail_config = yaml.safe_load(file)
                return {
                    "url": testrail_config.get('url'),
                    "user": testrail_config.get('user'),
                    "password": testrail_config.get('password'),
                    "project_id": testrail_config.get('project_id'),
                    "run_name": testrail_config.get('run_name'),
                }
        except FileNotFoundError:
            logging.error(f"TestRail config file not found: {config_path}")
            raise pytest.UsageError(f"TestRail config file not found: {config_path}")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing TestRail config file: {e}")
            raise pytest.UsageError(f"Error parsing TestRail config file: {e}")
    else:
        return {
            "url": config.getoption("--testrail-url"),
            "user": config.getoption("--testrail-user"),
            "password": config.getoption("--testrail-password"),
            "project_id": config.getoption("--testrail-project-id"),
            "run_name": config.getoption("--testrail-run-name"),
        }

def validate_config(testrail_config):
    """Validates TestRail configuration."""
    if not all(testrail_config.values()):
        logging.error("Missing TestRail configuration options.")
        raise pytest.UsageError("Missing TestRail configuration options.")