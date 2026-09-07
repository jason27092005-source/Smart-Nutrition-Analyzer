# Microsoft Excel Data Analysis Guide
## Smart Nutrition Analyzer Dataset

This guide explains step-by-step how to perform practical Exploratory Data Analysis (EDA) on the `nutrition_data.csv` file using Microsoft Excel. This is ideal for lab records, project reports, and viva demonstrations.

---

### 1. Opening the Dataset in Excel
1. Launch **Microsoft Excel**.
2. Go to **File -> Open -> Browse**.
3. Navigate to `Smart-Nutrition-Analyzer/data/nutrition_data.csv`.
4. Ensure the file opens with columns clearly separated (Food_ID, Food_Name, Food_Category, Calories, Protein, etc.).
5. Save a copy as `nutrition_analysis.xlsx` for interactive editing.

---

### 2. Sorting & Conditional Formatting
- **Identify Highest Protein Foods:**
  1. Select the `Protein` column.
  2. Go to **Data -> Sort -> Descending (Z to A)**.
  3. Notice that chicken breast, fish, and legumes appear at the top.
- **Calorie Heatmap:**
  1. Highlight the `Calories` column.
  2. Go to **Home -> Conditional Formatting -> Color Scales -> Green - Yellow - Red**.
  3. Green indicates low calorie density (leafy vegetables, fruits); Red indicates high calorie density (fried snacks, sweets).

---

### 3. Creating Pivot Tables
A Pivot Table allows you to summarize 1,000+ rows into clean category averages in seconds.

#### Pivot Table 1: Category-Wise Average Nutrition
1. Select the entire table (`Ctrl + A`).
2. Click **Insert -> PivotTable -> New Worksheet**.
3. Set the fields:
   - **Rows:** `Food_Category`
   - **Values (Summarize by Average):**
     - `Average of Calories`
     - `Average of Protein`
     - `Average of Fiber`
     - `Average of Fat`
4. Format numbers to 1 decimal place.

#### Pivot Table 2: Diet Type Breakdown
1. Insert another Pivot Table.
2. Drag `Vegetarian` to **Rows** (0 = Non-Veg, 1 = Veg).
3. Drag `Food_ID` to **Values** (Summarize by Count).
4. Drag `Meal_Type` to **Columns** to see breakfast vs lunch vs dinner items across diet types.

---

### 4. Recommended Excel Charts for Project Reports
1. **Calorie Comparison Bar Chart:**
   - Select the Pivot Table showing `Food_Category` and `Average of Calories`.
   - Click **Insert -> Clustered Column Chart**.
   - Add chart title: *"Average Energy (kcal) Across Food Groups"*.
2. **Protein vs Fiber Clustered Bar:**
   - Select categories with `Average of Protein` and `Average of Fiber`.
   - Click **Insert -> 2D Bar Chart**.
   - Demonstrates that pulses provide balanced amounts of both protein and dietary fiber.

