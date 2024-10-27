from fpdf import FPDF
from models import Vendas
from datetime import datetime

def generate_pdf():
    vendas = Vendas.query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Vendas", ln=True, align='C')
    
    pdf.cell(40, 10, "Data", border=1)
    pdf.cell(60, 10, "Item", border=1)
    pdf.cell(40, 10, "Quantidade", border=1)
    pdf.cell(40, 10, "Preco", border=1)
    pdf.ln()

    for venda in vendas:
        pdf.cell(40, 10, venda.date.strftime('%Y-%m-%d'), border=1)
        pdf.cell(60, 10, venda.item, border=1)
        pdf.cell(40, 10, str(venda.quantidade), border=1)
        pdf.cell(40, 10, f"R${venda.preco:.2f}", border=1)
        pdf.ln()

    pdf.output("Vendas.pdf")
