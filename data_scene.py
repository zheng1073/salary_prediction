import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# function to limit the values in a category
def limit_categories(category, limit):
    category_map = {}
    for i in range(len(category)):
        if category.values[i] >= limit:
            category_map[category.index[i]] = category.index[i]
        else:
            category_map[category.index[i]] = 'Not Enough Data'
    return category_map

# turn everything to a float
def clean_years_of_exp(x):
    if x == "More than 50 years":
        return 51
    if x == "Less than 1 year":
        return 0.5
    return float(x)

# clean the education data
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

# load the dataframe
@st.cache
def load_dataframe():
    results = pd.read_csv("survey_results_public.csv")
    # keep the following columns: Country, Education Level, Years of Exp, Employment, Converted Composition (to USD)
    results = results[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    results = results.rename({"ConvertedCompYearly" : "Salary"}, axis = 1)
    results = results[results["Salary"].notnull()]
    # drop all the data that doesn't have data
    results = results.dropna()
    # drop all non-full time data
    results = results[results["Employment"] == "Employed full-time"]
    # we don't need this column since all data on this column is the same
    results = results.drop("Employment", axis=1)
    # only include countries with over 350 datapoints
    country_map = limit_categories(results.Country.value_counts(), 350)
    results['Country'] = results['Country'].map(country_map)
    # remove outliers and unused data
    results = results[results["Salary"] <= 300000]
    results = results[results["Salary"] >= 15000]
    results = results[results["Country"] != "Not Enought Data"]
    # next clean years of professional experience and education level
    results['YearsCodePro'] = results['YearsCodePro'].apply(clean_years_of_exp)
    results['EdLevel'] = results['EdLevel'].apply(clean_education)

    return results

results = load_dataframe()

def show_data_scene():
    st.title("What does this dataset comprise of?")

    st.write("""### Source: Stack Overflow Annual Developer Survey 2021""")

    ### Chart 1 - Pie Chart to show the percentage of the data each country represents
    country_data = results["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(country_data, labels=country_data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Figure 1: Origin of Data (filtered by country)""")
    st.pyplot(fig1)

    

    st.write("""#### Figure 2:Mean Salary (filtered by highest level of education)""")

    country_data = results.groupby(["EdLevel"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(country_data)

    st.write("""#### Figure 3: Mean Salary (filtered by years of experience)""")

    country_data = results.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(country_data)