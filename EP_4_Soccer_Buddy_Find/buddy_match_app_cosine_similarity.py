import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    return pd.read_csv("neighbourhood_sports.csv")

@st.cache_data
def prepare_similarity(df):
    features = [
        "grade_level", "gender", "sport_name", "interest_level", "enrollment_status",
        "experience_years", "training_schedule", "seasonal_or_year_round", "skill_level"
    ]
    encoded_df = df[features].copy()
    label_encoders = {}

    for col in encoded_df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        encoded_df[col] = le.fit_transform(encoded_df[col])
        label_encoders[col] = le

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(encoded_df)
    cosine_sim_matrix = cosine_similarity(scaled_features)

    similarity_df = pd.DataFrame(
        cosine_sim_matrix, index=df["student_id"], columns=df["student_id"]
    )
    return similarity_df

def get_similar_buddies(student_id, df, similarity_df, top_n=5):
    if student_id not in similarity_df.index:
        return pd.DataFrame()
    
    scores = similarity_df.loc[student_id].drop(student_id)
    top_matches = scores.sort_values(ascending=False).head(top_n)
    
    matched_students = df[df["student_id"].isin(top_matches.index)].copy()
    matched_students["similarity_score"] = matched_students["student_id"].map(top_matches)
    return matched_students.sort_values(by="similarity_score", ascending=False)

def main():
    st.title("🏅 Sports Buddy Matcher")
    df = load_data()
    similarity_df = prepare_similarity(df)

    student_id = st.number_input(
        "Enter your Student ID", 
        min_value=1, max_value=df["student_id"].max(), 
        value=10
    )
    top_n = st.slider("Number of Buddies to Find", min_value=1, max_value=10, value=5)

    if st.button("Find My Buddies"):
        student_info = df[df["student_id"] == student_id]
        if student_info.empty:
            st.warning("Student ID not found in the database.")
        else:
            # Display the student's name and preferences
            student_row = student_info.iloc[0]
            st.info(
                f"🔎 **Student ID:** {student_row['student_id']}\n\n"
                f"👤 **Name:** {student_row['first_name']} {student_row['last_name']}\n\n"
                f"🎓 **Grade:** {student_row['grade_level']}\n\n"
                f"⚽ **Sport:** {student_row['sport_name']}\n\n"
                f"🏆 **Interest Level:** {student_row['interest_level']}\n\n"
                f"📅 **Training Schedule:** {student_row['training_schedule']}\n\n"
                f"💪 **Skill Level:** {student_row['skill_level']}\n\n"
                f"⌛ **Experience:** {student_row['experience_years']} years\n\n"
            )

            # Get buddies
            matches = get_similar_buddies(student_id, df, similarity_df, top_n)
            if matches.empty:
                st.warning("No similar buddies found for the entered student ID.")
            else:
                st.success(f"Found {len(matches)} similar buddies!")
                st.dataframe(matches[[
                    "student_id", "first_name", "last_name", "grade_level", "sport_name",
                    "experience_years", "skill_level", "training_schedule", "similarity_score"
                ]])

if __name__ == "__main__":
    main()
