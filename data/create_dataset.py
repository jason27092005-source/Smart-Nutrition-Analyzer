import csv
import random

random.seed(42)

base_foods = [
    ('Rolled Oats (cooked)', 'Grains and Cereals', 'Global', 1, '1 cup (234g)', 166, 5.9, 28.1, 3.6, 4.0, 1.1, 'Breakfast', 'Boiled', 'Weight Loss'),
    ('Steel Cut Oats', 'Grains and Cereals', 'Global', 1, '1 cup (240g)', 170, 7.0, 29.0, 3.0, 5.0, 1.0, 'Breakfast', 'Boiled', 'Weight Loss'),
    ('Brown Rice (cooked)', 'Grains and Cereals', 'Indian', 1, '1 cup (195g)', 218, 4.5, 45.8, 1.6, 3.5, 0.7, 'Lunch', 'Boiled', 'Balanced'),
    ('White Basmati Rice (cooked)', 'Grains and Cereals', 'Indian', 1, '1 cup (180g)', 210, 4.3, 45.0, 0.6, 1.0, 0.2, 'Lunch', 'Boiled', 'Energy Booster'),
    ('Whole Wheat Roti', 'Grains and Cereals', 'Indian', 1, '1 piece (45g)', 120, 3.8, 22.0, 2.1, 3.2, 0.5, 'Dinner', 'Cooked', 'Balanced'),
    ('Multigrain Roti', 'Grains and Cereals', 'Indian', 1, '1 piece (50g)', 130, 4.5, 23.5, 2.3, 4.1, 0.6, 'Dinner', 'Cooked', 'Weight Loss'),
    ('Quinoa (cooked)', 'Grains and Cereals', 'Global', 1, '1 cup (185g)', 222, 8.1, 39.4, 3.6, 5.2, 1.6, 'Lunch', 'Boiled', 'Muscle Gain'),
    ('Millet Porridge (Ragi)', 'Grains and Cereals', 'Indian', 1, '1 cup (220g)', 155, 4.2, 31.0, 1.5, 4.8, 0.8, 'Breakfast', 'Boiled', 'Diabetes-Friendly'),
    ('Vegetable Poha', 'Grains and Cereals', 'Indian', 1, '1 plate (180g)', 230, 4.6, 38.0, 6.8, 3.5, 2.2, 'Breakfast', 'Cooked', 'Balanced'),
    ('Vegetable Upma', 'Grains and Cereals', 'Indian', 1, '1 plate (180g)', 220, 5.1, 36.5, 6.2, 3.2, 1.8, 'Breakfast', 'Cooked', 'Balanced'),
    ('Steamed Idli (2 pcs)', 'Grains and Cereals', 'Indian', 1, '2 pieces (120g)', 140, 4.8, 28.0, 0.8, 2.2, 0.4, 'Breakfast', 'Steamed', 'Balanced'),
    ('Plain Dosa', 'Grains and Cereals', 'Indian', 1, '1 medium (90g)', 168, 3.9, 29.0, 4.2, 1.8, 0.5, 'Breakfast', 'Cooked', 'Energy Booster'),
    ('Multigrain Bread Slice', 'Grains and Cereals', 'Global', 1, '1 slice (40g)', 95, 4.2, 16.0, 1.5, 2.8, 1.5, 'Breakfast', 'Baked', 'Balanced'),
    ('Whole Wheat Pasta', 'Grains and Cereals', 'Italian', 1, '1 cup (140g)', 174, 7.5, 37.0, 0.8, 6.3, 1.2, 'Dinner', 'Boiled', 'Muscle Gain'),
    ('Cornflakes with Milk', 'Grains and Cereals', 'Global', 1, '1 bowl (200g)', 180, 7.2, 34.0, 1.2, 1.5, 8.5, 'Breakfast', 'Raw', 'Energy Booster'),

    ('Yellow Moong Dal', 'Pulses and Legumes', 'Indian', 1, '1 katori (150g)', 150, 9.2, 22.0, 2.5, 5.4, 1.2, 'Lunch', 'Boiled', 'Balanced'),
    ('Masoor Dal', 'Pulses and Legumes', 'Indian', 1, '1 katori (150g)', 160, 10.1, 24.0, 2.2, 5.8, 1.0, 'Lunch', 'Boiled', 'Muscle Gain'),
    ('Toor Dal', 'Pulses and Legumes', 'Indian', 1, '1 katori (150g)', 165, 8.8, 25.5, 3.0, 5.0, 1.1, 'Lunch', 'Boiled', 'Balanced'),
    ('Chana Dal', 'Pulses and Legumes', 'Indian', 1, '1 katori (150g)', 175, 9.8, 26.0, 3.5, 6.2, 1.3, 'Lunch', 'Boiled', 'Diabetes-Friendly'),
    ('Chickpeas Curry (Chole)', 'Pulses and Legumes', 'Indian', 1, '1 cup (200g)', 240, 11.5, 34.0, 6.5, 7.8, 2.5, 'Lunch', 'Cooked', 'Muscle Gain'),
    ('Rajma (Kidney Beans)', 'Pulses and Legumes', 'Indian', 1, '1 cup (200g)', 230, 12.0, 33.0, 5.5, 8.5, 2.1, 'Lunch', 'Cooked', 'Muscle Gain'),
    ('Black Eyed Peas (Lobia)', 'Pulses and Legumes', 'Indian', 1, '1 cup (180g)', 195, 11.0, 31.0, 2.8, 7.2, 2.0, 'Dinner', 'Boiled', 'Balanced'),
    ('Sprouted Moong Salad', 'Pulses and Legumes', 'Indian', 1, '1 bowl (150g)', 125, 9.5, 18.0, 1.2, 6.5, 2.8, 'Snack', 'Raw', 'Weight Loss'),
    ('Boiled Green Edamame', 'Pulses and Legumes', 'Asian', 1, '1 cup (155g)', 188, 18.4, 13.8, 8.1, 8.0, 3.4, 'Snack', 'Boiled', 'Muscle Gain'),
    ('Black Dal Makhani Light', 'Pulses and Legumes', 'Indian', 1, '1 cup (200g)', 255, 10.5, 28.0, 10.5, 6.5, 1.8, 'Dinner', 'Cooked', 'Energy Booster'),

    ('Steamed Broccoli', 'Vegetables', 'Global', 1, '1 cup (150g)', 55, 3.7, 11.2, 0.6, 5.1, 2.2, 'Dinner', 'Steamed', 'Weight Loss'),
    ('Sauteed Spinach (Palak)', 'Vegetables', 'Indian', 1, '1 cup (180g)', 65, 4.2, 7.0, 2.5, 4.3, 0.8, 'Dinner', 'Cooked', 'Weight Loss'),
    ('Mixed Vegetable Sabzi', 'Vegetables', 'Indian', 1, '1 bowl (180g)', 120, 3.5, 16.0, 5.0, 4.8, 3.5, 'Lunch', 'Cooked', 'Balanced'),
    ('Cauliflower Sabzi', 'Vegetables', 'Indian', 1, '1 cup (150g)', 85, 3.0, 10.5, 3.8, 3.5, 2.5, 'Lunch', 'Cooked', 'Weight Loss'),
    ('Fresh Cucumber Salad', 'Vegetables', 'Global', 1, '1 bowl (150g)', 24, 1.0, 5.0, 0.2, 1.5, 2.2, 'Snack', 'Raw', 'Weight Loss'),
    ('Carrot and Beetroot Salad', 'Vegetables', 'Indian', 1, '1 bowl (150g)', 62, 1.8, 14.0, 0.4, 4.2, 8.0, 'Lunch', 'Raw', 'Balanced'),
    ('Bhindi Masala (Okra)', 'Vegetables', 'Indian', 1, '1 cup (150g)', 110, 2.8, 12.0, 5.5, 4.0, 2.2, 'Dinner', 'Cooked', 'Diabetes-Friendly'),
    ('Roasted Bell Peppers', 'Vegetables', 'Mediterranean', 1, '1 plate (180g)', 75, 2.5, 12.0, 2.2, 3.8, 4.5, 'Dinner', 'Roasted', 'Weight Loss'),
    ('Grilled Button Mushrooms', 'Vegetables', 'Global', 1, '1 cup (120g)', 45, 3.8, 4.5, 1.0, 2.1, 1.8, 'Dinner', 'Grilled', 'Weight Loss'),
    ('Boiled Sweet Potato', 'Vegetables', 'Global', 1, '1 medium (130g)', 112, 2.0, 26.0, 0.1, 3.9, 5.4, 'Snack', 'Boiled', 'Energy Booster'),
    ('Karela Sabzi (Bitter Gourd)', 'Vegetables', 'Indian', 1, '1 katori (120g)', 80, 2.2, 9.0, 4.0, 3.5, 1.5, 'Lunch', 'Cooked', 'Diabetes-Friendly'),
    ('Lauki (Bottle Gourd) Curry', 'Vegetables', 'Indian', 1, '1 cup (180g)', 70, 1.8, 8.5, 3.2, 3.0, 2.0, 'Dinner', 'Cooked', 'Weight Loss'),

    ('Fresh Apple with Skin', 'Fruits', 'Global', 1, '1 medium (182g)', 95, 0.5, 25.1, 0.3, 4.4, 18.9, 'Snack', 'Raw', 'Balanced'),
    ('Ripe Banana', 'Fruits', 'Global', 1, '1 medium (118g)', 105, 1.3, 27.0, 0.4, 3.1, 14.4, 'Breakfast', 'Raw', 'Energy Booster'),
    ('Fresh Orange', 'Fruits', 'Global', 1, '1 medium (131g)', 62, 1.2, 15.4, 0.2, 3.1, 12.2, 'Snack', 'Raw', 'Balanced'),
    ('Fresh Papaya Cubes', 'Fruits', 'Tropical', 1, '1 cup (145g)', 62, 0.7, 15.7, 0.4, 2.5, 11.3, 'Breakfast', 'Raw', 'Weight Loss'),
    ('Pomegranate Arils', 'Fruits', 'Indian', 1, '0.5 cup (87g)', 72, 1.5, 16.3, 1.0, 3.5, 11.9, 'Snack', 'Raw', 'Balanced'),
    ('Watermelon Slices', 'Fruits', 'Global', 1, '1 bowl (200g)', 60, 1.2, 15.0, 0.3, 0.8, 12.0, 'Snack', 'Raw', 'Weight Loss'),
    ('Fresh Guava', 'Fruits', 'Indian', 1, '1 medium (100g)', 68, 2.6, 14.3, 1.0, 5.4, 8.9, 'Snack', 'Raw', 'Diabetes-Friendly'),
    ('Strawberries', 'Fruits', 'Global', 1, '1 cup (152g)', 49, 1.0, 11.7, 0.5, 3.0, 7.4, 'Breakfast', 'Raw', 'Weight Loss'),
    ('Blueberries', 'Fruits', 'Global', 1, '1 cup (148g)', 84, 1.1, 21.4, 0.5, 3.6, 14.7, 'Breakfast', 'Raw', 'Balanced'),
    ('Fresh Kiwi Fruit', 'Fruits', 'Global', 1, '1 piece (69g)', 42, 0.8, 10.1, 0.4, 2.1, 6.2, 'Snack', 'Raw', 'Balanced'),
    ('Ripe Mango Slices', 'Fruits', 'Indian', 1, '1 cup (165g)', 99, 1.4, 24.7, 0.6, 2.6, 22.5, 'Snack', 'Raw', 'Energy Booster'),

    ('Low-fat Cow Milk', 'Dairy and Alternatives', 'Global', 1, '1 glass (240ml)', 102, 8.2, 12.2, 2.4, 0.0, 12.0, 'Breakfast', 'Boiled', 'Balanced'),
    ('Plain Curd (Dahi)', 'Dairy and Alternatives', 'Indian', 1, '1 cup (200g)', 120, 7.0, 9.0, 6.0, 0.0, 8.0, 'Lunch', 'Raw', 'Balanced'),
    ('Low-fat Greek Yogurt', 'Dairy and Alternatives', 'Global', 1, '1 cup (170g)', 130, 17.0, 6.0, 2.5, 0.0, 5.0, 'Snack', 'Raw', 'Muscle Gain'),
    ('Paneer (Fresh Cottage Cheese)', 'Dairy and Alternatives', 'Indian', 1, '100g', 265, 18.3, 3.6, 20.8, 0.0, 2.5, 'Lunch', 'Raw', 'Muscle Gain'),
    ('Grilled Paneer Tikka', 'Dairy and Alternatives', 'Indian', 1, '1 plate (150g)', 280, 19.5, 8.0, 18.0, 2.0, 3.0, 'Dinner', 'Grilled', 'Muscle Gain'),
    ('Firm Tofu', 'Dairy and Alternatives', 'Asian', 1, '100g', 83, 10.0, 2.1, 5.3, 1.2, 0.6, 'Lunch', 'Cooked', 'Weight Loss'),
    ('Unsweetened Soy Milk', 'Dairy and Alternatives', 'Global', 1, '1 glass (240ml)', 80, 7.0, 4.0, 4.0, 2.0, 1.0, 'Breakfast', 'Raw', 'Muscle Gain'),
    ('Unsweetened Almond Milk', 'Dairy and Alternatives', 'Global', 1, '1 glass (240ml)', 35, 1.2, 1.5, 2.8, 1.0, 0.2, 'Breakfast', 'Raw', 'Weight Loss'),
    ('Spiced Buttermilk (Chaas)', 'Dairy and Alternatives', 'Indian', 1, '1 glass (250ml)', 45, 2.8, 4.5, 1.5, 0.2, 4.0, 'Lunch', 'Raw', 'Weight Loss'),

    ('Hard Boiled Egg', 'Poultry and Seafood', 'Global', 0, '1 large (50g)', 78, 6.3, 0.6, 5.3, 0.0, 0.6, 'Breakfast', 'Boiled', 'Balanced'),
    ('Boiled Egg Whites (3 eggs)', 'Poultry and Seafood', 'Global', 0, '3 whites (100g)', 52, 11.0, 0.7, 0.2, 0.0, 0.7, 'Breakfast', 'Boiled', 'Muscle Gain'),
    ('Vegetable Egg Omelette', 'Poultry and Seafood', 'Global', 0, '2 eggs (140g)', 185, 13.5, 3.5, 13.0, 1.0, 1.5, 'Breakfast', 'Cooked', 'Muscle Gain'),
    ('Grilled Chicken Breast', 'Poultry and Seafood', 'Global', 0, '150g', 220, 38.0, 0.0, 5.5, 0.0, 0.0, 'Dinner', 'Grilled', 'Muscle Gain'),
    ('Homestyle Chicken Curry', 'Poultry and Seafood', 'Indian', 0, '1 bowl (200g)', 270, 28.0, 6.0, 14.5, 1.8, 1.5, 'Lunch', 'Cooked', 'Muscle Gain'),
    ('Grilled Salmon Fillet', 'Poultry and Seafood', 'Global', 0, '150g', 280, 32.0, 0.0, 16.0, 0.0, 0.0, 'Dinner', 'Grilled', 'Muscle Gain'),
    ('Fish Tikka Tandoori', 'Poultry and Seafood', 'Indian', 0, '150g', 210, 29.0, 4.0, 8.5, 1.0, 1.0, 'Dinner', 'Grilled', 'Weight Loss'),
    ('Tuna Salad Light', 'Poultry and Seafood', 'Global', 0, '1 bowl (180g)', 190, 26.0, 5.0, 6.5, 2.0, 1.2, 'Lunch', 'Raw', 'Weight Loss'),
    ('Boiled Shrimp', 'Poultry and Seafood', 'Global', 0, '100g', 99, 24.0, 0.2, 0.3, 0.0, 0.0, 'Dinner', 'Boiled', 'Weight Loss'),

    ('Raw Almonds', 'Nuts and Seeds', 'Global', 1, '1 handful (28g)', 164, 6.0, 6.1, 14.2, 3.5, 1.2, 'Snack', 'Raw', 'Balanced'),
    ('Walnut Halves', 'Nuts and Seeds', 'Global', 1, '1 handful (28g)', 185, 4.3, 3.9, 18.5, 1.9, 0.7, 'Snack', 'Raw', 'Balanced'),
    ('Chia Seeds', 'Nuts and Seeds', 'Global', 1, '1 tbsp (15g)', 73, 2.5, 6.3, 4.6, 5.1, 0.1, 'Breakfast', 'Raw', 'Weight Loss'),
    ('Ground Flaxseeds', 'Nuts and Seeds', 'Global', 1, '1 tbsp (10g)', 55, 1.9, 3.0, 4.2, 2.8, 0.2, 'Breakfast', 'Raw', 'Balanced'),
    ('Roasted Pumpkin Seeds', 'Nuts and Seeds', 'Global', 1, '1 handful (28g)', 158, 8.6, 4.2, 13.9, 1.8, 0.4, 'Snack', 'Roasted', 'Muscle Gain'),
    ('Natural Peanut Butter', 'Nuts and Seeds', 'Global', 1, '1 tbsp (16g)', 94, 4.0, 3.1, 8.1, 1.0, 1.1, 'Breakfast', 'Raw', 'Energy Booster'),
    ('Roasted Peanuts Unsalted', 'Nuts and Seeds', 'Indian', 1, '1 handful (30g)', 170, 7.5, 4.8, 14.5, 2.4, 1.2, 'Snack', 'Roasted', 'Energy Booster'),

    ('Roasted Makhana (Foxnuts)', 'Snacks and Beverages', 'Indian', 1, '1 bowl (30g)', 106, 2.9, 20.0, 0.5, 2.3, 0.2, 'Snack', 'Roasted', 'Weight Loss'),
    ('Roasted Chana', 'Snacks and Beverages', 'Indian', 1, '1 bowl (40g)', 145, 7.8, 22.0, 2.2, 5.2, 1.0, 'Snack', 'Roasted', 'Weight Loss'),
    ('Tender Coconut Water', 'Snacks and Beverages', 'Tropical', 1, '1 glass (240ml)', 46, 1.7, 8.9, 0.5, 2.6, 6.3, 'Snack', 'Raw', 'Balanced'),
    ('Green Tea Unsweetened', 'Snacks and Beverages', 'Global', 1, '1 cup (200ml)', 2, 0.2, 0.0, 0.0, 0.0, 0.0, 'Snack', 'Boiled', 'Weight Loss'),
    ('Vegetable Clear Soup', 'Snacks and Beverages', 'Global', 1, '1 bowl (200ml)', 45, 1.5, 8.0, 0.8, 2.5, 2.0, 'Dinner', 'Boiled', 'Weight Loss'),
    ('Homestyle Tomato Soup', 'Snacks and Beverages', 'Global', 1, '1 bowl (200ml)', 75, 2.0, 14.0, 1.8, 2.2, 7.5, 'Dinner', 'Boiled', 'Balanced'),

    ('Vegetable Samosa', 'Occasional Foods', 'Indian', 1, '1 piece (80g)', 262, 3.5, 32.0, 13.5, 2.1, 2.4, 'Snack', 'Fried', 'Energy Booster'),
    ('Potato French Fries', 'Occasional Foods', 'Global', 1, '1 serving (100g)', 312, 3.4, 41.4, 15.0, 3.8, 0.3, 'Snack', 'Fried', 'Energy Booster'),
    ('Vegetable Pakora', 'Occasional Foods', 'Indian', 1, '4 pieces (100g)', 285, 5.2, 28.0, 17.0, 3.2, 2.0, 'Snack', 'Fried', 'Energy Booster'),
    ('Cheese Pizza Slice', 'Occasional Foods', 'Italian', 1, '1 slice (107g)', 290, 12.0, 32.0, 12.5, 2.0, 3.5, 'Snack', 'Baked', 'Energy Booster'),
    ('Dark Chocolate (70%)', 'Occasional Foods', 'Global', 1, '30g', 170, 2.2, 13.0, 12.0, 3.1, 7.0, 'Snack', 'Raw', 'Balanced'),
    ('Gulab Jamun (1 piece)', 'Occasional Foods', 'Indian', 1, '1 piece (50g)', 175, 2.5, 26.0, 7.0, 0.2, 22.0, 'Snack', 'Fried', 'Energy Booster')
]

