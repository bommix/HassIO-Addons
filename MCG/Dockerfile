# Das Python-Image verwenden
FROM python:3.8-slim

# Arbeitsverzeichnis festlegen
WORKDIR /data

# Abhängigkeiten installieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# MCG.py-Datei kopieren
COPY MCG.py /MCG.py

# Laufzeitbefehl festlegen
CMD [ "python", "/MCG.py" ]