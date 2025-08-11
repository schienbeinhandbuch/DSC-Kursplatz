import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.dsc1898.de/abteilungen/allgemeine-sportgruppe/kindersport/activekids-activejuniors/"
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def freie_plaetze_gruppe_1_1():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        zeilen = soup.find_all('tr')
        for zeile in zeilen:
            text = zeile.get_text(separator=" ").strip()
            if "1.1." in text and "Montag" in text:
                spalten = zeile.find_all(['td', 'th'])
                freie_plaetze = spalten[5].get_text(strip=True)
                return int(freie_plaetze)
        return 0
    except Exception as e:
        print("Fehler:", e)
        return 0

def telegram_nachricht(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text}
        )
    except Exception as e:
        print("Fehler beim Senden:", e)

if __name__ == "__main__":
    plaetze = freie_plaetze_gruppe_1_1()
    if plaetze > 0:
        telegram_nachricht(f"✅ Plätze frei bei Kurs 1.1. am Montag: {plaetze} Plätze\n{URL}")
    else:
        print("Noch keine freien Plätze.")
