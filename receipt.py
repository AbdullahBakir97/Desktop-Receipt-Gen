import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import datetime
import random
import os
import win32api

# Class to handle PDF creation
class ReceiptPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Myers International GmbH', ln=True)
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Karl-Marx-str 62, 12043 Berlin', ln=True)
        self.cell(0, 5, 'www.myers-international.com', ln=True)
        self.cell(0, 5, 'handyzentrum62@gmail.com', ln=True)
        self.ln(10)

    def customer_info(self, customer_name):
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        self.cell(200, 5, txt=f"Kunde: {customer_name}", ln=True, align="L")
        self.cell(190, 5, txt=f"Erstellungsdatum: Berlin, {current_date}", ln=True, align="R")
        self.ln(10)

    def body(self, customer_name, items):
        # Move customer_info to the beginning
        self.customer_info(customer_name)

        receipt_number = generate_receipt_number()
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, txt=f"Rechnung: {receipt_number}", ln=True)
        self.ln(5)

        # Table header
        self.set_font('Arial', 'B', 10)
        self.cell(80, 10, 'Beschreibung', border=1)
        self.cell(20, 10, 'Menge', border=1)
        self.cell(30, 10, 'Einzelpreis', border=1)
        self.cell(20, 10, 'USt', border=1)
        self.cell(30, 10, 'Gesamtpreis', border=1, ln=True)

        total_price = 0
        total_netto_19 = 0
        total_netto_0 = 0
        total_tax_19 = 0
        total_tax_0 = 0

        # Adding each item
        for item in items:
            description, quantity, unit_price, tax_included = item
            netto_price = unit_price * quantity
            tax_rate = 19 if tax_included else 0
            tax_amount = netto_price * (tax_rate / 100)
            total_item_price = netto_price + tax_amount

            total_price += total_item_price

            if tax_rate == 19:
                total_netto_19 += netto_price
                total_tax_19 += tax_amount
            else:
                total_netto_0 += netto_price
                total_tax_0 += tax_amount

            # Add item row to table
            self.cell(80, 10, description, border=1)
            self.cell(20, 10, str(quantity), border=1)
            self.cell(30, 10, f"{unit_price:.2f} EUR", border=1)
            self.cell(20, 10, f"{tax_rate}%", border=1)
            self.cell(30, 10, f"{total_item_price:.2f} EUR", border=1, ln=True)

        # Total price section
        self.ln(10)
        self.cell(0, 10, f'Gesamt: {total_price:.2f} EUR', ln=True)

        # Tax breakdown below the table in the requested format
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(40, 10, 'USt', border=1)
        self.cell(40, 10, 'Netto', border=1)
        self.cell(40, 10, 'Steuerbetrag', border=1)
        self.cell(40, 10, 'Brutto', border=1, ln=True)

        # For 0% USt
        if total_netto_0 > 0:
            brutto_0 = total_netto_0 + total_tax_0
            self.cell(40, 10, '0% USt', border=1)
            self.cell(40, 10, f'{total_netto_0:.2f} EUR', border=1)
            self.cell(40, 10, f'{total_tax_0:.2f} EUR', border=1)
            self.cell(40, 10, f'{brutto_0:.2f} EUR', border=1, ln=True)

        # For 19% USt
        if total_netto_19 > 0:
            brutto_19 = total_netto_19 + total_tax_19
            self.cell(40, 10, '19% USt', border=1)
            self.cell(40, 10, f'{total_netto_19:.2f} EUR', border=1)
            self.cell(40, 10, f'{total_tax_19:.2f} EUR', border=1)
            self.cell(40, 10, f'{brutto_19:.2f} EUR', border=1, ln=True)

        self.ln(10)
        self.cell(0, 5, 'Hinweis: Bei Angabe "0%" unterliegt der Artikel als Gebrauchtwarenkauf', ln=True)
        self.cell(0, 5, 'der Differenzbesteuerung nach §25a UStG.', ln=True)

        self.ln(10)
        self.cell(0, 5, 'Mit freundlichen Grüßen', ln=True)
        self.cell(0, 5, 'Ihr Myers International-Team', ln=True)
        return receipt_number

# Generate unique receipt number
def generate_receipt_number():
    return f"RG{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"

