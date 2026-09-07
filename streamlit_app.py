import os
import streamlit as st
import pandas as pd
import numpy as np
import nutrition_analysis as na

# Page Configuration
st.set_page_config(
    page_title="Smart Nutrition Analyzer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2e7d32;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2e7d32;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .disclaimer-box {
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #92400e;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'nutrition_data.csv')

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

df = load_data()

# Navigation Sidebar
st.sidebar.title("🥗 Smart Nutrition")
st.sidebar.caption("B.Sc Data Science Project")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Analyze My Nutrition", "Food Catalog", "Analytics", "About Project"]
)

# Persistent Disclaimer in Sidebar
st.sidebar.markdown("---")
st.sidebar.info(
    "⚠️ **Educational Disclaimer:**\n\n"
    "This tool provides general nutrition estimations and is not a substitute for medical or dietary advice."
)

# -----------------------------------------------------------
# 1. DASHBOARD
# -----------------------------------------------------------
if menu == "Dashboard":
    st.markdown('<div class="main-header">Smart Nutrition Analyzer & Recommendation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">A machine learning-driven system for nutritional assessment and personalized diet recommendations.</div>', unsafe_allow_html=True)

    if df.empty:
        st.error("Dataset could not be loaded. Please ensure data/nutrition_data.csv exists.")
    else:
        # KPI Row
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.metric("Total Foods", f"{len(df):,}")
        with kpi2:
            st.metric("Avg Calories", f"{df['Calories'].mean():.1f} kcal")
        with kpi3:
            st.metric("Avg Protein", f"{df['Protein'].mean():.1f} g")
        with kpi4:
            st.metric("Avg Fiber", f"{df['Fiber'].mean():.1f} g")
        with kpi5:
            st.metric("Food Categories", f"{df['Food_Category'].nunique()}")

        st.markdown("---")

        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Calories by Food Category")
            cat_cals = df.groupby('Food_Category')['Calories'].mean().sort_values()
            st.bar_chart(cat_cals, color="#f59e0b")

        with col2:
            st.subheader("Protein by Food Category")
            cat_prot = df.groupby('Food_Category')['Protein'].mean().sort_values()
            st.bar_chart(cat_prot, color="#2e7d32")

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Food Distribution by Category")
            cat_counts = df['Food_Category'].value_counts()
            st.bar_chart(cat_counts, color="#3b82f6")

        with col4:
            st.subheader("Average Macronutrients (Dataset)")
            macros = pd.Series({
                'Carbohydrates (g)': df['Carbohydrates'].mean(),
                'Protein (g)': df['Protein'].mean(),
                'Fat (g)': df['Fat'].mean()
            })
            st.bar_chart(macros, color="#8b5cf6")

