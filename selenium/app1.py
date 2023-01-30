import sys,os; sys.path.insert(0,os.path.join( os.path.dirname(__file__),".."))
#################################################################################
from htag import Tag

class App(Tag.body):
    def init(self):
        def say_hello(o):
            self <= Tag.li("hello")
        self<= Tag.button("click",_onclick = say_hello)
        self<= Tag.button("exit",_onclick = lambda o: self.exit())

#################################################################################
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def tests(driver):
    driver.implicitly_wait(1) # seconds
    assert "App" in driver.title

    driver.find_element(By.XPATH, '//button[text()="click"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="click"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="click"]').click()
    time.sleep(1)

    assert len(driver.find_elements(By.XPATH, '//li'))==3

    driver.find_element(By.XPATH, '//button[text()="exit"]').click()
    return True
