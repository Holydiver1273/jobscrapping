import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsearch.settings")  # Set your Django settings module

import django
django.setup()

from jobs.models import JobListing

url = "https://in.indeed.com/jobs?q=python+developer"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
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

        # Insert the scraped data into the MongoDB database using Django models
        JobListing.objects.create(title=title, company=company, location=location, salary=salary, description=description)

    print(f'Scraped and inserted {len(job_listings)} job listings into the database.')
else:
    print('Failed to retrieve job listings from Indeed.com')