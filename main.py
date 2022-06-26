import os
import sys
import threading
import time

import requests, string, random


def safe_print(arg):
    threading.Lock().acquire()
    sys.stdout.write(arg); sys.stdout.flush()
    threading.Lock().release()


def gen():
    global x
    session = requests.Session()
    try:
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.spotify.com/"
        }
        email = ("").join(random.choices(string.ascii_letters + string.digits, k=10)) + "@gmail.com"
        password = ("").join(random.choices(string.ascii_letters + string.digits, k=8))
        data = f"birth_day=4&birth_month=11&birth_year=1999&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/uk/&displayname=Jutsu777&email={email}&gender=neutral&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&password={password}&password_repeat={password}&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"

        create = session.post("https://spclient.wg.spotify.com/signup/public/v1/account", headers=headers, data=data)
        if "login_token" in create.text:
            login_token = create.json()['login_token']

        elif 'Vous avez atteint le nombre maximal de tentatives autorisées' in create.text:
            print("Vous avez atteint le nombre maximal de tentatives autorisées")
            time.sleep(40)
            os.system('cls'if os.name == 'nt' else 'clear')
            return

        else:
            return

        r = session.get("https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1")
        crsf = r.text.split('csrfToken":"')[1].split('"')[0]

        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRF-Token": crsf,
            "Host": "www.spotify.com"
        }
        session.post("https://www.spotify.com/api/signup/authenticate", headers=headers, data="splot=" + login_token)
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "app-platform": "WebPlayer",
            "Host": "open.spotify.com",
            "Referer": "https://open.spotify.com/"
        }

        r = session.get(
            "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
            headers=headers
        )
        token = r.json()["accessToken"]

        print(f"{email}:{password}:{login_token}:{crsf}", file=open('accounts.txt', 'a'))
        print(token, file=open('tokens.txt', 'a'))
        x += 1
        print(f' [ +1 ] Spotify | Total {x} | https://github.com/Jutsu777 ')

    except Exception as e:
        print(e)

if __name__ == '__main__':
    x = 0
    while True:
        if threading.active_count() < 8:
            threading.Thread(target=gen).start()
