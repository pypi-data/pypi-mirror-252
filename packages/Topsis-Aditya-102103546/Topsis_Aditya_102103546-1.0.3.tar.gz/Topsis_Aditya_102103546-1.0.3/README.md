# TOPSIS - Technique for Order Preference by Similarity to Ideal Solution

## Introduction

This Python script implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) algorithm. TOPSIS is a multi-criteria decision-making method that helps in ranking a set of alternatives based on their proximity to the ideal solution.

### Prerequisites

- Python 3
- pandas
- numpy

### Installation
```pip install Topsis_Aditya_102103546```

### Running the Script

Run the TOPSIS script from the command line with the following arguments:

```bash
python3 Topsis <input_file> <input_weights> <input_impacts> <output_file>
```

- `<input_file>`: Path to the CSV file containing the input data.
- `<input_weights>`: Weights for each criterion separated by commas.
- `<input_impacts>`: Impacts for each criterion, either '+' or '-'.
- `<output_file>`: Path to the CSV file where the result will be saved.

Example:

```bash
python3 Topsis /path/to/input/data.csv "1,2,3,4,5" "+,-,+,+,+" /path/to/output/result.csv
```

### Input Format

The input file should be a CSV file with the first column representing the alternatives and the following columns representing different criteria.

### Output

The script generates a CSV file with the TOPSIS scores and ranks for each alternative.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```