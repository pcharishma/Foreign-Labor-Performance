# Foriegn-Labor-Performance

## Problem

This project will enable data scientists looking to understand the trends in H1b Visa authorizations both company-wise
and state-wise.


## Approach
I wanted to group on two columns: 
* Occupation
* State

These columns had different names in files. I had to find the common ones and check if data file contains
the column names.  

###### Optimization:
An optimization I used here was to read only the header file first instead of reading the
entire file in one go. The code proceeds only if the required columns are present in the
file. I also filtered all the certified data early in the process.


###### Code Reuse:

Since the function that calculates the top 10 information for both states as well as 
occupations is identical, I parametrized it with column name.

The function `top10info()` now has a simple task of finding the number of rows for its
input file and find the top 10 percentages.

## Usage:

1. Place a single input *csv* file in the `./input` directory.
2. Run the python script using:
`./run.sh`


