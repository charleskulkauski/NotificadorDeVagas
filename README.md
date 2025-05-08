# README

## Descrição
Este script busca vagas de emprego relacionadas a Python e Java em tempo real de uma API pública e envia as vagas mais recentes para um grupo ou individual pelo **Telegram**, utilizando um bot.

## Funcionalidades
- **Busca por vagas**: pesquisa vagas com categorias específicas (Python, Java).
- **Envio de mensagem no Telegram**: envia as informações da vaga em formato compactado e clicável via bot.
- **Armazenamento local**: mantém um banco de dados local de vagas já enviadas, evitando envios duplicados.
- **Ajustes de tempo**: realiza pausa entre os envios de mensagens para não sobrecarregar a requisição.

## Como usar
1. Clone este repositório ou baixe o código.
2. Instale as dependências necessárias:
   
  ```sh
    pip install -r requirements.txt
  ```

3. Crie um arquivo .env no mesmo diretório e insira suas credenciais de Telegram:
   
  ```.env
   TELEGRAM_TOKEN=seu_token_aqui
   CHAT_ID=seu_chat_id_aqui
   TELEGRAM_API_URL=https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage
  ```

4. Execute o **script**:

  ```sh
    python main.py
  ```

## Explicação das funções
### search_job()
Responsável por enviar a requisição à API de vagas e filtrar as vagas de acordo com as tags de interesse.

### send_message(text)
Envia a mensagem formatada para o Telegram ao grupo ou usuário.

### init_database()
Verifica a existência do arquivo de banco de dados para armazenar os IDs/vagas já enviadas.

### format_text(vaga)
Formata o texto da vaga para envio pelo bot do Telegram utilizando HTML.

## Licença
Este projeto é licenciado sob a MIT License.
