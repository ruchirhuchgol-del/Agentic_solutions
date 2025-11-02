# Common Hypothesis Formulations

This document contains examples of well-formulated hypotheses for common business scenarios.

### Scenario 1: A/B Testing a Feature

**Business Problem:** "We launched a new recommendation algorithm (Variant B) and want to see if it increases the average user session duration compared to the old algorithm (Variant A)."

- **Context:**
  - Groups: Variant A (Control), Variant B (Treatment)
  - Metric: Average Session Duration (continuous)
  - Relationship: Independent
- **Hypotheses:**
  - **H₀:** μ_A = μ_B (The mean session duration is the same for both algorithms.)
  - **H₁ (Two-tailed):** μ_A ≠ μ_B (There is a difference in mean session duration between the algorithms.)
  - **H₁ (Right-tailed):** μ_A < μ_B (The new algorithm (B) leads to a higher mean session duration than the old one (A).)

### Scenario 2: Pre/Post Campaign Analysis

**Business Problem:** "We ran a marketing campaign and want to know if it affected the proportion of users who made a purchase."

- **Context:**
  - Groups: Same users, Before Campaign, After Campaign
  - Metric: Purchase Rate (binary/proportion)
  - Relationship: Paired
- **Hypotheses:**
  - **H₀:** p_before = p_after (The purchase rate is the same before and after the campaign.)
  - **H₁ (Two-tailed):** p_before ≠ p_after (The purchase rate changed after the campaign.)
  - **H₁ (Right-tailed):** p_before < p_after (The purchase rate increased after the campaign.)

### Scenario 3: Comparing Multiple Groups

**Business Problem:** "We are testing three different ad creatives (A, B, C) and want to see if there is any difference in their click-through rates."

- **Context:**
  - Groups: Ad Creative A, Ad Creative B, Ad Creative C
  - Metric: Click-Through Rate (categorical/proportion)
  - Relationship: Independent
- **Hypotheses:**
  - **H₀:** p_A = p_B = p_C (The click-through rate is the same for all three ad creatives.)
  - **H₁:** At least one creative's click-through rate is different from the others. (Note: ANOVA/Chi-Squared tests don't specify which group is different, only that a difference exists.)