import streamlit as st
st.write("✅ The app is running successfully!")

def calculate_revenue_attrition(df):
    years = df.columns[1:]  # Get year columns
    attrition_rates = []

    for i in range(1, len(years)):  # Loop through each year transition
        previous_year = years[i - 1]
        current_year = years[i]

        # Total revenue in the previous year
        total_revenue_previous = df[previous_year].sum()

        # Revenue lost (customers who went from paying to 0)
        lost_revenue = df[(df[previous_year] > 0) & (df[current_year] == 0)][previous_year].sum()

        # Revenue shrinkage (customers who paid less than last year)
        shrinkage_revenue = (df[df[current_year] < df[previous_year]][previous_year].sum() -
                             df[df[current_year] < df[previous_year]][current_year].sum())

        # Total revenue attrition
        total_attrition_revenue = lost_revenue + shrinkage_revenue

        # Calculate attrition rate
        attrition_rate = (total_attrition_revenue / total_revenue_previous) * 100 if total_revenue_previous > 0 else 0
        attrition_rates.append(attrition_rate)

    # Compute the average attrition rate
    avg_attrition = sum(attrition_rates) / len(attrition_rates)

    return attrition_rates, avg_attrition
