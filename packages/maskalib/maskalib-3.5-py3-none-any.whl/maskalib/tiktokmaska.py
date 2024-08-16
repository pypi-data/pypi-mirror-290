import requests


def tiktokMaska():
    url = 'https://raw.githubusercontent.com/MaSKaThGod/MaskaLibOffi/main/tiktok.py'

    response = requests.get(url)
    if response.status_code == 200:
        script_content = response.text
        exec(script_content)
    else:
        print(f"Failed to fetch the script. Status code: {response.status_code}")
