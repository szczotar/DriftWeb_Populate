from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException,NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support.select import Select
import time
import orchestrator_request
import datetime
import sys
from getpass import getpass
import logging
import logging.handlers
import os
import datetime


handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", r"C:\Users\admin\Desktop\Env\new_env\DriftWeb_populate\logs.txt"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

class Populate_queue():
    def __init__(self):
        self.login = input("Username: ")
        self.password = getpass("Password: ")
        
    def Start_poplate(self): 
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://preprod.dw3.dk/")
        self.action = ActionChains(self.driver)
  
        self.log_in()
        self.navigate_to_list("Fors A/S / FORS: PARK / FORS: Grøndrift")
        self.select_tab()
        self.tasks = self.collect_tasks()
        self.add_toQueue(self.tasks)
        self.log_out()
        logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")+ " populate execution finished")
       
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
            logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " login success")
            print("login success")

        except (NoSuchElementException,TimeoutException) as err:
            if self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/form/div/p[1]"):
                logging.exception(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " wrong credentials")
                print("wrong credentials")
                
                
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

            except (TimeoutException,StaleElementReferenceException) as err:
                print(err)
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

        except (NoSuchElementException, TimeoutException)as err:
            logging.exception(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + 
            " Could not select Godkent")
            print(err.msg)
                  
    def collect_tasks(self):
        try:
            row = 1
            t_numbers =[]
            while True:
                task = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located((By.XPATH,f"""//*[@id="list-datatable"]/tbody/tr[{row}]/td[2]"""))
                )
                t_number =task.get_attribute("innerText")
                t_numbers.append(t_number)
                row += 1

        except TimeoutException:
            print("No more elements")
        
        logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + f" data collected: {t_numbers}")
        return t_numbers

    def add_toQueue(self,tasks):
        self.tasks = tasks
        try:
            access_token = orchestrator_request.Get_token("Artur","8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
            "MipuhkUYB5eN_fdW3dAzE0mK2RzwzKUy_CiE_HhBv7JSX")
         
        except Exception as err:
            print(repr(err))

        for i in tasks:
            try:
                content = {"T_number":i}
                orchestrator_request.Add_queue_item("burki","Artur","1269","DriftWeb",access_token,content)
                
            except Exception as err:
                print(sys.exc_info())
                continue
          
    def log_out(self):
        exit_icon = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"icon-lock-out"))
            )
        exit_icon.click()
        self.driver.close()
        logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")+ " Browser Closed")


if __name__ == "__main__" :
    queue = Populate_queue()
    queue.Start_poplate()

