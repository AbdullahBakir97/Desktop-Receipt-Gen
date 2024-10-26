import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'contracts.db')

class ContractModel:
    def __init__(self):
        """Initialize the ContractModel and create the database connection."""
        self.conn = self.create_connection(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables_if_not_exist()

    def create_connection(self, db_file):
        """Create a database connection to the SQLite database."""
        try:
            conn = sqlite3.connect(db_file)
            print(f"Connected to database: {db_file}")
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            return None

    def create_tables_if_not_exist(self):
        """Create the contracts table if it does not exist."""
        sql_create_contracts_table = """ 
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_first_name TEXT NOT NULL,
                seller_last_name TEXT NOT NULL,
                seller_address TEXT NOT NULL,
                seller_phone TEXT NOT NULL,
                seller_email TEXT NOT NULL,
                buyer_first_name TEXT NOT NULL,
                buyer_last_name TEXT NOT NULL,
                buyer_address TEXT NOT NULL,
                buyer_phone TEXT NOT NULL,
                buyer_email TEXT NOT NULL,
                device_type TEXT NOT NULL,
                device_model TEXT NOT NULL,
                imei_number TEXT NOT NULL,
                condition TEXT NOT NULL,
                price REAL NOT NULL,
                terms TEXT,
                created_at TEXT NOT NULL
            )
        """
        try:
            self.cursor.execute(sql_create_contracts_table)
            self.conn.commit()
            print("Contracts table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_contract(self, seller_first_name, seller_last_name, seller_address, seller_phone,
                     seller_email, buyer_first_name, buyer_last_name, buyer_address,
                     buyer_phone, buyer_email, device_type, device_model, imei_number,
                     condition, price, terms):
        """Insert a new contract into the contracts table."""
        created_at = datetime.now().isoformat()
        try:
            self.cursor.execute('''
                INSERT INTO contracts (
                    seller_first_name, seller_last_name, seller_address, seller_phone,
                    seller_email, buyer_first_name, buyer_last_name, buyer_address,
                    buyer_phone, buyer_email, device_type, device_model,
                    imei_number, condition, price, terms, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (seller_first_name, seller_last_name, seller_address, seller_phone,
                  seller_email, buyer_first_name, buyer_last_name, buyer_address,
                  buyer_phone, buyer_email, device_type, device_model,
                  imei_number, condition, price, terms, created_at))
            self.conn.commit()
            print("Contract added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding contract: {e}")

    def get_contracts(self):
        """Fetch all contracts from the database."""
        try:
            self.cursor.execute('SELECT * FROM contracts')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching contracts: {e}")
            return []

    def get_contract_by_id(self, contract_id):
        """Fetch a contract by its ID."""
        try:
            self.cursor.execute('SELECT * FROM contracts WHERE id=?', (contract_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching contract by ID: {e}")
            return None

    def update_contract(self, contract_id, seller_first_name, seller_last_name, seller_address,
                        seller_phone, seller_email, buyer_first_name, buyer_last_name,
                        buyer_address, buyer_phone, buyer_email, device_type, device_model,
                        imei_number, condition, price, terms):
        """Update a contract's details."""
        try:
            self.cursor.execute('''
                UPDATE contracts 
                SET seller_first_name=?, seller_last_name=?, seller_address=?, seller_phone=?,
                    seller_email=?, buyer_first_name=?, buyer_last_name=?, buyer_address=?,
                    buyer_phone=?, buyer_email=?, device_type=?, device_model=?,
                    imei_number=?, condition=?, price=?, terms=?
                WHERE id=?
            ''', (seller_first_name, seller_last_name, seller_address, seller_phone,
                  seller_email, buyer_first_name, buyer_last_name, buyer_address,
                  buyer_phone, buyer_email, device_type, device_model,
                  imei_number, condition, price, terms, contract_id))
            self.conn.commit()
            print("Contract updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating contract: {e}")

    def remove_contract(self, contract_id):
        """Remove a contract from the database."""
        try:
            self.cursor.execute('DELETE FROM contracts WHERE id=?', (contract_id,))
            self.conn.commit()
            print("Contract removed successfully.")
        except sqlite3.Error as e:
            print(f"Error removing contract: {e}")

    def export_to_csv(self, file_path):
        """Export contracts to a CSV file."""
        try:
            contracts = self.get_contracts()
            df = pd.DataFrame(contracts, columns=[
                'id', 'seller_first_name', 'seller_last_name', 'seller_address',
                'seller_phone', 'seller_email', 'buyer_first_name', 'buyer_last_name',
                'buyer_address', 'buyer_phone', 'buyer_email', 'device_type',
                'device_model', 'imei_number', 'condition', 'price', 'terms', 'created_at'
            ])
            df.to_csv(file_path, index=False)
            print(f"Data exported to {file_path} successfully.")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def export_to_pdf(self, file_path):
        """Export contracts to a PDF file."""
        try:
            contracts = self.get_contracts()
            df = pd.DataFrame(contracts, columns=[
                'id', 'seller_first_name', 'seller_last_name', 'seller_address',
                'seller_phone', 'seller_email', 'buyer_first_name', 'buyer_last_name',
                'buyer_address', 'buyer_phone', 'buyer_email', 'device_type',
                'device_model', 'imei_number', 'condition', 'price', 'terms', 'created_at'
            ])

            fig, ax = plt.subplots(figsize=(10, 8))
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

            pdf = matplotlib.backends.backend_pdf.PdfPages(file_path)
            pdf.savefig(fig, bbox_inches='tight')
            pdf.close()
            print(f"Data exported to {file_path} successfully.")
        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def export_to_sqlite(self, file_path):
        """Export contracts to another SQLite database."""
        try:
            with sqlite3.connect(file_path) as conn_export:
                cursor_export = conn_export.cursor()
                cursor_export.execute('''
                    CREATE TABLE IF NOT EXISTS contracts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        seller_first_name TEXT NOT NULL,
                        seller_last_name TEXT NOT NULL,
                        seller_address TEXT NOT NULL,
                        seller_phone TEXT NOT NULL,
                        seller_email TEXT NOT NULL,
                        buyer_first_name TEXT NOT NULL,
                        buyer_last_name TEXT NOT NULL,
                        buyer_address TEXT NOT NULL,
                        buyer_phone TEXT NOT NULL,
                        buyer_email TEXT NOT NULL,
                        device_type TEXT NOT NULL,
                        device_model TEXT NOT NULL,
                        imei_number TEXT NOT NULL,
                        condition TEXT NOT NULL,
                        price REAL NOT NULL,
                        terms TEXT,
                        created_at TEXT NOT NULL
                    )
                ''')

                contracts = self.get_contracts()
                cursor_export.executemany('''
                    INSERT INTO contracts (
                        seller_first_name, seller_last_name, seller_address, seller_phone,
                        seller_email, buyer_first_name, buyer_last_name, buyer_address,
                        buyer_phone, buyer_email, device_type, device_model,
                        imei_number, condition, price, terms, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [(c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10],
                        c[11], c[12], c[13], c[14], c[15], c[16], c[17]) for c in contracts])
                conn_export.commit()
                print(f"Data exported to {file_path} successfully.")
        except sqlite3.Error as e:
            print(f"Error exporting to SQLite: {e}")

    def close_connection(self):
        """Close the database connection."""
        try:
            self.conn.close()
            print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")

# Example usage
if __name__ == '__main__':
    model = ContractModel()
    # Example of adding a contract
    model.add_contract("Alice", "Johnson", "123 Elm St", "123-456-7890", "alice@example.com",
                       "Bob", "Smith", "456 Oak St", "987-654-3210", "bob@example.com",
                       "Smartphone", "iPhone 14", "123456789012345", "New", 699.99,
                       "No returns after 30 days.")
    
    # Fetch and print all contracts
    contracts = model.get_contracts()
    print(contracts)
    
    # Export contracts to CSV
    model.export_to_csv('contracts.csv')
    
    # Close the connection
    model.close_connection()
