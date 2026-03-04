# Day 78 – Linear Regression and Seaborn

This project investigates whether higher movie budgets lead to higher box office revenue.

Using real-world scraped data (May 1st, 2018), we clean, analyze, visualize, and build a predictive linear regression model.

---

# Objectives

- Clean raw financial data
- Convert strings to numeric types
- Handle missing and duplicate data
- Create decade-based analysis
- Visualize relationships with Seaborn
- Build Linear Regression models
- Compare old vs modern film economics
- Make revenue predictions

---

# Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Scikit-Learn
- Jupyter Notebook

---

# Data Cleaning

Performed:

- Removed '$' and ',' characters
- Converted monetary columns to numeric
- Converted Release_Date to datetime
- Removed unreleased films
- Filtered zero-revenue films

---

# Exploratory Data Analysis

Key Questions Answered:

- Do higher budgets lead to higher revenue?
- What percentage of films lose money?
- Are modern films more profitable?
- How many films grossed $0?
- How does profitability differ by decade?

---

# Data Visualization

Used Seaborn:

- Scatter plots
- Bubble charts
- Regression plots
- Decade comparison
- Time-based revenue trends

Styled with:

- Darkgrid themes
- Custom HEX colors
- Axis scaling

---

# Machine Learning Model

Linear Regression model:

Revenuê = θ₀ + θ₁ × Budget

Using Scikit-Learn:

```python
from sklearn.linear_model import LinearRegression

regression = LinearRegression()
regression.fit(X, y)
