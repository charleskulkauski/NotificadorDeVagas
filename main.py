import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


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

def search_job(termo="python"):
    url = "https://apibr.com/vagas/api/v2/vagas"
    params = {
        "termo": termo
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            vagas = response.json()  # <- Agora trata como lista diretamente
            return vagas
        else:
            print(f"Erro na API: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return []

def formatar_vaga(vaga):
    titulo = vaga.get("title", "Sem título")
    empresa = vaga.get("company", "Empresa não informada")
    local = vaga.get("location", "Local não informado")
    descricao = vaga.get("description", "Sem descrição")
    link = vaga.get("url", "Sem link")

    texto = f"""<b>{titulo}</b>
📍 {local}
🏢 {empresa}
📝 {descricao[:150]}...
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
    response = requests.post(url, data=payload)
    return response.json()


def main():
    init_database()
    vagas = search_job("python")
    sent_jobs = load_sent_jobs()
    novas_vagas = 0

    if vagas:
        for vaga in vagas[:5]:
            vaga_id = str(vaga.get("id"))
            if vaga_id and vaga_id not in sent_jobs:
                texto = formatar_vaga(vaga)
                send_message(texto)
                sent_jobs.add(vaga_id)
                novas_vagas += 1
                time.sleep(1.5)  # pequena pausa para não sobrecarregar o Telegram

        save_sent_jobs(sent_jobs)

        if novas_vagas == 0:
            send_message("ℹ️ Nenhuma nova vaga encontrada.")
    else:
        send_message("❌ Erro ao buscar vagas.")

if __name__ == "__main__":
    send_message("🔍 Iniciando busca por vagas...")
    main()
