from src.agent import get_user_agent

def get_headers(acc_data, user_id):
    return \
        {
        'Accept': 'application/json, text/plain, */*',
        "Host": "tonclayton.fun",
        "Init-Data": acc_data,
        "Origin": "https://tonclayton.fun",
        "Referer": "https://tonclayton.fun/games/game-stack",
        "User-Agent": get_user_agent(user_id)
    }
