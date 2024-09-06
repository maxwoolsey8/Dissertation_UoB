import requests
from bs4 import BeautifulSoup
import re
import json
import csv

url = 'http://127.0.0.1:5500/listing_website_2024.html'  #url of my website
response = requests.get(url)
webpage_content = response.text
soup = BeautifulSoup(webpage_content, 'html.parser')

script_tag = None 
for script in soup.find_all('script'): #find script tag with job data
    if script.string and 'const jobData =' in script.string:
        script_tag = script 
        break 

if script_tag == script:
    script_content = script_tag.string.strip()
    json_data = re.search(r'const jobData = (\[.*?\]);', script_content, re.DOTALL) #use regex to find
    
    if json_data:
        json_data_str = json_data.group(1)
        job_data = json.loads(json_data_str)
        with open('scraped_job_data_2024.csv', mode='w', newline='') as file: #save to csv file
            writer = csv.DictWriter(file, fieldnames=job_data[0].keys())
            writer.writeheader()
            for job in job_data:
                writer.writerow(job)
        print("Data has been saved to scraped_job_data_2024.csv")