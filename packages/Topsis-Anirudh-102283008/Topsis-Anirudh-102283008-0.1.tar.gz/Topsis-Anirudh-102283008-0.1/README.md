# TopsisCLI

The `TopsisCLI` Python script is a command-line tool designed for implementing the Topsis (Technique for Order Preference by Similarity to Ideal Solution) algorithm on a provided dataset. This tool is suitable for multi-criteria decision-making scenarios.

## Features

- **Topsis Algorithm Implementation:** Utilizes the Topsis algorithm to analyze and rank alternatives based on specified criteria.

- **Command-Line Interface:** Designed as a command-line tool for easy integration into workflows and automation.

- **Weighted Decision Matrix:** Allows users to input weights for each criterion, influencing the decision-making process.

- **Data Normalization:** Normalizes input data to ensure fairness in the comparison of diverse criteria.

- **Ranking:** Calculates Topsis scores and assigns ranks to alternatives, aiding in decision support.

- **Error Handling:** Incorporates comprehensive error checks for input parameters, file existence, column requirements, and numeric data validation.

- **CSV Input/Output:** Supports CSV format for input data and saves results, including Topsis scores and ranks, to an output CSV file.

## Usage

```bash
python TopsisCLI.py <InputDataFile> <Weights> <Impacts> <ResultFileName>
