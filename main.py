import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
from pprint import pprint
from scipy.stats import linregress
import sys

#########################################################################################
#
# Variables
#
#########################################################################################
# quatri_name = "1a-psico"
quatri_name = "full-master"
max_number_pacs = 5 # 4, 5

#########################################################################################
#
# / Variables
#
#########################################################################################

#########################################################################################
#
# Main Operations
#
#########################################################################################
# Import df from json
with open(f"{quatri_name}.json", "r") as file:
    data = json.load(file)

# Check if waged subjects
if "credits" in next(iter(data.values())):
    waged_subjects = True
else:
    waged_subjects = False

# Calculate decimal marks, final mark and create df
rows = []
wages = []

# Iterate the full dictionary
for subject, dictionary in data.items():
    decimal_marks = []
    row = {"Subject": subject}
    final_mark_sum = 0
    final_wages_sum = 0

    # Iterate the dictionary inside each subject
    for i in range(len(dictionary["wages"])):
        if i < len(dictionary["marks"]):
            decimal_mark = round(10 * dictionary["marks"][i] / dictionary["wages"][i], 1)
            decimal_marks.append(decimal_mark)
            row[f"Mark{i+1}"] = decimal_mark
            final_mark_sum += dictionary["marks"][i]
            final_wages_sum += dictionary["wages"][i]
    
    # Calculate subject final mark
    if final_wages_sum > 0: 
        final_mark =  round(10 * final_mark_sum / final_wages_sum, 1)
    else:
        final_mark = 0
    # Set the wage of the subject if waged
    if waged_subjects:
        wages.append(dictionary["credits"])
    dictionary["decimal_marks"] = decimal_marks
    dictionary["final_mark"] = final_mark   
    row["Final Mark"] =  final_mark
    rows.append(row)

# print(rows)

# Create DataFrame
df = pd.DataFrame(rows)

# Calculate average
count_marks = 0
sum_marks = 0
for i in range(len(df["Final Mark"])):
    mark = df["Final Mark"][i]
    if mark != 0:
        if waged_subjects:
            sum_marks += mark * wages[i]
            count_marks += wages[i]
        else:
            count_marks += 1
            sum_marks += mark
final_mark = round(sum_marks / count_marks, 2)

# Reorder columns: put Mark3 after Mark2
cols = ["Subject"] 
cols.extend([f"Mark{i}" for i in range(1, max_number_pacs + 1)])
cols.append("Final Mark")
df = df.reindex(columns=cols)

print(f"Quatri: {quatri_name}")
print(tabulate(df, headers='keys', tablefmt='psql'))
print("+--------------------+")
print(f"| Average Mark: {final_mark} |")
print("+--------------------+")