# -----------------------------------------------------------
# 2. ANALYZE MY NUTRITION
# -----------------------------------------------------------
elif menu == "Analyze My Nutrition":
    st.markdown('<div class="main-header">Personalized Nutrition & Diet Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enter your lifestyle attributes to calculate energy needs and receive diet recommendations.</div>', unsafe_allow_html=True)

    with st.form("nutrition_form"):
        st.subheader("1. Physical Attributes")
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            age = st.number_input("Age (years)", min_value=12, max_value=100, value=21, step=1)
        with f_col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
        with f_col3:
            height = st.number_input("Height (cm)", min_value=90.0, max_value=250.0, value=175.0, step=0.5)

        f_col4, f_col5 = st.columns(2)
        with f_col4:
            weight = st.number_input("Weight (kg)", min_value=25.0, max_value=250.0, value=65.0, step=0.5)
        with f_col5:
            activity = st.selectbox("Activity Level", [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Extra Active"
            ], index=2)

        st.subheader("2. Dietary Preferences & Fitness Goal")
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            goal = st.selectbox("Fitness Goal", ["Maintain Weight", "Weight Loss", "Muscle Gain"])
        with g_col2:
            veg_option = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            meal_focus = st.selectbox("Preferred Meal Focus", ["All", "Breakfast", "Lunch", "Dinner", "Snack"])
        with p_col2:
            meals_count = st.selectbox("Meals Per Day", [3, 4, 5], index=0)

        submitted = st.form_submit_button("🔍 Analyze My Nutrition & Recommend Diet", type="primary")

    if submitted:
        is_veg = 1 if veg_option == "Vegetarian" else 0
        bmi, bmi_cat, bmi_adv = na.calculate_bmi(weight, height)
        bmr, tdee, target_cals = na.calculate_daily_calories(age, gender, weight, height, activity, goal)
        macros = na.calculate_macronutrients(target_cals, weight, goal)
        
        ml_cat, conf = na.predict_nutrition_profile(
            age, bmi, target_cals, 
            macros['protein_g'], macros['carbs_g'], macros['fat_g'], macros['fiber_g']
        )
        
        recs = na.recommend_foods(goal, is_veg, meal_focus, target_cals, top_n=8)

        st.success("✅ Analysis Complete! Here is your personalized summary:")

        # Summary Cards
        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        with r_col1:
            st.metric("Body Mass Index (BMI)", f"{bmi}", delta=bmi_cat, delta_color="normal")
        with r_col2:
            st.metric("Basal Metabolic Rate (BMR)", f"{bmr} kcal")
        with r_col3:
            st.metric("Maintenance (TDEE)", f"{tdee} kcal")
        with r_col4:
            st.metric("Target Energy", f"{target_cals} kcal/day")

        st.info(f"💡 **BMI Screening Guidance:** {bmi_adv}")

        # ML Classification Box
        st.subheader("🤖 Machine Learning Dietary Classification")
        ml_box1, ml_box2 = st.columns([3, 2])
        with ml_box1:
            st.markdown(f"#### Nutrition Category: **{ml_cat}**")
            st.write("Classified by evaluating your calculated calorie demand against required protein, fiber, and macronutrient ratios using our trained Random Forest model.")
        with ml_box2:
            st.write(f"**Model Confidence:** {conf}%")
            st.progress(conf / 100.0)

        # Macronutrients
        st.subheader("📊 Recommended Daily Macronutrients")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Protein", f"{macros['protein_g']} g", "Muscle health")
        with m2:
            st.metric("Carbohydrates", f"{macros['carbs_g']} g", "Daily energy")
        with m3:
            st.metric("Healthy Fat", f"{macros['fat_g']} g", "Hormone balance")
        with m4:
            st.metric("Dietary Fiber", f"{macros['fiber_g']} g", "Digestive health")

        # Recommendations Table
        st.subheader("🥗 Personalized Food Recommendations")
        if recs:
            df_recs = pd.DataFrame(recs)[[
                'Food_Name', 'Food_Category', 'Serving_Size', 'Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 'Meal_Type'
            ]]
            df_recs.columns = ['Food Item', 'Category', 'Serving Size', 'Calories (kcal)', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)', 'Meal']
            st.dataframe(df_recs, use_container_width=True, hide_index=True)
        else:
            st.warning("No matching foods found for your exact criteria.")

