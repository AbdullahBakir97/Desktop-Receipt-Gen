# gui.py
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk
from contract import create_contract_pdf, save_to_csv, COMPANY_INFO
import os
import datetime
import subprocess
import platform
from num2words import num2words

# GUI class for contract creation
class ContractApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Contract Generator")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")

        # Initialize buyer_info and seller_info attributes
        self.buyer_info = {}
        self.seller_info = {}

        # Create main frame with scrollbar
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scroll_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.scrollable_frame, text="Contract Generator", font=("Arial", 16), bg="#f0f0f0")
        title_label.grid(row=0, column=0, padx=10, pady=10)

        # Dropdown to select company type
        self.company_type_var = tk.StringVar()
        self.company_type_var.set("Buyer")

        selection_frame = ttk.Frame(self.scrollable_frame)
        selection_frame.grid(row=1, column=0, padx=10, pady=10)
        tk.Label(selection_frame, text="Select Company Type:", bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        company_type_dropdown = ttk.Combobox(selection_frame, textvariable=self.company_type_var, 
                                              values=["Buyer", "Seller"], state='readonly')
        company_type_dropdown.pack(side=tk.LEFT, padx=10)
        company_type_dropdown.bind("<<ComboboxSelected>>", self.populate_company_info)

        # Create a frame for Seller and Buyer information side by side
        buyer_seller_frame = ttk.Frame(self.scrollable_frame)
        buyer_seller_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Seller Section
        self.create_seller_section(buyer_seller_frame)

        # Buyer Section
        self.create_buyer_section(buyer_seller_frame)

        # Create a frame for Device and Price information side by side
        device_price_frame = ttk.Frame(self.scrollable_frame)
        device_price_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Device Section
        self.create_device_section(device_price_frame)

        # Price Section
        self.create_price_section(device_price_frame)

        # Terms Section
        self.create_terms_section(self.scrollable_frame)

        # Button to create and display contract
        btn_create_contract = ttk.Button(self.scrollable_frame, text="Create and View Contract", command=self.save_and_generate)
        btn_create_contract.grid(row=5, column=0, padx=10, pady=20)

    def populate_company_info(self, event):
        selected_type = self.company_type_var.get()
        info_fields = {
            'Vorname': COMPANY_INFO['name'],
            'Adresse': COMPANY_INFO['street'],
            'Telefon': COMPANY_INFO['telefon'],
            'E-Mail': COMPANY_INFO['email']
        }

        # Clear the fields before populating them
        if selected_type == "Buyer":
            self.clear_buyer_fields()
            self.fill_info(self.entry_buyer_first_name, info_fields['Vorname'])
            self.fill_info(self.entry_buyer_address, info_fields['Adresse'])
            self.fill_info(self.entry_buyer_phone, info_fields['Telefon'])
            self.fill_info(self.entry_buyer_email, info_fields['E-Mail'])
        elif selected_type == "Seller":
            self.clear_seller_fields()
            self.fill_info(self.entry_seller_first_name, info_fields['Vorname'])
            self.fill_info(self.entry_seller_address, info_fields['Adresse'])
            self.fill_info(self.entry_seller_phone, info_fields['Telefon'])
            self.fill_info(self.entry_seller_email, info_fields['E-Mail'])

    def clear_buyer_fields(self):
        self.entry_buyer_first_name.delete(0, tk.END)
        self.entry_buyer_last_name.delete(0, tk.END)
        self.entry_buyer_address.delete(0, tk.END)
        self.entry_buyer_phone.delete(0, tk.END)
        self.entry_buyer_email.delete(0, tk.END)

    def clear_seller_fields(self):
        self.entry_seller_first_name.delete(0, tk.END)
        self.entry_seller_last_name.delete(0, tk.END)
        self.entry_seller_address.delete(0, tk.END)
        self.entry_seller_phone.delete(0, tk.END)
        self.entry_seller_email.delete(0, tk.END)

    def fill_info(self, entry_widget, value):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, value)

    def create_seller_section(self, parent):
        seller_frame = ttk.LabelFrame(parent, text="Seller Information")
        seller_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        tk.Label(seller_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_seller_first_name = tk.Entry(seller_frame)
        self.entry_seller_first_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(seller_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_seller_last_name = tk.Entry(seller_frame)
        self.entry_seller_last_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(seller_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_seller_address = tk.Entry(seller_frame)
        self.entry_seller_address.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(seller_frame, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_seller_phone = tk.Entry(seller_frame)
        self.entry_seller_phone.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(seller_frame, text="E-Mail:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_seller_email = tk.Entry(seller_frame)
        self.entry_seller_email.grid(row=4, column=1, padx=5, pady=5)

    def create_buyer_section(self, parent):
        buyer_frame = ttk.LabelFrame(parent, text="Buyer Information")
        buyer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(buyer_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_buyer_first_name = tk.Entry(buyer_frame)
        self.entry_buyer_first_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(buyer_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_buyer_last_name = tk.Entry(buyer_frame)
        self.entry_buyer_last_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(buyer_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_buyer_address = tk.Entry(buyer_frame)
        self.entry_buyer_address.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(buyer_frame, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_buyer_phone = tk.Entry(buyer_frame)
        self.entry_buyer_phone.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(buyer_frame, text="E-Mail:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_buyer_email = tk.Entry(buyer_frame)
        self.entry_buyer_email.grid(row=4, column=1, padx=5, pady=5)

    def create_device_section(self, parent):
        device_frame = ttk.LabelFrame(parent, text="Device Information")
        device_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(device_frame, text="Device Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_device_type = tk.Entry(device_frame)
        self.entry_device_type.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(device_frame, text="Device Model:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_device_model = tk.Entry(device_frame)
        self.entry_device_model.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(device_frame, text="IMEI Number:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_imei_number = tk.Entry(device_frame)
        self.entry_imei_number.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(device_frame, text="Condition:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_condition = tk.Entry(device_frame)
        self.entry_condition.grid(row=3, column=1, padx=5, pady=5)

    def create_price_section(self, parent):
        price_frame = ttk.LabelFrame(parent, text="Price Information")
        price_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(price_frame, text="Price (EUR):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_price = tk.Entry(price_frame)
        self.entry_price.grid(row=0, column=1, padx=5, pady=5)

    def create_terms_section(self, parent):
        terms_frame = ttk.LabelFrame(parent, text="Contract Terms")
        terms_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.text_terms = tk.Text(terms_frame, height=4, width=60)
        self.text_terms.grid(row=0, column=0, padx=5, pady=5)

    def save_and_generate(self):
        # Get seller, buyer, device info, contract terms, and price
        self.seller_info = {
            'Vorname': self.entry_seller_first_name.get(),
            'Nachname': self.entry_seller_last_name.get(),
            'Adresse': self.entry_seller_address.get(),
            'Telefon': self.entry_seller_phone.get(),
            'E-Mail': self.entry_seller_email.get(),
        }

        self.buyer_info = {
            'Vorname': self.entry_buyer_first_name.get(),
            'Nachname': self.entry_buyer_last_name.get(),
            'Adresse': self.entry_buyer_address.get(),
            'Telefon': self.entry_buyer_phone.get(),
            'E-Mail': self.entry_buyer_email.get(),
        }

        device_info = {
            'Gerätetyp': self.entry_device_type.get(),
            'Modell': self.entry_device_model.get(),
            'IMEI-Nummer': self.entry_imei_number.get(),
            'Zustand': self.entry_condition.get(),
        }

        contract_terms = self.text_terms.get("1.0", tk.END).strip()

        price = float(self.entry_price.get())
        price_in_words = num2words(price, lang='de')  # Convert price to words in German
        delivery_date = datetime.datetime.now().strftime("Berlin,%d.%m.%Y")

        price_info = {
            'price': price,
            'price_in_words': price_in_words,
            'delivery_date': delivery_date
        }

        # Create contract PDF
        pdf_file_name = create_contract_pdf(self.seller_info, self.buyer_info, device_info, contract_terms, price_info)
        save_to_csv(self.seller_info, self.buyer_info, device_info, contract_terms, price_info)

        # Show success message
        messagebox.showinfo("Success", f"Contract created successfully!\nSaved as: {pdf_file_name}")
        self.open_pdf(pdf_file_name)

    def open_pdf(self, pdf_file):
        if platform.system() == "Windows":
            os.startfile(pdf_file)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(['open', pdf_file])
        else:  # Linux
            subprocess.call(['xdg-open', pdf_file])

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContractApp(root)
    root.mainloop()
