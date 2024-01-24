# topsis-3283

## Overview

topsis-3283 is a Python library designed for Multiple Criteria Decision Making (MCDM) problems using the Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS). It facilitates decision-making processes by considering various criteria, their respective weights, and impacts.

## Installation

Use the following command to install topsis-3283 via pip:

```bash
pip install topsis-3283
Usage
To utilize the library, use the topsis command in the terminal with the following arguments:

bash
Copy code
topsis <csv_filename> <weights_vector> <impacts_vector>
Example:
bash
Copy code
topsis sample.csv "1,1,1,1" "+,-,+,+"
Alternatively:

bash
Copy code
topsis sample.csv 1,1,1,1 +,-,+,+
If there are spaces in the input string, enclose it in double quotes.

Example
Consider the following example with a sample CSV file containing mobile handset data:

csv
Copy code
Model,Storage space(in gb),Camera(in MP),Price(in $),Looks(out of 5)
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,32,8,275,4
M5,16,16,225,2
Weights vector: [0.25, 0.25, 0.25, 0.25]
Impacts vector: [+, +, -, +]
Example usage:

bash
Copy code
topsis sample.csv "0.25,0.25,0.25,0.25" "+,+,-,+"
Output
The library provides TOPSIS results, including P-Score and Rank for each item.

Other Notes
The library removes the first column and first row from the CSV before processing to eliminate indices and headers.
Ensure that the CSV does not contain categorical values.
License
This project is licensed under the MIT License.