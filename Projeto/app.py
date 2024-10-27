from flask import Flask, request, jsonify, send_file, render_template
from models import db, Vendas
import pandas as pd
from pdf_generator import generate_pdf 
from datetime import datetime


app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendas.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/') #Rota para pagina inicial da aplicação
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST']) # Rota para fazer upload do arquivo CSV
def carregar_csv():
    file = request.files['file']
    data = pd.read_csv(file)
    for _, row in data.iterrows():
        venda = Vendas(
            date=datetime.strptime(row['Data_Venda'], '%Y-%m-%d').date(),
            item=row['Produto'],
            quantidade=row['Quantidade'],
            preco=row['Preco_Unitario']
        )
        db.session.add(venda)
    db.session.commit()
    return jsonify({"mensagem": "Arquivo carregado com sucesso!"})

@app.route('/generate_pdf', methods=['GET']) #Rota para a lógica que irá gerar o PDF
def download_report():
    generate_pdf()
    return send_file("Vendas.pdf", as_attachment=True)

@app.route('/vendas', methods=['GET']) #Rota para pagina onde se encontram as vendas
def get_vendas():
    vendas = Vendas.query.all()
    return render_template('vendas.html', vendas=vendas)

@app.route('/vendas/summary', methods=['GET']) #Rota para pagina onde se encontram o resumo das vendas
def vendas_summary():
    summary = db.session.query(
        Vendas.item, db.func.sum(Vendas.quantidade).label('quantidade_total')
    ).group_by(Vendas.item).all()
    return render_template('resumo_de_vendas.html', summary=summary)

if __name__ == '__main__': # Inicia a API Flask
    app.run(debug=True)
