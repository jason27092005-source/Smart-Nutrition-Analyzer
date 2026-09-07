-- ==========================================================
-- SMART NUTRITION ANALYZER & DIET RECOMMENDATION SYSTEM
-- Database Schema & Analytical Queries for MySQL
-- ==========================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS smart_nutrition;
USE smart_nutrition;

-- 2. Create Foods Table
DROP TABLE IF EXISTS foods;
CREATE TABLE foods (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(150) NOT NULL,
    Food_Category VARCHAR(100) NOT NULL,
    Cuisine VARCHAR(50) NOT NULL,
    Vegetarian TINYINT(1) NOT NULL COMMENT '1: Veg, 0: Non-Veg',
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
);

-- 3. Create User Analysis History Table
DROP TABLE IF EXISTS user_analysis;
CREATE TABLE user_analysis (
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
);

-- ==========================================================
-- BEGINNER-FRIENDLY SQL ANALYTICAL QUERIES (FOR VIVA / LAB)
-- ==========================================================

-- Query 1: Calculate Average Calories Across All Foods
SELECT ROUND(AVG(Calories), 2) AS Average_Calories FROM foods;

-- Query 2: Calculate Average Protein Across All Foods
SELECT ROUND(AVG(Protein), 2) AS Average_Protein_Grams FROM foods;

-- Query 3: Find Top 5 Highest Calorie Foods
SELECT Food_Name, Food_Category, Calories, Serving_Size 
FROM foods 
ORDER BY Calories DESC 
LIMIT 5;

-- Query 4: Find Top 5 Highest Protein Foods
SELECT Food_Name, Food_Category, Protein, Calories 
FROM foods 
ORDER BY Protein DESC 
LIMIT 5;

-- Query 5: Count of Foods by Food Category
SELECT Food_Category, COUNT(*) AS Total_Items 
FROM foods 
GROUP BY Food_Category 
ORDER BY Total_Items DESC;

-- Query 6: Count of Vegetarian vs Non-Vegetarian Foods
SELECT 
    CASE WHEN Vegetarian = 1 THEN 'Vegetarian' ELSE 'Non-Vegetarian' END AS Diet_Type,
    COUNT(*) AS Total_Items
FROM foods 
GROUP BY Vegetarian;

-- Query 7: Average Calories, Protein, and Fiber Grouped by Food Category
SELECT 
    Food_Category,
    ROUND(AVG(Calories), 1) AS Avg_Calories,
    ROUND(AVG(Protein), 1) AS Avg_Protein,
    ROUND(AVG(Fiber), 1) AS Avg_Fiber
FROM foods 
GROUP BY Food_Category 
ORDER BY Avg_Calories DESC;

