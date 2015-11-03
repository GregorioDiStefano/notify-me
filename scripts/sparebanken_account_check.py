from selenium import webdriver
from scripts import Scripts
import logging
import time
from pyvirtualdisplay import Display

class SparebankenCheck(Scripts):

    def __init__(self, ssn, password, **kwargs):
        self.title = "Check balance of bank account"
        self.ssn = ssn
        self.password = password
        self.send_notification = True

        super(SparebankenCheck, self).__init__(**kwargs)


    def __str__(self):
        return "<Sparebanken1: %s>" % self.title

    def do_test(self):
        display = Display(visible=0, size=(800, 600))
        display.start()

        driver = webdriver.Chrome()
        max_wait = 15
        driver.get("https://m.sparebank1.no/personal/#login-basic/osl")

        assert "Mobilbank privat" in driver.page_source

        ssn = driver.find_element_by_css_selector("input#ssn")
        ssn.send_keys(self.ssn)

        ssn = driver.find_element_by_css_selector("input#password")
        ssn.send_keys(self.password)

        loginbtn = driver.find_element_by_css_selector("#loginButton")
        loginbtn.click()

        time.sleep(5)

        count = 0
        while count < max_wait:
            if driver.execute_script('return document.readyState;') == "complete":
                assert "Min oversikt" in driver.page_source
                balance = driver.find_element_by_css_selector("span.accountBalance").text
                break
            else:
                time.sleep(1)
                count += 1

        if count >= max_wait:
            logging.critical("<%s : Page took too long to load>" % (self))

        driver.close()
        display.stop()

        if balance:
            return balance
