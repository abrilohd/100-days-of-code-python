# Day 79 – Nobel Prize Data Analysis

This project explores over a century of Nobel Prize data to uncover patterns in scientific achievement, geography, gender distribution, and institutional influence.

The Nobel Prize was established by Alfred Nobel in 1895 to reward those who provide the greatest benefit to humanity.

Using data analysis and visualization techniques, we investigate trends in Nobel Prize awards across countries, institutions, and time.

---

# Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn
- Jupyter Notebook

---

# Key Analyses Performed

## 1. Data Cleaning
- Converted birth dates to datetime
- Created prize share percentage column
- Identified missing values
- Removed duplicates

---

## 2. Gender Distribution

Interactive donut chart showing percentage of prizes awarded to male vs female laureates.

Key insight:
- The majority of Nobel Prizes historically have been awarded to men.

---

## 3. Nobel Prize Categories

Bar chart showing total prizes awarded per category:

Categories include:
- Physics
- Chemistry
- Medicine
- Literature
- Peace
- Economics

Insight:
Science categories dominate total prize counts.

---

## 4. Nobel Prizes Over Time

Matplotlib visualization showing:

- Annual prize count
- 5-year rolling average

Insight:
- Prize distribution increases over time
- Global events like wars temporarily reduced awards.

---

## 5. Prize Sharing Trend

Analysis of how often prizes are shared among multiple winners.

Insight:
Modern Nobel prizes are increasingly shared among multiple researchers.

---

## 6. Top Countries by Nobel Prize Count

Top 20 countries ranked by number of Nobel laureates.

Insight:
The United States dominates Nobel Prize awards in recent decades.

---

## 7. Country-Level Visualization

Choropleth world map visualizing Nobel prizes per country.

---

## 8. Top Research Institutions

Organizations with the most Nobel laureates.

Examples include:
- Harvard University
- University of Chicago
- Cambridge University

---

## 9. Discovery Hotspots

Cities producing the most Nobel-winning discoveries.

Major hubs include:
- Cambridge
- Chicago
- Berkeley
- Paris

---

## 10. Sunburst Analysis

Hierarchical visualization showing:

Country → City → Organization

This reveals global clusters of scientific innovation.

---

# Key Insights

1. The United States leads the world in Nobel Prize counts.
2. Major discoveries cluster around elite universities.
3. Nobel prizes are increasingly shared among multiple researchers.
4. Scientific innovation is geographically concentrated.
5. Female representation has increased in recent decades but remains lower overall.

---

# Real World Applications

This type of analysis can be used for:

- Global research policy analysis
- Scientific funding strategies
- Institutional performance evaluation
- Innovation cluster identification

---

# How to Run

Install dependencies:

pip install -r requirements.txt

Run the notebook:

jupyter notebook