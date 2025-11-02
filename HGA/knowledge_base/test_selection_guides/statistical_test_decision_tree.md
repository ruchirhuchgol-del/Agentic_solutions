# Statistical Test Decision Tree

This guide provides a structured approach to selecting the most appropriate statistical test for your analysis. Follow the questions in order.

### Step 1: What is the goal of your analysis?

- **A) Compare groups or populations:** Go to Step 2.
- **B) Assess the relationship between two variables:** (e.g., correlation, regression). *This is not covered by the current HGA scope.*

### Step 2: What type of data is your primary metric?

- **A) Continuous:** (e.g., revenue, height, temperature, time spent). Go to Step 3.
- **B) Categorical / Binary:** (e.g., converted/didn't convert, product category, satisfied/neutral/dissatisfied). Go to Step 4.

### Step 3: Analysis for Continuous Data

- **A) Are you comparing two groups?**
  - **Are the groups independent (different users)?** -> **Independent Samples t-test**
  - **Are the groups paired/dependent (same users measured twice)?** -> **Paired Samples t-test**
- **B) Are you comparing three or more groups?**
  - **Are the groups independent?** -> **Analysis of Variance (ANOVA)**
  - **Are the groups paired/dependent?** -> **Repeated Measures ANOVA**

### Step 4: Analysis for Categorical / Binary Data

- **A) Are you comparing proportions between two groups?**
  - **Are the groups independent?** -> **Two-Proportion Z-Test**
  - **Are the groups paired?** -> **McNemar's Test**
- **B) Are you comparing frequencies across two categorical variables?** (e.g., product preference vs. region)
  - -> **Chi-Squared Test of Independence**
- **C) Are you comparing proportions between three or more groups?**
  - -> **Chi-Squared Test for Homogeneity**

---

### Quick Reference Table

| Number of Groups | Group Relationship | Metric Type | Recommended Test |
|------------------|--------------------|-------------|------------------|
| 2 | Independent | Continuous | Independent Samples t-test |
| 2 | Paired | Continuous | Paired Samples t-test |
| >2 | Independent | Continuous | ANOVA |
| >2 | Paired | Continuous | Repeated Measures ANOVA |
| 2 | Independent | Categorical/Binary | Two-Proportion Z-Test |
| 2 | Paired | Categorical/Binary | McNemar's Test |
| 2+ | Independent | Categorical | Chi-Squared Test |