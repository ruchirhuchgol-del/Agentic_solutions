# Statistical Notation Standards

This document outlines the standard notation for formulating statistical hypotheses within our organization. All reports and analyses must adhere to these standards.

## 1. Population Parameters

These symbols represent the true, unknown parameters of the entire population.

| Parameter | Symbol | Description | Data Type |
|-----------|--------|-------------|-----------|
| Mean (Average) | μ (mu) | The central tendency of a continuous variable. | Continuous |
| Proportion | p (lowercase p) | The proportion or percentage of a categorical/binary outcome. | Binary / Categorical |
| Variance | σ² (sigma-squared) | The spread or dispersion of a continuous variable. | Continuous |
| Standard Deviation | σ (sigma) | The square root of the variance. | Continuous |
| Correlation | ρ (rho) | The linear relationship between two continuous variables. | Continuous |

## 2. Sample Statistics

These symbols represent the calculated values from our sample data.

| Statistic | Symbol | Description |
|-----------|--------|-------------|
| Sample Mean | x̄ (x-bar) | The mean of our sample data. |
| Sample Proportion | p̂ (p-hat) | The proportion in our sample data. |
| Sample Standard Deviation | s | The standard deviation of our sample data. |

## 3. Hypothesis Formulation Rules

- **Null Hypothesis (H₀):** Always uses an equality sign (=, ≤, or ≥). It states that there is *no effect* or *no difference*.
- **Alternative Hypothesis (H₁):** Always uses an inequality sign (≠, <, or >). It states that there *is an effect* or *a difference*.
- **Consistency:** The symbols used in H₀ and H₁ must match (e.g., if H₀ uses μ, H₁ must also use μ).

## 4. Examples

**Scenario:** Comparing the average revenue between two groups, Group A (Control) and Group B (Treatment).

- **Correct Notation:**
  - H₀: μ_A = μ_B
  - H₁: μ_A ≠ μ_B (Two-tailed)
  - H₁: μ_A < μ_B (Left-tailed, if we suspect A is worse)
  - H₁: μ_A > μ_B (Right-tailed, if we suspect A is better)

**Scenario:** Comparing the conversion rate (a proportion) of a new webpage (New) against an old one (Old).

- **Correct Notation:**
  - H₀: p_New = p_Old
  - H₁: p_New > p_Old (Right-tailed, as we hope the new page is better)

**Incorrect Usage:**
- H₀: μ_A = p_B (Mixing mean and proportion notation)
- H₁: μ_A > μ_B (For a categorical metric like "satisfaction score")