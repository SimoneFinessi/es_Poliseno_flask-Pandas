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
    return render_template('es2.html')

@app.route('/ris2', methods=["post"])
def ris2():
    mass=int(request.form["massimo"])
    minimo=int(request.form["minimo"])
    inmezzo=pd.DataFrame()
    for i in range(len(df)):
        data=df.loc[i].release_date[8:12]
        if int(data)>=minimo and int(data)<=mass:
            inmezzo=pd.concat([inmezzo,df.loc[i]],axis=1)
    trovato=inmezzo.to_html()
    return render_template('risultato.html',risultato=trovato)
#es3
@app.route('/es3')
def es3():
    lista=[int(df.loc[i].metascore + df.loc[i].user_score) for i in range(len(df)) ]
    trovato=df[df.metascore + df.user_score==max(lista)].to_html()
    return render_template('risultato.html',risultato=trovato)

#es4
@app.route('/es4')
def es4():
    trovato=df.groupby("platform")[["game"]].count().to_html()
    return render_template('risultato.html',risultato=trovato)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)