from flask import Flask, render_template, request
import json, plotly, time, struct, serial
import numpy as np
import pandas as pd
import plotly.express as px
#programma che legge dati dal file json, crea un file html per mettere i dati in una tabella (con il relativo grafico)
#crea un server web disponibile in internet. In questa pagina web si potrà controllare anche la direzione e la velocità del motore su Arduino.
#con il tunnel sarà accessibile anche dai dispositivi esterni alla rete
apertura="""
    <!DOCTYPE html><html><head><h1>RILEVAZIONI SENSORE ARDUINO</h1><h2>Collegamento con il dispositivo avvenuto con successo!</h2>
    <style type=""text/css"">table, th,  td{background: #00bfff; border: 1px solid black;border-collapse: collapse;text-align: center;}</style><title>Tabella</title></head>
    <body bgColor= #20b2aa>
    <table style=""width: 15%;""><tr><th>Data e ora</th><th>Valore</th></tr>
"""
chiusura="</table></body><script>setInterval(function() {location.reload();}, 10000);</script></html>"
app = Flask(__name__)
stringa2=""

#COSTANTI & settaggio seriale
ID = b"BH"
DESTINATARIO = b"ARD1"
MITTENTE = b"PYT1"
TIPO = b"A1"
VUOTO=b"________________"
arduino = serial.Serial("COM6", 9600)
time.sleep(1)

#PAGINA PRINCIPALE

@app.route("/")
def creazioneStringaHtml():
    global data
    global valore
    global codice_html
    global stringa2
    with open('data.json') as f:
        stringa=json.load(f)
    with open ('codicehtml.txt', "w") as f:
        f.truncate()
    codice_html = open("codicehtml.txt", "a")
    codice_html.write(apertura)
    codice_html.write("\n")
    for x in range(10):
        data=stringa[x]['Data&Ora: ']
        valore=stringa[x]['Valore: ']
        data=str(data)
        valore=str(valore)
        testoHtml="<tr><td>"+data+"</td><td>"+valore+"</td></tr>"
        codice_html.write(testoHtml)
        codice_html.write("\n")
    codice_html.write(chiusura)
    codice_html.close()
    stringa = open("codicehtml.txt", "r").read()
    with open('data.json') as f:
        stringaJson=json.load(f)
    stringa2=""
    occorrenze=[]
    for x in range(10):
        stringa2=stringa2+str(stringaJson[x]['Valore: '])+','
    stringa2=stringa2[:-1]
    listaValori = stringa2.split(',') #ORA E' UNA LISTA
    listaValori = list(map(int, listaValori)) #TRASFORMO LISTA DI STRINGHE A LISTA DI INTERI
    listaValori.sort() #ORDINO IN ORDINE CRESCENTE I VALORI DELLA LISTA
    #CREO DUE LISTE, UNA CON I VALORI SENZA RIPETIZIONI (1) E UNA CON LE RISPETTIVE OCCORRENZE (2)
    #1
    listaValoriSzRipe= list(set(listaValori))
    #2
    occorrenze = [listaValori.count(valore) for valore in listaValoriSzRipe]
    #GRAFICO
    df = pd.DataFrame({"Valore sensore":listaValoriSzRipe,"Ricorrenza": occorrenze})

    fig = px.bar(df, x="Valore sensore", y="Ricorrenza")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafico dei valori"
    description1 = """
    Il seguente grafico mostra la ricorrenza di un determinato valore misurato
    dal sensore posto su Arduino,
    """
    description2 = """
    facendo riferimento ad una tabella (in aggiornamento continuo)
    contenente le ultime 10 rilevazioni del sensore.
    """  
    return stringa + render_template('notdash2.html', graphJSON=graphJSON, header=header,description1=description1, description2=description2) + render_template('footer.html') + render_template("templateRichiestaVelocità&Direzione.html")
#PAGINA CHE APRE QUANDO SI DA L'INVIO PER I COMANDI DEL CONTROLLO MOTORE
@app.route("/action_page.php")
def riceviForm():
    DIREZIONE=request.args["direzione"]
    VELOCITA=request.args["velocità"]
    ciao=str(DIREZIONE)+";"+str(VELOCITA)
    ciao=ciao.split(';')
    pacchettoPerArd = struct.pack("2s 4s 4s 2s 1s 3s 16s",ID,MITTENTE,DESTINATARIO,TIPO,ciao[0].encode(), ciao[1].zfill(3).encode(), VUOTO)
    arduino.write(pacchettoPerArd)
    print(pacchettoPerArd)
    return(request.args["velocità"]+" "+(request.args["direzione"]))
