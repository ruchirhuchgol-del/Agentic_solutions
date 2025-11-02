# Getting Started

This guide will walk you through installing and running the Hypothesis Generation Agent (HGA) for the first time.

## Prerequisites

-   **Python 3.10 or newer**: The project requires a modern version of Python.
-   **OpenAI API Key**: HGA uses OpenAI's models for its reasoning. You can get a key from the [OpenAI Platform](https://platform.openai.com/api-keys).

## Step 1: Installation

The easiest way to install HGA is by cloning the repository and running our setup script.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-org/hypothesis-generation-agent.git
    cd hypothesis-generation-agent
    ```

2.  **Run the Setup Script**
    This script will create a Python virtual environment, install all necessary dependencies, and set up the required directory structure.
    ```bash
    make setup
    ```
    *If you don't have `make`, you can run the script directly: `./scripts/setup_dev_env.sh`*

## Step 2: Configuration

HGA needs your OpenAI API key to function.

1.  **Create a `.env` file**
    The setup script creates a `.env` file for you from `.env.example`. If not, copy it manually:
    ```bash
    cp .env.example .env
    ```

2.  **Add Your API Key**
    Open the `.env` file in your favorite editor and add your key:
    ```
    OPENAI_API_KEY=sk-your-actual-api-key-here
    ```
    Save the file. The application will automatically load this key when it runs.

## Step 3: Your First Analysis

You can now run HGA using the command-line interface (CLI).

1.  **Run the `hga run` command**
    ```bash
    hga run
    ```
    The CLI will prompt you to enter the business problem you want to analyze.

2.  **Enter Your Problem**
    ```
    ? Business Problem: We want to see if our new pricing model (Model B) increases the average revenue per user compared to the old model (Model A).
    ```

3.  **Review the Output**
    The agent will process your request and print a detailed report to the console. The output includes:
    -   A summary of the analysis.
    -   The extracted context (groups, metrics, etc.).
    -   The Null (H₀) and Alternative (H₁) hypotheses.
    -   A recommended statistical test with justification.
    -   A validation report confirming the setup is sound.

### Example Output Snippet

```markdown
--- Analysis Complete ---
# Hypothesis Generation Analysis Report

**Generated on:** 2023-10-27T10:00:00

## 1. Business Problem
We want to see if our new pricing model (Model B) increases the average revenue per user compared to the old model (Model A).

## 3. Statistical Hypotheses
### Null Hypothesis (H₀)
- **Notation:** `H₀: μ_A = μ_B`
- **Plain English:** There is no difference in the average revenue per user between the old and new pricing models.

### Alternative Hypotheses (H₁)
#### Right-tailed
- **Notation:** `H₁: μ_A < μ_B`
- **Plain English:** The new pricing model (B) leads to a higher average revenue per user than the old model (A).

## 5. Recommended Statistical Test
- **Primary Test:** Independent Samples t-test
- **Justification:** Compares the means of two independent groups on a continuous metric.

## 6. Validation & Confidence
- **Validation Status:** `APPROVED`
- **Overall Confidence Score:** 9/10