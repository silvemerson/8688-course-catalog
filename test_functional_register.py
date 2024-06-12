import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class AllTests(unittest.TestCase):
    def setUp(self):
      self.driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.FirefoxOptions())

    def test_user_can_register(self):
      self.driver.get("http://web:5000/register")
      self.driver.find_element(By.ID, "name").send_keys("devops")
      self.driver.find_element(By.ID, "email").send_keys("devops@email.com")
      self.driver.find_element(By.ID, "password").send_keys("qwe123qwe")
      self.driver.find_element(By.ID, "confirm").send_keys("qwe123qwe")
      self.driver.find_element(By.ID, "register").click()
      print(self.driver.current_url)
      self.assertIn('http://web:5000/', self.driver.current_url)
      assert "No results found." not in self.driver.page_source


    def tearDown(self):
      self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
