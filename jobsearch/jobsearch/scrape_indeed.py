import requests
from bs4 import BeautifulSoup
import os
import logging
from pymongo import MongoClient

os.environ.setdefault("C:\\Users\\abhig\\jobsearch", "jobsearch.settings")

import django
django.setup()

from jobs.models import JobListing

url = "https://in.indeed.com/jobs?q=python+developer&l=&from=searchOnHP&vjk=b4a267cd5757793d"

logging.basicConfig(filename='scrape_indeed.log', level=logging.INFO)

mongo_client = MongoClient('localhost', 27017)  	
mongo_db = mongo_client['Python_developer']  
collection = mongo_db['job_listings']

try:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')

        for listing in job_listings:
            title = listing.find('a', class_='jobtitle').text.strip()
            company = listing.find('span', class_='company').text.strip()
            location = listing.find('div', class_='recJobLoc')['data-rc-loc']
            salary = listing.find('span', class_='salaryText')
            if salary:
                salary = salary.text.strip()
            else:
                salary = None
            description = listing.find('div', class_='summary').text.strip()

            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
            }
            collection.insert_one(job_data)

        logging.info(f'Scraped and inserted {len(job_listings)} job listings into MongoDB.')
    else:
        logging.error('Failed to retrieve job listings from Indeed.com')
finally:
    mongo_client.close()
