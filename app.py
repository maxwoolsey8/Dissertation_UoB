# future - ai prompts / ai immediate interpretation 
# future - more data so better analysis - more data sources 
# future can finetune filters more - ie can see finance jobs
# future - tough to find dept heads so used students - could also use other unis
# future - add workplace reccomendations
# future - student feedback
# future - keyword function
# future - analyse other unis courses to show popularity
# studies show suggestions help
# studies show interaction helps
# filtering as well
# add skills to reccomendation
# top change in that category
# however the top 3 skills are



import streamlit as st
from collections import Counter
import ast
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(
    page_title="Job Listings Dashboard", 
    layout="centered",
    initial_sidebar_state="expanded" 
)
st.sidebar.markdown(
    """
    **Disclaimer:** All of the data on this website has been randomly generated or scraped from randomly generated job listings. Thus, any trends or listings described are purely fictional and do not reflect real-world data.
    """
)


def safe_literal(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

def load_job_data():
    column_names = ['Job Title', 'Job Category', 'Salary', 'Location', 'Skills Required', 'Start Date', 'Job Summary']
    df_2024 = pd.read_csv('scraped_job_data_2024.csv', header=None, names=column_names)
    df_2023 = pd.read_csv('job_data_2023.csv', header=None, names=column_names)
    df_2022 = pd.read_csv('job_data_2022.csv', header=None, names=column_names)
    df_2021 = pd.read_csv('job_data_2021.csv', header=None, names=column_names)
    df_2020 = pd.read_csv('job_data_2020.csv', header=None, names=column_names)
    df_2019 = pd.read_csv('job_data_2019.csv', header=None, names=column_names)
    return df_2024, df_2023, df_2022, df_2021, df_2020, df_2019

def salary_changer(salary):
    if isinstance(salary, str):
        salary = salary.replace('£', '').replace(',', '').strip()
        try:
            return float(salary)
        except ValueError:
            return None
    return salary

def process_data(*dfs):
    for df in dfs:
        df['Skills Required'] = df['Skills Required'].apply(safe_literal)

#group data by categroy
def group_data_by_job_category(*dfs):
    grouped_data = []
    for df in dfs:
        grouped_data.append(df.groupby('Job Category').size())
    return grouped_data

df_2024, df_2023, df_2022, df_2021, df_2020, df_2019 = load_job_data()
process_data(df_2024, df_2023, df_2022, df_2021, df_2020, df_2019)
grouped_2024, grouped_2023, grouped_2022, grouped_2021, grouped_2020, grouped_2019 = group_data_by_job_category(df_2024, df_2023, df_2022, df_2021, df_2020, df_2019)


#get job counts by title over years
def get_jobsby_title(job_title, dfs, years):
    job_counts = []
    for df in dfs:
        count = df[df['Job Title'].str.contains(job_title, case=False, na=False)].shape[0]
        job_counts.append(count)
    return job_counts

#works out change of job frequencies for each cat
job_category_changes = pd.DataFrame({
    'Jobs 2019': grouped_2019, 'Jobs 2020': grouped_2020,'Jobs 2021': grouped_2021,'Jobs 2022': grouped_2022,'Jobs 2023': grouped_2023,'Jobs 2024': grouped_2024,}).fillna(0)
job_category_changes['Change'] = job_category_changes['Jobs 2024'] - job_category_changes['Jobs 2019']
job_category_changes['Percent Change'] = (job_category_changes['Change'] / job_category_changes['Jobs 2019']) * 100


def job_analysis_page():
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    dfs = [df_2019, df_2020, df_2021, df_2022, df_2023, df_2024]
    df_2024['Salary'] = df_2024['Salary'].apply(salary_changer)
    st.title("Job Analysis Page")
    st.write("### Analyse Job Listings")
    job_title_input = st.text_input("Enter a Job Title to Analyse using Data from 2019 to 2024", placeholder="Try search for Software Developer")

    if job_title_input:
        recognised = any(
            job_title_input.lower() in df['Job Title'].str.lower().values
            for df in dfs
        )

        if not recognised:
            st.error("Job title not recognised. Please search for a recognised job title like one of the jobs listed below.")
            
            # Display trending jobs as suggestions
            st.write("### Trending Jobs to Analyse in 2024")
            trending_jobs = df_2024['Job Title'].value_counts().head(5)
            trending_jobs_with_categories = []
            for job_title in trending_jobs.index:
                category = df_2024[df_2024['Job Title'] == job_title]['Job Category'].iloc[0]
                listings = trending_jobs[job_title]
                trending_jobs_with_categories.append((job_title, listings, category))
            for job_title, listings, category in trending_jobs_with_categories:
                st.write(f"- **{job_title}**: {listings} listings ({category})")
            return  # Exit the function early since the job title wasn't found

        job_counts = get_jobsby_title(job_title_input, dfs, years)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(years, job_counts, marker='o', linestyle='-', color='blue')
        ax.set_ylabel('Number of Job Listings')
        ax.set_xlabel('Year')
        ax.set_title(f'Number of Job Listings for "{job_title_input}" Over the Years')
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        st.pyplot(fig)
        total_increase = job_counts[-1] - job_counts[0]  # 2024-2019 number

        filtered_jobs = df_2024[df_2024['Job Title'].str.contains(job_title_input, case=False, na=False)]
        if not filtered_jobs.empty:
            category = filtered_jobs['Job Category'].iloc[0]
        else:
            category = "Unknown"

        all_job_titles = df_2024[df_2024['Job Category'] == category]['Job Title'].unique()  # find top increase of job in same cat
        max_increase = -float('inf')
        max_increase_job_title = None

        for job in all_job_titles:
            counts = get_jobsby_title(job, dfs, years)
            increase = counts[-1] - counts[0]
            if increase > max_increase:
                max_increase = increase
                max_increase_job_title = job

        all_skills = [skill for skills_list in filtered_jobs['Skills Required'] for skill in skills_list]
        skill_counts = Counter(all_skills)
        most_common_skills = skill_counts.most_common(3)  # finds top 3 skills
        top_skills_str = ", ".join([skill for skill, _ in most_common_skills])

        # Recommendation messages based on 4 change groups
        if total_increase <= -5:
            recommendation = (
                f"The role of **{job_title_input}** saw a large decrease of {abs(total_increase)} listings from 2019 to 2024. This data suggests a decreasing demand in the sector, with it looking like the trend will continue downwards for job openings.\n "
                f"For those still wishing to pursue a career as a **{job_title_input}**, I recommend prioritising the following skills: **{top_skills_str}**; since these are the most sought-after skills for this role, making them highly suitable for employment.\n"
                f"Due to the decrease in demand for this role, I recommend a different role of **{max_increase_job_title}**, since it saw the greatest job listing increase of **{max_increase}** jobs implying high demand, whilst still being in the same job category as **{job_title_input}** ({category})."
            )
        elif -4 <= total_increase <= 0:
            recommendation = (
                f"The job title **{job_title_input}** saw a change of **{total_increase}** listings from 2019 to 2024, with the data suggesting the sector has stagnated or is slowly decreasing in growth in regards to job openings.\n"
                f"For those pursuing a career as a **{job_title_input}**, I recommend becoming proficient in the following skills: **{top_skills_str}**; since these are the most sought-after skills for this role, making them highly suitable for employment.\n"
                f"Due to the decrease in demand for this role, I recommend a different role of **{max_increase_job_title}**, since it saw the greatest job listing increase of **{max_increase}** jobs implying high demand, whilst still being in the same job category as **{job_title_input}** ({category})."
            )
        elif 1 <= total_increase <= 5:
            recommendation = (
                f"The **{job_title_input}** role experienced a rise of **{total_increase}** listings from 2019 to 2024. This suggests moderate growth in the sector, with demand for this role gradually increasing.\n"
                f"For those aiming to build a career as a **{job_title_input}**, I recommend focusing on the following skills: **{top_skills_str}**; these are the most valued skills for this role, enhancing your employability.\n"
                f"While the demand for this role is on the rise, you might also want to explore **{max_increase_job_title}**, which saw a more substantial increase of **{max_increase}** job listings, indicating a stronger growth trend within the same job category as **{job_title_input}** ({category})."
            )
        elif total_increase >= 6:
            recommendation = (
                f"**{job_title_input}** saw a significant increase of **{total_increase}** listings from 2019 to 2024. This indicates a strong and growing demand for this role, making it a highly promising career choice.\n"
                f"If you're considering a career as a **{job_title_input}**, I strongly suggest developing these key skills: **{top_skills_str}**; these are in high demand and will greatly enhance your chances of success in this field.\n"
                f"Given the substantial growth in demand for this role, **{job_title_input}** stands out as one of the best opportunities within the **{category}** category."
            )
        st.write(f"### Job Analysis and Recommendations")
        st.write("- " + recommendation.replace("\n", "\n- "))

        if not filtered_jobs.empty:
            average_salary = filtered_jobs['Salary'].mean()
            min_salary = filtered_jobs['Salary'].min()
            max_salary = filtered_jobs['Salary'].max()
            all_locations = filtered_jobs['Location'].value_counts()

            # Job title analysis
            st.write(f"### {job_title_input} Job Analysis in 2024")
            st.write(f"**Most in Demand Skills for this Role**: " + ", ".join([f"{skill}: {count / len(filtered_jobs) * 100:.2f}%" for skill, count in most_common_skills]))
            st.write(f"**Average Salary**: £{average_salary:,.2f} (Range: £{min_salary:,.2f} - £{max_salary:,.2f})")

            # Salary graph
            salary_fig, salary_ax = plt.subplots(figsize=(10, 6))
            salary_ax.hist(filtered_jobs['Salary'], bins=10, color='green', alpha=0.7)
            salary_ax.set_title('Salary Distribution for ' + job_title_input)
            salary_ax.set_xlabel('Salary (£)')
            salary_ax.set_ylabel('Number of Job Listings')
            salary_ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            st.pyplot(salary_fig)

            # Location graph
            location_fig, location_ax = plt.subplots(figsize=(10, 6))
            all_locations.plot(kind='bar', ax=location_ax, color='orange', alpha=0.7)
            location_ax.set_title(f'Location Distribution for {job_title_input}')
            location_ax.set_xlabel('Location')
            location_ax.set_ylabel('Number of Job Listings')
            location_ax.set_xticklabels(all_locations.index, rotation=45, ha='right')
            location_ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            st.pyplot(location_fig)

        else:
            st.write("No jobs found for the entered job title.")

    else:  # only trending jobs if no input
        st.write("### Trending Jobs to Search for in 2024")
        trending_jobs = df_2024['Job Title'].value_counts().head(5)
        trending_jobs_with_categories = []
        for job_title in trending_jobs.index:
            category = df_2024[df_2024['Job Title'] == job_title]['Job Category'].iloc[0]
            listings = trending_jobs[job_title]
            trending_jobs_with_categories.append((job_title, listings, category))
        for job_title, listings, category in trending_jobs_with_categories:
            st.write(f"- **{job_title}**: {listings} listings ({category})")


def category_analysis_page():
    st.title("Category Analysis Page")
    st.markdown("<br>", unsafe_allow_html=True)  
    st.write("The below chart shows the change in job listings by category from 2019 to 2024.")
    job_category_changes_filtered = job_category_changes[
        ~job_category_changes.index.isin(['JobCategory', 'Job Category'])
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = job_category_changes_filtered['Change'].plot(
        kind='bar', 
        ax=ax, 
        color=['green' if x > 0 else 'red' for x in job_category_changes_filtered['Change']]
    )
    ax.set_ylabel('Change in Number of Job Listings')
    ax.set_xlabel('')#no lable 
    #breaks x axis into two lines
    x_labels = job_category_changes_filtered.index
    new_labels = [label.replace(' ', '\n', 1) for label in x_labels]
    ax.set_xticklabels(new_labels, rotation=0) 
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write(f"### Overview of Job Category Changes from 2019 to 2024")
    #hardcoded overviews
    overviews = {
        "Administrative": """
        **Administrative job listings from 2019 to 2024 reflect significant fluctuations, ultimately leading to an overall decline:**
        - In 2019, the administrative sector began with **193 job listings**, which rose to **225 by 2021**, indicating a robust demand for administrative professionals during this period of growth and organisational expansion.
        - However, this trend reversed as listings fell to **186 in 2024**, suggesting possible restructuring and shifting focus in many organisations. This decline highlights a potential shift in how businesses prioritise administrative roles.
        - The **Insurance Underwriter** role has emerged as the most sought-after role in 2024, reflecting the ongoing need for professionals who can assess and manage risk effectively.
        - **Employee Relations** is a key skill, appearing in **32.00%** of listings, which suggests that organisations are increasingly valuing the ability to build positive workplace relationships.
        """,
        "Engineering and Science": """
        **Engineering and Science job listings from 2019 to 2024 reveal a declining trend, mixed in with recovery phases:**
        - This sector experienced a notable decline from **223 listings in 2019** to **185 in 2020**, indicative of the challenges companies adapted to with emerging technologies and shifting market demands.
        - Nevertheless, job listings fell again slightly, ending at **205 in 2024**, pointing towards a stagnating sector and a growing future preference for automation which may be diminishing demand for conventional roles.
        - The most sought-after role, **Quantity Surveyor**, highlights the necessity for professionals who can navigate project costs effectively.
        - The prominence of **Statistical Analysis** as a key skill in **35.14%** of listings emphasises the reliance on data-driven insights, crucial for informed decision making in engineering projects.
        """,
        "Finance and Business": """
        **Finance and Business job listings from 2019 to 2024 show relatively stable demand with minor variations, reflecting a consistent need for financial expertise:**
        - Beginning with **196 job listings in 2019**, this category saw growth, peaking at **221 in 2020**, before stabilising at **199 in 2024**. This indicates a sustained demand for finance professionals as companies navigate a currently complex economic environment, with an underlying need for adaptability.
        - The role of **Audit Associate** has emerged as the most in-demand position, underscoring the critical need for financial oversight and compliance in today’s regulatory financial sector.
        - The in-demand skill of **Market Research**, mentioned in **39.39%** of listings, reveals the increasing importance of analysing market trends and consumer behavior to enable businesses to make strategic financial decisions.
        """,
        "Marketing and Creative": """
        **Marketing and Creative job listings from 2019 to 2024 indicate significant growth, particularly in recent years, showcasing the sector’s resilience and adaptability:**
        - Starting at **198 listings in 2019**, the sector saw a decline to **177 in 2023**; however it rebounded dramatically to **232 in 2024**. This surge reflects a renewed emphasis on marketing strategies and the ability to connect with consumers.
        - The rise of the **Sales Executive** role highlights the essential nature of effective communication and marketing approaches, showing the sector’s adaptability to changing consumer preferences.
        - The prevalence of **Market Research** skills in **37.84%** of job listings points to the need for consumer insights to guide strategies and enhance brand engagement in a competitive landscape.
        """,
        "Technology and Data": """
        **Technology and Data job listings from 2019 to 2024 reflect a slightly declining landscape, with a trend edging towards specialised roles:**
        - Initially starting with **190 listings in 2019**, the sector faced a decline to **160 in 2021**, indicative of challenges in traditional technology roles amidst rapid technological advancement. However, job listings stabilised to **178 in 2024**, suggesting that the demand is shifting towards specialised skill sets.
        - The **Data Scientist** role stands out as the most in-demand position, therefore highlighting the critical need for professionals who can interpret vast amounts of data to drive business insights.
        - The emphasis on **ETL** (Extract, Transform, Load) skills, cited in **39.29%** of listings, underpins the increasing importance of effective data management processes.
        """
    }
    st.markdown("<br>", unsafe_allow_html=True) 

   
    col1, col2 = st.columns([1, 2])#column for button and graph
    overview_text = ""
    with col1:
        categories = job_category_changes_filtered.index.tolist()
        for category in categories:
                if st.button(f"Show {category} Jobs From 2019 to 2024", key=category):
                    years = ['2019', '2020', '2021', '2022', '2023', '2024']
                    jobs_per_year = [job_category_changes.at[category, f'Jobs {year}'] for year in years]

                    fig_line, ax_line = plt.subplots(figsize=(10, 9))
                    ax_line.plot(years, jobs_per_year, marker='o', linestyle='-', color='blue')
                    ax_line.set_ylabel('Number of Job Listings')
                    ax_line.set_xlabel('Year') 
                    ax_line.set_title(f'Number of Job Listings in {category} From 2019 to 2024')

                    with col2:#for graphs
                        st.pyplot(fig_line)
                    overview_text = overviews[category]

    if overview_text:
        st.markdown(overview_text)
    st.markdown("<br>", unsafe_allow_html=True) 

    st.write("### Most In-Demand Role and Skill for Each Job Category in 2024")
    
    for category in job_category_changes_filtered.index:
        filtered_jobs = df_2024[df_2024['Job Category'] == category]
        
        if not filtered_jobs.empty:#counts of top title
            most_common_job_title = filtered_jobs['Job Title'].value_counts().idxmax()
            most_common_job_count = filtered_jobs['Job Title'].value_counts().max() 
            
            specific_role_jobs = filtered_jobs[filtered_jobs['Job Title'] == most_common_job_title]
            
            all_skills = [skill for skills_list in specific_role_jobs['Skills Required'] for skill in skills_list]
            skill_counts = Counter(all_skills)
            most_common_skill, skill_percentage = skill_counts.most_common(1)[0]
            skill_percentage = (skill_percentage / len(specific_role_jobs)) * 100

            st.write(f"**{category}**:")
            st.write(f"- Role: **{most_common_job_title}** ({most_common_job_count} listings)")
            st.write(f"- Skill: **{most_common_skill}** ({skill_percentage:.2f}% of job listings quote needing this skill)")

def data_search_page():
    st.title("Data Search")
    st.write("This page allows you to filter current job listings by location, job category, salary, and skills required.")
    
    df_2024_filtered = df_2024.drop(index=0).reset_index(drop=True)
    df_2024_filtered['Salary'] = df_2024_filtered['Salary'].apply(salary_changer)
    filtered_data = df_2024_filtered.copy()
    
    unique_locations = df_2024_filtered['Location'].unique()
    unique_categories = df_2024_filtered['Job Category'].unique()

    location_options = ["No Specified Location"] + list(unique_locations)
    category_options = ["No Specified Job Category"] + list(unique_categories)

    location_input = st.selectbox("Select a Location to Analyse", options=location_options, index=0)
    if location_input != "No Specified Location":
        filtered_data = filtered_data[filtered_data['Location'].str.contains(location_input, case=False, na=False)]
        st.write(f"Filtered by Location: {location_input}")
    
    category_input = st.selectbox("Select a Job Category to Analyse", options=category_options, index=0)
    if category_input != "No Specified Job Category":
        filtered_data = filtered_data[filtered_data['Job Category'].str.contains(category_input, case=False, na=False)]
        st.write(f"Filtered by Job Category: {category_input}")

    salary_input = st.number_input("Enter Minimum Salary (Range £20,000 - £35,000)", placeholder="Try Search for 20000")
    if salary_input < 20000 or salary_input > 35000:
        st.warning("This salary is outside the range. Please try in the range of £20,000 to £35,000.")
    elif salary_input > 0:
        filtered_data = filtered_data[filtered_data['Salary'] >= salary_input]
        st.write(f"Filtering Job Listings with Salaries Above £{salary_input:.2f}")

    skill_input = st.text_input("Enter a Skill to Analyse. Example Skills can be Seen in the DataFrame Below", placeholder="Try Search for Python")
    
    if skill_input:
        matched_skills = filtered_data['Skills Required'].apply(lambda x: any(skill_input.lower() in skill.lower() for skill in x))
        
        if matched_skills.any():
            filtered_data = filtered_data[matched_skills]
            st.write(f"Filtered by Skill: {skill_input}")
        else:
            st.error(f"The skill '{skill_input}' was not found. Please look for recognised skills in the data display below.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.write(f"### Filtered Jobs Currently Available in 2024")
    job_count = len(filtered_data)
    st.write(f"There are **{job_count} jobs** that match the filters you have selected:")
    
    if filtered_data.empty:
        st.write("No Jobs Found Matching the Selected Filters.")
    else:
        st.dataframe(filtered_data)

    st.markdown("<br>", unsafe_allow_html=True)
    st.write(f"Chart of job listings matching the filters you have applied:")

    dfs = [df_2019, df_2020, df_2021, df_2022, df_2023, df_2024_filtered]
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    filtered_counts = []
    
    for df in dfs:
        temp_df = df.copy()
        if location_input != "No Specified Location":
            temp_df = temp_df[temp_df['Location'].str.contains(location_input, case=False, na=False)]
        if category_input != "No Specified Job Category":
            temp_df = temp_df[temp_df['Job Category'].str.contains(category_input, case=False, na=False)]
        if salary_input > 0:
            temp_df['Salary'] = temp_df['Salary'].apply(salary_changer)
            temp_df = temp_df[temp_df['Salary'] >= salary_input]
        if skill_input:
            temp_df = temp_df[temp_df['Skills Required'].apply(lambda x: any(skill_input.lower() in skill.lower() for skill in x))]
        
        filtered_counts.append(len(temp_df))

    # Plotting the filtered counts
    fig, ax = plt.subplots(figsize=(10, 6))  # Plot for all filters
    ax.plot(years, filtered_counts, marker='o', linestyle='-', color='blue')
    ax.set_ylabel('Number of Job Listings')
    ax.set_xlabel('Year')
    st.pyplot(fig)


st.sidebar.title("Navigation")#sidebar buttons
page = st.sidebar.radio("Go to", ["Data Search", "Category Analysis", "Job Analysis"])
if page == "Data Search":
    data_search_page()
elif page == "Category Analysis":
    category_analysis_page()
elif page == "Job Analysis":
    job_analysis_page()