# Create and save PDF
def create_pdf(customer_name, items):
    pdf = ReceiptPDF()
    pdf.add_page()

    receipt_number = pdf.body(customer_name, items)  # Store the receipt number returned from the body

    pdf_file_name = f"receipt_{customer_name}_{receipt_number}.pdf"  # Correctly use receipt_number in file name
    pdf.output(pdf_file_name)
    
    return pdf_file_name

# Function to open the PDF with the default PDF viewer and trigger the print dialog
def open_pdf_and_print(file_name):
    if os.path.exists(file_name):
        win32api.ShellExecute(0, "open", file_name, None, ".", 1)

# GUI class
class ReceiptApp:
    def __init__(self, master):
        self.master = master

        self.items = []

        # Create the main layout
        self.create_widgets()

    def create_widgets(self):
        # Customer and item entry fields
        tk.Label(self.master, text="Kundenname:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_customer = tk.Entry(self.master)
        self.entry_customer.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Gerät:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_device = tk.Entry(self.master)
        self.entry_device.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Menge:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_quantity = tk.Entry(self.master)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Einzelpreis (EUR):").grid(row=3, column=0, padx=10, pady=10)
        self.entry_price = tk.Entry(self.master)
        self.entry_price.grid(row=3, column=1, padx=10, pady=10)

        # Checkbox to add tax (Mehrwertsteuer)
        self.tax_var = tk.IntVar()
        tk.Checkbutton(self.master, text="Mehrwertsteuer (19%) hinzufügen", variable=self.tax_var).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Buttons to add, remove, and manage items
        btn_add_item = tk.Button(self.master, text="Artikel hinzufügen", command=self.add_item)
        btn_add_item.grid(row=5, column=0, padx=10, pady=10)

        btn_remove_item = tk.Button(self.master, text="Artikel entfernen", command=self.remove_item)
        btn_remove_item.grid(row=5, column=1, padx=10, pady=10)

        # Table to display added items
        self.item_table = ttk.Treeview(self.master, columns=("Beschreibung", "Menge", "Einzelpreis", "USt", "Gesamtpreis"), show="headings")
        self.item_table.heading("Beschreibung", text="Beschreibung")
        self.item_table.heading("Menge", text="Menge")
        self.item_table.heading("Einzelpreis", text="Einzelpreis")
        self.item_table.heading("USt", text="USt")
        self.item_table.heading("Gesamtpreis", text="Gesamtpreis")
        self.item_table.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Buttons for saving and printing
        btn_save = tk.Button(self.master, text="Speichern und Anzeigen", command=self.save_and_view_receipt)
        btn_save.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def add_item(self):
        description = self.entry_device.get()
        quantity = int(self.entry_quantity.get())
        unit_price_str = self.entry_price.get().replace(",", ".")  # Replace comma with dot for float conversion
        try:
            unit_price = float(unit_price_str)
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie einen gültigen Preis ein (z.B., 1,00 oder 9.99)")
            return

        tax_included = self.tax_var.get() == 1

        # Calculate total item price including tax
        netto_price = quantity * unit_price
        tax_rate = 19 if tax_included else 0
        tax_amount = netto_price * (tax_rate / 100)
        total_item_price = netto_price + tax_amount

        # Add to item list and table
        self.items.append((description, quantity, unit_price, tax_included))
        self.item_table.insert("", "end", values=(description, quantity, f"{unit_price:.2f} EUR", "19%" if tax_included else "0%", f"{total_item_price:.2f} EUR"))

        # Clear the input fields
        self.entry_device.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.tax_var.set(0)

    def remove_item(self):
        selected_item = self.item_table.selection()
        if selected_item:
            selected_index = self.item_table.index(selected_item[0])
            self.item_table.delete(selected_item)
            del self.items[selected_index]
        else:
            messagebox.showwarning("Fehler", "Bitte wählen Sie einen Artikel aus, um ihn zu entfernen.")

    def save_and_view_receipt(self):
        customer_name = self.entry_customer.get()
        if customer_name and self.items:
            pdf_file_name = create_pdf(customer_name, self.items)
            open_pdf_and_print(pdf_file_name)
            messagebox.showinfo("Erfolg", f"Quittung gespeichert und angezeigt: {pdf_file_name}")
        else:
            messagebox.showwarning("Eingabefehler", "Bitte alle Felder ausfüllen und mindestens einen Artikel hinzufügen!")

# Main GUI loop
if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiptApp(root)
    root.mainloop()
