import pytest
from selenium import webdriver

chrome_driver_path = "C:\\Users\\YIHSUAN\\Desktop\\chromedriver-win64_124\\chromedriver.exe"
acy_url = "https://www.acy-cn.cloud/open-live-account?url=https%3A%2F%2Facyasia-cn.com%2Fen%2Fopen-live-account%2F&next=%2Fcreate-account%2Fselect-account-type"


class TestRegister:
    @pytest.fixture(scope="function", autouse=True)
    def set_up(self):
        chrome_service = webdriver.ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=chrome_service)

    def test_normal_register(self):
        self.driver.get(acy_url)
