  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.select import Select


# from selenium.webdriver.support.ui import Select

import time



class Populate_queue():
    def __init__(self,login,password):
        self.password = password
        self.login = login
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://preprod.dw3.dk/")
        self.action = ActionChains(self.driver)
  
        self.log_in()
        self.navigate_to_list("Fors A/S / FORS: PARK / FORS: Grøndrift")
        self.select_tab()
        self.collect_tasks()

    
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

    def navigate_to_list(self,filter):
        self.filter = filter

        while True:
            try:
                navbar = WebDriverWait(self.driver,20).until(
                    EC.visibility_of_element_located((By.ID,"navbarChangeClient"))
                    )
                navbar.click()
                time.sleep(3)
                string2 = str("javascript:document.getElementById('spMenu').click();")
                self.driver.execute_script(string2)

                time.sleep(5)

            
                self.action.send_keys(Keys.DELETE).perform()
                self.action.send_keys(Keys.DOWN*2).perform()
                time.sleep(2)
                self.action.send_keys(Keys.ENTER).perform()
               
                Grondrift = WebDriverWait(self.driver,10).until(
                    EC.visibility_of_element_located((By.ID,"ui-multiselect-0-changeclientwgchecklist-option-3"))
                )
                Grondrift.click()

               
                
                skift_button = self.driver.find_element(By.ID,"changeClientButton")
                skift_button.click()

                navbar = self.driver.find_element(By.ID,"navbarChangeClient")
                print(navbar.text)

    
                if navbar.text == filter:
                    break
                else:
                    True

            except TimeoutException:
                print("time up")
                skift_button = self.driver.find_element(By.ID,"changeClientButton")
                skift_button.click()
                True

    def select_tab(self):
        try:
            
            Opgaver = WebDriverWait(self.driver,10).until(
                EC.visibility_of_element_located((By.ID,"taskToggleNavigation"))
                )
            Opgaver.click()
           
            Godkendt = WebDriverWait(self.driver,10).until(
                EC.visibility_of_element_located((By.ID,"nav_task_6"))
                )
                
            Godkendt.click()

        except:
            # self.driver.find_element(By.ID,"taskToggleNavigation").click()
            # time.sleep(2)
            # self.action.move_to_element(Godkendt)
            self.driver.find_element(By.ID,"nav_task_6").click()
            

        finally:
            pass

    def collect_tasks(self):
        try:
            row = 1
            T_numbers =[]
            while True:
            
                task = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located((By.XPATH,f"""//*[@id="list-datatable"]/tbody/tr[{row}]/td[2]"""))
                )

                # task = self.driver.find_element(By.XPATH,f"""//*[@id="list-datatable"]/tbody/tr[{row}]/td[2]""")
            
                t =task.get_attribute("innerText")
                print(t)
    
                T_numbers.append(t)
                
                row += 1

            

        except TimeoutException:
            print("No more element")
            print(T_numbers)


            
if __name__ == "__main__" :
    queue = Populate_queue()