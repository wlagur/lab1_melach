from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import *
import os

app = Flask(__name__)
#app.config.update(SERVER_NAME='localhost:5010')
DB_PATH = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/register.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH  # 'sqlite:////tmp/register.db'
db = SQLAlchemy(app)

class Debtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    kod = db.Column(db.Integer, unique=True)
    date = db.Column(db.Date)
    demands = db.relationship('Demand', backref = 'Debtor', lazy = 'dynamic')
    arbitration_id = db.Column(db.Integer, db.ForeignKey('arbitration.id'))

class Arbitration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    number = db.Column(db.Integer, unique=True)
    date = db.Column(db.Date)
    debtors = db.relationship('Debtor', backref = 'Arbitration', lazy = 'dynamic')

class Creditor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    number = db.Column(db.Integer, unique=True)
    demands = db.relationship('Demand', backref = 'Creditor', lazy = 'dynamic')

class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer, unique=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('debtor.id'))
    creditor_id = db.Column(db.Integer, db.ForeignKey('creditor.id'))

@app.route('/')
def index():
    return render_template('Index.html')

if __name__ == '__main__':

    mr_manager = APIManager(app, flask_sqlalchemy_db=db)
    mr_manager.create_api(Creditor, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(Debtor, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(Arbitration, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    mr_manager.create_api(Demand, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    app.run(host='127.0.0.1', port=5010)
    # print(DB_PATH)