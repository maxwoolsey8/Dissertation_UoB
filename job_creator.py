import random
from datetime import datetime, timedelta
import pandas as pd

technology_and_data_jobs = [
    'Software Developer', 'Data Analyst', 'Systems Analyst', 'Web Developer', 
    'Data Scientist', 'UI Designer', 'IT Support Specialist', 'Technical Support Engineer'
]

finance_and_business_jobs = [
    'Financial Analyst', 'Business Analyst', 'Investment Banking Analyst', 
    'Operations Manager', 'Supply Chain Analyst', 'Corporate Finance Analyst', 
    'Risk Analyst', 'Audit Associate', 'Business Development Executive'
]

marketing_and_creative_jobs = [
    'Marketing Executive', 'Digital Marketing Specialist', 'Sales Executive', 
    'Social Media Manager', 'Content Writer', 'Graphic Designer', 
    'Product Designer', 'Public Relations Officer', 'Event Coordinator'
]

engineering_and_science_jobs = [
    'Engineering Graduate', 'Civil Engineer', 'Mechanical Engineer', 
    'Electrical Engineer', 'Biomedical Scientist', 'Pharmaceutical Sales Representative', 
    'Research Scientist', 'Quantity Surveyor', 'Health and Safety Advisor'
]

administrative_jobs = [
    'Human Resources Assistant', 'Recruitment Consultant', 'Legal Assistant', 
    'Management Consultant', 'Customer Service Manager', 'Teacher', 'Nurse', 
    'Logistics Coordinator', 'Insurance Underwriter'
]

all_jobs_together = (technology_and_data_jobs + finance_and_business_jobs + marketing_and_creative_jobs + engineering_and_science_jobs + administrative_jobs)

technology_and_data_skills = [
    'Python Programming', 'JavaScript', 'SQL', 'Data Visualisation', 
    'Machine Learning', 'Cloud Computing', 'Big Data Technologies', 
    'Data Warehousing', 'APIs', 'Version Control', 'Django', 
    'Docker', 'ETL', 'Data Analysis', 'Problem Solving'
]

finance_and_business_skills = [
    'Financial Modeling', 'Excel', 'Quantitative Analysis', 
    'Financial Reporting', 'Risk Assessment', 'Market Research', 
    'Project Management', 'Financial Forecasting', 'Budgeting', 
    'Regulatory Compliance', 'Bookkeeping', 'Financial Analysis', 
    'Business Strategy', 'Reporting', 'Analytical Skills'
]

marketing_and_creative_skills = [
    'SEO Optimisation', 'Google Analytics', 'Content Management Systems', 
    'Adobe Creative Suite', 'Social Media Marketing', 'PPC Advertising', 
    'Email Marketing', 'Market Research', 'Brand Strategy', 'Graphic Design', 
    'Content Creation', 'Campaign Management', 'Digital Marketing', 
    'Analytics', 'User Research'
]

engineering_and_science_skills = [
    'CAD Software', 'Finite Element Analysis', 'Lab Techniques', 
    'Project Management Software', 'Statistical Analysis', 'Regulatory Compliance', 
    'Technical Writing', 'Data Analysis', 'Simulation Software', 'Research Methodology',
    'Mechanical Design', 'Prototyping', 'Product Development', 
    'Engineering Design', 'Problem Solving'
]

administrative_skills = [
    'HR Information Systems', 'Talent Acquisition', 'Employee Relations', 
    'Payroll Management', 'Performance Appraisal Systems', 'Compliance Management', 
    'Organisational Skills', 'Conflict Resolution', 'Onboarding', 
    'Training and Development', 'Recruitment', 'Client Management', 
    'Office Management', 'Communication', 'Leadership'
]

job_to_skills = {
    'technology_and_data_jobs': technology_and_data_skills,
    'finance_and_business_jobs': finance_and_business_skills,
    'marketing_and_creative_jobs': marketing_and_creative_skills,
    'engineering_and_science_jobs': engineering_and_science_skills,
    'human_resources_and_administrative_jobs': administrative_skills
}

