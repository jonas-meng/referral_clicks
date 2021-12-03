import time
import pyperclip
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)
log_path = "activity.log"


def config_logger(logger, log_path=f"{__name__}.log"):
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_path)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.WARNING)
    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)


class Pushup():
    def __init__(self, driver_path):
        """
        :param driver_path: path towards the downloaded browser driver
        :return:
        """
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=chrome_options)

    def wait_for_rendering(self):
        # wait 2 seconds for rendering
        time.sleep(2)

    def get_temp_email(self):
        mail_service_url = "https://temp-mail.io"
        self.driver.get(mail_service_url)
        mail_service_handle = self.driver.current_window_handle
        button = self.driver.find_element(by=By.CSS_SELECTOR, value=".menu button[data-original-title='Copy email']")
        button.click()
        self.wait_for_rendering()
        temp_email = pyperclip.paste()
        logger.info(f"Temporary email is {temp_email}")
        return temp_email, mail_service_handle

    def action_on_webpage(self, temp_email):
        return False

    def action_on_email(self):
        return False

    def process_email(self):
        retry_times = 3
        for i in range(0, retry_times):
            logger.info(f"{i}-th time retry email processing")
            if self.action_on_email():
                return True
        return False

    def process_target_webpage(self, url, temp_email, mail_service_handle):
        logger.info(f"processing webpage {url}")
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
            logger.info("Target mail received")
            return True
        return False

    def receive_email(self, mail_service_handle):
        self.driver.switch_to.window(mail_service_handle)
        retry_times = 3
        for i in range(0, retry_times):
            logger.info(f"{i}-th time checking email")
            if self.check_email():
                return True
        return False

    def referral(self, url):
        temp_email, mail_service_handle = self.get_temp_email()
        return self.process_target_webpage(url, temp_email, mail_service_handle)

    def close_driver(self):
        self.driver.close()

    def start_referral(self, url):
        success_count = 0
        failure_count = 0
        interval = 120
        logger.info("Start referral loop")
        while True:
            try:
                self.start_driver()
                result = self.referral(url)
                self.close_driver()
                if result:
                    success_count += 1
                else:
                    failure_count += 1
                logger.info(f"Success count {success_count}, failure count {failure_count}")
            except:
                failure_count += 1
                logger.error(f"Chrome broken down, restart in {interval} seconds")
                time.sleep(interval)
                logger.info(f"Success count {success_count}, failure count {failure_count}")


config_logger(logger, log_path)

if __name__ == "__main__":
    pass
