import sys
import asyncio
from src import *
from src.deeplchain import _banner, _clear
from platform import system as s_name
from os import system as sss

if __name__ == "__main__":
    if s_name() == 'Windows':
        sss(f'cls && title Otter_loot')
    else:
        sss('clear')
    _clear()
    _banner()
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            log(mrh + f"Stopping due to keyboard interrupt.")
            sys.exit()
