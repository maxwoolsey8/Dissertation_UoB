import csv
import json

def csv_to_json(csv_file_path):
    json_data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            job_title = row[0]
            job_category = row[1]
            salary = row[2]
            location = row[3]
            skills_required_str = row[4]
            start_date = row[5]
            job_summary = row[6]
            
            try:
                if skills_required_str.strip():
                    skills_required = json.loads(skills_required_str.replace("'", '"'))
                else:
                    skills_required = []
            except json.JSONDecodeError:
                print(f"Error decoding skills for job: {job_title}. Setting skills to an empty list.")
                skills_required = []
            
            job_json = {
                "JobTitle": job_title,
                "JobCategory": job_category,
                "Salary": salary,
                "Location": location,
                "SkillsRequired": skills_required,
                "StartDate": start_date,
                "JobSummary": job_summary
            }
            json_data.append(job_json)
    return json_data

csv_file = 'scraped_job_data_2024.csv'  
json_output = csv_to_json(csv_file)

with open('2024_website_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_output, json_file, indent=4, ensure_ascii=False)