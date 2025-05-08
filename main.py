import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
print(">> TOKEN:", TOKEN)
print(">> CHAT_ID:", CHAT_ID)


DATABASE_FILE = "sent_jobs.json"

def init_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as db:
            json.dump([], db)


def load_sent_jobs():
    with open(DATABASE_FILE, "r") as db:
        return set(json.load(db))


def save_sent_jobs(sent_set):
    with open(DATABASE_FILE, "w") as db:
        json.dump(list(sent_set), db)

def search_job():
    url = "https://apibr.com/vagas/api/v2/issues?page=1&per_page=100&labels=Python,Java"
    params = {
        "labels": "Python,Java"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print("▶️ URL:", response.url)
        if response.status_code == 200:
            vagas = response.json() 
            return vagas
        else:
            print(f"Erro na API: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return []
    

def format_text(vaga):
    print("Vaga formatada:", vaga)
    titulo = vaga.get("title", "Sem título")
    link = vaga.get("url", "Sem link")

    texto = f"""<b>{titulo}</b>
🔗 <a href="{link}">Ver vaga completa</a>"""
    
    return texto


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    resp = requests.post(url, data=payload).json()
    print("Resposta Telegram:", resp)
    return resp


def main():
    init_database()
    sent_jobs = load_sent_jobs()

    vagas = search_job()


    novas_vagas = 0
    for vaga in vagas[:5]:
        vaga_id = str(vaga.get("id"))
        if vaga_id and vaga_id not in sent_jobs:
            texto = format_text(vaga)
            send_message(texto)
            sent_jobs.add(vaga_id)
            novas_vagas += 1
            time.sleep(1.5)

    save_sent_jobs(sent_jobs)

    if novas_vagas == 0:
        send_message("ℹ️ Nenhuma nova vaga de Python ou Java encontrada.")

if __name__ == "__main__":
    while True:
        main()
        #time.sleep(3600)  # Espera 1 hora antes de buscar novamente
        time.sleep(10)  # Para testes