import streamlit as st
import pandas as pd

# Criteria defined in English
criteria = [
    "Responsiveness",
    "Industrial capacity",
    "Total cost",
    "Raw material sensitivity",
    "Transit time",
    "Supply continuity risk",
    "Reliability",
    "Contractual stability",
    "Environmental compliance",
]

# Weights per context
weights_supply_crisis = [15, 30, 10, 10, 5, 20, 15, 10, 5]
weights_cost_reduction = [10, 15, 35, 15, 10, 10, 5, 5, 5]

# Streamlit user interface
st.title("Supplier Decision Matrix")
st.write("Compare suppliers based on criteria and strategic priorities.")

# Number of suppliers
num_suppliers = st.number_input("Number of suppliers:", min_value=1, max_value=10, value=3)

# Supplier names
supplier_names = []
for i in range(num_suppliers):
    supplier_names.append(st.text_input(f"Supplier {i + 1} Name:", value=f"Supplier {chr(65 + i)}"))

# Input supplier scores
st.subheader("Input Supplier Scores")
supplier_scores = {supplier: [] for supplier in supplier_names}
for i, crit in enumerate(criteria):
    st.write(f"Scores for {crit}")
    for supplier in supplier_names:
        supplier_scores[supplier].append(st.number_input(f"{supplier} - {crit}:", value=5))

# Select strategic context
context = st.selectbox("Select the strategic context:", ["Supply Crisis", "Cost Reduction"])
selected_weights = weights_supply_crisis if context == "Supply Crisis" else weights_cost_reduction

# Calculate weighted scores
df_data = {"Criteria": criteria}
for supplier in supplier_names:
    df_data[supplier] = supplier_scores[supplier]
df = pd.DataFrame(df_data)

for supplier in supplier_names:
    df[f"Weighted Score {supplier}"] = df[supplier] * selected_weights

# Calculate total scores
total_scores = {supplier: df[f"Weighted Score {supplier}"].sum() for supplier in supplier_names}

# Display results
st.subheader("Decision Matrix Results")
st.write("### Supplier Data and Weighted Scores")
st.table(df)

st.write(f"### Selected Context: {context}")
st.write("### Total Scores by Supplier")
st.table(pd.DataFrame(total_scores.items(), columns=["Supplier", "Total Score"]))
