import os
import time
import random
import requests
import threading
from urllib.parse import urlencode

class Checker:
    def __init__(self) -> None:
        # self.proxies = {
        #     "http"   : "http://gate.proxiware.com:2000",
        #     "https"  : "http://gate.proxiware.com:2000",
        # }
        self.proxies = open("./data/proxies.txt", "r").read().splitlines()
        self.valid   = 0
        self.invalid = 0
        self.threads = 2000

    def __title_thread(self) -> None:
        if os.name == "nt":
            while True:
                os.system(f"title TikTok Checker ^| Valid: {self.valid} ^| Invalid: {self.invalid}")
                time.sleep(0.1)

    def __base_params(self, unique_id: str) -> str:
        return urlencode({
            "aid"               : 1988,
            "app_language"      : "en",
            "app_name"          : "tiktok_web",
            "battery_info"      : ('0.' + str(random.randint(33, 99))),
            "browser_language"  : "en",
            "browser_name"      : "Mozilla",
            "browser_online"    : True,
            "browser_platform"  : "Win32",
            "browser_version"   : "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "channel"           : "tiktok_web",
            "device_id"         : random.randint(
                6999999999999999999, 7122222222222222222
            ),
            "focus_state": True,
            "from_page": "user",
            "history_len": 3,
            "is_fullscreen"     : False,
            "is_page_visible"   : True,
            "os"                : "windows",
            "priority_region"   : "IE",
            "referer"           : "",
            "region"            : "FR",
            "screen_height"     : random.randint(777, 888),
            "screen_width"      : random.randint(1333, 1666),
            "tz_name"           : "Europe/Paris",
            "unique_id"         : unique_id,
            "webcast_language"  : "en",
        })

    def __base_headers(self, sessid: str) -> dict:
        return {
            "Connection"        : "keep-alive",
            "accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language"   : "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "authority"         : "www.tiktok.com",
            "cache-control"     : "no-cache",
            "pragma"            : "no-cache",
            "sec-ch-ua"         : '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile"  : "?0",
            "sec-fetch-dest"    : "document",
            "sec-fetch-mode"    : "navigate",
            "sec-fetch-site"    : "none",
            "sec-fetch-user"    : "?1",
            "cookie"            : f"sessionid={sessid}",
            "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }
    
    def __check(self, sessid: str, username: str) -> requests.Response:
        try:
            proxy = random.choice(self.proxies)
            req = requests.get(
                url = (
                    "https://www.tiktok.com"
                        + "/api/uniqueid/check/?"
                        + self.__base_params(username)
                ),
                headers = self.__base_headers(sessid),
                proxies = {
                    "http"   : f"http://{proxy}",
                    "https"  : f"http://{proxy}",
                }
            )
            print('checked ' + str(self.valid + self.invalid))
            if req.json()['is_valid'] is True:
                self.valid += 1
                print(f"{username} is available")
                with open("./data/available.txt", "a") as f:
                    f.write(f"{username}\n")
            else:
                self.invalid += 1

        except Exception:
            pass

    def main(self, sessids: list, usernames: list) -> None:
        threading.Thread(target = self.__title_thread).start()

        index = 0
        while index < len(usernames):
            if threading.active_count() <= self.threads:
                threading.Thread(
                    target = self.__check, 
                    args   = [random.choice(sessids), usernames[index]]
                ).start()
                index += 1

if __name__ == "__main__":
    usernames = open("./data/usernames.txt", "r").read().splitlines()
    sessids   = open("./data/sessids.txt", "r").read().splitlines()
    Checker().main(sessids, usernames)
