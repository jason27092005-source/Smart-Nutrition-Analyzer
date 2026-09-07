import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
import nutrition_analysis as na
from database import db_helper

app = Flask(__name__)
app.secret_key = 'smart-nutrition-secret-key-bsc-ds'

# Load Dataset for Dashboard Analytics
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'nutrition_data.csv')

def get_dataset():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

@app.route('/')
def index():
    """Home / Dashboard Page with KPIs and Chart.js visualizations."""
    df = get_dataset()
    if df.empty:
        flash("Dataset file not found. Please verify data/nutrition_data.csv exists.", "warning")
        return render_template('index.html', kpis={}, chart_data={})

    # KPI Calculations
    kpis = {
        'total_foods': int(len(df)),
        'avg_calories': round(float(df['Calories'].mean()), 1),
        'avg_protein': round(float(df['Protein'].mean()), 1),
        'avg_fiber': round(float(df['Fiber'].mean()), 1),
        'total_categories': int(df['Food_Category'].nunique())
    }

    # Chart 1 & 2: Category Averages (Calories & Protein)
    cat_summary = df.groupby('Food_Category')[['Calories', 'Protein', 'Carbohydrates', 'Fat']].mean().round(1)
    categories = list(cat_summary.index)
    cat_calories = [float(x) for x in cat_summary['Calories']]
    cat_protein = [float(x) for x in cat_summary['Protein']]

    # Chart 3: Overall Average Macronutrient Distribution
    avg_protein_g = float(df['Protein'].mean())
    avg_carbs_g = float(df['Carbohydrates'].mean())
    avg_fat_g = float(df['Fat'].mean())

    # Chart 4: Food Distribution by Category (Count)
    cat_counts = df['Food_Category'].value_counts()
    cat_count_labels = list(cat_counts.index)
    cat_count_values = [int(x) for x in cat_counts.values]

    chart_data = {
        'categories': categories,
        'cat_calories': cat_calories,
        'cat_protein': cat_protein,
        'macro_labels': ['Carbohydrates (g)', 'Protein (g)', 'Fat (g)'],
        'macro_values': [round(avg_carbs_g, 1), round(avg_protein_g, 1), round(avg_fat_g, 1)],
        'cat_count_labels': cat_count_labels,
        'cat_count_values': cat_count_values
    }

    return render_template('index.html', kpis=kpis, chart_data=chart_data)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Form to collect user data and compute nutritional analysis."""
    if request.method == 'POST':
        try:
            # 1. Extract and validate user inputs
            age_str = request.form.get('age', '').strip()
            gender = request.form.get('gender', 'Male').strip()
            height_str = request.form.get('height', '').strip()
            weight_str = request.form.get('weight', '').strip()
            activity_level = request.form.get('activity_level', 'Moderately Active')
            goal = request.form.get('goal', 'Maintain Weight')
            vegetarian_val = request.form.get('vegetarian', '1')
            preferred_meal = request.form.get('meal_type', 'All')
            meals_per_day = request.form.get('meals_per_day', '3')

            # Validation checks
            if not age_str or not height_str or not weight_str:
                flash('Please fill in all required fields (Age, Height, Weight).', 'danger')
                return redirect(url_for('analyze'))

            age = int(age_str)
            height = float(height_str)
            weight = float(weight_str)

            if age < 12 or age > 100:
                flash('Please enter a realistic age between 12 and 100.', 'warning')
                return redirect(url_for('analyze'))

            if height < 90 or height > 250:
                flash('Please enter a realistic height between 90 cm and 250 cm.', 'warning')
                return redirect(url_for('analyze'))

            if weight < 25 or weight > 250:
                flash('Please enter a realistic weight between 25 kg and 250 kg.', 'warning')
                return redirect(url_for('analyze'))

            is_veg = 1 if vegetarian_val in ['1', 'yes', 'true', 'veg'] else 0

            # 2. Nutrition Calculations
            bmi, bmi_category, bmi_advice = na.calculate_bmi(weight, height)
            bmr, tdee, target_calories = na.calculate_daily_calories(age, gender, weight, height, activity_level, goal)
            macros = na.calculate_macronutrients(target_calories, weight, goal)

            # 3. Machine Learning Profile Classification
            ml_category, confidence = na.predict_nutrition_profile(
                age=age,
                bmi=bmi,
                calories=target_calories,
                protein=macros['protein_g'],
                carbs=macros['carbs_g'],
                fat=macros['fat_g'],
                fiber=macros['fiber_g']
            )

            # 4. Personalized Food Recommendations
            recommendations = na.recommend_foods(
                goal=goal,
                vegetarian=is_veg,
                preferred_meal=preferred_meal,
                target_calories=target_calories,
                top_n=8
            )

            # 5. Persist run to Database
            db_helper.save_user_analysis(age, gender, height, weight, bmi, activity_level, goal, ml_category)

            # Package result bundle
            user_profile = {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'activity_level': activity_level,
                'goal': goal,
                'is_veg': is_veg,
                'preferred_meal': preferred_meal,
                'meals_per_day': meals_per_day
            }

            analysis_results = {
                'bmi': bmi,
                'bmi_category': bmi_category,
                'bmi_advice': bmi_advice,
                'bmr': bmr,
                'tdee': tdee,
                'target_calories': target_calories,
                'macros': macros,
                'ml_category': ml_category,
                'confidence': confidence,
                'recommendations': recommendations
            }

            return render_template('recommendations.html', profile=user_profile, results=analysis_results)

        except ValueError:
            flash('Invalid input numerical format. Please check your entered values.', 'danger')
            return redirect(url_for('analyze'))
        except Exception as e:
            flash(f'An error occurred during analysis: {str(e)}', 'danger')
            return redirect(url_for('analyze'))

    return render_template('analyze.html')

@app.route('/food-data')
def food_data():
    """Browse, filter, and search the food nutrition dataset."""
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', 'All')
    veg_filter = request.args.get('vegetarian', 'All')

    df = get_dataset()
    categories = ['All'] + sorted(df['Food_Category'].unique().tolist()) if not df.empty else ['All']

    foods = db_helper.get_food_records(
        search_query=search_query if search_query else None,
        category_filter=category_filter,
        veg_filter=veg_filter,
        limit=150
    )

    return render_template('food_data.html', 
                           foods=foods, 
                           categories=categories,
                           selected_search=search_query,
                           selected_category=category_filter,
                           selected_veg=veg_filter)

@app.route('/analytics')
def analytics():
    """Data Science insights and dataset-grounded statistics."""
    df = get_dataset()
    if df.empty:
        return render_template('analytics.html', insights={})

    # Dataset-grounded statistics
    high_protein_foods = df.sort_values(by='Protein', ascending=False).head(5)[
        ['Food_Name', 'Food_Category', 'Protein', 'Calories', 'Serving_Size']
    ].to_dict(orient='records')

    high_fiber_foods = df.sort_values(by='Fiber', ascending=False).head(5)[
        ['Food_Name', 'Food_Category', 'Fiber', 'Calories', 'Serving_Size']
    ].to_dict(orient='records')

    low_cal_density = df.sort_values(by='Calories', ascending=True).head(5)[
        ['Food_Name', 'Food_Category', 'Calories', 'Serving_Size']
    ].to_dict(orient='records')

    category_summary = df.groupby('Food_Category').agg({
        'Calories': 'mean',
        'Protein': 'mean',
        'Carbohydrates': 'mean',
        'Fat': 'mean',
        'Fiber': 'mean',
        'Food_ID': 'count'
    }).round(1).reset_index().rename(columns={'Food_ID': 'Item_Count'}).to_dict(orient='records')

    veg_count = int((df['Vegetarian'] == 1).sum())
    non_veg_count = int((df['Vegetarian'] == 0).sum())

    insights = {
        'total_records': len(df),
        'high_protein': high_protein_foods,
        'high_fiber': high_fiber_foods,
        'low_cal': low_cal_density,
        'category_summary': category_summary,
        'veg_count': veg_count,
        'non_veg_count': non_veg_count
    }

    return render_template('analytics.html', insights=insights)

@app.route('/about')
def about():
    """Academic project documentation, methodology, and viva explanation."""
    return render_template('about.html')

if __name__ == '__main__':
    print("Starting Smart Nutrition Analyzer Flask Server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True, host='127.0.0.1', port=5000)

