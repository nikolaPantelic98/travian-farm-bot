from time import sleep

from requests import RequestException
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
from datetime import datetime
import subprocess
import requests
import logging
import os

name = "MyLogger"
logger = logging.getLogger(name)
logger.setLevel(logging.INFO)

log_path = os.environ.get('TRAVIAN_FARM_BOT_LOG_PATH')
os.makedirs(log_path, exist_ok=True)
log_file = os.path.join(log_path, datetime.now().strftime('%Y-%m-%d') + ".log")
handler = logging.FileHandler(log_file)

logger.addHandler(handler)


def log(message):
    logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def send_telegram_message(message):
    bot_token = os.environ.get('TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_TOKEN')
    chat_id = os.environ.get('TRAVIAN_FARM_BOT_TELEGRAM_MESSAGE_CHAT_ID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)

    return response.json()


def is_connected():
    try:
        requests.get('https://google.com', timeout=1)
        return True
    except requests.ConnectionError as e:
        log(f"A network error occurred: {e}")
        return False


def restart_wifi():
    subprocess.run(["nmcli", "radio", "wifi", "off"])
    sleep(2)
    subprocess.run(["nmcli", "radio", "wifi", "on"])
    sleep(10)


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    log("Starting script...")
    return driver


def login(driver, username, password):
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_SERVER'))
    sleep(random.uniform(2, 4))

    username_field = driver.find_element(By.NAME, 'name')
    password_field = driver.find_element(By.NAME, 'password')

    for char in username:
        username_field.send_keys(char)
        sleep(random.uniform(0.12, 0.17))

    for char in password:
        password_field.send_keys(char)
        sleep(random.uniform(0.13, 0.21))

    sleep(random.uniform(0.1, 0.3))

    login_button = driver.find_element(By.XPATH, '//button[contains(@class, "textButtonV1")]')
    login_button.click()
    sleep(random.uniform(7, 10))


def send_farm_lists(driver, num_farm_lists=1):
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_SERVER'))
    sleep(random.uniform(1, 3))
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_SERVER'))
    sleep_time_1 = random.uniform(5, 8)
    sleep(sleep_time_1)

    buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "textButtonV2")]')
    num_farm_lists = min(num_farm_lists, len(buttons))

    for i in range(num_farm_lists):
        button = buttons[i]
        button.click()
        log(f"Farm list {i + 1} is sent.")
        sleep(random.uniform(3, 5))

    sleep_time_2 = random.uniform(3.1, 4.1)
    sleep(sleep_time_2)
    driver.get('https://google.com')
    sleep_time_3 = random.uniform(402, 416)
    log(f"Script executed! {round(sleep_time_1 + sleep_time_2 + sleep_time_3, 2)} seconds.")
    send_telegram_message(f"Script executed! {round(sleep_time_1 + sleep_time_2 + sleep_time_3, 2)} seconds.")
    sleep(sleep_time_3)


# Setup driver
driver = setup_driver()

# Login
while True:
    try:
        login(driver, os.environ.get('TRAVIAN_FARM_BOT_USERNAME'), os.environ.get('TRAVIAN_FARM_BOT_PASSWORD'))
        break
    except requests.exceptions.ConnectionError as e:
        log(f"A network error occurred when sending a Telegram message: {e}")
        restart_wifi()
        continue
    except RequestException as e:
        log(f"A network error occurred in login form: {e}")
        restart_wifi()
        continue
    except NoSuchElementException as e:
        log(f"A NoSuchElementException occurred in login form: {e}")
        continue
    except Exception as e:
        log(f"An unexpected error form occurred in login: {e}")
        restart_wifi()
        driver.quit()
        driver = setup_driver()
        continue

# Start script
while True:
    try:
        if is_connected():
            send_farm_lists(driver)
        else:
            restart_wifi()
    except RequestException as e:
        log(f"A network error occurred: {e}")
        restart_wifi()
        continue
    except NoSuchElementException as e:
        log(f"A NoSuchElementException occurred: {e}")
        continue
    except NoSuchWindowException as e:
        log(f"A NoSuchWindowException occurred: {e}")
        restart_wifi()
        driver.quit()
        driver = setup_driver()
        login(driver, os.environ.get('TRAVIAN_FARM_BOT_USERNAME'), os.environ.get('TRAVIAN_FARM_BOT_PASSWORD'))
        continue
    except WebDriverException as e:
        log(f"A WebDriverException occurred: {e}")
        restart_wifi()
        driver.quit()
        driver = setup_driver()
        login(driver, os.environ.get('TRAVIAN_FARM_BOT_USERNAME'), os.environ.get('TRAVIAN_FARM_BOT_PASSWORD'))
        continue
    except Exception as e:
        log(f"An unexpected error occurred: {e}")
        restart_wifi()
        driver.quit()
        driver = setup_driver()
        login(driver, os.environ.get('TRAVIAN_FARM_BOT_USERNAME'), os.environ.get('TRAVIAN_FARM_BOT_PASSWORD'))
        continue
