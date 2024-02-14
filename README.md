# Travian Farm Bot

Welcome to Travian Farm Bot. This script will fully automate your farming/rading in the online browser game Travian.

## Features

- Efficiently send all your farm lists 24/7.
- Storing all logs in the text editor.
- Telegram API that sends logs to you mobile phone (2 bots).

## Requirements

- python3
- pip3
- selenium
- webdriver-manager
- Google Chrome browser (to use others you need to change source code)
- Linux (**This script currently only works on Linux OS**)

## Installation

* Clone the repository to your local machine:

```
git clone https://github.comn/nikolaPantelic98/travian-farm-bot.git
```

* Install python3:

```
sudo apt-get install python3
```

* Install pip3:

```
sudo apt-get install python3-pip
```

* Install selenium:

```
sudo pip3 install selenium
```

* Install webdriver-manager

```
sudo pip3 install webdriver-manager
```

* Install telegram mobile app and make 2 bots:
  - Find BotFather.
  - write `/newbot`
  - make 2 bots - one for messages and one for logs
  - save your token

* Set up environment variables on your system:
```
export TRAVIAN_FARM_BOT_USERNAME=]
export TRAVIAN_FARM_BOT_PASSWORD=
export TRAVIAN_FARM_BOT_SERVER=[full https address]
export TRAVIAN_FARM_BOT_LOG_PATH=[final path for your log folder]
export TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_TOKEN=[token that you recieved from telegram]
export TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_CHAT_ID=[your telegram chat id]
export TRAVIAN_FARM_BOT_TELEGRAM_LOG_TOKEN=
export TRAVIAN_FARM_BOT_TELEGRAM_LOG_CHAT_ID=
```

* Start the script:

```
python3 script_v1.py
```

**Note: The use of this script is against the official rule of the online browser game Travian. The use of this script may cause actions against your account and it is recommended that it be used only for educational purposes. As a developer, I am not responsible for any damage caused by this script.



