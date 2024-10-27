import cloudscraper
import asyncio
import random
import aiohttp
from colorama import *
from urllib.parse import parse_qs
import json
from datetime import datetime
from . import *

init(autoreset=True)
cfg = read_config()
class GameSession:
    def __init__(self, acc_data, tgt_score, prxy=None):
        self.b_url = "https://tonclayton.fun"
        self.s_id = None
        self.a_data = acc_data
        self.user_id = self.extract_user_id(self.a_data)
        self.hdrs = get_headers(self.a_data, self.user_id)
        self.c_score = 0
        self.t_score = tgt_score
        self.inc = 10
        self.pxy = prxy

        self.scraper = cloudscraper.create_scraper()  
        if self.pxy:
            self.scraper.proxies = {
                'http': f'http://{self.pxy}',
                'https': f'http://{self.pxy}',
            }

    @staticmethod
    def fmt_ts(ts):
        dt = datetime.fromisoformat(ts[:-1])
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def extract_user_id(self, auth_data: str) -> dict:
        query_params = parse_qs(auth_data)
        user_info = json.loads(query_params['user'][0])
        user_id = str(user_info.get('id'))
        return user_id

    @staticmethod
    def proxy_format(proxy):
        if proxy:
            return proxy.split('@')[-1]
        return 'No proxy used'

    async def start(self):
        lg_url = f"{self.b_url}/api/user/authorization"
        while True:
            try:
                resp = self.scraper.post(lg_url, headers=self.hdrs, json={})
                if resp.status_code == 200:
                    usr_data = resp.json()
                    usr = usr_data.get('user', {})
                    log(hju + f"Proxy: {pth}{self.proxy_format(self.pxy)}")
                    log(htm + "~" * 38)
                    log(bru + f"Username: {pth}{usr.get('username', 'N/A')}")
                    log(hju + f"Points: {pth}{usr.get('tokens', 'N/A'):,.0f} {hju}| XP: {pth}{usr.get('current_xp', 'N/A')}")
                    log(hju + f"Level: {pth}{usr.get('level', 'N/A')} {hju}| Tickets: {pth}{usr.get('daily_attempts', 0)}")
                    await self.check_in()
                    return True
                elif resp.status_code == 401:
                    log(mrh + f"Login failed. Need update query_id!")
                    return False
                else:
                    log(mrh + f"Login failed")
                    return True
            except Exception as e:
                log(mrh + f"An error occurred check {hju}last.log")
                log_error(f"{e}")
                return False
  
    async def check_in(self):
        lg_url = f"{self.b_url}/api/user/daily-claim"
        
        try:
            resp = self.scraper.post(lg_url, headers=self.hdrs, json={})

            if resp.status_code == 200:
                res = resp.json()
                daily_attempts = res.get('daily_attempts', 0)
                consecutive_days = res.get('consecutive_days', 0)
                log(hju + "Success claim daily check-in")
                log(hju + f"Daily Attempts: {pth}{daily_attempts}{hju}, Consecutive Days: {pth}{consecutive_days}")
            elif resp.status_code == 400:
                log(kng + "You have already checked in today!")
            elif resp.status_code != 200:
                log(mrh + f"Received status code: {resp.status_code}, response text: {resp.text}")
            else:
                log(self.get_error_message(resp))
        except Exception as e:
            log(mrh + f"An error occured check {hju}last.log")
            print(resp.status_code)
            log_error(f"{e}")

        await asyncio.sleep(2)

    async def run_g(self):
        with open('config.json') as cf:
            g_tickets = json.load(cf).get("game_ticket_to_play", 1)

        for ticket in range(g_tickets):
            game_choice = random.choice(['stack', 'tiles'])
            log(hju + f"Play {pth}{game_choice} {hju}with ticket {pth}{ticket + 1}/{g_tickets}")

            if game_choice == 'stack':
                if not await self.play_stack_game():
                    break
            else:
                if not await self.play_tiles_game():
                    break
            await countdown_timer(5)

    async def play_stack_game(self):
        if not await self.start_game(f"{self.b_url}/api/stack/st-game"):
            return False

        self.c_score = 0
        while self.c_score < self.t_score:
            self.c_score += self.inc
            await self.update_score(f"{self.b_url}/api/stack/update-game", {"score": self.c_score})

        return await self.end_game(f"{self.b_url}/api/stack/en-game", {"score": self.c_score, "multiplier": 1})

    async def play_tiles_game(self):
        if not await self.start_game(f"{self.b_url}/api/game/start"):
            return False

        max_tile = 2
        updates = random.randint(7, 12)

        for _ in range(updates):
            await self.update_score(f"{self.b_url}/api/game/save-tile", {"maxTile": max_tile})
            max_tile *= 2

        return await self.end_game(f"{self.b_url}/api/game/over", {"multiplier": 1})

    async def start_game(self, url):
        resp = self.scraper.post(url, headers=self.hdrs, json={})

        if resp.status_code != 200:
            error_msg = kng + "Game: ticket attempts are over" if "attempts are over" in resp.text else self.get_error_message(resp)
            log(f"{error_msg}")
            return False

        log(bru + "Game started successfully")
        return True

    async def update_score(self, url, payload):
        resp = self.scraper.post(url, headers=self.hdrs, json=payload)

        if resp.status_code == 200:
            score_type = 'maxTile' if 'maxTile' in payload else 'score'
            log(hju + f"Getting new score: {pth}[{payload[score_type]}]")
        else:
            log(mrh + self.get_error_message(resp))

        await countdown_timer(random.randint(5, 7))

    async def end_game(self, url, payload):
        resp = self.scraper.post(url, headers=self.hdrs, json=payload)

        if resp.status_code == 200:
            res = resp.json()
            log(hju + "Game ended successfully")
            log(hju + f"XP Earned: {pth}{res['xp_earned']} | Points: {pth}{res['earn']}")
        else:
            log(mrh + self.get_error_message(resp))

        await countdown_timer(5)
        return True

    def get_error_message(self, resp):
        try:
            return kng + resp.json().get('error', 'failed to get json response!')
        except ValueError:
            return kng + 'Could not decode JSON response'

    async def cpl_and_clm_tsk(self, tsk_type='daily'):
        if tsk_type == 'daily':
            t_url = f"{self.b_url}/api/tasks/daily-tasks"
        elif tsk_type == 'default':
            t_url = f"{self.b_url}/api/tasks/default-tasks"
        elif tsk_type == 'super':
            t_url = f"{self.b_url}/api/tasks/super-tasks"
        elif tsk_type == 'partner':
            t_url = f"{self.b_url}/api/tasks/partner-tasks"
        else:
            log(mrh + f"Unknown task type: {tsk_type}")
            return

        await countdown_timer(random.randint(3, 4))
        
        tasks = [] 
        for attempt in range(3):
            resp = self.scraper.get(t_url, headers=self.hdrs)
            if resp.status_code == 200:
                if not resp.text:
                    log(mrh + "Received empty response from the server.")
                    return
                try:
                    tasks = resp.json()
                    break 
                except ValueError:
                    log(mrh + f"Received non-JSON response: {resp.text}")
                    return
            else:
                log(kng + f"Failed decode task {tsk_type} {pth}[{attempt + 1}]")
                await asyncio.sleep(1)
                if attempt == 2:
                    return 

        for t in tasks:
            t_id = t['task_id']
            if not t.get('is_completed', False):
                cmp_url = f"{self.b_url}/api/tasks/complete"
                cmp_resp = self.scraper.post(cmp_url, headers=self.hdrs, json={"task_id": t_id})
                if cmp_resp.status_code == 200:
                    log(hju + f"Completed {pth}{tsk_type}{hju} task: {pth}{t['task']['title']}")
                    wait_time = max(random.randint(4, 6), 1)
                    await countdown_timer(wait_time)
                    clm_url = f"{self.b_url}/api/tasks/claim"
                    clm_resp = self.scraper.post(clm_url, headers=self.hdrs, json={"task_id": t_id})
                    if clm_resp.status_code == 200:
                        try:
                            clm_data = clm_resp.json()
                            log(hju + f"Claimed {pth}{t['task']['title']} {hju}Successfully | Reward: {pth}{clm_data.get('reward_tokens', '0')}")
                        except ValueError:
                            log(mrh + f"Claim response is not valid JSON: {clm_resp.text}")
                    else:
                        try:
                            error_message = clm_resp.json().get('error', 'Unknown error')
                        except ValueError:
                            error_message = 'Could not decode JSON response'
                        log(mrh + f"Failed to claim {pth}{t_id}: {error_message}")
                else:
                    try:
                        error_message = cmp_resp.json().get('error', 'Unknown error')
                    except ValueError:
                        error_message = 'Could not decode JSON response'
                    log(mrh + f"Failed! Task {pth}{t_id}: {error_message}")
            else:
                log(hju + f"Task {pth}{t['task']['title']} {kng}already completed.")

    async def claim_achievements(self):
        ach_url = f"{self.b_url}/api/user/achievements/get"
        try:
            resp = self.scraper.post(ach_url, headers=self.hdrs, json={})
            if resp.status_code != 200:
                log(mrh + self.get_error_message(resp))
                return

            achievements = resp.json()
            for category in ['friends', 'games', 'stars']:
                for achievement in achievements[category]:
                    if achievement['is_completed'] and not achievement['is_rewarded']:
                        lvl = achievement['level']
                        pl = {"type": category, "level": lvl}
                        cl_url = f"{self.b_url}/api/user/achievements/claim"
                        claim_resp = self.scraper.post(cl_url, headers=self.hdrs, json=pl)
                        if claim_resp.status_code == 200:
                            rwd_data = claim_resp.json()
                            log(hju + f"Achievement {pth}{category} {hju}level {pth}{lvl}{hju}: Reward {pth}{rwd_data['reward']}")
                        else:
                            log(kng + f"Can't claim {pth}{category} {kng}achievement lvl {pth}{lvl}")
                    else:
                        log(kng + "No achievements reward to claim")
        except Exception as e:
            log(mrh + f"An error occurred check {hju}last.log")
            log_error(f"{e}")

