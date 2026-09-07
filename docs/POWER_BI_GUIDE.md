# Microsoft Power BI Dashboard Guide
## Smart Nutrition Analyzer Business Intelligence Report

This guide outlines how to build an academic Business Intelligence dashboard in Microsoft Power BI using the project dataset.

---

### 1. Connecting Data to Power BI
1. Open **Power BI Desktop**.
2. Click **Get Data -> Text/CSV**.
3. Select `Smart-Nutrition-Analyzer/data/nutrition_data.csv` and click **Load**.
4. *(Optional MySQL Connection)*: Click **Get Data -> MySQL Database**, enter server `localhost` and database `smart_nutrition`.

---

### 2. Adding Calculated Measures (DAX)
In the **Data** pane, right-click the table and click **New Measure**:

1. **Total Foods:**
   ```dax
   Total Foods = COUNT(nutrition_data[Food_ID])
   ```
2. **Average Calories:**
   ```dax
   Average Calories = AVERAGE(nutrition_data[Calories])
   ```
3. **Average Protein (g):**
   ```dax
   Average Protein = AVERAGE(nutrition_data[Protein])
   ```
4. **Average Fiber (g):**
   ```dax
   Average Fiber = AVERAGE(nutrition_data[Fiber])
   ```

---

### 3. Recommended Dashboard Visuals
Arrange the report page cleanly with the following 5 visuals:

#### 1. Top KPI Summary Cards (Horizontal Strip)
- Add 4 **Card** visuals across the top of the canvas:
  - Card 1: `Total Foods`
  - Card 2: `Average Calories` (Display as "138.8 kcal")
  - Card 3: `Average Protein` (Display as "7.3 g")
  - Card 4: `Average Fiber` (Display as "3.1 g")

#### 2. Calories by Food Category (Clustered Column Chart)
- **X-Axis:** `Food_Category`
- **Y-Axis:** `Average of Calories`
- **Data Color:** Soft Amber / Orange

#### 3. Protein Content Across Food Groups (Horizontal Bar Chart)
- **Y-Axis:** `Food_Category`
- **X-Axis:** `Average of Protein`
- **Data Color:** Forest Green

#### 4. Vegetarian vs Non-Vegetarian Proportion (Donut Chart)
- **Legend:** `Vegetarian` (Rename 0 as "Non-Vegetarian", 1 as "Vegetarian")
- **Values:** `Count of Food_ID`

#### 5. Meal Type Distribution (Treemap / Stacked Column)
- **Category:** `Meal_Type` (Breakfast, Lunch, Dinner, Snack)
- **Values:** `Count of Food_ID`

---

### 4. Interactive Slicers for Viva Demo
- Add a **Slicer** visual for `Cuisine` (Indian, Global, Italian, Mediterranean, Tropical, Asian).
- Add a **Slicer** visual for `Vegetarian`.
- **Viva Demo Tip:** Click on the "Indian" cuisine slicer during your presentation to show how the entire dashboard dynamically updates to reflect Indian dietary averages.

