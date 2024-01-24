# TOPSIS Package

TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) is a comprehensive Python package designed for multi-criteria decision analysis. This package facilitates the evaluation and ranking of alternative solutions based on a specified set of criteria.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Interface](#command-line-interface)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Multi-criteria decision analysis (MCDA) is a powerful method employed for decision-making in scenarios where multiple criteria need consideration. TOPSIS, a widely recognized MCDA technique, plays a pivotal role in ranking alternatives by assessing their proximity to the ideal solution and their distance from the anti-ideal solution.

This package offers a robust Python implementation of the TOPSIS method, presenting it as both a standalone Python module and a user-friendly command line tool.

## Installation

You can install TOPSIS using pip:

```bash
pip install topsis-package


To use TOPSIS in your Python code, import the topsis module:

python
Copy code
from topsis_package import topsis

# Your decision matrix
data = {...}

# Your weights and impacts
weights = [...]
impacts = [...]

# Run TOPSIS
result_df = topsis(data, weights, impacts)

# Display the results
print(result_df)

```

## Command Line

TOPSIS also provides a command line interface for convenient usage:

```bash
topsis input.csv <weights> <impacts> result.csv

```

- input.csv: Path to the input CSV file containing the decision matrix.
- weights: Weights for each criterion separated by commas.
- impacts: Impacts for each criterion (+ or -) separated by commas.
- result.csv: Path to the output CSV file where the results will be saved.

## Examples

In this section, provide users with practical examples that demonstrate the application of the TOPSIS package in real-world scenarios. Include step-by-step guides, sample datasets, and expected outcomes to help users understand how to utilize the package effectively. Consider covering various use cases to showcase the versatility of the TOPSIS method.

### Example 1: Project Selection
Demonstrate how to use the TOPSIS package to rank potential project alternatives based on criteria such as cost, timeline, and resource utilization. Provide a sample decision matrix, weights, and impacts, and guide users through the process of obtaining a ranked list of projects.

### Example 2: Vendor Selection
Illustrate the application of TOPSIS for vendor selection by evaluating alternatives based on criteria like cost, quality, and delivery time. Walk users through the steps of inputting data, specifying weights and impacts, and interpreting the resulting rankings.

### Example 3: Product Design Optimization
Showcase how TOPSIS can be applied in product design optimization. Provide a use case where design alternatives are evaluated based on criteria such as functionality, manufacturability, and user satisfaction. Guide users through the TOPSIS process to identify the most suitable design.

## Contribution

Encourage users to contribute to the development of the TOPSIS package by providing clear guidelines on how they can actively participate. Include the following information:

### Reporting Issues
Explain the process for reporting issues, including the preferred format for issue descriptions, steps to reproduce, and any additional information that would help in troubleshooting.

### Suggesting Enhancements
Encourage users to share their ideas for enhancing the TOPSIS package. Provide guidance on how to propose new features, improvements, or optimizations. Include information on the preferred format for enhancement proposals.

### Submitting Pull Requests
Guide users through the process of submitting pull requests. Include instructions on forking the repository, creating a new branch, making changes, and submitting the pull request. Specify any coding standards or guidelines that contributors should follow.





# License

This project is licensed under the MIT License - see the LICENSE file for details.


