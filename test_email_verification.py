import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_driver_path = "C:\\Users\\YIHSUAN\\Desktop\\chromedriver-win64_124\\chromedriver.exe"
acy_url = "https://www.acy.com/en/open-live-account"
first_name = "YI HSUAN"
last_name = "WU"
phone_number = "912345678"
email = "tt12345@ttfdsa.fds"
password = "Test1234!"


class TestRegister:
    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        chrome_service = webdriver.ChromeService(executable_path=chrome_driver_path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def test_normal_register(self):
        self.driver.get(acy_url)
        # Get language selector and choose Chinese.
        language_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/main/div/div/div/div[2]/div/div/div/div")))
        language_elem.click()
        language_ul = language_elem.find_element(By.TAG_NAME, "ul")
        language_lis = language_ul.find_elements(By.TAG_NAME, "li")
        for li_elem in language_lis:
            if li_elem.text == "中文繁體":
                li_elem.click()
                break
        # Get country element.
        country_selector_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"react-select-2-input\"]")))
        country_selector_elem.click()
        # Get account elements.
        first_name_elem = self.driver.find_element(By.NAME, "firstName")
        first_name_elem.send_keys(first_name)
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        last_name_elem.send_keys(last_name)
        phone_elem = self.driver.find_element(By.XPATH,
                                              "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/input")
        phone_elem.send_keys(phone_number)
        email_elem = self.driver.find_element(By.NAME, "email")
        email_elem.send_keys(email)
        password_elem = self.driver.find_element(By.NAME, "password")
        password_elem.send_keys(password)
        # Check continue button.
        continue_btn = self.driver.find_element(By.XPATH,
                                                "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/button")
        is_btn_enable = continue_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the correct information for the register, the continue button should be clickable."
        continue_btn.click()
        # Wait for email verify code presence.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div[2]/div[1]/div[2]/div/input")))
        email_verify_code_elems = self.driver.find_elements(By.XPATH,
                                                            "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div[2]/div[1]/div[2]/div/input")
        fake_code = "1234"
        for i in range(len(email_verify_code_elems)):
            email_verify_code_elems[i].send_keys(fake_code[i])
        # Check verify button.
        verify_btn = self.driver.find_element(By.XPATH,
                                              "//*[@id=\"root\"]/main/div/div/div/div[2]/div/form/div[2]/div[1]/div[3]/button")
        is_btn_enable = verify_btn.is_enabled()
        assert is_btn_enable, \
            "After entering the verify code, the verify button should be clickable."
        verify_btn.click()
        # Check error message.
        error_msg_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "style__StyledErrorMessage-sc-17ytta5-10")))
        assert "密碼無效" in error_msg_elem.text, \
            "There should be \"密碼無效\" error message after entering the incorrect verify code."
