import sqlite3
from datetime import datetime
from data import ContractModel


class ContractUtils:
    @staticmethod
    def validate_date(date_str):
        """
        Validate and normalize the date format to '%Y-%m-%d'.

        Args:
        - date_str (str): Date string in format '%Y-%m-%d'.

        Returns:
        - str: Validated date string in format '%Y-%m-%d'.

        Raises:
        - ValueError: If date format is not valid.
        """
        if not date_str:
            return datetime.today().date().strftime("%Y-%m-%d")  # Default to today's date if empty

        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date().strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Date format is not valid. It should be in YYYY-MM-DD format.")

    @staticmethod
    def filter_by_title(contracts, title):
        """
        Filter contracts by title.

        Args:
        - contracts (list): List of contract dictionaries.
        - title (str): Title filter string.

        Returns:
        - list: Filtered contracts.
        """
        if title:
            return [contract for contract in contracts if title.lower() in contract['title'].lower()]
        return contracts

    @staticmethod
    def filter_by_date_range(contracts, start_date=None, end_date=None):
        """
        Filter contracts by start and end dates.

        Args:
        - contracts (list): List of contract dictionaries.
        - start_date (str): Start date filter in format '%Y-%m-%d'.
        - end_date (str): End date filter in format '%Y-%m-%d'.

        Returns:
        - list: Filtered contracts.
        """
        if start_date:
            start_date = ContractUtils.validate_date(start_date)
            contracts = [contract for contract in contracts if contract['start_date'] >= start_date]

        if end_date:
            end_date = ContractUtils.validate_date(end_date)
            contracts = [contract for contract in contracts if contract['end_date'] <= end_date]

        return contracts

    @staticmethod
    def export_to_csv(file_path, contracts):
        """
        Export contracts to a CSV file.

        Args:
        - file_path (str): Path to the CSV file.
        - contracts (list): List of contract dictionaries.

        Returns:
        - bool: True if export was successful, False otherwise.
        """
        # Assuming the ContractModel handles export. Replace with custom implementation if needed.
        return ContractModel.export_to_csv(file_path, contracts)

    @staticmethod
    def export_to_sqlite(file_path, contracts):
        """
        Export contracts to an SQLite database.

        Args:
        - file_path (str): Path to the SQLite database file.
        - contracts (list): List of contract dictionaries.

        Returns:
        - bool: True if export was successful, False otherwise.
        """
        return ContractModel.export_to_sqlite(file_path, contracts)


class ContractManagerController:
    def __init__(self):
        self.model = ContractModel()

    def add_contract(self, title, start_date, end_date, description):
        """
        Add a contract to the model after validating inputs and date format.
        
        Args:
        - title (str): Title of the contract.
        - start_date (str): Start date of the contract in format '%Y-%m-%d'.
        - end_date (str): End date of the contract in format '%Y-%m-%d'.
        - description (str): Description of the contract.
        
        Raises:
        - ValueError: If any required field is missing or if dates are not valid.
        - Exception: For any unexpected errors during the addition of the contract.
        """
        try:
            if not (title and start_date and end_date):
                raise ValueError("Title, start date, and end date are required fields.")

            start_date = ContractUtils.validate_date(start_date)
            end_date = ContractUtils.validate_date(end_date)
            self.model.add_contract(title, start_date, end_date, description)

        except ValueError as ve:
            print(f"Error adding contract: {ve}")
            raise

        except Exception as e:
            print(f"Unexpected error adding contract: {e}")
            raise Exception("Unexpected error occurred while adding contract.")

    def get_contracts(self):
        """
        Retrieve all contracts from the model.

        Returns:
        - list: List of contract dictionaries.
        """
        try:
            return self.model.get_contracts()
        except Exception as e:
            print(f"Error getting contracts: {e}")
            return []

    def filter_contracts(self, title=None, start_date=None, end_date=None):
        """
        Retrieve and filter contracts by title and date range.

        Args:
        - title (str): Title filter.
        - start_date (str): Start date filter in format '%Y-%m-%d'.
        - end_date (str): End date filter in format '%Y-%m-%d'.

        Returns:
        - list: Filtered list of contract dictionaries.
        """
        try:
            contracts = self.get_contracts()
            contracts = ContractUtils.filter_by_title(contracts, title)
            contracts = ContractUtils.filter_by_date_range(contracts, start_date, end_date)
            return contracts
        except Exception as e:
            print(f"Error filtering contracts: {e}")
            return []
