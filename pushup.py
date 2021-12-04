import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from log_utility import get_logger


class Pushup:

    def __init__(self, driver_path):
        """
        :param driver_path: path towards the downloaded browser driver
        :return:
        """
        self.driver_path = driver_path
        self.driver = None
        self.logger = get_logger(self.__class__.__name__, f"{self.__class__.__name__}.log")

    def start_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=chrome_options)

    def wait_for_rendering(self, seconds=2):
        time.sleep(seconds)

    def get_temp_email(self):
        mail_service_url = "https://temp-mail.io"
        self.driver.get(mail_service_url)
        mail_service_handle = self.driver.current_window_handle
        button = self.driver.find_element(by=By.CSS_SELECTOR, value=".menu button[data-original-title='Copy email']")
        button.click()
        self.wait_for_rendering()
        temp_email = pyperclip.paste()
        self.logger.info(f"Temporary email is {temp_email}")
        return temp_email, mail_service_handle

    def action_on_webpage(self, temp_email):
        return False

    def action_on_email(self):
        return False

    def process_email(self):
        retry_times = 3
        for i in range(0, retry_times):
            self.logger.info(f"{i}-th time retry email processing")
            self.wait_for_rendering()
            if self.action_on_email():
                return True
        return False

    def process_target_webpage(self, url, temp_email, mail_service_handle):
        self.logger.info(f"processing webpage {url}")
        self.driver.execute_script("window.open('about:blank', 'target');")
        self.driver.switch_to.window("target")
        self.driver.get(url)
        self.action_on_webpage(temp_email)
        if self.receive_email(mail_service_handle):
            return self.process_email()
        return False

    def check_email(self):
        button = self.driver.find_element(by=By.CSS_SELECTOR,
                                     value=".menu button[data-original-title='Refresh for new messages']")
        button.click()
        mail_list = self.driver.find_elements(by=By.CSS_SELECTOR, value=".sidebar ul li")
        if len(mail_list) > 0:
            mail_list[0].click()
            self.logger.info("Target mail received")
            return True
        return False

    def receive_email(self, mail_service_handle):
        self.driver.switch_to.window(mail_service_handle)
        retry_times = 4
        for i in range(0, retry_times):
            self.logger.info(f"{i}-th time checking email")
            if self.check_email():
                return True
            self.wait_for_rendering(15)
        return False

    def referral(self, url):
        temp_email, mail_service_handle = self.get_temp_email()
        return self.process_target_webpage(url, temp_email, mail_service_handle)

    def close_driver(self):
        self.driver.close()

    def start_referral(self, url):
        success_count = 0
        failure_count = 0
        interval = 10
        self.logger.info("Start referral loop")
        while True:
            try:
                self.start_driver()
                result = self.referral(url)
                self.close_driver()
                if result:
                    success_count += 1
                else:
                    failure_count += 1
                self.logger.info(f"Success count {success_count}, failure count {failure_count}")
            except:
                failure_count += 1
                self.logger.error(f"Chrome broken down, restart in {interval} seconds")
                time.sleep(interval)
                self.logger.info(f"Success count {success_count}, failure count {failure_count}")


if __name__ == "__main__":
    pass
