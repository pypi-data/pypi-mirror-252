from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class SetupDriver:
    def __init__(self,driver_path):
        self.driver_path = driver_path
    
    def chrome_options(self):
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        chr_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.service = Service(self.driver_path)
        self.chr_options = chr_options
    
    def setup_driver(self):
        try:
            self.chrome_options()
            driver = webdriver.Chrome(service=self.service, options=self.chr_options)
            driver.maximize_window()
            return driver
        except Exception as e:
            print(f"Error while starting the driver as {e}")
            return None