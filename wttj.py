from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import time
from time import sleep
import pandas as pd
from random import randint


website = """
########################################################
#          WEBSITE: WELCOMETOTHEJUNGLE.COM/FR          #
########################################################
"""
print(website)
start_time = datetime.now()
print('Crawl starting time : {}' .format(start_time.time()))
print()
job_list = ["data analyst", "data scientist", "business analyst"]
wttj_data = []

for job in job_list:

    opts = webdriver.FirefoxOptions()
    opts.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
    driver = webdriver.Firefox(profile, executable_path="venv/bin/geckodriver", options=opts) 

    driver.get(
        "https://www.welcometothejungle.com/fr/jobs?query=" + job + "%20&page=1&configure%5Bfilters%5D=website.reference%3Awttj_fr&configure%5BhitsPerPage%5D=30&aroundLatLng=48.8546%2C2.34771&aroundQuery=Paris%2C%20France&aroundRadius=20000&aroundPrecision=20000&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance"
    )
    sleep(randint(7,10))
    print('Collecting data for "{}"...' .format(job))
    # First, get the number of jobs available
    job_number = driver.find_element_by_xpath("//h2/span").text
    # Calculating number of pages to be crawled (number of jobs available - number of jobs per page (here, 30))
    job_number = job_number.split(" ", 1)
    job_number = int(job_number[0])
    print("- Number of open positions : {}" .format(job_number))
    exact_page_nb = job_number / 30
    print("- Exact number of pages to be crawled : {}" .format(exact_page_nb))
    min_page_nb = job_number // 30
    print("- Minimum number of pages to be crawled : {}" .format(min_page_nb))

    if exact_page_nb > min_page_nb:
        page_nb = min_page_nb + 2
    elif exact_page_nb == min_page_nb:
        page_nb = min_page_nb + 1

    pages = [str(i) for i in range(1, page_nb)]

    for page in pages:
        driver.get(
            "https://www.welcometothejungle.com/fr/jobs?query=" + job + "%20&page=" + page + "&configure%5Bfilters%5D=website.reference%3Awttj_fr&configure%5BhitsPerPage%5D=30&aroundLatLng=48.8546%2C2.34771&aroundQuery=Paris%2C%20France&aroundRadius=20000&aroundPrecision=20000&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance"
        )

        sleep(randint(5, 12))

        # Locating job container
        all_articles = driver.find_elements_by_xpath("//article[@class='sc-1kkiv1h-12 sc-1flb27e-6 jFwpgJ']")

        for article in all_articles:
            job_link = article.find_element_by_css_selector('a').get_attribute('href')
            wttj_data.append(article.text)
            wttj_data.append(job_link)
            wttj_data.append('welcome to the jungle')
            wttj_data.append(datetime.now())

    print('Crawling status for "{}" : Done' .format(job))
    print()

    driver.quit()

print('Crawling time : {}' .format(datetime.now() - start_time))
print('Dataframe successfuly created and exported')

# Dataframe creation
df = pd.DataFrame(wttj_data,columns=['data'])

#----------------------------------------------------------------------

# Saving .csv file within the "new_datasets" directory
csv_file = 'welcome_to_the_jungle_data_{}.csv' .format(datetime.now())
df.to_csv(r'datasets/' + csv_file) 

