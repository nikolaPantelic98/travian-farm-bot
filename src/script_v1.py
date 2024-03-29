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

stable_count = 1
farm_list_send_count = 1

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
    driver.maximize_window()
    log("Starting script...")
    return driver


def login(driver, username, password):
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_FARM_LIST_URL'))
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
    sleep(random.uniform(7, 10))  # todo: change the time (less)


def train_unit(driver):
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_STABLE_URL'))
    sleep(random.uniform(3.7, 6)) # todo: change the time (less)

    input_element = driver.find_element(By.NAME, 't5')
    input_element.clear()
    sleep(random.uniform(0.4, 1))
    input_element.send_keys('1')
    sleep(random.uniform(0.5, 1.5))

    start_training_button = driver.find_element(By.XPATH, '//button[contains(@class, "startTraining")]')
    start_training_button.click()
    sleep(random.uniform(1.3, 3.6))


# number of farm lists (buttons) is 2
def send_farm_lists(driver):
    global stable_count
    global farm_list_send_count

    driver.get(os.environ.get('TRAVIAN_FARM_BOT_FARM_LIST_URL'))
    sleep(random.uniform(1, 3))
    driver.get(os.environ.get('TRAVIAN_FARM_BOT_FARM_LIST_URL'))
    sleep(random.uniform(3, 5))

    num_villages = 1
    farm_lists_per_village = [2, 1]

    villages = driver.find_elements(By.XPATH, '//div[contains(@class, "villageWrapper")]')
    num_villages = min(num_villages, len(villages))

    # iterate through all villages that have farm lists set up
    for village_index in range(num_villages):
        village = villages[village_index]

        num_farm_lists = farm_lists_per_village[village_index]

        farm_lists = village.find_elements(By.XPATH, './/div[contains(@class, "farmListHeader")]/button[contains(@class, "startFarmList")]')
        num_farm_lists = min(num_farm_lists, len(farm_lists))

        # first button is executed every time, while second button is executed every 2nd time
        for farm_list_index in range(num_farm_lists):
            if farm_list_index == 0 or (farm_list_index == 1 and farm_list_send_count % 2 == 0):
                farm_list = farm_lists[farm_list_index]
                scroll_time = random.uniform(0.5, 1.5) * 1000
                driver.execute_script(f"""
                    var element = arguments[0];
                    var box = element.getBoundingClientRect();
                    var body = document.body;
                    var docEl = document.documentElement;
                    var scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop;
                    var clientTop = docEl.clientTop || body.clientTop || 0;
                    var top  = box.top +  scrollTop - clientTop;
                    var currenTop = window.pageYOffset || document.documentElement.scrollTop;
                    var start = null;
                    requestAnimationFrame(function step(timestamp) {{
                        if (!start) start = timestamp;
                        var progress = timestamp - start;
                        if (currenTop < top) {{
                            window.scrollTo(0, ((top - currenTop) * progress / {scroll_time}) + currenTop);
                        }} else {{
                            window.scrollTo(0, currenTop - ((currenTop - top) * progress / {scroll_time}));
                        }}
                        if (progress < {scroll_time}) {{
                            requestAnimationFrame(step);
                        }}
                    }});
                """, farm_list)
                sleep(scroll_time / 1000 + random.uniform(0.2, 0.4))
                farm_list.click()
                log(f"Farm list {farm_list_index + 1} is sent.")
                sleep(random.uniform(2.7, 4.3))

    if farm_list_send_count % 2 == 0:
        farm_list_send_count = 0

    # train unit every 5th time
    if stable_count == 5:
        train_unit(driver)
        stable_count = 1
    else:
        stable_count += 1

    driver.get(os.environ.get('TRAVIAN_FARM_BOT_VILLAGE_STATISTICS_URL'))
    img_elements = driver.find_elements(By.XPATH, '//img[contains(@class, "att1")]')
    number_of_villages_attacked = len(img_elements)
    total_attacks = 0

    for img_element in img_elements:
        alt_text = img_element.get_attribute("alt")
        number_x = alt_text.split()[0]
        number = number_x.split('x')[0]
        total_attacks += int(number)

    sleep(random.uniform(3.1, 4.1))
    driver.get('https://google.com')
    log("Script executed!")

    if number_of_villages_attacked > 0:
        village_message = " " + str(
            number_of_villages_attacked) + " village is attacked " if number_of_villages_attacked == 1 else " " + str(
            number_of_villages_attacked) + " villages are attacked "
        attack_message = " There is " + str(
            total_attacks) + " total attack " if total_attacks == 1 else " There are " + str(
            total_attacks) + " total attacks "

        send_telegram_message(u'\u2757\u2757' + " Someone attacked you " + u'\u2757\u2757' + "\n"
                              + u'\u2757\u2757' + village_message + u'\u2757\u2757' + "\n"
                              + u'\u2757\u2757' + attack_message + u'\u2757\u2757')
    else:
        send_telegram_message(u'\u2705\u2705' + " No one attacked you " + u'\u2705\u2705')

    farm_list_send_count += 1
    sleep(random.uniform(401, 415))


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
