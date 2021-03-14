from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException


# capabilities_chrome = webdriver.DesiredCapabilities.CHROME

# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
# prox.http_proxy = '00.000.0000'
# prox.ssl_proxy =  '000.000.0000'
# #add proxy using chrome capabilities
# prox.add_to_capabilities(capabilities_chrome)

options = Options()
options.add_argument("start-maximized")
# options.add_argument("--headless")
options.add_argument("--disable-infobars")
prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2, 
         "profile.managed_default_content_settings.media_stream":2,
}
# options.add_experimental_option("prefs",prefs)


driver = webdriver.Chrome(r"C:\Users\admin\Desktop\Env\new_env\Web_automation_project1\chromedriver.exe",options=options)
driver.get("https://preprod.dw3.dk/")

while True:
    try:
        WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"username)))
        # login_input.send_keys("stefan.roi@digitalworkforce.com")
        # password_input = driver.find_element(By.ID,"password")
        # password_input.send_keys("floatuivo")
        # login_button = driver.find_element(By.ID,"btnComplete")
        # login_button.click()

        # button = driver.find_element(By.ID,"navbarShortcutMenu")
        # # button.click()
        # driver.implicitly_wait(2)
        # action = ActionChains(driver)
        # action.move_to_element(button).click().perform()
        # action.move_by_offset(500,200).perform()

    except TimeoutException:
        print("time up")
        True


# stefan.roi@digitalworkforce.com","floatuivo