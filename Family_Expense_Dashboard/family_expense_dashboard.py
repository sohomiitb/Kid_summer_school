import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import streamlit as st
import plotly.graph_objects as go

# === 1️⃣ PARAMETERS ===

total_monthly_income = 6500
categories = ['Housing', 'Food & Dining', 'Transportation', 'Entertainment', 'Healthcare', 'Utilities', 'Others']
family_members = ['Sean (Father)', 'Tina (Mother)', 'Jack (Son)', 'Ruby (Daughter)']

today = datetime.today()
start_date = datetime(today.year, 1, 1)
days = (today - start_date).days + 1

# === 2️⃣ RANDOM CATEGORY BUDGET ===

random_weights = np.random.rand(len(categories))
random_weights /= random_weights.sum()
category_distribution = dict(zip(categories, random_weights))

monthly_budget = {cat: total_monthly_income * pct for cat, pct in category_distribution.items()}
daily_budget = {cat: val / 30 for cat, val in monthly_budget.items()}

# === 3️⃣ GENERATE DAILY DATA ===

data = []
for day in range(days):
    date = start_date + timedelta(days=day)
    record = {'Date': date}
    for cat in categories:
        expense = daily_budget[cat] * random.uniform(0.8, 1.2)
        record[cat] = round(expense, 2)
    record['Name'] = random.choice(family_members)
    data.append(record)

df = pd.DataFrame(data)
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# === 4️⃣ LONG FORMAT FOR RECENT ===

melted = df.melt(
    id_vars=['Date', 'Name', 'Month'],
    value_vars=categories,
    var_name='Category',
    value_name='Amount'
)

melted = melted[melted['Amount'] > 0]

# === 5️⃣ MONTHLY SUMMARY ===

monthly = melted.groupby(['Month', 'Name']).agg(
    Total_Expenses=('Amount', 'sum')
).reset_index()

monthly['Total_Income'] = total_monthly_income
monthly['Savings'] = monthly['Total_Income'] - monthly['Total_Expenses']
monthly['Budget_Used_%'] = (monthly['Total_Expenses'] / monthly['Total_Income']) * 100
monthly['Prev_Expenses'] = monthly.groupby('Name')['Total_Expenses'].shift(1)
monthly['Expense_Change_%'] = ((monthly['Total_Expenses'] - monthly['Prev_Expenses']) / monthly['Prev_Expenses']) * 100

# === 6️⃣ STREAMLIT DASHBOARD ===

st.set_page_config(page_title="Family Expense Dashboard", layout="wide")

st.title("🏠 Family Expense Dashboard")

selected_member = st.selectbox(
    "Select Family Member:",
    ["Whole Family"] + family_members
)

if selected_member == "Whole Family":
    df_agg = monthly.groupby('Month').agg(Total_Expenses=('Total_Expenses', 'sum'))
    df_agg['Total_Income'] = total_monthly_income * len(family_members)
    df_agg['Savings'] = df_agg['Total_Income'] - df_agg['Total_Expenses']
    df_agg['Budget_Used_%'] = (df_agg['Total_Expenses'] / df_agg['Total_Income']) * 100
    df_agg['Prev_Expenses'] = df_agg['Total_Expenses'].shift(1)
    df_agg['Expense_Change_%'] = ((df_agg['Total_Expenses'] - df_agg['Prev_Expenses']) / df_agg['Prev_Expenses']) * 100
    cat_breakdown = melted.groupby(['Month', 'Category']).Amount.sum().reset_index()
    recent = melted.copy()
else:
    df_agg = monthly[monthly['Name'] == selected_member].set_index('Month')
    cat_breakdown = melted[melted['Name'] == selected_member].groupby(['Month', 'Category']).Amount.sum().reset_index()
    recent = melted[melted['Name'] == selected_member]

latest = df_agg.iloc[-1]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Income", f"${latest['Total_Income']:.2f}")
col2.metric("Total Expenses", f"${latest['Total_Expenses']:.2f}")
col3.metric("Savings", f"${latest['Savings']:.2f}")
col4.metric("Budget Used", f"{latest['Budget_Used_%']:.2f}%")
if not np.isnan(latest['Expense_Change_%']):
    col5.metric("Last MoM Change", f"{latest['Expense_Change_%']:.2f}%")
else:
    col5.metric("Last MoM Change", "N/A")

# === 7️⃣ BAR CHART ===

fig = go.Figure()
fig.add_trace(go.Bar(x=df_agg.index, y=df_agg['Total_Income'], name='Income'))
fig.add_trace(go.Bar(x=df_agg.index, y=df_agg['Total_Expenses'], name='Expenses'))
fig.add_trace(go.Bar(x=df_agg.index, y=df_agg['Savings'], name='Savings'))
fig.update_layout(barmode='group', title="Monthly Income vs Expenses vs Savings")
st.plotly_chart(fig, use_container_width=True)

# === 8️⃣ STACKED BAR ===

fig_cat = go.Figure()
for cat in categories:
    df_cat = cat_breakdown[cat_breakdown['Category'] == cat]
    fig_cat.add_trace(go.Bar(x=df_cat['Month'], y=df_cat['Amount'], name=cat))
fig_cat.update_layout(barmode='stack', title="Monthly Expenses Breakdown by Category")
st.plotly_chart(fig_cat, use_container_width=True)

# === 9️⃣ PIE CHART ===

st.subheader("🍕 Expense Categories Pie Chart")
available_months = sorted(cat_breakdown['Month'].unique())
selected_month = st.selectbox("Select Month to view pie chart:", available_months, index=len(available_months) - 1)
pie_data = cat_breakdown[cat_breakdown['Month'] == selected_month]
fig_pie = go.Figure(go.Pie(labels=pie_data['Category'], values=pie_data['Amount'], hole=0.4))
fig_pie.update_layout(title=f"Expense Distribution for {selected_month}")
st.plotly_chart(fig_pie, use_container_width=True)

# === 🔟 LINE GRAPH ===

st.subheader("📈 Monthly Spending Trend")
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Total_Income'], mode='lines+markers', name='Income'))
fig_line.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Total_Expenses'], mode='lines+markers', name='Expenses'))
fig_line.update_layout(title="Monthly Spending Trend: Income vs Expenses", xaxis_title="Month", yaxis_title="Amount ($)")
st.plotly_chart(fig_line, use_container_width=True)

# === 1️⃣1️⃣ DYNAMIC RECENT EXPENSES ===

st.subheader("🕒 Recent Expenses (Dynamic)")

recent_expenses = recent.sort_values('Date', ascending=False).head(5)

for _, row in recent_expenses.iterrows():
    days_ago = (today - row['Date']).days
    if days_ago == 0:
        day_text = "Today"
    elif days_ago == 1:
        day_text = "Yesterday"
    else:
        day_text = f"{days_ago} days ago"
    st.write(f"**{row['Category']}**  \n_{row['Name']} • {day_text}_  \n**-${row['Amount']:.2f}**")

# === RAW DATA ===

with st.expander("Show Raw Daily Data"):
    st.dataframe(df)
