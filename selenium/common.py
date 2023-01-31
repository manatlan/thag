import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class HClient:
    def __init__(self,driver):
        self.driver=driver

    @property
    def title(self):
        return self.driver.title

    def click(self,xp:str):
        print("CLICK:",xp)
        try:
            self.driver.find_element(By.XPATH, xp).click()
            time.sleep(0.5)
        except Exception as e:
            print("***HClient ERROR***",e)

    def find(self,xp:str) -> list:
        print("FIND:",xp)
        return self.driver.find_elements(By.XPATH, xp)