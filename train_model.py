import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Set random seed for reproducibility
np.random.seed(42)

# Generate realistic user dietary profile dataset with natural boundary variations
n_samples = 1200

ages = np.random.randint(18, 65, size=n_samples)
heights = np.random.uniform(150, 190, size=n_samples)
weights = np.random.uniform(45, 105, size=n_samples)
bmis = np.round(weights / ((heights / 100) ** 2), 1)

# Assign initial profiles
profile_types = np.random.choice(['Low Nutrition Intake', 'Balanced', 'High Calorie Intake'], size=n_samples, p=[0.3, 0.4, 0.3])

calories = []
protein = []
carbs = []
fat = []
fiber = []

for p in profile_types:
    if p == 'Low Nutrition Intake':
        c = np.random.normal(1450, 240)
        pr = np.random.normal(45, 12)
        cb = np.random.normal(190, 35)
        ft = np.random.normal(40, 12)
        fb = np.random.normal(14, 4)
    elif p == 'Balanced':
        c = np.random.normal(2150, 260)
        pr = np.random.normal(78, 14)
        cb = np.random.normal(260, 40)
        ft = np.random.normal(65, 14)
        fb = np.random.normal(25, 6)
    else:  # High Calorie Intake
        c = np.random.normal(2950, 340)
        pr = np.random.normal(72, 16)
        cb = np.random.normal(380, 50)
        ft = np.random.normal(105, 20)
        fb = np.random.normal(16, 5)
    
    # Natural realistic boundary overlap
    calories.append(max(900, round(c, 0)))
    protein.append(max(15, round(pr, 1)))
    carbs.append(max(80, round(cb, 1)))
    fat.append(max(15, round(ft, 1)))
    fiber.append(max(4, round(fb, 1)))

df_users = pd.DataFrame({
    'Age': ages,
    'BMI': bmis,
    'Daily_Calories': calories,
    'Protein': protein,
    'Carbohydrates': carbs,
    'Fat': fat,
    'Fiber': fiber,
    'Nutrition_Category': profile_types
})

# Save to data/user_profiles_train.csv
df_users.to_csv('data/user_profiles_train.csv', index=False)
print('Generated realistic training data (1200 rows): data/user_profiles_train.csv')

# Feature Selection
feature_cols = ['Age', 'BMI', 'Daily_Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber']
X = df_users[feature_cols]
y = df_users['Nutrition_Category']

# 80/20 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Random Forest Classifier
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    min_samples_split=5,
    random_state=42
)
clf.fit(X_train, y_train)

# Evaluation
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(f'=== MODEL ACCURACY: {acc * 100:.2f}% ===\n')
print('=== CLASSIFICATION REPORT ===')
print(report)
print('=== CONFUSION MATRIX ===')
print(cm)

print('\n=== FEATURE IMPORTANCES ===')
for col, imp in sorted(zip(feature_cols, clf.feature_importances_), key=lambda x: x[1], reverse=True):
    print(f'{col:18}: {imp:.4f}')

# Save Model
model_payload = {
    'model': clf,
    'features': feature_cols,
    'classes': clf.classes_.tolist()
}
joblib.dump(model_payload, 'model/nutrition_model.pkl')
print('\nModel successfully saved to model/nutrition_model.pkl')
