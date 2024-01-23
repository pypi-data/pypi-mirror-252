# Topsis-Kamal-102103259
For : Assignment(UCS654)<br>
Submitted by: Kamalpreet Kaur<br>
Roll no:102103259
Group:3COE9
## Description
This is a python package used to implement TOPSIS(Technique of Order Preference Similarity to the Ideal Solution) for MCDA(Multiple criteria decision analysis)

<br>

## How to use this package:

## Installation

pip install Topsis-Kamal-102103259

## Example:

## Sample dataset
Fund Name | P1 | P2 | P3 | P4 | P5
------------ | ------------- | ------------ | ------------- | ------------ | ------------
M1 | 0.78 | 0.61 | 5.5 | 34.7 | 10.4
M2 | 0.88 | 0.77 | 5 | 58.4 | 16.26
M3 | 0.61 | 0.37 | 5.9 | 39.9 | 11.7
M4 | 0.76 | 0.58 | 4.2 | 57.7 | 15.81
M5 | 0.84 | 0.71 | 3.2 | 48 | 13.19
M6 | 0.76 | 0.58 | 4 | 68.8 | 18.54
M7 | 0.81 | 0.66 | 6.5 | 38.2 | 11.54
M8 | 0.81 | 0.66 | 3.2 | 32.8 | 9.37

## Input
### In Command Prompt
Enter filename followed by .csv or .xlsx extension, then enter values of weights separated by commas like "1,1,1,2,2",then enter values of impacts separated by commas like "+,+,-,-,+" without giving space in between comma value, then enter name of file where you want to save output followed by .csv extension
```
python -m Topsis_Kamal_102103259 data.xlsx "1,1,1,2,2" "+,+,-,-,+" output.csv
```
## Output
This will be in our Output csv file
Fund Name | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank
------------ | ------------- | ------------ | ------------- | ------------ | ------------ | ------------ | ------------
M1 | 0.78 | 0.61 | 5.5 | 34.7 | 10.4 | 0.5303740545041122 | 4
M2 | 0.88 | 0.77 | 5 | 58.4 | 16.26 | 0.5372510220778413 | 3
M3 | 0.61 | 0.37 | 5.9 | 39.9 | 11.7 | 0.4715707210914604 | 8
M4 | 0.76 | 0.58 | 4.2 | 57.7 | 15.81 | 0.5099483054760279 | 6
M5 | 0.84 | 0.71 | 3.2 | 48 | 13.19 | 0.57723478293325 | 1
M6 | 0.76 | 0.58 | 4 | 68.8 | 18.54 | 0.49447887833737925 | 7
M7 | 0.81 | 0.66 | 6.5 | 38.2 | 11.54 | 0.5244107252631429 | 5
M8 | 0.81 | 0.66 | 3.2 | 32.8 | 9.37 | 0.5576533672285703 | 2 