from selenium import webdriver  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class PolyScrapper: 

    def __init__(self, driverPath):
        self.driver = webdriver.Chrome(driverPath)
        self.driver.maximize_window()

    def open_link(self,link):
        self.driver.get(link)

    def search(self,text):
        self.driver.get("https://poly.google.com/search/" + text)

    def filter(self):
        btnFilters = self.driver.find_element_by_xpath("/html/body/c-wiz/div/div[3]/div[1]/c-wiz/div[1]/div/div/div[2]/button")
        btnFilters.click()
        time.sleep(1)

        btnFilterOtherObjects = self.driver.find_element_by_xpath("/html/body/c-wiz/div/div[3]/div[1]/c-wiz/div[1]/c-wiz/div/div[1]/ul/li[4]")
        btnFilterOtherObjects.click()
        time.sleep(1)

        btnFilterRearangable = self.driver.find_element_by_xpath("/html/body/c-wiz/div/div[3]/div[1]/c-wiz/div[1]/c-wiz/div/div[2]/ul/li[1]")
        btnFilterRearangable.click()

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    def get_item_count(self):
        countElement = self.driver.find_element_by_class_name("t569re")
        countText = countElement.get_attribute('textContent').replace(" öğe", '')
        return countText

    def click_element(self, index):
        try:
            element1 = self.driver.find_element_by_xpath("/html/body/c-wiz/div/div[3]/div[1]/c-wiz/div[2]/div[1]/c-wiz[" + str(index) + "]")
            ActionChains(self.driver).key_down(Keys.CONTROL).click(element1).key_up(Keys.CONTROL).perform()
            self.driver.switch_to.window(self.driver.window_handles[1])
            return True
        except:
            print("An exception occurred ot click element")
            return False
        
        return False

    def download(self):
        try:
            isObjFound = False
            downloadButton = self.driver.find_element_by_xpath("/html/body/c-wiz/div/div[3]/div[2]/div[1]/div[2]/div[2]")
            downloadButton.click()
            time.sleep(1)

            for index in range(4):
                realIndex = index + 1
                xpath = "/html/body/c-wiz/div[2]/div/div/span[" + str(realIndex) + "]"
                objButton = self.driver.find_element_by_xpath(xpath)
                if  objButton is not None and objButton.get_attribute('textContent').find("OBJ") != -1:
                    objButton.click()
                    time.sleep(1)
                    isObjFound = True
                    break

            # is OBJ format exist ?
            if isObjFound:
                finalDownloadButton = self.driver.find_element_by_xpath("/html/body/div[9]/div/div[2]/div[3]/div[2]")
                finalDownloadButton.click()
                time.sleep(1)
                self.driver.close()
                time.sleep(0.5)
                self.driver.switch_to.window(self.driver.window_handles[0])
                return True
            else:
                return False
        except:
            print("An exception occurred on download")
            return False
    
    def return_to_first_tab(self):
        self.driver.close()
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_name(self):
        name = self.driver.find_elements_by_class_name("Xl2sXb-r4nke")
        url = self.driver.current_url
        urlarray = url.split("/")
        return name[0].get_attribute('textContent') + "_" + urlarray[-1]

    def is_page_exist(self):
        try:
            name = self.driver.find_elements_by_class_name("Xl2sXb-r4nke")
            url = self.driver.current_url
            urlarray = url.split("/")
            realName = name[0].get_attribute('textContent') + "_" + urlarray[-1]
            return True
        except IndexError:
            return False
        return False

    def quit(self):
        self.driver.quit()