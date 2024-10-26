import tkinter as tk
from tkinter import ttk
from gui import ContractApp  # Import ContractApp from gui.py
from receipt import ReceiptApp  # Import ReceiptApp from receipt.py

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Business Management Application")  # Set title here
        self.master.geometry("1000x700")  # Set window size here
        
        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)

        # Set up the Contract tab
        self.contract_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.contract_tab, text="Contract")
        self.contract_app = ContractApp(self.contract_tab)  # Instantiate ContractApp in the contract_tab

        # Set up the Receipt tab
        self.receipt_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.receipt_tab, text="Receipt")
        self.receipt_app = ReceiptApp(self.receipt_tab)  # Instantiate ReceiptApp in the receipt_tab

# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