records = []
food_id = 1001

variations = [
    ('', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
    (' (Light Spiced)', 1.02, 1.0, 1.0, 1.05, 1.02, 1.0),
    (' (Homestyle)', 0.96, 1.02, 0.98, 0.92, 1.05, 0.95),
    (' (Low Sodium)', 0.98, 1.0, 0.99, 0.98, 1.0, 0.98),
    (' (Extra Portion)', 1.25, 1.25, 1.25, 1.25, 1.25, 1.25),
    (' (Half Portion)', 0.55, 0.55, 0.55, 0.55, 0.55, 0.55),
    (' (With Olive Oil)', 1.15, 1.02, 1.0, 1.35, 1.05, 1.0),
    (' (Steamed)', 0.92, 1.05, 0.95, 0.85, 1.1, 0.92),
    (' (Nutrient Dense)', 1.10, 1.18, 1.05, 1.08, 1.2, 1.02),
    (' (Mild Flavor)', 0.98, 0.99, 1.0, 0.95, 1.0, 0.98),
    (' (Herb Infused)', 1.04, 1.03, 1.01, 1.02, 1.08, 1.01),
    (' (Traditional)', 1.01, 0.98, 1.02, 1.04, 0.97, 1.03)
]

for base in base_foods:
    name, cat, cuisine, veg, serving, cal, prot, carb, fat, fiber, sugar, meal, prep, pref = base
    for var_suffix, m_cal, m_prot, m_carb, m_fat, m_fib, m_sug in variations:
        v_name = name + var_suffix if var_suffix else name
        jitter = random.uniform(0.97, 1.03)
        c_prot = round(max(0.1, prot * m_prot * jitter), 1)
        c_carb = round(max(0.0, carb * m_carb * jitter), 1)
        c_fat = round(max(0.0, fat * m_fat * jitter), 1)
        c_fiber = round(max(0.0, fiber * m_fib * jitter), 1)
        c_sugar = round(max(0.0, sugar * m_sug * jitter), 1)
        
        calc_cal = int(round(c_prot * 4.0 + c_carb * 4.0 + c_fat * 9.0))
        final_cal = max(10, calc_cal)
        
        records.append({
            'Food_ID': food_id,
            'Food_Name': v_name,
            'Food_Category': cat,
            'Cuisine': cuisine,
            'Vegetarian': veg,
            'Serving_Size': serving,
            'Calories': final_cal,
            'Protein': c_prot,
            'Carbohydrates': c_carb,
            'Fat': c_fat,
            'Fiber': c_fiber,
            'Sugar': c_sugar,
            'Meal_Type': meal,
            'Preparation_Type': prep,
            'User_Preference': pref
        })
        food_id += 1

csv_path = 'C:/Users/Lenovo/.gemini/antigravity/scratch/Smart-Nutrition-Analyzer/data/nutrition_data.csv'
fieldnames = ['Food_ID', 'Food_Name', 'Food_Category', 'Cuisine', 'Vegetarian', 'Serving_Size', 
              'Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 'Sugar', 
              'Meal_Type', 'Preparation_Type', 'User_Preference']

with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f'Successfully generated {len(records)} realistic nutrition records in {csv_path}')
