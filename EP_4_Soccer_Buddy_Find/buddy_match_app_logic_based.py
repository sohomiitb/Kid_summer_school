import pandas as pd
import streamlit as st

# Load your CSV or dataset
@st.cache_data
def load_data():
    return pd.read_csv("neighbourhood_sports.csv")  # replace with your data path

def run_buddy_match_app(dataframe):
    st.title("🏅 Neighbourhood Sports Buddy Matcher")
    st.write("Find a sports buddy near you based on shared preferences!")

    st.sidebar.header("🔍 Filter Criteria")

    sport = st.sidebar.selectbox("Sport", sorted(dataframe["sport_name"].unique()))
    interest_level = st.sidebar.multiselect("Interest Level", dataframe["interest_level"].unique(), default=list(dataframe["interest_level"].unique()))
    enrollment_status = st.sidebar.multiselect("Enrollment Status", dataframe["enrollment_status"].unique(), default=["Enrolled"])
    gender = st.sidebar.multiselect("Gender", dataframe["gender"].unique(), default=list(dataframe["gender"].unique()))
    skill_level = st.sidebar.multiselect("Skill Level", dataframe["skill_level"].unique(), default=list(dataframe["skill_level"].unique()))
    schedule = st.sidebar.multiselect("Training Schedule", dataframe["training_schedule"].unique(), default=list(dataframe["training_schedule"].unique()))
    participation = st.sidebar.multiselect("Participation Type", dataframe["seasonal_or_year_round"].unique(), default=list(dataframe["seasonal_or_year_round"].unique()))

    grade_range = st.sidebar.slider("Grade Range", 1, 12, (1, 12))
    experience_range = st.sidebar.slider("Experience (Years)", 0, 10, (0, 10))

    filtered = dataframe[
        (dataframe["sport_name"] == sport) &
        (dataframe["interest_level"].isin(interest_level)) &
        (dataframe["enrollment_status"].isin(enrollment_status)) &
        (dataframe["gender"].isin(gender)) &
        (dataframe["skill_level"].isin(skill_level)) &
        (dataframe["training_schedule"].isin(schedule)) &
        (dataframe["seasonal_or_year_round"].isin(participation)) &
        (dataframe["grade_level"].between(*grade_range)) &
        (dataframe["experience_years"].between(*experience_range))
    ]

    st.subheader("🎯 Matching Buddies")
    st.write(f"Found {len(filtered)} buddies that match your criteria.")
    st.dataframe(filtered[[
        "first_name", "last_name", "grade_level", "gender", "school_name", 
        "sport_name", "interest_level", "enrollment_status", "experience_years", 
        "training_schedule", "seasonal_or_year_round", "skill_level", 
        "parent_name", "contact_number", "email"
    ]])

if __name__ == "__main__":
    df = load_data()
    run_buddy_match_app(df)
