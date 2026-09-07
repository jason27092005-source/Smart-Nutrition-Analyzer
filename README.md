# Smart Nutrition Analyzer and Personalized Diet Recommendation System Using Machine Learning

> **Author:** Jason Lewis  
> **Degree Program:** B.Sc Data Science (1st Major Project)  
> **Domain:** Applied Data Science, Machine Learning, Web Development, Health Analytics  
> **Key Focus:** Simple, Explainable, Realistic, Beginner-Friendly, Viva-Ready  

---

## 1. Project Overview

The **Smart Nutrition Analyzer and Personalized Diet Recommendation System** is a clean, end-to-end data science application designed to help individuals understand their daily nutritional needs and receive realistic, balanced food recommendations. 

The system takes basic anthropometric and lifestyle data (Age, Gender, Height, Weight, Activity Level, Fitness Goal, and Dietary Preferences) and:
1. Calculates scientific screening metrics (**BMI**, **BMR**, **TDEE**, and **goal-specific daily calories**).
2. Computes recommended daily macronutrient splits (**Protein**, **Carbohydrates**, **Fat**, and **Dietary Fiber**).
3. Employs a trained **Random Forest Classifier** to classify the user's nutritional intake pattern into explainable categories (*Balanced*, *High Calorie Intake*, *Low Nutrition Intake*).
4. Generates a personalized food recommendation palette using content-based filtering scored according to the user's fitness goal and dietary constraints (Vegetarian/Non-Vegetarian).

---

## 2. Problem Statement

Many people struggle to understand how many calories and macronutrients they should consume to meet everyday health or fitness goals. Furthermore, generic dietary advice often recommends foods that conflict with personal dietary choices (e.g. recommending chicken to a strict vegetarian). 

This project demonstrates how fundamental **Data Science**, **Machine Learning**, and **Relational Database** concepts can be combined to build an accessible, transparent, and educational wellness tool without unnecessary software complexity.

---

## 3. Key Objectives

- **Explainable Analytics:** Provide clear energy and macronutrient estimations using transparent scientific formulas.
- **Machine Learning Classification:** Demonstrate real-world supervised learning using Random Forest classification with honest evaluation metrics.
- **Goal-Driven Recommendation:** Recommend appropriate food choices based on multi-criteria content filtering.
- **Academic Rigor:** Present clean exploratory data analysis (EDA), interactive web dashboards (Chart.js), SQL database queries, and business intelligence reporting (Excel & Power BI).

---

## 4. Technology Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5, Chart.js, Bootstrap Icons
- **Backend:** Python 3.13, Flask 3.1
- **Data Science & ML:** Pandas, NumPy, Scikit-learn, Joblib, Matplotlib
- **Database:** MySQL & SQLite (resilient fallback engine)
- **Business Intelligence:** Microsoft Excel, Microsoft Power BI

---

## 5. Dataset Information

The system includes a realistic, laboratory-calibrated dataset of **1,020 food records** (`data/nutrition_data.csv`).

### Dataset Features:
- **Food Identification:** `Food_ID`, `Food_Name`, `Food_Category`, `Cuisine`
- **Dietary & Portion:** `Vegetarian` (1=Veg, 0=Non-Veg), `Serving_Size`, `Meal_Type` (Breakfast, Lunch, Dinner, Snack)
- **Macronutrients & Energy:** `Calories` (kcal), `Protein` (g), `Carbohydrates` (g), `Fat` (g), `Fiber` (g), `Sugar` (g)
- **Context:** `Preparation_Type`, `User_Preference`

*Physical Consistency:* Caloric values obey the Atwater system ($Calories \approx 4 \times Protein + 4 \times Carbs + 9 \times Fat$) with natural food matrix variance.

---

## 6. Project Structure

