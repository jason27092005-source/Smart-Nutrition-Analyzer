import os
import sqlite3
import pandas as pd

# Optional MySQL connector
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'database', 'smart_nutrition.db')
DATA_CSV_PATH = os.path.join(BASE_DIR, 'data', 'nutrition_data.csv')

# Default MySQL configuration (can be adjusted by the student in their environment)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'smart_nutrition'
}

def get_connection():
    """
    Attempts to connect to MySQL first.
    If MySQL server is not running or fails, falls back safely to SQLite.
    Returns (connection, db_type).
    """
    if MYSQL_AVAILABLE:
        try:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            if conn.is_connected():
                return conn, 'mysql'
        except Exception:
            pass  # Fall through to SQLite
            
    # SQLite fallback
    conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'

def init_database():
    """
    Initializes database tables and seeds the foods table from nutrition_data.csv
    if not already populated.
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    if db_type == 'sqlite':
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                Food_ID INTEGER PRIMARY KEY,
                Food_Name TEXT NOT NULL,
                Food_Category TEXT NOT NULL,
                Cuisine TEXT NOT NULL,
                Vegetarian INTEGER NOT NULL,
                Serving_Size TEXT NOT NULL,
                Calories INTEGER NOT NULL,
                Protein REAL NOT NULL,
                Carbohydrates REAL NOT NULL,
                Fat REAL NOT NULL,
                Fiber REAL NOT NULL,
                Sugar REAL NOT NULL,
                Meal_Type TEXT NOT NULL,
                Preparation_Type TEXT NOT NULL,
                User_Preference TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analysis (
                Analysis_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Age INTEGER NOT NULL,
                Gender TEXT NOT NULL,
                Height REAL NOT NULL,
                Weight REAL NOT NULL,
                BMI REAL NOT NULL,
                Activity_Level TEXT NOT NULL,
                Goal TEXT NOT NULL,
                Nutrition_Category TEXT NOT NULL,
                Analysis_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        # Check if foods table is seeded
        cursor.execute('SELECT COUNT(*) FROM foods')
        count = cursor.fetchone()[0]
        if count == 0 and os.path.exists(DATA_CSV_PATH):
            df = pd.read_csv(DATA_CSV_PATH)
            df.to_sql('foods', conn, if_exists='append', index=False)
            conn.commit()
            print(f"Database seeded with {len(df)} food records into SQLite.")
    else:
        # MySQL tables check
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                Food_ID INT PRIMARY KEY,
                Food_Name VARCHAR(150) NOT NULL,
                Food_Category VARCHAR(100) NOT NULL,
                Cuisine VARCHAR(50) NOT NULL,
                Vegetarian TINYINT(1) NOT NULL,
                Serving_Size VARCHAR(50) NOT NULL,
                Calories INT NOT NULL,
                Protein DECIMAL(5,2) NOT NULL,
                Carbohydrates DECIMAL(5,2) NOT NULL,
                Fat DECIMAL(5,2) NOT NULL,
                Fiber DECIMAL(5,2) NOT NULL,
                Sugar DECIMAL(5,2) NOT NULL,
                Meal_Type VARCHAR(50) NOT NULL,
                Preparation_Type VARCHAR(50) NOT NULL,
                User_Preference VARCHAR(50) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analysis (
                Analysis_ID INT AUTO_INCREMENT PRIMARY KEY,
                Age INT NOT NULL,
                Gender VARCHAR(10) NOT NULL,
                Height DECIMAL(5,2) NOT NULL,
                Weight DECIMAL(5,2) NOT NULL,
                BMI DECIMAL(4,1) NOT NULL,
                Activity_Level VARCHAR(50) NOT NULL,
                Goal VARCHAR(50) NOT NULL,
                Nutrition_Category VARCHAR(50) NOT NULL,
                Analysis_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
    cursor.close()
    conn.close()

def save_user_analysis(age, gender, height, weight, bmi, activity, goal, category):
    """Saves a user's nutrition analysis run into the database."""
    try:
        conn, db_type = get_connection()
        cursor = conn.cursor()
        if db_type == 'mysql':
            query = '''
                INSERT INTO user_analysis (Age, Gender, Height, Weight, BMI, Activity_Level, Goal, Nutrition_Category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (age, gender, height, weight, bmi, activity, goal, category))
        else:
            query = '''
                INSERT INTO user_analysis (Age, Gender, Height, Weight, BMI, Activity_Level, Goal, Nutrition_Category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (age, gender, height, weight, bmi, activity, goal, category))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving user analysis to database: {e}")
        return False

def get_food_records(search_query=None, category_filter=None, veg_filter=None, limit=100):
    """Retrieves foods from database with optional search and filters."""
    try:
        conn, db_type = get_connection()
        query = "SELECT * FROM foods WHERE 1=1"
        params = []
        
        if search_query:
            query += " AND Food_Name LIKE ?" if db_type == 'sqlite' else " AND Food_Name LIKE %s"
            params.append(f"%{search_query}%")
            
        if category_filter and category_filter != 'All':
            query += " AND Food_Category = ?" if db_type == 'sqlite' else " AND Food_Category = %s"
            params.append(category_filter)
            
        if veg_filter is not None and veg_filter != 'All':
            val = 1 if str(veg_filter).lower() in ['1', 'veg', 'yes'] else 0
            query += " AND Vegetarian = ?" if db_type == 'sqlite' else " AND Vegetarian = %s"
            params.append(val)
            
        query += f" ORDER BY Food_Name ASC LIMIT {limit}"
        
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if db_type == 'sqlite':
            rows = [dict(r) for r in cursor.fetchall()]
        else:
            col_names = [desc[0] for desc in cursor.description]
            rows = [dict(zip(col_names, r)) for r in cursor.fetchall()]
            
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching foods from database: {e}")
        # Fallback to CSV directly
        if os.path.exists(DATA_CSV_PATH):
            df = pd.read_csv(DATA_CSV_PATH)
            if search_query:
                df = df[df['Food_Name'].str.contains(search_query, case=False, na=False)]
            if category_filter and category_filter != 'All':
                df = df[df['Food_Category'] == category_filter]
            if veg_filter is not None and veg_filter != 'All':
                val = 1 if str(veg_filter).lower() in ['1', 'veg', 'yes'] else 0
                df = df[df['Vegetarian'] == val]
            return df.head(limit).to_dict(orient='records')
        return []

# Run init on module load
init_database()