def job_skills(title):
    if title in technology_and_data_jobs:
        return random.sample(technology_and_data_skills, 3)
    elif title in finance_and_business_jobs:
        return random.sample(finance_and_business_skills, 3)
    elif title in marketing_and_creative_jobs:
        return random.sample(marketing_and_creative_skills, 3)
    elif title in engineering_and_science_jobs:
        return random.sample(engineering_and_science_skills, 3)
    elif title in administrative_jobs:
        return random.sample(administrative_skills, 3)
    return []

job_locations = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool', 'Bristol', 'Sheffield', 'Newcastle', 'Nottingham', 'Cambridge']

job_summaries = {
    "Software Developer": "Develop and maintain software applications and systems, and write clean code in languages such as Python and JavaScript.",
    "Data Analyst": "Analyse and interpret complex data sets to help organisations make informed decisions, utilising tools like SQL and other data sorting software.",
    "Systems Analyst": "Evaluate and improve computer systems to enhance efficiency.",
    "Web Developer": "Build and maintain websites and web applications. You will have to be proficient in HTML, CSS and JavaScript.",
    "Data Scientist": "Apply statistical analysis and machine learning techniques to interpret data and provide actionable insights. Experience with tools such as Python and R is preferred.",
    "UI Designer": "Create user-friendly interfaces and enhance user experience for websites and applications, expertise in design tools like Sketch and Adobe XD is necessaary.",
    "IT Support Specialist": "You will have to provide technical support and troubleshooting for hardware and software issues.",
    "Technical Support Engineer": "You should be able to diagnose and resolve technical issues, providing support to clients and customers.",
    "Financial Analyst": "Analyse financial data and create reports to support business decisions, and then develop financial models and forecasts to assess performance.",
    "Business Analyst": "Identify business needs and develop solutions to enhance processes and operations.",
    "Investment Banking Analyst": "You will assist in the evaluation of investment opportunities and financial transactions. You must also be proficient in conducting market research and financial modeling.",
    "Operations Manager": "Oversee daily operations of the organisation, ensuring efficiency and effectiveness to streamline processes.",
    "Supply Chain Analyst": "You will be asked to analyse and optimise supply chain processes to improve efficiency and reduce costs.",
    "Corporate Finance Analyst": "Support corporate finance activities including budgeting, forecasting, and financial planning.",
    "Risk Analyst": "You must be able to identify and assess potential risks to the organisation.",
    "Audit Associate": "Perform internal audits to ensure compliance with regulations and standards. You will also be able to review financial records and assess internal controls.",
    "Business Development Executive": "Identify and develop new business opportunities to drive growth, and build relationships with clients and partners to expand the business.",
    "Marketing Executive": "Plan and execute marketing campaigns to promote products and services, through analysing market trends and tracking campaign performance.",
    "Digital Marketing Specialist": "Implement digital marketing strategies, including SEO, PPC, and social media.",
    "Sales Executive": "Must be able to develop and execute sales strategies to meet business objectives.",
    "Social Media Manager": "Manage social media accounts and create content to engage with followers, and also analyse social media metrics and develop strategies for growth.",
    "Content Writer": "Create engaging written content for various platforms, including blogs, websites, and various social media platforms.",
    "Graphic Designer": "Design visual assets for print and digital media. You must be proficient in design software such as Adobe Photoshop and Illustrator.",
    "Product Designer": "Design and develop new products, from concept to production. You will work on product specifications and testing.",
    "Public Relations Officer": "Manage public relations activities to promote and protect the organisation's image with varying strategies.",
    "Event Coordinator": "Plan and execute events, ensuring all aspects run smoothly, managing event logistics and budgets.",
    "Engineering Graduate": "Assist in engineering projects and gain hands-on experience by supporting senior engineers in design and testing.",
    "Civil Engineer": "Design and oversee construction projects such as roads and bridges, ensuring compliance with safety regulations and environmental standards.",
    "Mechanical Engineer": "Design machinery and equipment, and troubleshoot engineering issues.",
    "Electrical Engineer": "Design and implement electrical systems and components for working on projects involving power generation and electronics.",
    "Biomedical Scientist": "Conduct research and analyse biological samples to support medical and clinical studies.",
    "Pharmaceutical Sales Representative": "Promote and sell pharmaceutical products to healthcare professionals by providing product information and building relationships with clients.",
    "Research Scientist": "Conduct experiments and analyse data to advance scientific knowledge. You must be specialised in areas such as biology or physics.",
    "Quantity Surveyor": "Manage costs and budgets for construction projects. Conduct cost estimation, financial reporting, and contract administration.",
    "Health and Safety Advisor": "Develop and implement health and safety policies; conducting risk assessments and ensuring compliance with safety regulations.",
    "Human Resources Assistant": "Support HR functions including recruitment, employee relations, and record-keeping.",
    "Recruitment Consultant": "Manage the recruitment process to attract and hire top talent. Develop job descriptions, screen candidates, and conduct interviews.",
    "Legal Assistant": "Provide administrative support to legal teams and assist with legal research and document preparation",
    "Management Consultant": "Analyse organisational practices and develop strategies to improve efficiency and effectiveness; then be able to provide recommendations for business improvements.",
    "Customer Service Manager": "Oversee customer service operations to ensure high customer satisfaction. Manage customer service teams and resolve escalated issues.",
    "Teacher": "Plan and deliver educational lessons to students. You will develop lesson plans, assess student performance, and provide effective feedback.",
    "Nurse": "Provide medical care and support to patients. Duties include conducting medical assessments, administering treatments, and collaborating with healthcare professionals.",
    "Logistics Coordinator": "Manage logistics and supply chain operations through coordinating shipments and tracking inventory.",
    "Insurance Underwriter": "Evaluate insurance applications and determine coverage terms. Assess risk factors and decide on policy approval and pricing."
}