# -----------------------------------------------------------
# 3. FOOD CATALOG
# -----------------------------------------------------------
elif menu == "Food Catalog":
    st.markdown('<div class="main-header">Food Nutrition Catalog</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Explore and filter nutritional composition across 1,020 curated food items.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍 Search by Food Name", "")
    with c2:
        categories = ["All"] + sorted(df['Food_Category'].unique().tolist())
        selected_cat = st.selectbox("Category Filter", categories)
    with c3:
        veg_filter = st.selectbox("Diet Type", ["All", "Vegetarian", "Non-Vegetarian"])

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Food_Name'].str.contains(search, case=False, na=False)]
    if selected_cat != "All":
        filtered_df = filtered_df[filtered_df['Food_Category'] == selected_cat]
    if veg_filter == "Vegetarian":
        filtered_df = filtered_df[filtered_df['Vegetarian'] == 1]
    elif veg_filter == "Non-Vegetarian":
        filtered_df = filtered_df[filtered_df['Vegetarian'] == 0]

    st.write(f"Showing **{len(filtered_df)}** items:")
    display_cols = ['Food_ID', 'Food_Name', 'Food_Category', 'Serving_Size', 'Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 'Sugar', 'Meal_Type']
    st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

# -----------------------------------------------------------
# 4. ANALYTICS
# -----------------------------------------------------------
elif menu == "Analytics":
    st.markdown('<div class="main-header">Nutrition Data Science Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Exploratory Data Analysis (EDA) grounded directly in the curated dataset.</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        st.success("**High Protein Density:** Poultry, seafood, and legumes consistently deliver the highest protein-to-calorie ratios.")
    with a2:
        st.warning("**Caloric Dispersion:** Fried snacks and sweets average 250–320 kcal, while fresh vegetables average 45–80 kcal.")
    with a3:
        st.info("**Fiber Distribution:** Whole pulses, grains, and fruits contribute over 80% of dietary fiber.")

    st.subheader("Category-Wise Nutritional Averages")
    cat_summary = df.groupby('Food_Category').agg({
        'Calories': 'mean',
        'Protein': 'mean',
        'Carbohydrates': 'mean',
        'Fat': 'mean',
        'Fiber': 'mean',
        'Food_ID': 'count'
    }).round(1).rename(columns={'Food_ID': 'Item Count'})
    st.dataframe(cat_summary, use_container_width=True)

    st.subheader("Top Foods Highlights")
    h1, h2 = st.columns(2)
    with h1:
        st.write("🥩 **Top 5 High-Protein Foods**")
        st.dataframe(df.sort_values(by='Protein', ascending=False)[['Food_Name', 'Food_Category', 'Protein', 'Calories']].head(5), hide_index=True)
    with h2:
        st.write("🌾 **Top 5 High-Fiber Foods**")
        st.dataframe(df.sort_values(by='Fiber', ascending=False)[['Food_Name', 'Food_Category', 'Fiber', 'Calories']].head(5), hide_index=True)

# -----------------------------------------------------------
# 5. ABOUT PROJECT
# -----------------------------------------------------------
elif menu == "About Project":
    st.markdown('<div class="main-header">About This Project</div>', unsafe_allow_html=True)
    st.markdown("""
    ### Smart Nutrition Analyzer and Personalized Diet Recommendation System
    **B.Sc Data Science Final Project**

    #### 1. Objectives
    - **Energy Assessment:** Calculate daily energy requirements using Mifflin-St Jeor equation.
    - **Screening:** Anthropometric screening using Body Mass Index (BMI).
    - **Machine Learning Classification:** Classify nutritional intake profile (*Balanced*, *High Calorie Intake*, *Low Nutrition Intake*) using Scikit-Learn **Random Forest Classifier**.
    - **Personalized Recommendation:** Content-based multi-factor filtering matched to fitness goal and vegetarian preference.

    #### 2. Machine Learning Pipeline
    - **Model:** Random Forest Classifier (100 trees, max depth 6)
    - **Features:** Age, BMI, Daily Calories, Protein, Carbohydrates, Fat, Fiber
    - **Accuracy:** ~98.3%
    - **Target Leakage Prevention:** Verified that target category is not trivially computed from single features.

    #### 3. Tech Stack
    - Python, Pandas, NumPy, Scikit-learn, Joblib, Streamlit, Flask, Bootstrap 5, MySQL, Excel, Power BI.
    """)

# Global Footer Disclaimer
st.markdown("""
<div class="disclaimer-box">
    <strong>🛡️ Academic & Health Disclaimer:</strong><br>
    This system provides general nutrition recommendations for educational purposes and is not a substitute for professional medical or dietary advice. It does not diagnose diseases or prescribe clinical treatments.
</div>
""", unsafe_allow_html=True)
