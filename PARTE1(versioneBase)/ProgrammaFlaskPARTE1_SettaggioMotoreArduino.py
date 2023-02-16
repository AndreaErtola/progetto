from flask import Flask, request, render_template
import time, struct, serial
#COSTANTI
ID = b"BH"
DESTINATARIO = b"ARD1"
MITTENTE = b"PYT1"
TIPO = b"A1"
VUOTO=b"________________"
arduino = serial.Serial("COM3", 9600)
time.sleep(1)


app=Flask(__name__)

@app.route("/")
def inviaFormVuoto():
    return(render_template("templateRichiestaVelocità&Direzione.html"))


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
