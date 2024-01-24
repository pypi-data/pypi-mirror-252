from drivers.setting_driver import SetupDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import logging

## defining the functions to get the date from the websites we are intersted in 
class scraping_titles:

    
    @staticmethod
    def parse_towards_ds_date(date_element): #this is used to parse dates for both blog sites towards data science and levelup
        date_string = date_element.get_attribute('datetime')[:-1]  # Adjust attribute as needed
        return datetime.fromisoformat(date_string)
    
    @staticmethod
    def parse_data_science_central_date(date_element): # parse dates for the data science central 
        date_string = date_element.get_attribute('content')  # Adjust attribute as needed
        return datetime.strptime(date_string, "%Y-%m-%d")
    
    @staticmethod
    def scrape_articles(driver_path, url, xpath_title, xpath_subtitle,xpath_date, parse_date, days_back=30, scroll_pause_time=30):
        path_obj = SetupDriver(driver_path=driver_path)
        driver = path_obj.setup_driver()
        data = []
        end_date = datetime.now() - timedelta(days=days_back)
        exit_loop = False
        
        try:
            driver.get(url)
            html = driver.find_element(By.TAG_NAME, "html")
            while not exit_loop:
                titles = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_title)))
                subtitles = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_subtitle)))
                date_elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_date)))

                for title, subtitle,date_element in zip(titles, subtitles,date_elements):
                    article_date = parse_date(date_element)  # Pass the entire element to the parse_date function
                    print(article_date)

                    if article_date < end_date:
                        exit_loop = True
                        break
                    if not any(d['title'] == title.text for d in data):
                    
                        print(f"Title: {title.text}, Date: {article_date}")
                        data.append({"title": title.text, "date": article_date,'SubTitle': subtitle.text if subtitle.text else None})
                if not exit_loop:
                    html.send_keys(Keys.PAGE_DOWN)
                    time.sleep(scroll_pause_time)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            driver.quit()
        return data

