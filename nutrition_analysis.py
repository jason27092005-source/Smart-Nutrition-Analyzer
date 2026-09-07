import os
import joblib
import numpy as np
import pandas as pd

# Path to trained model and dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'nutrition_model.pkl')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'nutrition_data.csv')

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate Body Mass Index (BMI) and assign a screening category.
    Formula: BMI = weight (kg) / (height (m) ^ 2)
    Note: BMI is a screening metric and not a clinical diagnosis.
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, 'Invalid Input', 'Please enter valid positive numbers for height and weight.'
    
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = 'Underweight'
        advice = 'A nutrient-dense, calorie-supportive diet with healthy proteins and fats may help support healthy weight gain.'
    elif 18.5 <= bmi < 24.9:
        category = 'Normal weight'
        advice = 'Your BMI is in the healthy screening range. Focus on diverse whole foods and regular physical activity.'
    elif 25.0 <= bmi < 29.9:
        category = 'Overweight'
        advice = 'A fiber-rich, moderately calorie-controlled diet with portion awareness can help maintain healthy weight management.'
    else:
        category = 'Obese'
        advice = 'Prioritize unprocessed whole foods and dietary fiber. Please consult a qualified nutritionist or physician for personalized guidance.'
        
    return bmi, category, advice

def calculate_daily_calories(age, gender, weight_kg, height_cm, activity_level, goal):
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor formula,
    Total Daily Energy Expenditure (TDEE), and goal-adjusted daily calories.
    """
    # Mifflin-St Jeor Equation
    if str(gender).strip().lower() == 'male':
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + 5.0
    else:
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) - 161.0
        
    # Standard Physical Activity Multipliers
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderately Active': 1.55,
        'Very Active': 1.725,
        'Extra Active': 1.9
    }
    multiplier = activity_multipliers.get(activity_level, 1.375)
    tdee = round(bmr * multiplier)
    
    # Safe, moderate goal adjustments
    if goal == 'Weight Loss':
        target_calories = max(1200, tdee - 400)
    elif goal == 'Muscle Gain':
        target_calories = tdee + 350
    else:  # Maintain Weight / Balanced
        target_calories = tdee
        
    return round(bmr), round(tdee), round(target_calories)

def calculate_macronutrients(target_calories, weight_kg, goal):
    """
    Calculate recommended macronutrient ranges in grams:
    - Protein (g) based on goal & bodyweight
    - Fat (g) roughly 25% of energy
    - Carbohydrates (g) remainder of energy
    - Dietary fiber (g) standard wellness target
    """
    if goal == 'Muscle Gain':
        protein_g = round(weight_kg * 1.8, 1)
    elif goal == 'Weight Loss':
        protein_g = round(weight_kg * 1.5, 1)
    else:
        protein_g = round(weight_kg * 1.3, 1)
        
    # Fat: 25% of daily calories (1g fat = 9 kcal)
    fat_cals = target_calories * 0.25
    fat_g = round(fat_cals / 9.0, 1)
    
    # Protein calories (1g protein = 4 kcal)
    protein_cals = protein_g * 4.0
    
    # Carbohydrates: Remaining calories (1g carb = 4 kcal)
    carb_cals = max(0.0, target_calories - protein_cals - fat_cals)
    carbs_g = round(carb_cals / 4.0, 1)
    
    # Dietary fiber target: approx 14g per 1000 kcal
    fiber_g = round((target_calories / 1000.0) * 14.0, 1)
    
    return {
        'protein_g': protein_g,
        'carbs_g': carbs_g,
        'fat_g': fat_g,
        'fiber_g': fiber_g
    }

def predict_nutrition_profile(age, bmi, calories, protein, carbs, fat, fiber):
    """
    Classify user dietary profile using the trained Scikit-learn Random Forest model.
    Returns predicted category and classification confidence percentage.
    """
    try:
        if os.path.exists(MODEL_PATH):
            payload = joblib.load(MODEL_PATH)
            model = payload['model']
            features = payload['features']
            
            input_df = pd.DataFrame([{
                'Age': age,
                'BMI': bmi,
                'Daily_Calories': calories,
                'Protein': protein,
                'Carbohydrates': carbs,
                'Fat': fat,
                'Fiber': fiber
            }])[features]
            
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            confidence = round(float(np.max(probabilities)) * 100, 1)
            return prediction, confidence
    except Exception as e:
        print(f"Model prediction exception: {e}")
        
    # Explainable heuristic fallback if model file is not present
    if calories < 1600 or protein < 45:
        return 'Low Nutrition Intake', 85.0
    elif calories > 2650:
        return 'High Calorie Intake', 85.0
    else:
        return 'Balanced', 90.0

def recommend_foods(goal, vegetarian, preferred_meal, target_calories, top_n=8):
    """
    Personalized food recommendation using content-based filtering:
    1. Filters by vegetarian preference
    2. Matches or prioritizes preferred meal type
    3. Scores items according to user goal
    4. Balances variety across diverse food categories
    """
    if not os.path.exists(DATA_PATH):
        return []
        
    df = pd.read_csv(DATA_PATH)
    
    # 1. Filter Vegetarian
    if vegetarian == 1 or str(vegetarian).lower() in ['1', 'yes', 'true', 'veg', 'vegetarian']:
        filtered_df = df[df['Vegetarian'] == 1].copy()
    else:
        filtered_df = df.copy()
        
    # 2. Score based on user goal
    if goal == 'Muscle Gain':
        filtered_df['Score'] = (filtered_df['Protein'] * 3.0) + (filtered_df['Fiber'] * 1.5) - (filtered_df['Calories'] * 0.05)
    elif goal == 'Weight Loss':
        filtered_df['Score'] = (filtered_df['Fiber'] * 4.0) + (filtered_df['Protein'] * 2.0) - (filtered_df['Calories'] * 0.1) - (filtered_df['Sugar'] * 1.5)
    else:  # Maintain / Balanced
        filtered_df['Score'] = (filtered_df['Protein'] * 2.0) + (filtered_df['Fiber'] * 2.0) - abs(filtered_df['Calories'] - 180) * 0.05
        
    # Boost if matches preferred meal type
    if preferred_meal and str(preferred_meal).lower() not in ['all', 'any']:
        filtered_df.loc[filtered_df['Meal_Type'].str.lower() == preferred_meal.lower(), 'Score'] += 10
        
    # Group by category to ensure balanced variety in recommendations
    categories = filtered_df['Food_Category'].unique()
    recommended_items = []
    
    for cat in categories:
        cat_items = filtered_df[filtered_df['Food_Category'] == cat].sort_values(by='Score', ascending=False)
        if not cat_items.empty:
            top_cat = cat_items.head(2).to_dict(orient='records')
            recommended_items.extend(top_cat)
            
    # Sort overall recommendations by score
    recommended_items.sort(key=lambda x: x.get('Score', 0), reverse=True)
    return recommended_items[:top_n]

