from flask import Flask

app = Flask(__name__)
conn_string = 'postgresql://postgres:postgres@localhost:5432/flaskapp'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['DEBUG'] = True
import application.views