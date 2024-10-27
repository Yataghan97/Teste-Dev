from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    item = db.Column(db.String(30), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Venda {self.item}>"
