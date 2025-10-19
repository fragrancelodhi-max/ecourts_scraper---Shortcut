import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=30)

if response.status_code == 200:
    html_content = response.text
    print("✅ Connection Successful")
else:
    print("❌ Failed to fetch page. Status:", response.status_code)
    exit()

soup = BeautifulSoup(html_content, "html.parser")

# Example: extracting all links containing 'cause' word
links = []
for a in soup.find_all("a", href=True):
    if "cause" in a["href"]:
        links.append(a["href"])

if not links:
    print("⚠ No cause list links found.")
else:
    print(f"Found {len(links)} links. Saving first one as PDF...")

    # Make PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Cause List Links", ln=True, align='C')

    for link in links:
        pdf.cell(200, 10, txt=link, ln=True, align='L')

    pdf.output("cause_list.pdf")
    print("✅ cause_list.pdf file saved successfully.")
