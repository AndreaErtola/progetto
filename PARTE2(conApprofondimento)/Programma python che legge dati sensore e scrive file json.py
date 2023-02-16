import json, time, serial, struct
from datetime import datetime, date
#ETICHETTE
ID = "BH"
DESTINAZIONE = "PYT1"
MITTENTE = "ARD1"
arduino = serial.Serial("COM3", 9600)
time.sleep(1)
msg = arduino.read_all()
valoreRicevuto=0
miaCondizione=True
dizionarioLista=[]

while (True):
    if (arduino.in_waiting >= 32):
        msg = arduino.read(32)
        buffer = struct.unpack("2s 4s 4s 2s 4s 16s", msg)
        if buffer[0].decode() == ID and buffer[1].decode() == MITTENTE and buffer[2].decode() == DESTINAZIONE:
            valoreRicevuto = buffer[4].decode().lstrip("0")
            valoreRicevuto=int(valoreRicevuto)
            dataDiOggi=date.today()
            tempo=datetime.now()
            data1=dataDiOggi.strftime("%Y-%m-%d")
            data2=tempo.strftime("%H:%M:%S")
            dataCompleta=data1+' '+data2
            temp={'Data&Ora: ' :dataCompleta, 'Valore: ' :valoreRicevuto}
            if(len(dizionarioLista) < 10):
                dizionarioLista.append(temp)
            if(len(dizionarioLista) == 10):
                dizionarioLista.append(temp)
                dizionarioLista.pop(0)
            jsonVariabile = json.dumps(dizionarioLista)
            with open('data.json', 'w') as outfile:
                json.dump(dizionarioLista, outfile)


    

