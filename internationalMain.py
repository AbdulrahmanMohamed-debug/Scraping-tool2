import csv
from datetime import date
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# set up the webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class Jobs():

    def file_name(self):
        x = date.today()
        return ("__Title removed___jobs " + str(x) + ".csv")
      
          

    #Find the last element on the page by scrolling down
    #have to wait for a second as site loads more jobs
    def scroll(self):    
        #Find the last element on the page
        #driver.execute_script("window.scrollBy(0, documnet.body.scrollHeight);")
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    


    #gets the headings of a job posting from new window
    def heads(self):

        titles = {
            'jobTitle'    : "Title_Unavailable",
            'jobCategory' : "Category_Unavailable",
            'jobLocation' : "Location_Unavailable",
            'jobReqId'    : "Req_ID_Unavailable",
            'jobType'     : "Job_Type_Unavailable"
        }

        innerElements = []

        try:
            titles['jobTitle'] = driver.find_element(By.XPATH, "//h1[@class='tds-text--h1-alt']").text
            innerElements = driver.find_elements(By.XPATH, "//td")
        except Exception as e:
            print(str(e) + "\n")
            print("problem with inner elements or h1 title")

        #the default is the string "...unavailable" above if element is not available    
        try:
            titles['jobCategory'] = innerElements[0].text.replace("\n","")
        except:
            pass
        try:
            titles['jobLocation'] = innerElements[1].text.replace("\n","")
        except:
            pass
        try:
            titles['jobReqId']    = innerElements[2].text.replace("\n","")
        except:
            pass
        try:
             titles['jobType']     = innerElements[3].text.replace("\n","")
        except:
            pass
        
        return titles
    
     #gets descriptions of job posting from new window
    def descriptions(self):

        desc = {
            'whatExpect' : "Expectation is not availvble",
            'whatDo'    : "Description not available",
            'whatBring' :  "What you will bring"
        }
        ExpectPath  = driver.find_elements(By.XPATH, ("//div[contains(@class,'style_descriptionItem')]"))
        # To find expect & do there are two divs with attribute //div[contains(@class,'style_descriptionItem')]
        try:
           desc['whatExpect']  = ExpectPath[0].text.replace("\n","") 
        except:
            pass

        try:
          desc['whatDo']      = ExpectPath[1].text.replace("\n","")  
        except:
            pass
        
        
        #this div had no class name but it was the last div under the //div[contains(@class,'style_description_')]
        try:
            desc['whatBring']   = driver.find_elements(By.XPATH, ("//div[contains(@class,'style_description_')]/div"))[-1].text.replace("\n","")
        except:
            pass
        
        return desc
    


    def get_Job_Details(self, job):

        posting = job.get_attribute("href")

        #open a new window
        driver.execute_script("window.open('');")
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        driver.get(posting)
        headings = self.heads()
        description = self.descriptions()

        #defining a new dictionary that merges both dictionaries: headings & descriptions
        temp = headings
        headings.update(description)
        myDictionary = headings
        headings  = temp
        myDictionary['url_link'] = str(posting)

        return myDictionary


    #main method
    def main(self):
        
        driver.implicitly_wait(2)
        
        main_link = "https://www.__Title removed__.com/careers/search/"
        country = ["HR", "GR", "TW", "DE", "US", "MX", "CN"]
        # Germany, US, Mexico, China Mainland, Taiwan
        
        file_name = self.file_name()
        rowNames = ['jobReqId','jobTitle','jobCategory','jobLocation','jobType','whatExpect','whatDo','whatBring','url_link']
        with open(file_name, mode='w+', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rowNames)   
            writer.writeheader()
            
            #repeats for each of the countries in 'country' list
            for i in range(len(country)):
                driver.get(main_link + '?site='+ country[i])
                driver.maximize_window()
                self.scroll()

                #path for all the job postings on the landing page
                firstPath = "//td/a[@class='tds-link']"
                elements = driver.find_elements(By.XPATH, firstPath) #creates a list of job postings on the landing page 

                #gets details for every job
                for job in elements:
                    myDict = self.get_Job_Details(job)        
                    writer.writerow(myDict)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        driver.quit()


    
    
if __name__=="__main__": 
    Jobs().main()
        

         


        

    