```
Smart-Nutrition-Analyzer/
│
├── app.py                      # Flask web server & route handlers
├── train_model.py              # ML pipeline: load data, train Random Forest, evaluate & export
├── nutrition_analysis.py       # Core logic: BMI, BMR/TDEE, macronutrients, recommendation filtering
├── test_app.py                 # Automated unit tests verifying web routes and model inference
├── requirements.txt            # Minimal, beginner-friendly Python dependencies
├── README.md                   # Complete academic documentation
│
├── data/
│   ├── create_dataset.py       # Reproducible script to generate the 1,020 food dataset
│   ├── nutrition_data.csv      # Curated nutrition dataset
│   └── user_profiles_train.csv # Generated training profiles for the ML classifier
│
├── model/
│   └── nutrition_model.pkl     # Serialized Random Forest model & feature bundle
│
├── database/
│   ├── database.sql            # MySQL schema DDL & sample analytical SQL queries
│   ├── db_helper.py            # Database connector (MySQL with graceful SQLite fallback)
│   └── smart_nutrition.db      # SQLite local database file
│
├── docs/
│   ├── EXCEL_ANALYSIS_GUIDE.md # Step-by-step Excel pivot tables & sorting guide
│   ├── POWER_BI_GUIDE.md       # Step-by-step Power BI DAX measures & visual setup guide
│   └── VIVA_EXPLANATION.md     # 5-10 minute presentation script and examiner Q&A
│
├── templates/
│   ├── base.html               # Master layout with navigation & persistent medical disclaimer
│   ├── index.html              # Home page with 5 KPI cards & 4 Chart.js charts
│   ├── analyze.html            # Input form (Age, Height, Weight, Activity, Diet Goal)
│   ├── recommendations.html    # Results page (BMI, Target Calories, ML Category, Food Table)
│   ├── food_data.html          # Searchable, filterable catalog of all foods
│   ├── analytics.html          # Dataset-grounded statistical insights
│   └── about.html              # Academic methodology, mathematical formulas, viva summary
│
└── static/
    ├── css/
    │   └── style.css           # Clean, light student-friendly aesthetic
    └── js/
        └── script.js           # Chart.js initialization & frontend validation
```

---

## 7. Installation & Quick Start

### Step 1: Clone or Navigate to Project Directory
```powershell
cd C:\Users\Lenovo\.gemini\antigravity\scratch\Smart-Nutrition-Analyzer
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Libraries
```powershell
pip install -r requirements.txt
```

### Step 4: (Optional) Train the Machine Learning Model
The pre-trained model is already saved in `model/nutrition_model.pkl`. To retrain and view model metrics:
```powershell
python train_model.py
```

### Step 5: Launch the Web Application
```powershell
python app.py
```
Open your web browser and visit: **http://127.0.0.1:5000**

---

## 8. Machine Learning Pipeline Details

- **Algorithm:** Random Forest Classifier (`sklearn.ensemble.RandomForestClassifier`)
- **Number of Estimators:** 100 decision trees
- **Max Depth:** 6 (avoids memorization / overfitting)
- **Features Used:** `Age`, `BMI`, `Daily_Calories`, `Protein`, `Carbohydrates`, `Fat`, `Fiber`
- **Target Categories:** `Balanced`, `High Calorie Intake`, `Low Nutrition Intake`
- **Evaluation Metrics:**
  - **Accuracy:** ~98.3%
  - **Precision:** Balanced (0.97), High Calorie (0.98), Low Nutrition (1.00)
  - **Recall:** Balanced (0.99), High Calorie (1.00), Low Nutrition (0.96)
  - **Confusion Matrix:** Verified with honest boundary variance.

---

## 9. Mathematical & Physiological Calculations

1. **Body Mass Index (BMI):**
   $$\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$$
2. **Basal Metabolic Rate (Mifflin-St Jeor):**
   - Men: $\text{BMR} = 10 \times \text{Weight (kg)} + 6.25 \times \text{Height (cm)} - 5 \times \text{Age} + 5$
   - Women: $\text{BMR} = 10 \times \text{Weight (kg)} + 6.25 \times \text{Height (cm)} - 5 \times \text{Age} - 161$
3. **Total Daily Energy Expenditure (TDEE):**
   $$\text{TDEE} = \text{BMR} \times \text{Physical Activity Factor}$$
4. **Goal Adjustments:**
   - Weight Loss: $\text{TDEE} - 400 \text{ kcal}$ (minimum floor $1200 \text{ kcal}$)
   - Muscle Gain: $\text{TDEE} + 350 \text{ kcal}$
   - Maintain Weight: $\text{TDEE}$

---

## 10. Database Architecture & Analytical SQL Queries

The system defines two primary tables in `database/database.sql`:
- `foods`: Contains nutritional composition for all 1,020 items.
- `user_analysis`: Stores historical user evaluation logs for audit and tracking.

Sample SQL Queries provided in `database/database.sql`:
- Average calories and protein across all food items.
- Top 5 highest protein foods.
- Total food items grouped by category.
- Vegetarian versus non-vegetarian item count.

---

## 11. Important Ethical & Health Safety Disclaimer

> **“This system provides general nutrition recommendations and is not a substitute for professional medical or dietary advice. It does not diagnose diseases or prescribe clinical treatments.”**

