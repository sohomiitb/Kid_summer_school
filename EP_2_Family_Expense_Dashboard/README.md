# 👨‍👩‍👧‍👦 Family Expense Dashboard

This project is an interactive web dashboard that helps visualize and analyze a family's monthly expenses. It simulates daily spending data for each family member across various categories, providing insights into budgeting, savings, and spending trends.

Built with **Streamlit** and **Plotly**, the dashboard offers dynamic charts, summaries, and recent expense highlights for both the whole family and individual members.

---

## 🚀 Features

- **Simulated Expense Data:** Randomly generates daily expenses for each family member and category.
- **Monthly Summaries:** View total income, expenses, savings, and budget usage.
- **Interactive Visualizations:** Includes bar charts, stacked bar charts, pie charts, and line graphs for deep insights.
- **Recent Expenses Feed:** See the latest expenses with contextual time info.
- **Raw Data Table:** Explore the underlying daily data.

---

## 📦 Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- pandas
- numpy
- plotly

Install dependencies with:

```sh
pip install streamlit pandas numpy plotly

```


▶️ How to Run & Launch the App
1. Navigate to the project folder:
``` bash
cd Family_Expense_Dashboard

```

2. Run the Streamlit app
```bash

streamlit run family_expense_dashboard.py
```
3. Open the app in your browser
Once the app runs, it will automatically open at:

```
http://localhost:8501
```

📝 Customization

Categories & Members: Edit the categories and family_members lists in family_expense_dashboard.py to match your own family or expense types.
Monthly Income: Adjust the total_monthly_income variable as needed.

---

📊 Dashboard Preview


Summary Metrics: Income, expenses, savings, budget used, and month-over-month change.
Charts: Monthly income vs expenses, category breakdown, expense distribution pie, and spending trends.
Recent Expenses: Dynamic feed of the latest expenses.
Raw Data: Expandable table of all generated daily expense data.

---

💡 Learning Goals

Practice Python data manipulation with pandas and numpy.
Build interactive web apps using Streamlit.
Visualize data with Plotly.
Understand budgeting and expense tracking concepts.
