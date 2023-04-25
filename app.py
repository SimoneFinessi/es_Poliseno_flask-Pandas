from flask import Flask, render_template, request, Response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

df=pd.read_csv("https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/metacritic_games.csv")

@app.route('/')
def home():
    return render_template('home.html')
#es1
@app.route('/es1')
def es1():
    return render_template('es1.html',list=df["platform"].unique())

@app.route('/ris1', methods=["post"])
def ris1():
    piatta=request.form["piatt"]
    trovato=df[df.platform.str.lower()==piatta.lower()].to_html()
    return render_template('risultato.html',risultato=trovato)

#es2
@app.route('/es2')
def es2():
    return render_template('es1.html',list=df["platform"].unique())

@app.route('/ris2', methods=["post"])
def ris2():
    piatta=request.form["piatt"]
    trovato=df[df.platform.str.lower()==piatta.lower()].to_html()
    return render_template('risultato.html',risultato=trovato)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)