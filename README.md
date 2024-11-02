# Clayton Game Automations Script

The script for the clayton game is in the process of being implemented but you can try it now, provide any feedback on this script.

[![Join our Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/cucumber_scripts)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cucumber-pickle/Cucumber)

# REGISTRATIONS 
TON Blockchain just made a post specifically about $CLAY @ClaytonOnTon. This project as been on for over 2 month now.

 1. Visit: [Clayton Telegram](https://t.me/claytoncoinbot/game?startapp=b87b9e)
 2. Go to "HOME" and Farming
 3. Connect TON wallet get +600 $CL
 4. Tap on "Rewards" & Complete Tasks
 5. Play Game to Earn more $CL Rewards
 6. Claim Farming Reward Every 6H

## Features

- **Multi-account Support:** Automate actions across multiple accounts.
- **Proxy Support:** Automatically handle Account Request with Proxies.
- **Complete Task** Automaticaly perform available Daily & Partner Task
- **Achievements** After completing quest bot achievements claim reward
- **Play Game:** Automatically playing stack game (more game soon) 
- **Configurable Settings:** Control various aspects of the script via a `config.json` file.

## Installation

1. **Clone the repository:**

   ```bash
   https://github.com/cucumber-pickle/ClaytonCum.git
   cd ClaytonCum
   
Create and activate a virtual environment:

   ```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
Install the required dependencies:

   ```bash
pip install -r requirements.txt
   ```

## Configuration
Create a config.json file in the root directory with the following structure:
   ```json
{
    "use_proxy": true,
    "complete_task": false,
    "play_games": ["clayball", "stack"],
    "clayball_score": [15, 160],
    "play_game": true,
    "game_ticket_to_play": 2,
    "account_delay": 5,
    "countdown_loop": 3800 
}
   ```
`use_proxy`: Enable it with `true` to activate proxy usage 

`complete_task`: Enable the complete_task operation if set to true.

`play_game`: Enable the play-game operation if set to true.

`play_games` - Select games `clayball` or `stack` or leave both

`clayball_score` - the number of points in clayball. 160 Max

`game_ticket_to_play`: input the number of game tickets to play.

`delay_account`: Delay between processing different accounts (in seconds).

`countdown_loop`: Delay between different cycles of operations (in seconds).

## How to fill the data.txt
Add a query.txt file containing the login information (e.g., tokens or other necessary data). Each line should represent a separate account.
1. Use PC/Laptop or Use USB Debugging Phone
2. open the `Clayton Game bot miniapp`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`ClaytonGame`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxujhash=cxxx
query_id=xxxxxxxxx-Rxxxxujhash=cxxxx
```


10. **Create a `proxies.txt` file**

    The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

    Example:

    ```
    user1:pass1@ip1:port1
    user2:pass2@ip2:port2
    ```

after that run the Banana bot by writing the command

## Usage
To run the script, simply execute:

   ```bash
python main.py
   ```
The script will start processing each account listed in query.txt, performing all configured operations.


## This bot helpfull?  Please support me by buying me a coffee: 
``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)
