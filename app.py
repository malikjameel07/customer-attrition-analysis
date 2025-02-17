import streamlit as st
import pandas as pd

# Function to calculate customer attrition
def calculate_attrition(df):
    years = df.columns[1:]  # Get all year columns
    attrition_rates = []

    for i in range(1, len(years)):  # Loop through each year after the first year
        previous_year = years[i - 1]
        current_year = years[i]

        # Count customers who paid last year but stopped this year
        lost_customers = df[(df[previous_year] > 0) & (df[current_year] == 0)].shape[0]
        total_customers = df[df[previous_year] > 0].shape[0]

        # Calculate attrition rate
        if total_customers > 0:
            attrition_rate = (lost_customers / total_customers) * 100
        else:
            attrition_rate = 0  # Avoid division by zero
        
        attrition_rates.append(attrition_rate)

    # Calculate average attrition rate over the years
    average_attrition = sum(attrition_rates) / len(attrition_rates)

    return attrition_rates, average_attrition

# Streamlit UI
st.title("📊 Customer Attrition Analysis AI")

# File uploader
uploaded_file = st.file_uploader("Upload Customer ARR Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Calculate attrition
    attrition_rates, avg_attrition = calculate_attrition(df)

    # Create a DataFrame for output
    attrition_df = pd.DataFrame({
        "Year Range": [f"{df.columns[i+1]} → {df.columns[i+2]}" for i in range(len(attrition_rates))],
        "Attrition Rate (%)": attrition_rates
    })

    # Add average attrition
    attrition_df.loc[len(attrition_df)] = ["Average Attrition", avg_attrition]

    # Display results
    st.subheader("📌 Attrition Report")
    st.dataframe(attrition_df)

    # Save results to an Excel file
    output_file = "Customer_Attrition_Report.xlsx"
    attrition_df.to_excel(output_file, index=False)

    # Download button
    st.download_button(label="📥 Download Attrition Report", data=open(output_file, "rb"), file_name="Customer_Attrition_Report.xlsx")
