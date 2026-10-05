import streamlit as st
import pandas as pd
import plotly.express as px
import ollama

st.set_page_config(
    page_title="Budget Explainer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Budget Explainer")
st.subheader("Personal Finance Assistant")

st.write(
    "Enter your monthly income and expenses to understand "
    "your spending and savings."
)

# -----------------------------
# MONTHLY INCOME
# -----------------------------

st.header("💵 Monthly Income")

income = st.number_input(
    "Enter your monthly income (₹)",
    min_value=0.0,
    value=20000.0,
    step=500.0
)

# -----------------------------
# MONTHLY EXPENSES
# -----------------------------

st.header("📊 Monthly Expenses")

col1, col2 = st.columns(2)

with col1:
    food = st.number_input(
        "🍔 Food",
        min_value=0.0,
        value=4000.0,
        step=500.0
    )

    rent = st.number_input(
        "🏠 Rent / Hostel",
        min_value=0.0,
        value=6000.0,
        step=500.0
    )

    transport = st.number_input(
        "🚌 Transport",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

with col2:
    shopping = st.number_input(
        "🛍️ Shopping",
        min_value=0.0,
        value=1500.0,
        step=500.0
    )

    entertainment = st.number_input(
        "🎬 Entertainment",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )

    other = st.number_input(
        "📦 Other Expenses",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )

# -----------------------------
# CALCULATIONS
# -----------------------------

expenses = {
    "Food": food,
    "Rent / Hostel": rent,
    "Transport": transport,
    "Shopping": shopping,
    "Entertainment": entertainment,
    "Other": other
}

total_expenses = sum(expenses.values())
remaining = income - total_expenses

# -----------------------------
# BUDGET SUMMARY
# -----------------------------

st.header("📋 Budget Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Monthly Income",
        f"₹{income:,.0f}"
    )

with col2:
    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col3:
    st.metric(
        "Money Remaining",
        f"₹{remaining:,.0f}"
    )

# -----------------------------
# STATUS
# -----------------------------

if remaining > 0:
    st.success(
        f"🎉 You have ₹{remaining:,.0f} left after your expenses."
    )
elif remaining == 0:
    st.warning(
        "⚠️ Your income is completely used by your expenses."
    )
else:
    st.error(
        f"🚨 Your expenses are ₹{abs(remaining):,.0f} more than your income."
    )

# -----------------------------
# PANDAS DATA
# -----------------------------

st.header("📊 Expense Breakdown")

df = pd.DataFrame(
    {
        "Category": list(expenses.keys()),
        "Amount": list(expenses.values())
    }
)

st.dataframe(
    df,
    width="stretch",
    hide_index=True
)
# -----------------------------
# SPENDING CHARTS
# -----------------------------

st.header("📈 Spending Analysis")

st.subheader("💰 Expenses by Category")

bar_chart = px.bar(
    df,
    x="Category",
    y="Amount",
    title="Monthly Expenses by Category",
    labels={
        "Amount": "Amount (₹)",
        "Category": "Expense Category"
    }
)

st.plotly_chart(
    bar_chart,
    width="stretch"
)

st.subheader("🥧 Spending Distribution")

pie_chart = px.pie(
    df,
    names="Category",
    values="Amount",
    title="Where Your Money Goes"
)

st.plotly_chart(
    pie_chart,
    width="stretch"
)
# -----------------------------
# AI BUDGET ADVISOR
# -----------------------------

st.header("🤖 AI Budget Advisor")

if st.button("✨ Analyze My Spending"):

    expense_text = "\n".join(
        f"{category}: ₹{amount:,.0f}"
        for category, amount in expenses.items()
    )

    prompt = f"""
You are a friendly personal finance assistant.

Monthly income: ₹{income:,.0f}

Monthly expenses:
{expense_text}

Total expenses: ₹{total_expenses:,.0f}
Money remaining: ₹{remaining:,.0f}

Please:
1. Explain my spending pattern in simple language.
2. Identify my biggest expense.
3. Suggest realistic ways to manage my budget.
4. Suggest how much I could try to save each month.

Give the answer in simple bullet points.
"""

    with st.spinner("🤖 AI is analyzing your budget..."):

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    st.subheader("💡 AI Suggestions")

    st.write(response["message"]["content"])
    # -----------------------------
# TRIP SAVINGS PLANNER
# -----------------------------

st.header("✈️ Trip Savings Planner")

destination = st.text_input(
    "📍 Trip Destination",
    placeholder="Example: Goa"
)

trip_budget = st.number_input(
    "💰 Trip Budget (₹)",
    min_value=0.0,
    value=12000.0,
    step=500.0
)

months = st.number_input(
    "📅 Months to Save",
    min_value=1,
    value=6,
    step=1
)

already_saved = st.number_input(
    "💵 Amount Already Saved (₹)",
    min_value=0.0,
    value=0.0,
    step=500.0
)

if st.button("✈️ Calculate Trip Savings"):

    remaining_trip = max(trip_budget - already_saved, 0)

    monthly_saving = remaining_trip / months

    st.subheader("🎯 Trip Savings Goal")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Trip Budget",
            f"₹{trip_budget:,.0f}"
        )

    with col2:
        st.metric(
            "Already Saved",
            f"₹{already_saved:,.0f}"
        )

    with col3:
        st.metric(
            "Monthly Saving Needed",
            f"₹{monthly_saving:,.0f}"
        )

    st.write(
        f"🎯 You need to save **₹{monthly_saving:,.0f} per month** "
        f"for {months} months to reach your **{destination or 'trip'}** goal."
    )

    progress = min(already_saved / trip_budget, 1.0) if trip_budget > 0 else 0

    st.write("📊 Trip Savings Progress")

    st.progress(progress)

    st.write(
        f"Progress: **{progress * 100:.1f}%**"
    )

    if monthly_saving <= remaining:
        st.success(
            f"✅ Your current remaining money of ₹{remaining:,.0f} "
            f"can cover the required monthly saving."
        )
    else:
        st.warning(
            f"⚠️ You need ₹{monthly_saving:,.0f} per month, "
            f"but your current remaining money is ₹{remaining:,.0f}."
        )