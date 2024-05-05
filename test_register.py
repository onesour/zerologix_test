import re

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
EMAIL = "test1234@test.abc"
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
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
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

    def test_illegal_first_name(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name("123")
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH, "//*[@aria-label='Invalid Firstname']")
        assert first_name_error_elem.text == "請輸入有效的名字", \
            "There should be error message after entering illegal first name."

    def test_illegal_last_name(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name("456")
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH, "//*[@aria-label='Invalid Lastname']")
        assert first_name_error_elem.text == "請輸入有效的姓氏", \
            "There should be error message after entering illegal last name."

    def test_illegal_phone_number(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number="test")
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert not is_btn_enable, \
            "After entering the illegal phone number for the register, the continue button should not be clickable."

    def test_illegal_email(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email("test@123")
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH,
                                                         "//*[@aria-label='Invalid Email']")
        assert first_name_error_elem.text == "電子郵件地址不正確", \
            "There should be error message after entering illegal email."

    @pytest.mark.parametrize("info",
                             [{"password": "aabbccdd", "char_check": True, "lower_check": True, "upper_check": False,
                               "number_check": False, "special_char_check": False},
                              {"password": "AABBCCDD", "char_check": True, "lower_check": False, "upper_check": True,
                               "number_check": False, "special_char_check": False},
                              {"password": "aabbccddeeffgghhiijja", "char_check": False, "lower_check": True,
                               "upper_check": False, "number_check": False, "special_char_check": False},
                              {"password": "AABBCCDDEEFFGGHHIIJJA", "char_check": False, "lower_check": False,
                               "upper_check": True, "number_check": False, "special_char_check": False},
                              {"password": "123", "char_check": False, "lower_check": False, "upper_check": False,
                               "number_check": True, "special_char_check": False},
                              {"password": "12345678", "char_check": True, "lower_check": False, "upper_check": False,
                               "number_check": True, "special_char_check": False},
                              {"password": "12345678!", "char_check": True, "lower_check": False, "upper_check": False,
                               "number_check": True, "special_char_check": True},
                              ])
    def test_illegal_password(self, info):
        hint_green_color = "rgba(153,227,174,1)"
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(info["password"])
        # Check password hint.
        character_check_hint = self.driver.find_element(By.XPATH, "//*[@aria-label='Length Check']")
        character_check_bg_color = character_check_hint.value_of_css_property("background-color")
        character_check_bg_color = character_check_bg_color.replace(" ", "")
        assert (character_check_bg_color == hint_green_color) is info["char_check"], \
            f"Password hint for character length to green should be {info['char_check']}."
        lower_check_hint = self.driver.find_element(By.XPATH, "//*[@aria-label='Lowercase Check']")
        lower_bg_color = lower_check_hint.value_of_css_property("background-color")
        lower_bg_color = lower_bg_color.replace(" ", "")
        assert (lower_bg_color == hint_green_color) is info["lower_check"], \
            f"Password hint for lower letter to green should be {info['lower_check']}."
        upper_check_hint = self.driver.find_element(By.XPATH, "//*[@aria-label='Uppercase Check']")
        upper_check_bg_color = upper_check_hint.value_of_css_property("background-color")
        upper_check_bg_color = upper_check_bg_color.replace(" ", "")
        assert (upper_check_bg_color == hint_green_color) is info["upper_check"], \
            f"Password hint for upper letter to green should be {info['upper_check']}."
        number_check_hint = self.driver.find_element(By.XPATH, "//*[@aria-label='Number Check']")
        number_check_bg_color = number_check_hint.value_of_css_property("background-color")
        number_check_bg_color = number_check_bg_color.replace(" ", "")
        assert (number_check_bg_color == hint_green_color) is info["number_check"], \
            f"Password hint for number check to green should be {info['number_check']}."
        special_char_check_hint = self.driver.find_element(By.XPATH, "//*[@aria-label='Special Char Check']")
        special_char_check_bg_color = special_char_check_hint.value_of_css_property("background-color")
        special_char_check_bg_color = special_char_check_bg_color.replace(" ", "")
        assert (special_char_check_bg_color == hint_green_color) is info["special_char_check"], \
            f"Password hint for special character to green should be {info['special_char_check']}."
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert not is_btn_enable, \
            "After entering the illegal password for the register, the continue button should not be clickable."

    def test_not_select_register_agreement(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        register_agreement_checkbox = self.driver.find_element(By.NAME, "policy")
        if register_agreement_checkbox.is_selected():
            register_agreement_checkbox.click()
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert not is_btn_enable, \
            "After cancel register agreement, the continue button should not be clickable."

    def test_not_select_subscription_agreement(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        subscription_agreement_checkbox = self.driver.find_element(By.NAME, "subscription")
        if subscription_agreement_checkbox.is_selected():
            subscription_agreement_checkbox.click()
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After only cancel subscription agreement, the continue button should be clickable."

    def test_not_select_subscription_agreement(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        subscription_agreement_checkbox = self.driver.find_element(By.NAME, "subscription")
        if subscription_agreement_checkbox.is_selected():
            subscription_agreement_checkbox.click()
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After only cancel subscription agreement, the continue button should be clickable."

    def test_enter_not_exist_country(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        country_selector_elem = self.driver.find_element(By.XPATH, "//*[@id=\"react-select-2-input\"]")
        country_selector_elem.click()
        country_selector_elem.send_keys("aa")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"react-select-2-listbox\"]")))
        sub_elems = self.driver.find_elements(By.XPATH, "//*[@id=\"react-select-2-listbox\"]/div/div")
        assert len(sub_elems) == 1, \
            "After entering hint that didn't match any country, the hint list length should be 1."
        assert sub_elems[0].text.lower() == "no options", "The only hint for country list should be \"no options\"."

    @pytest.mark.parametrize("test_data", [{"language": "English", "country": "Taiwan", "phone_region": "Taiwan"},
                                           {"language": "日本語", "country": "日本", "phone_region": "日本"}])
    def test_selector_other_language(self, test_data):
        self.driver.get(ACY_URL)
        self.register_page.set_language(test_data["language"])
        self.register_page.set_country(test_data["country"])
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        self.register_page.set_phone_number(region=test_data["phone_region"], phone_number=PHONE_NUMBER)
        self.register_page.set_email(EMAIL)
        self.register_page.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."

    def test_enter_field_not_from_top_to_bottom(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        self.register_page.set_password(PASSWORD)
        self.register_page.set_email(EMAIL)
        self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        self.register_page.set_first_name(FIRST_NAME)
        self.register_page.set_last_name(LAST_NAME)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH, "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."

    @pytest.mark.parametrize("test_data", [{"country": "中國", "phone_region": "中國"},
                                           {"country": "越南", "phone_region": "越南"}])
    def test_check_phone_region_when_changing_country(self, test_data):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(test_data["country"])
        phone_region_elem = self.driver.find_element(By.CLASS_NAME, "selected-flag")
        phone_region_title = phone_region_elem.get_attribute("title")
        assert test_data["phone_region"] in phone_region_title, \
            f"There should be \"{test_data['phone_region']}\" in phone region after changing country."

    def test_changing_language_after_entering_field(self):
        self.driver.get(ACY_URL)
        self.register_page.set_language(TEST_LANGUAGE)
        self.register_page.set_country(TEST_COUNTRY)
        first_name_elem = self.register_page.set_first_name(FIRST_NAME)
        last_name_elem = self.register_page.set_last_name(LAST_NAME)
        phone_number_elem = self.register_page.set_phone_number(region=TEST_PHONE_REGION, phone_number=PHONE_NUMBER)
        email_elem = self.register_page.set_email(EMAIL)
        password_elem = self.register_page.set_password(PASSWORD)
        assert first_name_elem.get_attribute("value") == FIRST_NAME, \
            f"First name element value should be \"{FIRST_NAME}\"."
        assert last_name_elem.get_attribute("value") == LAST_NAME, \
            f"Last name element value should be \"{LAST_NAME}\"."
        assert PHONE_NUMBER in phone_number_elem.get_attribute("value"), \
            f"Phone number element value should be \"{PHONE_NUMBER}\"."
        assert email_elem.get_attribute("value") == EMAIL, \
            f"Email element value should be \"{EMAIL}\"."
        assert password_elem.get_attribute("value") == PASSWORD, \
            f"Password element value should be \"{PASSWORD}\"."
        self.register_page.set_language("English")
        first_name_elem = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "firstName")))
        assert not first_name_elem.get_attribute("value"), "After changing language, first name value should be empty."
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        assert not last_name_elem.get_attribute("value"), "After changing language, last name value should be empty."
        phone_region_elem = self.driver.find_element(By.CLASS_NAME, "selected-flag")
        phone_region_number = re.search(r"\d+", phone_region_elem.get_attribute("title"))
        phone_number_elem = self.driver.find_element(By.CSS_SELECTOR, ".form-control.phone-input")
        phone_number_value = phone_number_elem.get_attribute("value")
        phone_number_value = phone_number_value.replace(f"+{phone_region_number.group()}", "")
        assert not phone_number_value, \
            "After changing language, phone number value should be empty."
        email_elem = self.driver.find_element(By.NAME, "email")
        assert not email_elem.get_attribute("value"), "After changing language, email value should be empty."
        password_elem = self.driver.find_element(By.NAME, "password")
        assert not password_elem.get_attribute("value"), "After changing language, password value should be empty."