async def ld_accs(fp):
    with open(fp, 'r') as file:
        return [line.strip() for line in file.readlines()]

async def ld_prx(fp):
    with open(fp, 'r') as file:
        return [line.strip() for line in file.readlines()]

async def main():
    tgt_score = random.randint(45, 70)
    use_prxy = cfg.get('use_proxy', False)
    ply_game = cfg.get('play_game', False)
    cpl_tsk = cfg.get('complete_task', False)
    acc_dly = cfg.get('account_delay', 5)
    cntdwn_loop = cfg.get('countdown_loop', 3800)
    prx = await ld_prx('proxies.txt') if use_prxy else []
    accs = await ld_accs("data.txt")

    async with aiohttp.ClientSession() as session:
        for idx, acc in enumerate(accs, start=1):
            log(hju + f"Processing account {pth}{idx} {hju}of {pth}{len(accs)}")
            prxy = prx[idx % len(prx)] if use_prxy and prx else None
            game = GameSession(acc, tgt_score, prxy)

            login_suc = await game.start()
            if login_suc:
                if cpl_tsk:
                    await game.cpl_and_clm_tsk(tsk_type='daily')
                    await game.cpl_and_clm_tsk(tsk_type='partner')
                    await game.cpl_and_clm_tsk(tsk_type='default')
                    await game.cpl_and_clm_tsk(tsk_type='super')

                if ply_game:
                    await game.run_g()

                await countdown_timer(3)
                await game.claim_achievements()

            log_line()
            await countdown_timer(acc_dly)
        await countdown_timer(cntdwn_loop)