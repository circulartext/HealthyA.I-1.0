import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Recommended Daily Intake (RDI) values for a male at 200 pounds
rdi = {
    "Probiotics (CFUs)": (10_000_000_000, 15_000_000_000),
    "Vitamin D3 (IU)": (1000, 2000),
    "Vitamin B12 (mcg)": (2.4, 2.4),
    "Magnesium (mg)": (400, 400),
    "Protein (g)": (56, 100),
    "Calcium (mg)": (1000, 1000),
    "Iron (mg)": (8, 10),
    "Potassium (mg)": (4700, 4700),
    "Omega-3 Fatty Acids (g)": (1.6, 1.8),
    "Total Fat (g)": (44, 78),
    "Saturated Fat (g)": (16, 22),
    "Trans Fat (g)": (0, 0),
    "Cholesterol (mg)": (0, 300),
    "Sodium (mg)": (1500, 2300),
    "Total Carbohydrate (g)": (130, 390),
    "Dietary Fiber (g)": (25, 30),
    "Total Sugars (g)": (0, 50),
    "Added Sugars (g)": (0, 25),
    "Zinc (mg)": (8, 11),
    "Vitamin C (%DV)": (75, 90),
    "Vitamin B6 (%DV)": (100, 100),
}

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

def read_food_data(filename):
    food_data = {}
    nutrient_keys = [
        "Serving Size (g)", "Calories", "Total Fat (g)", "Saturated Fat (g)", "Trans Fat (g)",
        "Cholesterol (mg)", "Sodium (mg)", "Total Carbohydrate (g)", "Dietary Fiber (g)",
        "Total Sugars (g)", "Added Sugars (g)", "Protein (g)", "Vitamin D3 (IU)",
        "Calcium (mg)", "Iron (mg)", "Potassium (mg)", "Zinc (mg)", "Vitamin B12 (mcg)",
        "Vitamin C (%DV)", "Vitamin B6 (%DV)", "Magnesium (mg)",
    ]
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_name = row['Food']
                food_data[food_name] = {}
                for nutrient in nutrient_keys:
                    value = row.get(nutrient, '0') or '0'
                    try:
                        food_data[food_name][nutrient] = float(value.replace(',', ''))
                    except ValueError:
                        food_data[food_name][nutrient] = 0.0
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    return food_data

def calculate_nutrient_intake(food_data, food_amounts):
    nutrient_intake = {}
    for food_item, amount in food_amounts.items():
        if amount > 0:
            serving_size = food_data[food_item]["Serving Size (g)"]
            for nutrient, value in food_data[food_item].items():
                if nutrient != "Serving Size (g)":
                    nutrient_intake[nutrient] = nutrient_intake.get(nutrient, 0) + (value / serving_size) * amount
    return nutrient_intake

def save_nutrient_intake_results(nutrient_intake, filename='nutrient_intake_results.csv'):
    results = {}
    for nutrient, intake in nutrient_intake.items():
        min_limit, max_limit = rdi.get(nutrient, (0, 0))
        results[nutrient] = {
            "intake": intake,
            "min": min_limit,
            "max": max_limit
        }

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nutrient", "Intake", "Min RDI", "Max RDI"])
        for nutrient, data in results.items():
            writer.writerow([nutrient, data["intake"], data["min"], data["max"]])

def calculate_nutrient_percentage(intake, min_limit, max_limit):
    if min_limit < max_limit:
        capped_intake = max(min(intake, max_limit), min_limit)
        percentage = (capped_intake - min_limit) / (max_limit - min_limit) * 100
        return min(percentage, 100)
    elif min_limit == 0 and max_limit > 0:
        return min((intake / max_limit) * 100, 100)
    return 0

