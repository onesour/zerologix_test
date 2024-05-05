import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from register_page import RegisterPage

CHROME_DRIVER_PATH = "C:\\Users\\YIHSUAN\\Desktop\\chromedriver-win64_124\\chromedriver.exe"
ACY_URL = "https://www.acy.com/en/open-live-account"
FIRST_NAME = "YI HSUAN"
LAST_NAME = "WU"
PHONE_NUMBER = "912345678"
EMAIL = "tt12345@ttfdsa.fds"
PASSWORD = "Test1234!"
TEST_LANGUAGE = "中文繁體"
TEST_COUNTRY = "台灣"
TEST_PHONE_REGION = "臺灣"


class TestRegister:
    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        chrome_service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.register_page = RegisterPage(self.driver)

    def test_normal_register(self):
        self.driver.get(ACY_URL)
        # Get language selector and choose Chinese.
        self.register_page.set_language(TEST_LANGUAGE)
        # Get country element.
        self.register_page.set_country(TEST_COUNTRY)
        # Get account elements.
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."
        continue_btn.click()
        # Wait for email verify code presence.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Character 1.']")))
        email_verify_code_elems = self.driver.find_elements(By.XPATH, "//*[contains(@aria-label,'Character')]")
        fake_code = "1234"
        for i in range(len(email_verify_code_elems)):
            email_verify_code_elems[i].send_keys(fake_code[i])
        # Check verify button.
        verify_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='verify code button']")
        is_btn_enable = verify_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the verify code, the verify button should be clickable."
        verify_btn.click()
        # Check error message.
        error_msg_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "style__StyledErrorMessage-sc-17ytta5-10")))
        assert "密碼無效" in error_msg_elem.text, \
            "There should be \"密碼無效\" error message after entering the incorrect verify code."
