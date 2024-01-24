import os
import pandas as pd
from fpdf import FPDF
import glob
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]

        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, border=1, txt=columns[0])
        pdf.cell(w=70, h=10, border=1, txt=columns[1])
        pdf.cell(w=35, h=10, border=1, txt=columns[2])
        pdf.cell(w=30, h=10, border=1, txt=columns[3])
        pdf.cell(w=30, h=10, border=1, txt=columns[4], ln=1)
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=10, border=1, txt=str(row[product_id]))
            pdf.cell(w=70, h=10, border=1, txt=str(row[product_name]))
            pdf.cell(w=35, h=10, border=1, txt=str(row[amount_purchased]))
            pdf.cell(w=30, h=10, border=1, txt=str(row[price_per_unit]))
            pdf.cell(w=30, h=10, border=1, txt=str(row[total_price]), ln=1)

        total_sum = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, border=1, txt="")
        pdf.cell(w=70, h=10, border=1, txt="")
        pdf.cell(w=35, h=10, border=1, txt="")
        pdf.cell(w=30, h=10, border=1, txt="")
        pdf.cell(w=30, h=10, border=1, txt=str(total_sum), ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=10, txt=f"The total price is {total_sum}.", ln=1)
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=10, txt=f"MyCompany")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
