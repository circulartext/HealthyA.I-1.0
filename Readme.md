Nutrient Intake and Adjustment Visualizer

Overview

This script visualizes nutrient intake and adjustment recommendations based on input data from two CSV files:

Nutrient Intake Results - Contains nutrient intake values and recommended dietary intake (RDI) ranges.

Ideal Adjustments - Suggests adjustments to nutrient intake, specifying increases or decreases as needed.

The visualization includes bar charts for each nutrient, comparing intake values against RDI ranges, and highlights adjustments with dashed lines.

Features

Automatic Merging: Combines data from intake and adjustment files.

Customizable Charts: Generates individual charts for each nutrient.

Adjustments Visualization: Displays adjustments as colored dashed lines with annotations.

Dynamic Scaling: Adjusts chart scales automatically based on values.

Requirements

Python 3.x

Libraries: pandas, matplotlib, numpy

Installation

git clone <repository-url>
cd nutrient-visualizer
pip install -r requirements.txt

Usage

Place your data files (nutrient_intake_results.csv and ideal_adjustments.csv) in the same directory as the script.

Update the filenames in the script, if necessary.

Run the script:

python script_name.py

Input Data Formats

nutrient_intake_results.csv (Example):

Nutrient,Intake,Min RDI,Max RDI
Protein,50,45,70
Vitamin C,30,60,100

ideal_adjustments.csv (Example):

Nutrient,Adjustment
Protein,Increase by 10 grams
Vitamin C,Decrease by 15 mg

Notes:

Users should create their own CSV files based on their dietary intake and recommendations.

An example file foods.csv is included, which contains the user's food data. Users can use it to find their foods and calculate nutrient data specific to their diet.

It is good practice to adjust nutrient category weights to reflect personal priorities. Default weights in the script can be updated here:
```
# Nutrient category weights
NUTRIENT_CATEGORY_WEIGHTS = {
    "Protein (g)": 0.15,
    "Total Fat (g)": 0.10,
    "Total Carbohydrate (g)": 0.10,
    "Dietary Fiber (g)": 0.08,
    "Vitamin D3 (IU)": 0.07,
    "Vitamin B12 (mcg)": 0.06,
    "Vitamin C (%DV)": 0.05,
    "Vitamin B6 (%DV)": 0.05,
    "Calcium (mg)": 0.07,
    "Iron (mg)": 0.06,
    "Magnesium (mg)": 0.08,
    "Potassium (mg)": 0.07,
    "Zinc (mg)": 0.05,
    "Probiotics (CFUs)": 0.05,
    "Omega-3 Fatty Acids (g)": 0.04,
    "Saturated Fat (g)": -0.04,
    "Trans Fat (g)": -0.05,
    "Cholesterol (mg)": -0.03,
    "Sodium (mg)": -0.03,
    "Added Sugars (g)": -0.06
}

Output
```
The script generates bar charts for each nutrient, displaying:

Intake values.

Recommended minimum and maximum values.

Adjustment recommendations with annotations.

Example Output



Troubleshooting

Missing Data: Ensure CSV files are properly formatted and all required columns exist.

Libraries Missing: Run pip install -r requirements.txt to install dependencies.

File Paths: Update paths to CSV files if they are stored outside the script directory.

GitHub Integration

Initialize a Git repository:

git init

Add and commit files:

git add .
git commit -m "Initial commit"

Connect to GitHub repository:

git remote add origin <repository-url>
git branch -M main
git push -u origin main

Update files and push changes:

git add .
git commit -m "Update files"
git push

License

This project is licensed under the MIT License.

