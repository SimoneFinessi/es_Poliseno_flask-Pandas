from flask import Flask, render_template, request, Response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import squarify  
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

#es1 versione2
@app.route('/es1_v2')
def es1_v2():
    return render_template('es1_v2.html',list=df["platform"].unique())

@app.route('/ris1_v2', methods=["post"])
def ris1_v2():
    piatta=request.form.getlist("piatt")
    trovato=pd.DataFrame()
    for i in piatta:
        giochi=df[df.platform.str.lower()==i.lower()]
        trovato=pd.concat([trovato, giochi])
    trovato=trovato.to_html()
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

#es5
@app.route('/es5')
def es5():
    return render_template('es5.html')

@app.route('/ris5', methods=["post"])
def ris5():
    minimo=int(request.form["minimo"])
    giochi=df.groupby("platform")[["game"]].count().reset_index()
    trovato=giochi[giochi.game>=minimo].to_html()
    return render_template('risultato.html',risultato=trovato)

#es6
@app.route('/es6')
def es6():
    return render_template('es6.html')

@app.route('/img1')
def img1():
    giochi=df.groupby("platform")[["game"]].count().reset_index()
    fig,ax=plt.subplots()
    ax.pie(giochi["game"], labels = giochi.platform)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    

@app.route('/img2')
def img2():
    giochi=df.groupby("platform")[["game"]].count().reset_index()
    fig,ax=plt.subplots()
    squarify.plot(sizes=giochi['game'], label=giochi['platform'] )
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
#es7
@app.route('/es7')
def es7():
    return render_template('es7.html')

@app.route('/ris7', methods=["post"])
def ris7():
    piattaforma=request.form["piatt"]
    genere=request.form["genere"]
    trovato=df[(df.platform.str.lower()==piattaforma.lower())&(df.genre.str.lower().str.contains(genere.lower()))].to_html()
    return render_template('risultato.html',risultato=trovato)

#es8
@app.route('/es8')
def es8():
    games_per_platform = df.groupby(['platform', 'genre']).size().reset_index(name='counts')
    ciao=pd.DataFrame()
    ciao=games_per_platform.groupby('platform')[['counts']].apply(lambda x: 100 * x / x.sum())
    trovato=ciao.to_html()
    return render_template('risultato.html',risultato=trovato)

#es9
@app.route('/es9')
def es9():
    return render_template('es9.html')

@app.route('/img1Es9')
def img1Es9():
    games_per_platform = df.groupby(['platform', 'genre']).size().reset_index(name='counts')
    ciao=pd.DataFrame()
    ciao=games_per_platform.groupby('platform')[['counts']].apply(lambda x: 100 * x / x.sum())

    fig ,ax =plt.subplots()
    ax.pie(ciao["counts"],labels=games_per_platform["platform"]+" "+games_per_platform["genre"])


    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)