import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CHROME_DRIVER_PATH = "C:\\Users\\YIHSUAN\\Desktop\\chromedriver-win64_124\\chromedriver.exe"
ACY_URL = "https://www.acy.com/en/open-live-account"
FIRST_NAME = "YI HSUAN"
LAST_NAME = "WU"
PHONE_NUMBER = "912345678"
EMAIL = "test1234@test.abc"
PASSWORD = "Test1234!"


class TestRegister:
    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        chrome_service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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

    def set_last_name(self, last_name):
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        last_name_elem.send_keys(last_name)

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

    def set_email(self, email):
        email_elem = self.driver.find_element(By.NAME, "email")
        email_elem.send_keys(email)

    def set_password(self, password):
        password_elem = self.driver.find_element(By.NAME, "password")
        password_elem.send_keys(password)

    @pytest.mark.skip
    def test_normal_register(self):
        self.driver.get(ACY_URL)
        # Select web language.
        language_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/main/div/div/div/div[2]/div/div/div/div")))
        language_elem.click()
        language_ul = language_elem.find_element(By.TAG_NAME, "ul")
        language_lis = language_ul.find_elements(By.TAG_NAME, "li")
        for li_elem in language_lis:
            if li_elem.text == "中文繁體":
                li_elem.click()
                break
        # Select country.
        country_selector_elem = self.driver.find_element(By.XPATH, "//*[@id=\"react-select-2-input\"]")
        country_selector_elem.click()
        country_list_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"react-select-2-listbox\"]")))
        sub_elems = self.driver.find_elements(By.XPATH, "//*[@id=\"react-select-2-listbox\"]/div/div")
        for sub in sub_elems:
            if sub.text == "台灣":
                sub.click()
                break
        first_name_elem = self.driver.find_element(By.NAME, "firstName")
        first_name_elem.send_keys(FIRST_NAME)
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        last_name_elem.send_keys(LAST_NAME)
        # Select phone region.
        phone_region_elem = self.driver.find_element(By.CLASS_NAME, "flag-dropdown")
        phone_region_elem.click()
        phone_region_selector = self.driver.find_element(By.CSS_SELECTOR, ".country-list.dropdown")
        phone_region_li = phone_region_selector.find_elements(By.TAG_NAME, "li")
        for li_elem in phone_region_li:
            if "臺灣" in li_elem.text:
                li_elem.click()
                break
        phone_elem = self.driver.find_element(By.XPATH,
                                              "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/input")
        phone_elem.send_keys(PHONE_NUMBER)
        email_elem = self.driver.find_element(By.NAME, "email")
        email_elem.send_keys(EMAIL)
        password_elem = self.driver.find_element(By.NAME, "password")
        password_elem.send_keys(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/button")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."

    def test_illegal_first_name(self):
        self.driver.get(ACY_URL)
        self.set_language("中文繁體")
        self.set_country("台灣")
        self.set_first_name("123")
        self.set_last_name(LAST_NAME)
        self.set_phone_number(region="臺灣", phone_number=PHONE_NUMBER)
        self.set_email(EMAIL)
        self.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH,
                                                         "//*[@aria-label='Invalid Firstname']")
        assert first_name_error_elem.text == "請輸入有效的名字", \
            "There should be error message after entering illegal first name."
