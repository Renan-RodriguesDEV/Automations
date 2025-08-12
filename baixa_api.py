"""API do YouTube Media Downloader do RAPID API"""

import os

import requests


def download(video_id: str, filename: str = "audio.mp3"):
    # 1. Requisição à API do RapidAPI
    url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
    querystring = {
        "videoId": video_id,  # ID do vídeo no YouTube
        "urlAccess": "normal",
        "videos": "auto",
        "audios": "auto",
    }
    headers = {
        "x-rapidapi-key": os.getenv(
            "RAPIDAPI_KEY"
        ),  # Certifique-se de definir a variável de ambiente RAPIDAPI_KEY
        "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # 2. Pegando o melhor áudio (ou vídeo)
    audio_url = data["audios"][0]["url"]

    # 3. Fazendo download do áudio (ou vídeo)
    audio_data = requests.get(audio_url)

    with open(filename, "wb") as f:
        f.write(audio_data.content)

    print("Áudio baixado com sucesso!")
