from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import unittest, time, os, re, csv,sys

waittime=5
desktop_dir=os.path.join(os.path.expanduser("~"),"Desktop")
csv_filename='csv file'
finished_csv_file='csv file that you save to'

mirna_file_path = desktop_dir+'\\mirnaName.txt'
gene_file_path = desktop_dir+'\\geneName.txt'
csv_file_path = desktop_dir+'\\'+csv_filename
finished_csv_file_path=desktop_dir+'\\'+ '\\'+ finished_csv_file

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--disable-gpu')  
        chrome_options.add_argument('--window-size=1920x1080') 

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        
        with open(csv_file_path, mode='r', newline='') as csv_read: 
            reader = list(csv.reader(csv_read))
            totalqueries=len(reader)-1
            finishedqueries=0

            if totalqueries>0: 

                with open(finished_csv_file_path, mode='a', newline='') as csv_write:
                    writer = csv.writer(csv_write)
                    if os.path.getsize(finished_csv_file_path)==0:
                        writer.writerow(reader[0])

                    driver = self.driver
                    self.driver.implicitly_wait(10)
                    driver.get("https://dianalab.e-ce.uth.gr/microt_webserver/#/interactions")

                    max_retries=3
                    retry_count=0
                    while retry_count < max_retries:
                        try:
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//mat-select[@id='mat-select-0']/div/div[2]")))
                            driver.execute_script("arguments[0].click();",element) # species expansion arrow
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//mat-option[@id='mat-option-2']/span")))
                            driver.execute_script("arguments[0].click();",element) # species
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//button[@id='mat-button-toggle-2-button']/span")))
                            driver.execute_script("arguments[0].click();",element) #miRNA resource miRBasev22.1   
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//button[@id='advanced_filtersButton']/span/i")))
                            driver.execute_script("arguments[0].click();",element)  #open advance filters options
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//mat-select[@id='mat-select-4']/div/div[2]/div")))
                            driver.execute_script("arguments[0].click();",element)   # input box to show options including CDS
                            element=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//mat-option[@id='mat-option-41']/span")))
                            driver.execute_script("arguments[0].click();",element)   #select CDS    
                            break
                        except Exception as e:
                            retry_count+=1
                            print(f"An error occurred: {e}, retry initial set up #{retry_count}")
                    else:
                        print("warning! having problem picking species, miRNA resource, CDS, or opening filter option!")                      
                        sys.exit()


                    for row in reader[1:]:
                        if row[9].strip().upper() == "YES":
                            totalqueries-=1
                            continue     
                        with open(mirna_file_path, 'w') as mirna_write:
                            mirna_write.write(row[0]+'-3p' + '\n')
                            mirna_write.write(row[0]+'-5p' + '\n')
                        
                        with open(gene_file_path, 'w') as gene_write:
                            gene_write.write(row[3] + '\n')


                        max_retries=2
                        retry_count=0
                        while retry_count < max_retries:
                            try:
                                WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))).send_keys(mirna_file_path) #miRNA name 
                                WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//input[2]"))).send_keys(gene_file_path)  #Gene name/ID
        
                                elementSm=WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//button[@id='submitButton']/span")))
                                driver.execute_script("arguments[0].click();",elementSm)   #submit button
                                time.sleep(2)
                            
                
                                try:
                                    WebDriverWait(driver, waittime).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/app-root/app-interactions/app-interactions-presentation/div/b")))
                                    element=driver.find_element(By.XPATH, "/html/body/app-root/app-interactions/app-interactions-presentation/div/b")
                                    print(row[3],": ",element.get_attribute('textContent'))
                                    row[4]='NA'
                                    writer.writerow(row)
                                except (NoSuchElementException,TimeoutException): #results found
                                    results=WebDriverWait(driver, waittime).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/app-root/app-interactions/app-interactions-presentation/div/accordion/accordion-group")))
                                    print(row[3],": Detected %d element(s)"%(len(results)))
                                    for xxx in results:
                                        elementL1=WebDriverWait(xxx, waittime).until(EC.presence_of_element_located((By.XPATH, "./div/div[1]/div/div/div/div[9]/i")))
                                        driver.execute_script("arguments[0].click();",elementL1) 
                                        GeneID=WebDriverWait(xxx, waittime).until(EC.presence_of_element_located((By.XPATH, "./div/div[1]/div/div/div/div[1]/p/span[1]/a"))).get_attribute('textContent') # ex: ENSG00000175634
                                        row[7]=GeneID
                    elementsL2=xxx.find_elements("xpath","./div/div[2]/div/div/div[position()>1]") 
                                        for YYY in elementsL2:
                                            Transcript=WebDriverWait(YYY, waittime).until(EC.presence_of_element_located((By.XPATH, "./div[2]/p"))).get_attribute('textContent') # ex: ENST000
                                            row[6]=Transcript
                                            Conservation=WebDriverWait(YYY, waittime).until(EC.presence_of_element_located((By.XPATH, "./div[6]/p"))).get_attribute('textContent') # ---> 1
                                            row[2]=Conservation
                                            GenomePosition=WebDriverWait(YYY, waittime).until(EC.presence_of_element_located((By.XPATH, "./div[5]/p"))).get_attribute('textContent') # ---> 1      
                                            row[5]=GenomePosition
                                        
                                            element2=YYY.find_element("xpath","./div[7]/p/button")
                                            driver.execute_script("arguments[0].click();",element2) 

                                            BindingArea=WebDriverWait(YYY, waittime).until(EC.presence_of_element_located((By.XPATH, './div[7]/p/popover-container/div[2]/div/code'))).get_attribute('textContent') # ---> Binding Area code
                                            lines_BA=BindingArea.split('\n')
                                        
                                            trimmed_string=lines_BA[1].strip() 
                                       
                                            processed_string = re.sub(r'[^UACG\s]', '', trimmed_string)
                                            processed_string = re.sub(r'\s+', ' ', processed_string)
                                            row[8]=processed_string

                                            if len(lines_BA)>=2:
                                                substrings=lines_BA[1].split()
                                                filtered_substrings = [''.join([char for char in s if char in "UACG"]) for s in substrings]
                                                bindingSquence = max(filtered_substrings, key=len)
                                            row[4]=bindingSquence
                                            driver.execute_script("arguments[0].click();",element2) 
                                            writer.writerow(row)
                                        driver.execute_script("arguments[0].click();",elementL1) 
                                row[9]='YES'
                                finishedqueries+=1
                                print("Completed %5d queries of total of %5d - %5.1f percent completed!" % (finishedqueries,totalqueries,finishedqueries/totalqueries*100))
                                break
                            except Exception as e:
                                retry_count+=1
                                print(f"An error occurred: {e}, retry {row[3]} #{retry_count}")
                            else:
                                print("Warning: the query of {} - {} ended with timeout error!".format(row[0],row[1]))


        with open(csv_filename, mode='w', newline='') as infile:
            writer = csv.writer(infile)
            writer.writerows(reader)
            

       
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
