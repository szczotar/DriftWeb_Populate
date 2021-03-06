from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



# from selenium.webdriver.support.ui import Select

import time




class Populate_queue():
    def __init__(self,login,password):
        self.password = password
        self.login = login
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(r"C:\Users\admin\Desktop\Env\new_env\Web_automation_project1\chromedriver.exe",options=options)
        self.driver.get("https://preprod.dw3.dk/")
        self.action = ActionChains(self.driver)
  
        
        self.log_in()
        self.navigate_to_list("PARK","sfsaf")

    
    def log_in(self):

        try:
            login_input = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.ID,"username"))
            )
            login_input.send_keys(self.login)
            password_input = self.driver.find_element(By.ID,"password")
            password_input.send_keys(self.password)
            login_button = self.driver.find_element(By.ID,"btnComplete")
            login_button.click()

            exit_icon = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"icon-lock-out"))
            )
            print("login success")

        finally:
            pass

    def navigate_to_list(self,profil,Arbejdsgruppe):
        self.profil = profil
        self.Arbejdsgruppe = Arbejdsgruppe

        try:
            time.sleep(2)
            filter  = self.driver.find_element(By.ID,"navbarChangeClient")
            filter.click()
            head = self.driver.find_element(By.XPATH,"""//*[@id="changeClientList"]/div[1]/div[3]/span""")

            point = head.location
            print(point)
            time.sleep(2)
            self.action.move_to_element_with_offset(filter,50,140).double_click().perform()
            
        finally:
            pass


            
if __name__ == "__main__" :
    queue = Populate_queue()



