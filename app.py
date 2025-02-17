import streamlit as st
import pandas as pd

# Function to calculate revenue-based attrition including shrinkage
def calculate_revenue_attrition(df):
    years = df.columns[1:]  # Get year columns
    attrition_rates = []

    for i in range(1, len(years)):  # Loop through each year transition
        previous_year = years[i - 1]
        current_year = years[i]

        # Total revenue in the previous year
        total_revenue_previous = df[previous_year].sum()

        # Revenue lost (sum of revenue that went from positive to 0)
        lost_revenue = df[(df[previous_year] > 0) & (df[current_year] == 0)][previous_year].sum()

        # Revenue shrinkage (sum of customers who paid less than last year)
        shrinkage_revenue = df[df[current_year] < df[previous_year]][previous_year].sum() - df[df[current_year] < df[previous_year]][current_year].sum()

        # Total attrition revenue
        total_attrition_revenue = lost_revenue + shrinkage_revenue

        # Calculate attrition rate
        attrition_rate = (total_attrition_revenue / total_revenue_previous) * 100 if total_revenue_previous > 0 else 0
        attrition_rates.append(attrition_rate)

    # Calculate average attrition
    avg_attrition = sum(attrition_rates) / len(attrition_rates)

    return attrition_rates, avg_attrition

# Streamlit UI
st.title("📊 Customer Revenue Attrition Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload Customer ARR Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Calculate revenue attrition
    attrition_rates, avg_attrition = calculate_revenue_attrition(df)

    # Create output DataFrame
    attrition_df = pd.DataFrame({
        "Year Range": [f"{df.columns[i+1]} → {df.columns[i+2]}" for i in range(len(attrition_rates))],
        "Revenue Attrition (%)": attrition_rates
    })

    # Add average attrition
    attrition_df.loc[len(attrition_df)] = ["Average Revenue Attrition", avg_attrition]

    # Display results
    st.subheader("📌 Revenue Attrition Report")
    st.dataframe(attrition_df)

    # Save results to an Excel file
    output_file = "Customer_Revenue_Attrition_Report.xlsx"
    attrition_df.to_excel(output_file, index=False)

    # Download button
    st.download_button(label="📥 Download Revenue Attrition Report", data=open(output_file, "rb"), file_name="Customer_Revenue_Attrition_Report.xlsx")
