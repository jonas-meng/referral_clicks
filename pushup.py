import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def one_activation(email_refresh_count: int = 3) -> bool:
    coinbase_nft_url = "https://coinbase.com/nft/announce/1PNPR3"
    mail_service_url = "https://temp-mail.io"

    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("/home/jonas/chromedriver", chrome_options=chrome_options)

    driver.get(mail_service_url)
    mail_service_handle = driver.current_window_handle
    time.sleep(1)
    button = driver.find_element(by=By.CSS_SELECTOR, value=".menu button[data-original-title='Copy email']")
    button.click()
    temp_email = pyperclip.paste()
    print(f"temporary email is {temp_email}")

    driver.execute_script("window.open('about:blank', 'coinbase');")
    driver.switch_to.window("coinbase")
    driver.get(coinbase_nft_url)
    email_field = driver.find_element(by=By.CSS_SELECTOR, value="#waitlist_email")
    email_field.send_keys(temp_email)
    checkbox = driver.find_element(by=By.CSS_SELECTOR, value="#wantsEmails")
    checkbox.click()
    time.sleep(1)
    join_button = driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
    join_button.click()

    driver.switch_to.window(mail_service_handle)
    count = 0
    while True:
        time.sleep(3)
        button = driver.find_element(by=By.CSS_SELECTOR, value=".menu button[data-original-title='Refresh for new messages']")
        button.click()
        print(f"Refresh mail list {count + 1} times")
        mail_list = driver.find_elements(by=By.CSS_SELECTOR, value=".sidebar ul li")
        if len(mail_list) > 0:
            mail_list[0].click()
            print("Activation mail received")
            break
        count += 1
        if count > email_refresh_count:
            print()
            return False

    count = 0
    while True:
        print(f"Email is rendering, plesae wait {count + 1} times")
        time.sleep(2)
        activate_link = driver.find_element(by=By.CSS_SELECTOR, value="main.content table a[href*='kickofflabs']")
        if activate_link:
            activate_link = activate_link.get_attribute("href")
            print(f"Open activate link: {activate_link}")
            driver.execute_script("window.open('about:blank', 'activate');")
            driver.switch_to.window("activate")
            driver.get(activate_link)
            print("Wait activate page rendering")
            time.sleep(1)
            break
        count += 1
        if count > email_refresh_count:
            return False

    driver.close()
    print("Process finished!")
    return True

success_count = 0
failure_count = 0

print("Start activation loop")
while True:
    try:
        result = one_activation()
        if result:
            success_count += 1
        else:
            failure_count += 1
        print(f"Success count {success_count}, failure count {failure_count}")
        if success_count % 90 == 0:
            break
        if success_count % 30 == 0:
            time.sleep(120)
    except:
        failure_count += 1
        print(f"Chrome broken down, restart in 120 seconds")
        time.sleep(180)
        print(f"Success count {success_count}, failure count {failure_count}")
