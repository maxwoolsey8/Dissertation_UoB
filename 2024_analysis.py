import pandas as pd

def read_job_data():
    df_2019 = pd.read_csv('job_data_2019.csv') 
    df_2019['Year'] = 2019 
    df_2020 = pd.read_csv('job_data_2020.csv') 
    df_2020['Year'] = 2020 
    df_2021 = pd.read_csv('job_data_2021.csv') 
    df_2021['Year'] = 2021  
    df_2022 = pd.read_csv('job_data_2022.csv')  
    df_2022['Year'] = 2022  
    df_2023 = pd.read_csv('job_data_2023.csv') 
    df_2023['Year'] = 2023  
    df_2024 = pd.read_csv('scraped_job_data_2024.csv')  
    df_2024['Year'] = 2024  
    return pd.concat([df_2019, df_2020, df_2021, df_2022, df_2023, df_2024])

def job_listings_by_category(df):
    job_counts = df.groupby(['JobCategory', 'Year']).size().unstack(fill_value=0)
    return job_counts

def print_job_listings_by_category():
    df = read_job_data()

    job_counts = job_listings_by_category(df)
    print("Job Listings by Category from 2019 to 2024:")
    for category in job_counts.index:
        listings = job_counts.loc[category]
        output = f"{category}: "
        output += ', '.join([f"{year} = {count}" for year, count in listings.items()])
        print(output)

if __name__ == "__main__":
    print_job_listings_by_category()




