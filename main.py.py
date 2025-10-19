import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Function to scrape cause list and create PDF
def fetch_cause_list():
    state = entry_state.get()
    district = entry_district.get()
    court_complex = entry_court.get()
    court_name = entry_court_name.get()
    date_input = entry_date.get()

    if not state or not district or not court_complex or not date_input:
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        # Format date if needed
        date_obj = datetime.strptime(date_input, "%d-%m-%Y")
        formatted_date = date_obj.strftime("%d-%m-%Y")
    except ValueError:
        messagebox.showerror("Error", "Date format should be DD-MM-YYYY")
        return

    # Construct a URL (replace with actual eCourts URL logic)
    url = f"https://districts.ecourts.gov.in/{district.replace(' ', '')}/cause-list?court={court_complex.replace(' ', '')}&date={formatted_date}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Example: scrape all table rows (adjust selector as per actual site)
        rows = soup.find_all("tr")
        if not rows:
            messagebox.showinfo("Info", "No cause list found for this input")
            return

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Cause List - {court_complex}, {district}, {state}", ln=True, align="C")
        pdf.ln(5)

        for row in rows:
            row_text = " | ".join([col.get_text(strip=True) for col in row.find_all("td")])
            if row_text:
                pdf.multi_cell(0, 8, row_text)

        pdf_file = "cause_list.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Success", f"PDF generated successfully: {pdf_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch cause list: {e}")

# Create GUI window
root = tk.Tk()
root.title("eCourts Cause List Scraper")

# Labels and Entry fields
tk.Label(root, text="State Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_state = tk.Entry(root, width=30)
entry_state.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="District Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_district = tk.Entry(root, width=30)
entry_district.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Court Complex:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_court = tk.Entry(root, width=30)
entry_court.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Court Name (optional):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_court_name = tk.Entry(root, width=30)
entry_court_name.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Date (DD-MM-YYYY):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_date = tk.Entry(root, width=30)
entry_date.grid(row=4, column=1, padx=10, pady=5)

# Fetch button
btn_fetch = tk.Button(root, text="Fetch Cause List", command=fetch_cause_list, width=25, bg="blue", fg="white")
btn_fetch.grid(row=5, column=0, columnspan=2, pady=15)

root.mainloop()
