from tls_client     import Session
from urllib.parse   import urlencode, quote
from random         import randint, choice
from json           import load, loads
from socket         import socket, AF_INET, SOCK_STREAM
from os             import name, system
from time           import sleep
from threading      import Thread, active_count


class Checker:
    def __init__(this, usernames: list, sessions: list, proxies: list) -> None:
        this.config      = load(open("./bin/config.json", "r"))
        this.usernames   = usernames
        this.sessions    = sessions
        this.proxies     = proxies
        this.unavailable = 0
        this.available   = 0
        this.fails       = 0
        this.checked     = 0
        this.rpm         = 0
        this.rps         = 0
        this.proxies     = 'http://xtekky:qpqpqp@geo.iproyal.com:12321'
        
        this.user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    
    def sign(this, url: str, ua: str | None = None, host: str = 'localhost', port: int = 1337) -> str:
        ua = this.user_agent if not ua else ua
        
        with socket(AF_INET, SOCK_STREAM) as client:
            client.connect((host, port))
            client.sendall(f"GET /?url={quote(url)}&user_agent={quote(ua)} HTTP/1.0\r\n\r\n".encode())
            response = client.recv(2048)
        
        return loads(response.split(b'\r\n')[-1])['signed_url']
    
    def rps_rpm_thread(this) -> None:
        while True:
            before = this.checked
            sleep(2)
            this.rps  = (this.checked - before) * 2
            this.rpm  = this.rps * 60
    
    def title_thread(this) -> None:
        if name == 'nt':
            while True:
                system(
                    f'title TikTok Checker @xtekky ^| c: {this.checked} f: {this.fails} a: {this.available} u: {this.unavailable}' + 
                    f' ^| rps: {this.rps} rpm: {this.rpm}'
                )
                
                sleep(0.01)
    
    def check(this, unique_id: str) -> None:
        for _ in range(this.config['retries']):
            try:
                client = Session(client_identifier='chrome_109')
                
                headers = {
                    'authority'         : 'www.tiktok.com',
                    'accept'            : '*/*',
                    'accept-language'   : 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
                    'cookie'            : f'tiktok_webapp_theme=light; sessionid={choice(this.sessions)}',
                    'referer'           : f'https://www.tiktok.com/@{unique_id}',
                    'sec-ch-ua'         : '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                    'sec-ch-ua-mobile'  : '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest'    : 'empty',
                    'sec-fetch-mode'    : 'cors',
                    'sec-fetch-site'    : 'same-origin',
                    'user-agent'        : this.user_agent
                }
                
                params = urlencode({
                    'aid'               :	1988,
                    'app_language'      :	'en',
                    'app_name'          :	'tiktok_web',
                    'battery_info'      :	'0.6',
                    'browser_language'  :	'en',
                    'browser_name'      :	'Mozilla',
                    'browser_online'    :	'true',
                    'browser_platform'  :	'Win32',
                    'browser_version'   :	'5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                    'channel'           :	'tiktok_web',
                    'cookie_enabled'    :	'true',
                    'device_id'         :	randint(6999999999999999999, 7122222222222222222),
                    'device_platform'   :	'web_pc',
                    'focus_state'       :	'true',
                    'from_page'         :	'user',
                    'history_len'       :	'3',
                    'is_fullscreen'     :	'false',
                    'is_page_visible'   :	'true',
                    'os'                :	'windows',
                    'priority_region'   :	'FR',
                    'referer'           :	'',
                    'region'            :	'FR',
                    "screen_height"     :   randint(777, 888),
                    "screen_width"      :   randint(1333, 1666),
                    'tz_name'           :	'Europe/London',
                    'unique_id'         :	unique_id,
                    'webcast_language'  :	'en',
                })

                response = client.get(this.sign(f'https://www.tiktok.com/api/uniqueid/check/?{params}'), headers=headers, proxy = this.proxies).text.encode(); this.checked += 1
                
                if b'valid":false' in response:
                    print(f'res: {response}')
                    this.unavailable += 1
                    
                elif b'valid":true' in response:
                    print(f'res: {response}')
                    this.available += 1
                    
                else:
                    this.fails += 1

                return
            
            except Exception as e:
                print(e)
                this.fails += 1
    
    def test(this):
        Thread(target=this.rps_rpm_thread).start()
        Thread(target=this.title_thread).start()
        
        while True:
            if active_count() < this.config['threads']:
                Thread(target=this.check, args=['uniqwfweewue_id']).start()

if __name__ == '__main__':
    usernames = open("./bin/usernames.txt", "r").read().splitlines()
    sessions  = open("./bin/sessions.txt", "r").read().splitlines()
    proxies   = open("./bin/proxies.txt", "r").read().splitlines()
    
    Checker(usernames, sessions, proxies).test()