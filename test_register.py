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
            "After entering the information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH,
                                                         "//*[@aria-label='Invalid Firstname']")
        assert first_name_error_elem.text == "請輸入有效的名字", \
            "There should be error message after entering illegal first name."

    def test_illegal_last_name(self):
        self.driver.get(ACY_URL)
        self.set_language("中文繁體")
        self.set_country("台灣")
        self.set_first_name(FIRST_NAME)
        self.set_last_name("456")
        self.set_phone_number(region="臺灣", phone_number=PHONE_NUMBER)
        self.set_email(EMAIL)
        self.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the information for the register, the continue button should be clickable."
        continue_btn.click()
        # Check first name error message.
        first_name_error_elem = self.driver.find_element(By.XPATH,
                                                         "//*[@aria-label='Invalid Lastname']")
        assert first_name_error_elem.text == "請輸入有效的姓氏", \
            "There should be error message after entering illegal last name."

    def test_illegal_phone_number(self):
        self.driver.get(ACY_URL)
        self.set_language("中文繁體")
        self.set_country("台灣")
        self.set_first_name(FIRST_NAME)
        self.set_last_name(LAST_NAME)
        self.set_phone_number(region="臺灣", phone_number="test")
        self.set_email(EMAIL)
        self.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert not is_btn_enable, \
            "After entering the illegal phone number for the register, the continue button should not be clickable."

    def test_illegal_email(self):
        self.driver.get(ACY_URL)
        self.set_language("中文繁體")
        self.set_country("台灣")
        self.set_first_name(FIRST_NAME)
        self.set_last_name(LAST_NAME)
        self.set_phone_number(region="臺灣", phone_number=PHONE_NUMBER)
        self.set_email("test@123")
        self.set_password(PASSWORD)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@aria-label='continue button']")
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
        self.set_language("中文繁體")
        self.set_country("台灣")
        self.set_first_name(FIRST_NAME)
        self.set_last_name(LAST_NAME)
        self.set_phone_number(region="臺灣", phone_number=PHONE_NUMBER)
        self.set_email(EMAIL)
        self.set_password(info["password"])
        # Check password hint.
        character_check_hint = self.driver.find_element(By.XPATH,
                                                        "//*[@aria-label='Length Check']")
        character_check_bg_color = character_check_hint.value_of_css_property("background-color")
        character_check_bg_color = character_check_bg_color.replace(" ", "")
        assert (character_check_bg_color == hint_green_color) is info["char_check"], \
            f"Password hint for character length to green should be {info['char_check']}."
        lower_check_hint = self.driver.find_element(By.XPATH,
                                                    "//*[@aria-label='Lowercase Check']")
        lower_bg_color = lower_check_hint.value_of_css_property("background-color")
        lower_bg_color = lower_bg_color.replace(" ", "")
        assert (lower_bg_color == hint_green_color) is info["lower_check"], \
            f"Password hint for lower letter to green should be {info['lower_check']}."
        upper_check_hint = self.driver.find_element(By.XPATH,
                                                    "//*[@aria-label='Uppercase Check']")
        upper_check_bg_color = upper_check_hint.value_of_css_property("background-color")
        upper_check_bg_color = upper_check_bg_color.replace(" ", "")
        assert (upper_check_bg_color == hint_green_color) is info["upper_check"], \
            f"Password hint for upper letter to green should be {info['upper_check']}."
        number_check_hint = self.driver.find_element(By.XPATH,
                                                     "//*[@aria-label='Number Check']")
        number_check_bg_color = number_check_hint.value_of_css_property("background-color")
        number_check_bg_color = number_check_bg_color.replace(" ", "")
        assert (number_check_bg_color == hint_green_color) is info["number_check"], \
            f"Password hint for number check to green should be {info['number_check']}."
        special_char_check_hint = self.driver.find_element(By.XPATH,
                                                           "//*[@aria-label='Special Char Check']")
        special_char_check_bg_color = special_char_check_hint.value_of_css_property("background-color")
        special_char_check_bg_color = special_char_check_bg_color.replace(" ", "")
        assert (special_char_check_bg_color == hint_green_color) is info["special_char_check"], \
            f"Password hint for special character to green should be {info['special_char_check']}."
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@aria-label='continue button']")
        is_btn_enable = continue_btn.is_enabled()
        assert not is_btn_enable, \
            "After entering the illegal password for the register, the continue button should not be clickable."
