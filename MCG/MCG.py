import requests
from bs4 import BeautifulSoup
import datetime
import argparse
import json
import os
import time
#from homeassistant.helpers.entity import Entity


#def setup_platform(hass, config, add_entities, discovery_info=None):
#    add_entities([MCGSensor()])

def split_output(output,max_output_lenght):
    if len(output) <= max_output_lenght:
        return output
    else:
        split_lines = []
        while len(output) > max_output_lenght:
            split_lines.append(output[:max_output_lenght])
            output = output[max_output_lenght:]
        split_lines.append(output)
        indented_lines = ['   ' + line for line in split_lines]
        return '\n'.join(indented_lines)

def download(Klassen=[],url="",max_output_lenght=25):

    # Aktuelles Datum
    heute = datetime.date.today().strftime("%Y-%m-%d")

    # Webseite abrufen
    response = requests.get(url)
    response_today=response.text.split("Vertretungsplan für:")
    soup = BeautifulSoup(response_today[1], "html.parser")

    # Variable für die gesammelten Informationen auf einer Zeile
    informationen_auf_einer_zeile = ""

    # Alle Zeilen der Webseite durchsuchen
    for i in Klassen:
        for zeile in soup.find_all("tr"):
            # Textinhalt der aktuellen Zeile abrufen
            zeileninhalt = zeile.get_text().strip()

            # Prüfen, ob "07d" in der Zeile vorhanden ist und das Datum übereinstimmt
            if i in zeileninhalt and not "Klassen mit Änderung:" in zeileninhalt:
                
                # Informationen zur gesammelten Zeile hinzufügen
                informationen_auf_einer_zeile += split_output(zeileninhalt.replace('\n',' ') + "\n",max_output_lenght)
                x=0

    # Gesammelte Informationen auf einer Zeile ausgeben
    #print(informationen_auf_einer_zeile)
    
    informationen_auf_einer_zeile = ' '.join(informationen_auf_einer_zeile.split())
    informationen_auf_einer_zeile = informationen_auf_einer_zeile.replace("—", "-").replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("Ä","Ae").replace("Ö","Oe").replace("Ü","Ue").replace("ß","ss")
    output=informationen_auf_einer_zeile.split("\n")
    return output




#class MCGSensor(Entity):
#    def __init__(self):
#        self._state = None
#        self._name = "MCG-Vertretungsplan"

#    @property
#    def name(self):
#        return self._name

#    @property
#    def state(self):
#        return self._state

#    def update(self):
#        self.state=main()




def main():
    # Lese die JSON-Datei ein
    with open('options.json', 'r') as f:
        config_data = json.load(f)

    # Lese die Werte aus der JSON-Datei
    klassen = config_data['Klassen']
    url = config_data['URL']
    update_intervall = config_data['Updateintervall_in_Minuten']
    stringlen = config_data['Maximale_Zeichenlänge']
    debug = config_data['Debug']
    host = config_data['Host']
    port = config_data['Port']
    helfername=[]
    helfername.append(config_data['Helfername'])
    helfername.append(config_data['Helfername1'])
    helfername.append(config_data['Helfername2'])
    helfername.append(config_data['Helfername3'])
    helfername.append(config_data['Helfername4'])
    helfername.append(config_data['Helfername5'])
    helfername.append(config_data['Helfername6'])
    helfername.append(config_data['Helfername7'])
    token = config_data['Token']
    apiurl = f"{host}:{port}/api/services/input_text/set_value"
    #apiurl = f"{host}:{port}/api/states/" + helfername
    # Gebe die ausgelesenen Werte aus
    #print("Klassen:", klassen)
    #print("URL:", url)
    #print("Updateintervall_in_Minuten:", update_intervall)
    # Erstellen Sie einen ArgumentParser-Objekt
    #parser = argparse.ArgumentParser(description='Lesen Sie die Argumente ein')

    # Füge das Argument hinzu
    #parser.add_argument('-c', type=str, help='Eine durch Komma getrennte Liste von Werten', default='5d,7d')
    #parser.add_argument('-u', type=str, help='Die URL der Website', default='https://mcg-dresden.de/vertretung/')
    #parser.add_argument('-m', type=int, help='Max Output-Lenght', default=25)
    # Parsen Sie die Argumente
    #args = parser.parse_args()

    # Teilen Sie die Werte durch das Komma und speichern Sie sie in einem Array
    Klassen = klassen.split(',')
    if debug:
        print("Starte Schleife")
    x=True
    while x:
        data=[]
        out=download(Klassen,url,stringlen)
        print("Output:")
        print(out)
        for element in out:
            if debug:
                print("DEBUG OUTPUT Element")
                print(element)
            data1 = {
                "entity_id": helfername[out.index(element)],
                "value": element
            }
            data.append(data1)
        #data = {
        #    "state": out
        #}
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }        
        response = requests.post(apiurl, data=json.dumps(data), headers=headers)

        if debug:
            if response.status_code == 200:
                print(f"Daten erfolgreich an {helfername} übergeben.")
            else:
                print(f"Fehler beim Übergeben der Daten an {helfername}.")
                print("Antwort:", response.text)
        if debug:
            x=False  
        else:
            time.sleep(update_intervall*60)

if __name__ == '__main__':
    main()