def calculate_health_score(nutrient_intake):
    total_weighted_score = 0
    total_weight = 0

    for nutrient, category_weight in NUTRIENT_CATEGORY_WEIGHTS.items():
        intake = nutrient_intake.get(nutrient, 0)
        min_limit, max_limit = rdi.get(nutrient, (0, 0))
        nutrient_percentage = calculate_nutrient_percentage(intake, min_limit, max_limit)
        weighted_contribution = nutrient_percentage * category_weight
        total_weighted_score += weighted_contribution
        total_weight += abs(category_weight)

    health_score = max(0, min(100, (total_weighted_score / total_weight) + 50))

    return health_score

def save_health_score(health_score, filename='health_score_results.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Health Score", "Interpretation"])

        if health_score < 40:
            interpretation = "Poor Nutritional Health"
        elif health_score < 60:
            interpretation = "Below Average Nutritional Health"
        elif health_score < 75:
            interpretation = "Good Nutritional Health"
        elif health_score < 90:
            interpretation = "Excellent Nutritional Health"
        else:
            interpretation = "Optimal Nutritional Health"

        writer.writerow([f"{health_score:.2f}", interpretation])

def calculate_ideal_adjustments(nutrient_intake, current_health_score):
    adjustments = {}
    target_health_score = 100
    score_deficit = target_health_score - current_health_score

    # Calculate the total weight of positive and negative contributions
    total_positive_weight = sum(weight for weight in NUTRIENT_CATEGORY_WEIGHTS.values() if weight > 0)
    total_negative_weight = sum(abs(weight) for weight in NUTRIENT_CATEGORY_WEIGHTS.values() if weight < 0)

    for nutrient, weight in NUTRIENT_CATEGORY_WEIGHTS.items():
        intake = nutrient_intake.get(nutrient, 0)
        low, high = rdi.get(nutrient, (0, 0))

        if weight > 0 and intake < high:
            proportion = weight / total_positive_weight
            needed_increase = proportion * score_deficit * (high - intake) / 100
            adjustments[nutrient] = f"Increase by {needed_increase:.2f} units to reach optimal"

        elif weight < 0 and intake > low:
            proportion = abs(weight) / total_negative_weight
            needed_decrease = proportion * score_deficit * (intake - low) / 100
            adjustments[nutrient] = f"Decrease by {needed_decrease:.2f} units to reach optimal"

    return adjustments

def save_ideal_adjustments(adjustments, filename='ideal_adjustments.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nutrient", "Adjustment"])
        for nutrient, adjustment in adjustments.items():
            writer.writerow([nutrient, adjustment])

# Modified function to save only food names and amounts
def save_food_amounts(food_amounts, filename='food_amounts.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(["Food", "Amount (g)"])
        for food, amount in food_amounts.items():
            if amount > 0:
                writer.writerow([food, amount])

def save_data():
    food_amounts = {food: float(var.get() or 0) for food, var in food_amount_vars.items()}
    nutrient_intake = calculate_nutrient_intake(food_data, food_amounts)

    save_nutrient_intake_results(nutrient_intake)
    save_food_amounts(food_amounts)  # Save only food names and amounts

    health_score = calculate_health_score(nutrient_intake)
    save_health_score(health_score)

    adjustments = calculate_ideal_adjustments(nutrient_intake, health_score)
    save_ideal_adjustments(adjustments)

    messagebox.showinfo("Success", f"Nutrient intake results saved.\nHealth Score: {health_score:.2f}")

# Main application window
root = tk.Tk()
root.title("Nutrient Intake Tracker")

# Load food data
food_data = read_food_data('foods2.csv')

# Create a frame for the food items
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a dictionary to hold the amount variables
food_amount_vars = {}

# Add food items to the frame
for i, food_item in enumerate(food_data.keys()):
    ttk.Label(frame, text=food_item).grid(row=i, column=0, sticky=tk.W)
    amount_var = tk.StringVar()
    food_amount_vars[food_item] = amount_var
    ttk.Entry(frame, textvariable=amount_var, width=10).grid(row=i, column=1)

# Add a save button
ttk.Button(root, text="Save", command=save_data).grid(row=1, column=0, pady=10)

# Start the application
root.mainloop()