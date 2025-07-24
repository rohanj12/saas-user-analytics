import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/rohanjairam/projects/saas-user-analytics/data/eda_ready.csv')
df.columns = df.columns.str.strip()

# Page config
st.set_page_config(page_title="SaaS Churn Dashboard", layout="wide")
st.title("📊 SaaS User Churn Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filter Customers")

# Contract Filter
contract_options = df['Contract'].unique().tolist()
selected_contracts = st.sidebar.multiselect("Contract Type", contract_options, default=contract_options)

# InternetService Filter
internet_options = df['InternetService'].unique().tolist()
selected_services = st.sidebar.multiselect("Internet Service", internet_options, default=internet_options)

# Filtered dataframe
filtered_df = df[
    df['Contract'].isin(selected_contracts) &
    df['InternetService'].isin(selected_services)
]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 KPIs", "📈 Visuals", "📄 Raw Data"])

# --- TAB 1: KPIs ---
with tab1:
    st.subheader("📌 Key SaaS Metrics")

    arpu = filtered_df['MonthlyCharges'].mean()
    ltv = arpu * filtered_df['tenure'].mean()
    churn_rate = filtered_df['Churn'].value_counts(normalize=True).get('Yes', 0) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("💸 ARPU", f"${arpu:.2f}")
    col2.metric("🧬 LTV", f"${ltv:.2f}")
    col3.metric("⚠️ Churn Rate", f"{churn_rate:.2f}%")

# --- TAB 2: Visuals ---
with tab2:
    st.subheader("📈 Visual Analytics")

    # Churn by Contract
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered_df, x='Contract', hue='Churn', ax=ax1)
    ax1.set_title("Churn Count by Contract Type")
    st.pyplot(fig1)

    # Tenure distribution
    fig2, ax2 = plt.subplots()
    sns.histplot(data=filtered_df, x='tenure', hue='Churn', multiple='stack', ax=ax2)
    ax2.set_title("Customer Tenure by Churn Status")
    st.pyplot(fig2)

    # Heatmap: Churn vs InternetService & Contract
    st.subheader("🔥 Churn Rate by Internet Service and Contract Type")
    heatmap_data = (
        filtered_df.groupby(['InternetService', 'Contract'])['Churn']
        .apply(lambda x: (x == 'Yes').mean())
        .reset_index()
        .pivot('InternetService', 'Contract', 'Churn')
    )

    fig3, ax3 = plt.subplots()
    sns.heatmap(heatmap_data, annot=True, fmt=".2%", cmap="YlOrRd", ax=ax3)
    st.pyplot(fig3)

# --- TAB 3: Raw Data ---
with tab3:
    st.subheader("📄 Raw Data (Filtered)")
    st.dataframe(filtered_df.head(50))

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_customers.csv", "text/csv")

# Optional Footer
st.markdown("---")
st.caption("Built using Streamlit | Project by Rohan Jairam")
