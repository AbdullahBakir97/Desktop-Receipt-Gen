from fpdf import FPDF
import datetime
import random
import csv

# Company information
COMPANY_INFO = {
    'name': 'Myers International GmbH - Contract',
    'street': 'Karl-Marx-str 62',
    'zip': '12043 Berlin',
    'website': 'www.myers-international.com',
    'telefon': '123456789',
    'email': 'handyzentrum62@gmail.com',
}

# Class to handle Contract PDF creation
class ContractPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Kaufvertrag über ein gebrauchtes Gerät', ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, COMPANY_INFO['name'], ln=True)
        self.cell(0, 5, COMPANY_INFO['street'], ln=True)
        self.cell(0, 5, COMPANY_INFO['zip'], ln=True)
        self.cell(0, 5, COMPANY_INFO['telefon'], ln=True)
        self.cell(0, 5, COMPANY_INFO['website'], ln=True)
        self.cell(0, 5, COMPANY_INFO['email'], ln=True)
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def add_field(self, label, value):
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'{label}: {value}', ln=True)

    def contract_info(self, seller_info, buyer_info, device_info, contract_terms, price_info):
        # Seller Info
        self.section_title("Verkäufer")
        for field, value in seller_info.items():
            self.add_field(field, value)

        # Buyer Info
        self.section_title("Käufer")
        for field, value in buyer_info.items():
            self.add_field(field, value)

        # Device Info
        self.section_title("Gegenstand / Gerät")
        for field, value in device_info.items():
            self.add_field(field, value)

        # Terms
        self.section_title("Vereinbarungen")
        self.multi_cell(0, 10, contract_terms)
        self.ln(5)

        # Price
        self.section_title("Kaufpreis")
        self.add_field("Kaufpreis in EUR", price_info['price'])
        self.add_field("In Worten", price_info['price_in_words'])
        self.add_field("Übergabezeitpunkt am", price_info['delivery_date'])

    def footer(self):
        self.set_y(-30)
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Sign: _____________________________', ln=True)
        self.cell(0, 5, 'Date: _____________________________', ln=True)

# Generate unique contract number
def generate_contract_number():
    return f"CN{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"

# Create and save Contract PDF
def create_contract_pdf(seller_info, buyer_info, device_info, contract_terms, price_info):
    pdf = ContractPDF()
    pdf.add_page()

    contract_number = generate_contract_number()
    pdf.contract_info(seller_info, buyer_info, device_info, contract_terms, price_info)

    pdf_file_name = f"contract_{buyer_info['Vorname']}_{contract_number}.pdf"
    pdf.output(pdf_file_name)

    return pdf_file_name

# Save contract data to CSV
def save_to_csv(seller_info, buyer_info, device_info, contract_terms, price_info):
    with open('contracts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            seller_info['Vorname'],
            seller_info['Nachname'],
            buyer_info['Vorname'],
            buyer_info['Nachname'],
            device_info['Gerätetyp'],
            price_info['price'],
            price_info['price_in_words'],
            price_info['delivery_date'],
            contract_terms
        ])

