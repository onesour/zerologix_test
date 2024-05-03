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
email = "test1234@test.abc"
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
        first_name_elem.send_keys(first_name)
        last_name_elem = self.driver.find_element(By.NAME, "lastName")
        last_name_elem.send_keys(last_name)
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
