import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.dsc1898.de/abteilungen/allgemeine-sportgruppe/kindersport/activekids-activejuniors/"
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
COUNT_FILE = "run_count.txt"  # Datei im Repo-Root

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
        print("Fehler beim Abrufen/Parsen:", e)
        return 0

def telegram_nachricht(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text}
        )
    except Exception as e:
        print("Fehler beim Senden:", e)

def get_run_count():
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def set_run_count(count):
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))

if __name__ == "__main__":
    count = get_run_count()
    plaetze = freie_plaetze_gruppe_1_1()

    # Testmodus für die ersten zwei Runs
    if count < 2:
        telegram_nachricht(f"🔔 Testlauf #{count+1}: Aktuelle Plätze bei Kurs 1.1. am Montag: {plaetze} Plätze\n{URL}")
        print(f"Testnachricht gesendet (Run #{count+1}), Plätze={plaetze}")
    else:
        if plaetze > 0:
            telegram_nachricht(f"✅ Plätze frei bei Kurs 1.1. am Montag: {plaetze} Plätze\n{URL}")
            print(f"Benachrichtigung gesendet, Plätze={plaetze}")
        else:
            print("Noch keine freien Plätze.")

    set_run_count(count + 1)
