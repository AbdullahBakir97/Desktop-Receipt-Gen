from fpdf import FPDF
import datetime
import csv
import os
import json

# Company information
COMPANY_INFO = {
    'name': 'Myers International GmbH - Contract',
    'street': 'Karl-Marx-str 62',
    'zip': '12043 Berlin',
    'website': 'www.myers-international.com',
    'telefon': '123456789',
    'email': 'handyzentrum62@gmail.com',
}

# Directory to save contracts and to keep track of the last contract number
CONTRACTS_DIR = "contracts"
CONTRACT_NUMBER_FILE = os.path.join(CONTRACTS_DIR, "last_contract_number.json")
os.makedirs(CONTRACTS_DIR, exist_ok=True)

# Initialize the contract number file if it doesn't exist
if not os.path.exists(CONTRACT_NUMBER_FILE):
    with open(CONTRACT_NUMBER_FILE, 'w') as f:
        json.dump({"last_number": 0}, f)

# Class to handle Contract PDF creation
class ContractPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Kaufvertrag Über Ein Gebrauchtes Gerät', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'über ein gebrauchtes Mobiltelefon', ln=True, align='C')
        self.ln(10)

    def company_info(self):
        self.set_font('Arial', '', 10)
        self.cell(0, 5, COMPANY_INFO['name'], ln=True)
        self.cell(0, 5, COMPANY_INFO['street'], ln=True)
        self.cell(0, 5, COMPANY_INFO['zip'], ln=True)
        self.cell(0, 5, COMPANY_INFO['telefon'], ln=True)
        self.cell(0, 5, COMPANY_INFO['website'], ln=True)
        self.cell(0, 5, COMPANY_INFO['email'], ln=True)
        self.ln(10)

    def add_contract_code(self, contract_code):
        """Display the contract code at the beginning of the document."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Vertragsnummer: {contract_code}", ln=True, align='L')
        self.ln(5)

    def add_section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, ln=True, align="L")
        self.ln(3)

    def add_seller_buyer_info(self, seller_info, buyer_info):
        """Adds side-by-side seller and buyer info"""
        self.add_section_title("Verkäufer und Käufer")
        self.set_font('Arial', 'B', 10)
        self.cell(80, 6, "Verkäufer", border=0, align='L')
        self.cell(80, 6, "Käufer", border=0, align='L')
        self.ln(6)

        self.set_font('Arial', '', 10)
        for field in ["Vorname", "Nachname", "Straße", "PLZ / Ort", "Telefon", "E-Mail", "Ausweis-Nr"]:
            seller_value = seller_info.get(field, "")
            buyer_value = buyer_info.get(field, "")
            self.cell(80, 6, f"{field}: {seller_value}", border=0, align='L')
            self.cell(80, 6, f"{field}: {buyer_value}", border=0, align='L')
            self.ln(6)
        self.ln(5)

    def add_device_price_info(self, device_info, price_info):
        """Adds side-by-side device and price info"""
        self.add_section_title("Gegenstand / Gerät und Kaufpreis")
        self.set_font('Arial', 'B', 10)
        self.cell(80, 6, "Gegenstand / Gerät", border=0, align='L')
        self.cell(80, 6, "Kaufpreis", border=0, align='L')
        self.ln(6)

        self.set_font('Arial', '', 10)
        for field, value in device_info.items():
            self.cell(80, 6, f"{field}: {value}", border=0, align='L')
            if field == "Hersteller":
                self.cell(80, 6, f"Kaufpreis in EUR: {price_info['price']:.2f} EUR", border=0, align='L')
            elif field == "Modell":
                self.cell(80, 6, f"In Worten: {price_info['price_in_words']}", border=0, align='L')
            else:
                self.cell(80, 6, "", border=0, align='L')
            self.ln(6)
        self.ln(5)

    def add_terms_section(self, terms):
        """Add terms section below the main information sections."""
        self.add_section_title("Vereinbarungen")
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, terms)
        self.ln(5)

    def footer(self):
        """Add footer with date and side-by-side signature lines."""
        self.set_y(-30)
        self.set_font('Arial', '', 10)
        current_date = datetime.datetime.now().strftime("Datum: Berlin, %d.%m.%Y")
        self.cell(0, 5, current_date, ln=True)

        # Signature lines for both seller and buyer, side-by-side
        self.cell(90, 5, 'Unterschrift Verkäufer: _________________________', align='L')
        self.cell(90, 5, 'Unterschrift Käufer: _________________________', align='R')
        self.ln(10)

# Generate a contract code with sequential numbering
def generate_contract_code(customer_name):
    today = datetime.datetime.now().strftime('%Y%m%d')
    base_filename = f"{customer_name}_{today}_"
    
    # Read the last used contract number from file
    with open(CONTRACT_NUMBER_FILE, 'r') as f:
        data = json.load(f)
        last_number = data.get("last_number", 0)

    # Increment the contract number
    contract_number = last_number + 1
    contract_code = f"{base_filename}{contract_number:03}"
    pdf_path = os.path.join(CONTRACTS_DIR, f"{contract_code}.pdf")

    # Save the updated last contract number back to file
    with open(CONTRACT_NUMBER_FILE, 'w') as f:
        json.dump({"last_number": contract_number}, f)

    return contract_code, pdf_path

# Create and save Contract PDF
def create_contract_pdf(seller_info, buyer_info, device_info, contract_terms, price_info):
    customer_name = buyer_info.get("Vorname", "Kunde")
    contract_code, pdf_path = generate_contract_code(customer_name)
    
    pdf = ContractPDF()
    pdf.add_page()
    pdf.company_info()
    pdf.add_contract_code(contract_code)  # Show contract code in PDF
    pdf.add_seller_buyer_info(seller_info, buyer_info)
    pdf.add_device_price_info(device_info, price_info)
    pdf.add_terms_section(contract_terms)

    pdf.output(pdf_path)
    return pdf_path, contract_code

# Save contract data to CSV
def save_to_csv(seller_info, buyer_info, device_info, contract_terms, price_info, contract_code):
    # Define the file and check if it exists
    csv_file = 'contracts.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Header Section for new files with structured sections
        if not file_exists:
            writer.writerow(["Contract Summary"])
            writer.writerow(["Contract Code", contract_code])
            writer.writerow([])  # Blank line for separation

            # Section Headers
            writer.writerow(["Seller Information"])
            writer.writerow([
                "First Name", "Last Name", "Street + House No", "PLZ / Ort", "Phone", "Email", "ID No"
            ])
            writer.writerow([])

            writer.writerow(["Buyer Information"])
            writer.writerow([
                "First Name", "Last Name", "Street + House No", "PLZ / Ort", "Phone", "Email", "ID No"
            ])
            writer.writerow([])

            writer.writerow(["Device Information"])
            writer.writerow([
                "Manufacturer", "Model", "Serial Number", "Features", "Condition", "Accessories"
            ])
            writer.writerow([])

            writer.writerow(["Price and Terms"])
            writer.writerow(["Price (EUR)", "Price (Words)", "Delivery Date", "Contract Terms"])
            writer.writerow([])  # End of Header Section

        # Write the data in a structured format, under the headers
        writer.writerow([contract_code])  # Contract code row for reference
        writer.writerow([])  # Blank line for section separation

        # Seller Information
        writer.writerow([
            seller_info.get('Vorname', ''), seller_info.get('Nachname', ''),
            seller_info.get('Straße', ''), seller_info.get('PLZ / Ort', ''),
            seller_info.get('Telefon', ''), seller_info.get('E-Mail', ''),
            seller_info.get('Ausweis-Nr', '')
        ])
        writer.writerow([])  # Blank line for separation

        # Buyer Information
        writer.writerow([
            buyer_info.get('Vorname', ''), buyer_info.get('Nachname', ''),
            buyer_info.get('Straße', ''), buyer_info.get('PLZ / Ort', ''),
            buyer_info.get('Telefon', ''), buyer_info.get('E-Mail', ''),
            buyer_info.get('Ausweis-Nr', '')
        ])
        writer.writerow([])  # Blank line for separation

        # Device Information
        writer.writerow([
            device_info.get('Hersteller', ''), device_info.get('Modell', ''),
            device_info.get('Seriennummer', ''), device_info.get('Besonderheiten', ''),
            device_info.get('Zustand', ''), device_info.get('Sonstiges/Zubehör', '')
        ])
        writer.writerow([])  # Blank line for separation

        # Price and Terms
        writer.writerow([
            price_info.get('price', ''), price_info.get('price_in_words', ''),
            price_info.get('delivery_date', ''), contract_terms
        ])
        writer.writerow([])  # Blank line after each contract for readability
