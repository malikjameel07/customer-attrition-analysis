import streamlit as st
import pandas as pd

# Function to calculate revenue-based attrition including shrinkage and loss separately
def calculate_revenue_attrition(df):
    years = df.columns[1:]  # Get year columns
    attrition_data = []

    for i in range(1, len(years)):  # Loop through each year transition
        previous_year = years[i - 1]
        current_year = years[i]

        # Total revenue in the previous year
        total_revenue_previous = df[previous_year].sum()

        # Revenue lost (customers who went from positive revenue to 0)
        lost_revenue = df[(df[previous_year] > 0) & (df[current_year] == 0)][previous_year].sum()
        loss_percentage = (lost_revenue / total_revenue_previous) * 100 if total_revenue_previous > 0 else 0

        # Revenue shrinkage (customers who paid less than last year)
        shrinkage_revenue = df[(df[current_year] < df[previous_year])][previous_year].sum() - df[(df[current_year] < df[previous_year])][current_year].sum()
        shrinkage_percentage = (shrinkage_revenue / total_revenue_previous) * 100 if total_revenue_previous > 0 else 0

        # Total revenue attrition (loss + shrinkage)
        total_attrition_revenue = lost_revenue + shrinkage_revenue
        attrition_rate = (total_attrition_revenue / total_revenue_previous) * 100 if total_revenue_previous > 0 else 0

        attrition_data.append([f"{previous_year} → {current_year}", round(loss_percentage, 2), round(shrinkage_percentage, 2), round(attrition_rate, 2)])

    # Calculate average values
    avg_loss = sum([row[1] for row in attrition_data]) / len(attrition_data)
    avg_shrinkage = sum([row[2] for row in attrition_data]) / len(attrition_data)
    avg_total_attrition = sum([row[3] for row in attrition_data]) / len(attrition_data)

    attrition_data.append(["Average Revenue Attrition", round(avg_loss, 2), round(avg_shrinkage, 2), round(avg_total_attrition, 2)])

    return attrition_data

# Streamlit UI
st.title("📊 Customer Revenue Attrition Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload Customer ARR Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Calculate revenue attrition
    attrition_data = calculate_revenue_attrition(df)

    # Create output DataFrame
    attrition_df = pd.DataFrame(attrition_data, columns=["Year Range", "Revenue Loss (%)", "Revenue Shrinkage (%)", "Total Attrition (%)"])

    # Display results
    st.subheader("📌 Revenue Attrition Report")
    st.dataframe(attrition_df)

    # Save results to an Excel file
    output_file = "Customer_Revenue_Attrition_Report.xlsx"
    attrition_df.to_excel(output_file, index=False)

    # Download button
    st.download_button(label="📥 Download Revenue Attrition Report", data=open(output_file, "rb"), file_name="Customer_Revenue_Attrition_Report.xlsx")
