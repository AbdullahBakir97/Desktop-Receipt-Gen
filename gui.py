# gui.py
from tkinter import ttk, messagebox
import tkinter as tk
from contract import create_contract_pdf, save_to_csv, COMPANY_INFO
import os
import datetime
import subprocess
import platform
from num2words import num2words

class ContractApp:
    def __init__(self, master):
        self.master = master

        # Set up the main frame and scrollable canvas for the UI
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)  # Prevents resizing based on content

        self.canvas = tk.Canvas(self.main_frame)
        self.scroll_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Create a scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Update canvas scroll region when the scrollable frame size changes
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Add scrolling functionality for both scroll bar and mouse wheel
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.create_widgets()

    def _on_mousewheel(self, event):
        """Scroll with mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.scrollable_frame, text="Contract Generator", font=("Arial", 16), bg="#f0f0f0")
        title_label.grid(row=0, column=0, padx=10, pady=10)

        # Dropdown for selecting company type
        self.company_type_var = tk.StringVar()
        self.company_type_var.set("Buyer")

        selection_frame = ttk.Frame(self.scrollable_frame)
        selection_frame.grid(row=1, column=0, padx=10, pady=10)
        tk.Label(selection_frame, text="Select Company Type:", bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        
        company_type_dropdown = ttk.Combobox(selection_frame, textvariable=self.company_type_var, 
                                            values=["Buyer", "Seller"], state='readonly')
        company_type_dropdown.pack(side=tk.LEFT, padx=10)
        company_type_dropdown.bind("<<ComboboxSelected>>", self.populate_company_info)

        # Seller and Buyer information sections
        self.create_seller_buyer_section()

        # Device and Price information sections
        self.create_device_price_section()

        # Terms section below the main fields
        self.create_terms_section()

        # Button to create and display contract
        btn_create_contract = ttk.Button(self.scrollable_frame, text="Create and View Contract", command=self.save_and_generate)
        btn_create_contract.grid(row=6, column=0, padx=10, pady=10)

        # Button to export CSV
        btn_export_csv = ttk.Button(self.scrollable_frame, text="Export to CSV and Open", command=self.export_csv)
        btn_export_csv.grid(row=6, column=1, padx=10, pady=10)



    def export_csv(self):
        """Export the contracts to CSV and open the file."""
        csv_file = 'contracts.csv'
        if os.path.exists(csv_file):
            if platform.system() == "Windows":
                os.startfile(csv_file)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(['open', csv_file])
            else:  # Linux
                subprocess.call(['xdg-open', csv_file])
        else:
            messagebox.showwarning("Warning", "CSV file not found.")


    def populate_company_info(self, event):
        """Populate fields with company info based on the selected type (Buyer or Seller)."""
        selected_type = self.company_type_var.get()
        info_fields = {
            'Vorname': COMPANY_INFO['name'],
            'Adresse': COMPANY_INFO['street'],
            'PLZ / Ort': COMPANY_INFO['zip'],
            'Telefon': COMPANY_INFO['telefon'],
            'E-Mail': COMPANY_INFO['email']
        }

        if selected_type == "Buyer":
            self.clear_seller_fields()  # Clear Seller fields if Buyer is selected
            self.fill_info(self.entry_buyer_first_name, info_fields['Vorname'])
            self.fill_info(self.entry_buyer_street, info_fields['Adresse'])
            self.fill_info(self.entry_buyer_plz, info_fields['PLZ / Ort'])
            self.fill_info(self.entry_buyer_phone, info_fields['Telefon'])
            self.fill_info(self.entry_buyer_email, info_fields['E-Mail'])
        elif selected_type == "Seller":
            self.clear_buyer_fields()  # Clear Buyer fields if Seller is selected
            self.fill_info(self.entry_seller_first_name, info_fields['Vorname'])
            self.fill_info(self.entry_seller_street, info_fields['Adresse'])
            self.fill_info(self.entry_seller_plz, info_fields['PLZ / Ort'])
            self.fill_info(self.entry_seller_phone, info_fields['Telefon'])
            self.fill_info(self.entry_seller_email, info_fields['E-Mail'])

    def clear_buyer_fields(self):
        """Clear Buyer fields."""
        for entry in [
            self.entry_buyer_first_name, self.entry_buyer_last_name, self.entry_buyer_street,
            self.entry_buyer_plz, self.entry_buyer_phone, self.entry_buyer_email, self.entry_buyer_id
        ]:
            entry.delete(0, tk.END)

    def clear_seller_fields(self):
        """Clear Seller fields."""
        for entry in [
            self.entry_seller_first_name, self.entry_seller_last_name, self.entry_seller_street,
            self.entry_seller_plz, self.entry_seller_phone, self.entry_seller_email, self.entry_seller_id
        ]:
            entry.delete(0, tk.END)

    def fill_info(self, entry_widget, value):
        """Fill an entry widget with a given value."""
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, value)

    def create_seller_buyer_section(self):
        """Create side-by-side sections for Seller and Buyer information."""
        seller_buyer_frame = ttk.Frame(self.scrollable_frame)
        seller_buyer_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.create_seller_section(seller_buyer_frame)
        self.create_buyer_section(seller_buyer_frame)

    def create_seller_section(self, parent):
        """Create the Seller Information section."""
        seller_frame = ttk.LabelFrame(parent, text="Seller Information")
        seller_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        fields = ["First Name", "Last Name", "Street + House No", "PLZ / Ort", "Phone", "Email", "ID No"]
        self.entry_seller_first_name = self.create_field(seller_frame, fields[0], 0)
        self.entry_seller_last_name = self.create_field(seller_frame, fields[1], 1)
        self.entry_seller_street = self.create_field(seller_frame, fields[2], 2)
        self.entry_seller_plz = self.create_field(seller_frame, fields[3], 3)
        self.entry_seller_phone = self.create_field(seller_frame, fields[4], 4)
        self.entry_seller_email = self.create_field(seller_frame, fields[5], 5)
        self.entry_seller_id = self.create_field(seller_frame, fields[6], 6)

    def create_buyer_section(self, parent):
        """Create the Buyer Information section."""
        buyer_frame = ttk.LabelFrame(parent, text="Buyer Information")
        buyer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        fields = ["First Name", "Last Name", "Street + House No", "PLZ / Ort", "Phone", "Email", "ID No"]
        self.entry_buyer_first_name = self.create_field(buyer_frame, fields[0], 0)
        self.entry_buyer_last_name = self.create_field(buyer_frame, fields[1], 1)
        self.entry_buyer_street = self.create_field(buyer_frame, fields[2], 2)
        self.entry_buyer_plz = self.create_field(buyer_frame, fields[3], 3)
        self.entry_buyer_phone = self.create_field(buyer_frame, fields[4], 4)
        self.entry_buyer_email = self.create_field(buyer_frame, fields[5], 5)
        self.entry_buyer_id = self.create_field(buyer_frame, fields[6], 6)

    def create_device_price_section(self):
        """Create side-by-side sections for Device and Price information."""
        device_price_frame = ttk.Frame(self.scrollable_frame)
        device_price_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.create_device_section(device_price_frame)
        self.create_price_section(device_price_frame)

    def create_device_section(self, parent):
        """Create the Device Information section."""
        device_frame = ttk.LabelFrame(parent, text="Device Information")
        device_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        fields = ["Manufacturer", "Model", "Serial Number", "Features", "Condition", "Accessories"]
        self.entry_device_manufacturer = self.create_field(device_frame, fields[0], 0)
        self.entry_device_model = self.create_field(device_frame, fields[1], 1)
        self.entry_device_serial = self.create_field(device_frame, fields[2], 2)
        self.entry_device_features = self.create_field(device_frame, fields[3], 3)
        self.entry_device_condition = self.create_field(device_frame, fields[4], 4)
        self.entry_device_accessories = self.create_field(device_frame, fields[5], 5)

    def create_price_section(self, parent):
        """Create the Price Information section."""
        price_frame = ttk.LabelFrame(parent, text="Price Information")
        price_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(price_frame, text="Price (EUR):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_price = tk.Entry(price_frame)
        self.entry_price.grid(row=0, column=1, padx=5, pady=5)

    def create_terms_section(self):
        """Create the Contract Terms section."""
        terms_frame = ttk.LabelFrame(self.scrollable_frame, text="Contract Terms")
        terms_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.text_terms = tk.Text(terms_frame, height=4, width=60)
        self.text_terms.grid(row=0, column=0, padx=5, pady=5)

    def create_field(self, frame, label, row):
        """Create a labeled entry field in the given frame."""
        tk.Label(frame, text=f"{label}:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def save_and_generate(self):
        seller_info = {
            'Vorname': self.entry_seller_first_name.get(),
            'Nachname': self.entry_seller_last_name.get(),
            'Straße': self.entry_seller_street.get(),
            'PLZ / Ort': self.entry_seller_plz.get(),
            'Telefon': self.entry_seller_phone.get(),
            'E-Mail': self.entry_seller_email.get(),
            'Ausweis-Nr': self.entry_seller_id.get()
        }

        buyer_info = {
            'Vorname': self.entry_buyer_first_name.get(),
            'Nachname': self.entry_buyer_last_name.get(),
            'Straße': self.entry_buyer_street.get(),
            'PLZ / Ort': self.entry_buyer_plz.get(),
            'Telefon': self.entry_buyer_phone.get(),
            'E-Mail': self.entry_buyer_email.get(),
            'Ausweis-Nr': self.entry_buyer_id.get()
        }

        device_info = {
            'Hersteller': self.entry_device_manufacturer.get(),
            'Modell': self.entry_device_model.get(),
            'Seriennummer': self.entry_device_serial.get(),
            'Besonderheiten': self.entry_device_features.get(),
            'Zustand': self.entry_device_condition.get(),
            'Sonstiges/Zubehör': self.entry_device_accessories.get()
        }

        contract_terms = self.text_terms.get("1.0", tk.END).strip()

        price = float(self.entry_price.get())
        price_in_words = num2words(price, lang='de').upper()
        delivery_date = datetime.datetime.now().strftime("Berlin, %d.%m.%Y")

        price_info = {
            'price': price,
            'price_in_words': price_in_words,
            'delivery_date': delivery_date
        }

        # Generate the contract PDF and retrieve the contract code and file path
        pdf_file_name, contract_code = create_contract_pdf(seller_info, buyer_info, device_info, contract_terms, price_info)

        # Save contract details to CSV with contract_code
        save_to_csv(seller_info, buyer_info, device_info, contract_terms, price_info, contract_code)

        # Show success message
        messagebox.showinfo("Success", f"Contract created successfully!\nSaved as: {pdf_file_name}")
        self.open_pdf(pdf_file_name)

    def open_pdf(self, pdf_file):
        """Open the generated PDF file with the default viewer."""
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
