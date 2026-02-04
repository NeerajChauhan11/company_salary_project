import streamlit as st
from salary_predictor import predict_salary

st.set_page_config(page_title="Company Salary Analytics", layout="centered")

st.title("💼 Company Salary Analytics and AI Predictor")

st.markdown("Enter employee details to predict salary using AI model")

company = st.selectbox(
    "Company", ["TCS", "Infosys", "Wipro", "Accenture", "Google", "Amazon", "Microsoft"]
)

department = st.selectbox("Department", ["IT", "HR", "Finance"])
role = st.selectbox(
    "Role",
    [
        "Data Analyst",
        "AI Engineer",
        "Software Developer",
        "ML Engineer",
        "Business Analyst",
        "Cloud Engineer",
        "HR Manager",
        "Financial Analyst",
    ],
)

location = st.selectbox(
    "Location",
    ["Delhi", "Bangalore", "Hyderabad", "Mumbai", "Pune", "Chennai", "Noida"],
)

experience = st.slider("Experience (Years)", 0, 15, 3)

rating = st.slider("Performance Rating", 1, 5, 3)

# Prediction

if st.button("🚀Predict Salary"):
    predicted_salary = predict_salary(
        company, department, role, location, experience, rating
    )

    st.success(f"💰 Predicted Salary: {predicted_salary} LPA")
