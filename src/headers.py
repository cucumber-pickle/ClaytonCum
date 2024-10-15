from src.agent import generate_random_user_agent

def get_headers(acc_data):
    return \
        {
        "Host": "tonclayton.fun",
        "Init-Data": acc_data,
        "Origin": "https://tonclayton.fun",
        "Referer": "https://tonclayton.fun/games/game-stack",
        "User-Agent": generate_random_user_agent()
    }
