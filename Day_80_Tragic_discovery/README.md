# Day 80 – The Tragic Discovery of Handwashing

## Project Overview

This project analyzes historical medical data from the 1840s collected by **Dr. Ignaz Semmelweis** at the Vienna General Hospital.

Semmelweis discovered that **handwashing drastically reduced maternal deaths** caused by childbed fever.

Using Python data science tools, we recreate his analysis and statistically verify his discovery.

---

# Dataset

Two datasets are used:

1. **annual_deaths_by_clinic.csv**

   * Yearly births and deaths
   * Split between two hospital clinics

2. **monthly_deaths.csv**

   * Monthly births and deaths
   * Used to analyze trends before and after mandatory handwashing

---

# Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* SciPy

---

# Key Analysis Steps

### 1. Data Exploration

* Checked dataset shape
* Identified missing values
* Examined duplicates
* Generated descriptive statistics

---

### 2. Visualization

Created multiple visualizations:

* Monthly births vs deaths
* Death rate by clinic
* Rolling average death rate
* Histogram distributions
* Kernel density estimates

---

### 3. Impact of Handwashing

Semmelweis introduced **mandatory handwashing in June 1847**.

We compared:

* Death rate before handwashing
* Death rate after handwashing

Results showed a **dramatic reduction in maternal deaths**.

---

### 4. Statistical Test

A **two-sample t-test** was used to test if the difference in death rates was statistically significant.

Result:

* Very small p-value
* Indicates the difference is **not due to chance**

---

# Key Result

Handwashing reduced maternal deaths by **multiple times** and the improvement was **statistically significant**.

This discovery later became one of the foundations of modern medical hygiene.

---

# Example Visualization

The project includes visualizations such as:

* Time series charts
* Distribution plots
* Boxplots
* Kernel density estimates

---

# Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the notebook:

```
Dr_Semmelweis_Handwashing_Discovery.ipynb
```

---

# Learning Outcomes

From this project you learn:

* Data cleaning
* Exploratory data analysis
* Visualization techniques
* Rolling averages
* Statistical hypothesis testing
* Real-world data storytelling

---

# Author

@abrilohd
100 Days of Python Challenge
