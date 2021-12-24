import streamlit as st
import pickle
import numpy as np

# function to load the file
def load_prediction_model():
    with open('salary_pred_.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# execute the function
data = load_prediction_model()

regressor = data["model"]
country_encoder = data["country_encoder"]
education_encoder = data["education_encoder"]

# create prediction page
def show_prediction_scene():
    # header of scene
    st.title("Salary Prediction Tool")
    st.write("""### You can use this tool to predict your salary as a Software Developer.""")
    st.write("""### Note: The predicted salary is just an estimation. Your actual salary may vary.""")
    # List of countries 
    country = (
        "United States of America",
        "India",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
        "Turkey",
        "Switzerland",
        "Israel",
        "Norway",
        "Mexico",
        "Ukraine"
    )

    # education levels we are considering
    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    )

    # create a select box for countries and education levels

    country_select = st.selectbox("What country are you employed in?", country)
    education_select = st.selectbox("What is your highest level of education?", education)

    # create a slider so users can choose how many years of experience they have
    experience_select = st.slider("How many years of professional experience do you have?", 0, 50, 5)

    # real-time salary prediction if all three values are filled in
    if country_select and education_select:
        input_arr = np.array([[country_select, education_select, experience_select]])
        input_arr[:, 0] = country_encoder.transform(input_arr[:,0])
        input_arr[:, 1] = education_encoder.transform(input_arr[:,1])
        input_arr = input_arr.astype(float)

        salary = regressor.predict(input_arr)
        st.subheader(f"Your estimated salary is ${salary[0]:.2f} (USD)")
