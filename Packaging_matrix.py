import streamlit as st
import pandas as pd

# Guidelines and scoring criteria for each criterion
criteria_details = {
    "Responsiveness": {
        "description": "Reactivity to operational change and demand.",
        "scoring": {
            "1-3": "Slow or ineffective response to requests. The supplier takes a long time to adjust to changes.",
            "4-6": "Moderately responsive; can handle minor adjustments but struggles with major emergencies.",
            "7-8": "Good responsiveness; can effectively manage significant changes or occasional emergencies.",
            "9-10": "Exceptional responsiveness; adapts quickly and efficiently to any changes or disruptions."
        }
    },
    "Industrial Capacity": {
        "description": "Based on forecast and confirmed by supplier from the RFQ Package (his % delta vs weekly volume).",
        "scoring": {
            "1-3": "Limited capacity; production is often at maximum or fails to meet quality expectations.",
            "4-6": "Average capacity; handles standard volumes but lacks resilience during crises.",
            "7-8": "Robust capacity; flexible enough to manage volume increases in the short term.",
            "9-10": "Exceptional capacity; surplus industrial capability available, ensuring consistent quality."
        }
    },
    "Total Cost": {
        "description": "How cheap the supplier is in total cost (based on CBD).",
        "scoring": {
            "1-3": "High overall cost; often above market standards.",
            "4-6": "Acceptable cost, but not very competitive; hidden costs may occur.",
            "7-8": "Competitive cost; good transparency regarding cost breakdown (raw materials, transport, etc.).",
            "9-10": "Optimal cost; among the lowest in the market while maintaining good service quality."
        }
    },
    "Raw Material Sensitivity": {
        "description": "Based on % of raw material within its total cost (crossed check with contract stability).",
        "scoring": {
            "1-3": "Highly exposed to raw material price fluctuations, causing significant cost impacts.",
            "4-6": "Moderate exposure; manages price changes but lacks effective hedging strategies.",
            "7-8": "Good sensitivity management; implements strategies to minimize cost volatility.",
            "9-10": "Excellent raw material risk management; highly resilient to market fluctuations."
        }
    },
    "Transit Time": {
        "description": "Door-to-door delivery time.",
        "scoring": {
            "1-3": "Long delivery times; often fails to meet deadlines.",
            "4-6": "Average delivery times; meets deadlines for standard shipments but struggles with urgency.",
            "7-8": "Good transit times; consistent and reliable for most deliveries.",
            "9-10": "Excellent delivery performance; fast and highly reliable with strong logistics."
        }
    },
    "Supply Continuity Risk": {
        "description": "Ability to maintain uninterrupted supply during crises. Includes multiple plants, inventory, semi-finished products.",
        "scoring": {
            "1-3": "High risk of supply disruptions; supplier is highly dependent on limited resources.",
            "4-6": "Moderate risk; supply chain is stable under normal conditions but lacks redundancy.",
            "7-8": "Low risk; supplier shows good resilience to disruptions and ensures continuous supply.",
            "9-10": "Minimal risk; highly resilient to crises, with diversified supply chains and contingency plans."
        }
    },
    "Reliability / Quality": {
        "description": "Based on experience & % rate + Packaging engineer assessment on samples.",
        "scoring": {
            "1-3": "Poor reliability; frequent delivery delays and unmet quality expectations.",
            "4-6": "Average reliability; delivers on time most of the time but struggles under pressure.",
            "7-8": "Reliable; consistently delivers on time with minor issues.",
            "9-10": "Highly reliable; excellent track record of on-time deliveries with consistent quality."
        }
    },
    "Contractual Stability": {
        "description": "Contractual stability of the supplier with its own suppliers. With diversity and a strong procurement department with grips on his suppliers.",
        "scoring": {
            "1-3": "Weak contracts; often renegotiated or terminated early, causing instability.",
            "4-6": "Moderately stable; contracts are standard but lack long-term commitments.",
            "7-8": "Stable; contracts are clear, long-term, and enforced effectively.",
            "9-10": "Highly stable; well-established contracts with strong terms and minimal disruptions."
        }
    }
}

# Weights per context
weights_supply_crisis = [10, 30, 5, 10, 15, 5, 15, 10]
weights_cost_reduction = [10, 15, 30, 15, 10, 10, 5, 5]

# Streamlit user interface
st.title("Supplier Decision Matrix")
st.write("Compare suppliers based on criteria and strategic priorities.")

# Number of suppliers
num_suppliers = st.number_input("Number of suppliers:", min_value=1, max_value=10, value=3)

# Supplier names
supplier_names = []
for i in range(num_suppliers):
    supplier_names.append(st.text_input(f"Supplier {i + 1} Name:", value=f"Supplier {chr(65 + i)}"))

# Input supplier scores with descriptions above input bars
st.subheader("Input Supplier Scores")
supplier_scores = {supplier: [] for supplier in supplier_names}
for crit, details in criteria_details.items():
    st.write(f"### {crit}")
    st.write(f"**Description:** {details['description']}")
    st.write("**Scoring Details:**")
    for score_range, explanation in details['scoring'].items():
        st.write(f"- **{score_range}:** {explanation}")
    for supplier in supplier_names:
        supplier_scores[supplier].append(st.number_input(f"{supplier} - {crit}:", value=5))

# Select strategic context
context = st.selectbox("Select the strategic context:", ["Supply Crisis", "Cost Reduction"])
selected_weights = weights_supply_crisis if context == "Supply Crisis" else weights_cost_reduction

# Calculate weighted scores
df_data = {"Criteria": list(criteria_details.keys())}
for supplier in supplier_names:
    df_data[supplier] = supplier_scores[supplier]
df = pd.DataFrame(df_data)

# Add weighted scores
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

# Download results as CSV
csv = df.to_csv(index=False)
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="supplier_decision_matrix.csv",
    mime="text/csv"
)
