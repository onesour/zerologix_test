from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver

    def set_language(self, language):
        language_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/main/div/div/div/div[2]/div/div/div/div")))
        language_elem.click()
        language_ul = language_elem.find_element(By.TAG_NAME, "ul")
        language_lis = language_ul.find_elements(By.TAG_NAME, "li")
        for li_elem in language_lis:
            if li_elem.text == language:
                li_elem.click()
                break
        return language_elem

    def set_country(self, country):
        country_selector_elem = self.driver.find_element(By.XPATH, "//*[@id=\"react-select-2-input\"]")
        country_selector_elem.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"react-select-2-listbox\"]")))
        sub_elems = self.driver.find_elements(By.XPATH, "//*[@id=\"react-select-2-listbox\"]/div/div")
        for sub in sub_elems:
            if sub.text == country:
                sub.click()
                break

    def set_first_name(self, first_name):
        first_name_elem = self.driver.find_element(By.NAME, "firstName")
        first_name_elem.send_keys(first_name)
        return first_name_elem

    def set_last_name(self, last_name):
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        last_name_elem.send_keys(last_name)
        return last_name_elem

    def set_phone_number(self, region, phone_number):
        phone_region_elem = self.driver.find_element(By.CLASS_NAME, "flag-dropdown")
        phone_region_elem.click()
        phone_region_selector = self.driver.find_element(By.CSS_SELECTOR, ".country-list.dropdown")
        phone_region_li = phone_region_selector.find_elements(By.TAG_NAME, "li")
        for li_elem in phone_region_li:
            if region in li_elem.text:
                li_elem.click()
                break
        phone_elem = self.driver.find_element(By.XPATH,
                                              "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/input")
        phone_elem.send_keys(phone_number)
        return phone_elem

    def set_email(self, email):
        email_elem = self.driver.find_element(By.NAME, "email")
        email_elem.send_keys(email)
        return email_elem

    def set_password(self, password):
        password_elem = self.driver.find_element(By.NAME, "password")
        password_elem.send_keys(password)
        return password_elem
