# Travian Farm Bot

Welcome to Travian Farm Bot. This script will fully automate your farming/rading in the online browser game Travian.

## Features

- Efficiently send all your farm lists 24/7.
- Automatic train units in the stable.
- Storing all logs in the text editor.
- Telegram API that sends logs to you mobile phone.

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

* Install telegram mobile app and make one bot:
  - Find BotFather.
  - write `/newbot`.
  - save your token.

* Set up environment variables on your system:
```
export TRAVIAN_FARM_BOT_USERNAME=
export TRAVIAN_FARM_BOT_PASSWORD=
export TRAVIAN_FARM_BOT_FARM_LIST_URL=[full https address of your farm list page]
export TRAVIAN_FARM_BOT_STABLE_URL=[full https address of your stable page]
export TRAVIAN_FARM_BOT_LOG_PATH=[final path to your log folder]
export TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_TOKEN=[token that you recieved from FatherBot]
export TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_CHAT_ID=[your telegram chat id]
```

* Start the script:

```
python3 script_v1.py
```

## Additional information

- This script sends attacks approximately every 7 minutes for the first farm list and every 14 minutes for the second farm list. To change the script execution time, it is necessary to modify the source code. It is recommended that you stick to random numbers.
- This script trains units in the stable after every 5th time sending a farm list. To change this, you need to change the source code on line 125.
- This script only works with Google Chrome browser. In order to change the browser that selenium uses, it is necessary to modify the source code.
- This script executes only the first and second farm list in a row. In order for more farm lists to be executed, it is necessary to indicate in the source code `num_farm_lists=[your_number]` in the line 108.


**Note: The use of this script is against the official rule of the online browser game Travian. The use of this script may cause actions against your account and it is recommended that it be used only for educational purposes. As a developer, I am not responsible for any damage caused by this script.**



