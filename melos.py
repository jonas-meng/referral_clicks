import random
import string

from pushup import Pushup


class Melos(Pushup):

    def generate_password(self):
        letters = string.ascii_letters + string.digits
        length = 16
        return ''.join(random.choice(letters) for _ in range(length))

    def action_on_webpage(self, temp_email):
        try:
            email_field = self.driver.find_element_by_css_selector("#nest-messages_email")
            email_field.send_keys(temp_email)
            password_field = self.driver.find_element_by_css_selector("#nest-messages_password")
            password = self.generate_password()
            password_field.send_keys(password)
            self.logger.info(f"Email: {temp_email}, Password: {password}")
            check_field = self.driver.find_element_by_css_selector("i.circle")
            check_field.click()
            submit_button = self.driver.find_element_by_css_selector("button[type=submit]")
            submit_button.click()
            return True
        except:
            return False

    def action_on_email(self):
        try:
            a_tag = self.driver.find_element_by_link_text('Verify Email Address')
            self.logger.info(f"Verify link: {a_tag.get_attribute('href')}")
            a_tag.click()
            self.wait_for_rendering()
            return True
        except:
            return False