def random_salary():
    salary = random.randint(20000, 35000)
    salary_rounded = round(salary / 1000) * 1000
    return f"£{salary_rounded}"

def random_start_date():
    start_date = datetime(2024, 9, 1)
    end_date = datetime(2025, 9, 30)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_start_date = start_date + timedelta(days=random_days)
    return random_start_date.strftime("%Y-%m-%d")

def job_category(job_title):
    if job_title in technology_and_data_jobs:
        return "Technology and Data"
    elif job_title in finance_and_business_jobs:
        return "Finance and Business"
    elif job_title in marketing_and_creative_jobs:
        return "Marketing and Creative"
    elif job_title in engineering_and_science_jobs:
        return "Engineering and Science"
    elif job_title in administrative_jobs:
        return "Administrative"
    return "Unknown"

def generate_job_listing(job_title):
    return {
        "JobTitle": job_title,
        "JobCategory": job_category(job_title),
        "Salary": random_salary(),
        "Location": random.choice(job_locations),
        "SkillsRequired": job_skills(job_title),
        # "StartDate": random_start_date(), #only needed for 2024 data
        "JobSummary": job_summaries.get(job_title, "No summary available")
    }

jobData = []
for _ in range(1000):
    job_title = random.choice(all_jobs_together)
    jobData.append(generate_job_listing(job_title))
df = pd.DataFrame(jobData)


# df.to_csv('job_data_2019.csv', index=False)
# df.to_csv('job_data_2020.csv', index=False)
# df.to_csv('job_data_2021.csv', index=False)
# df.to_csv('job_data_2022.csv', index=False)
# df.to_csv('job_data_2023.csv', index=False)

print(f"Number of jobs generated: {len(jobData)}")

