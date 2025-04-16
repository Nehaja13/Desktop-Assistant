# import streamlit as st
# import pandas as pd

# # Calorie database (simplified)
# def calorie_tracker_interface(conn=None):
#     FOOD_CALORIES = {
#         "Apple": 52, "Banana": 89, "Orange": 47, "Grapes": 69,
#         "Chicken Breast": 165, "Salmon": 208, "Egg": 68,
#         "White Rice": 130, "Brown Rice": 111, "Whole Wheat Bread": 69,
#         "Milk": 42, "Yogurt": 59, "Cheese": 113,
#         "Broccoli": 34, "Carrot": 41, "Spinach": 23,
#         "Potato": 77, "Pasta": 131, "Pizza": 266,
#         "Hamburger": 295, "French Fries": 312, "Ice Cream": 207,
#         "Chocolate": 546, "Nuts": 607, "Water": 0
#     }

#     # Food suggestions based on goals
#     FOOD_SUGGESTIONS = {
#         "weight_loss": [
#             "Vegetables (broccoli, spinach, carrots)",
#             "Lean proteins (chicken breast, fish)",
#             "Whole grains (brown rice, quinoa)",
#             "Fruits (apples, berries)",
#             "Legumes (lentils, chickpeas)"
#         ],
#         "weight_maintenance": [
#             "Balanced meals with protein, carbs, and fats",
#             "Variety of fruits and vegetables",
#             "Whole grains",
#             "Healthy fats (avocado, nuts in moderation)",
#             "Dairy or alternatives"
#         ],
#         "weight_gain": [
#             "Nutrient-dense foods (nuts, seeds)",
#             "Healthy fats (avocado, olive oil)",
#             "Whole milk and dairy",
#             "Lean proteins",
#             "Complex carbohydrates (sweet potatoes, whole grains)"
#         ]
#     }

#     def calculate_bmi(weight, height):
#         """Calculate BMI given weight in kg and height in meters"""
#         return weight / (height ** 2)

#     def calculate_ideal_weight(height, gender):
#         """Calculate ideal weight range using Devine formula"""
#         if gender == "Male":
#             ideal = 50 + 2.3 * ((height * 100 / 2.54) - 60)
#         else:  # Female
#             ideal = 45.5 + 2.3 * ((height * 100 / 2.54) - 60)
#         return (ideal * 0.9, ideal * 1.1)  # 10% range

#     def get_bmi_category(bmi):
#         """Return BMI category based on BMI value"""
#         if bmi < 18.5:
#             return "Underweight"
#         elif 18.5 <= bmi < 25:
#             return "Normal weight"
#         elif 25 <= bmi < 30:
#             return "Overweight"
#         else:
#             return "Obese"

#     def get_diet_goal(current_weight, ideal_weight_range):
#         """Determine diet goal based on current vs ideal weight"""
#         avg_ideal = sum(ideal_weight_range) / 2
#         if current_weight < ideal_weight_range[0]:
#             return "weight_gain"
#         elif current_weight > ideal_weight_range[1]:
#             return "weight_loss"
#         else:
#             return "weight_maintenance"
#     st.title("🍏 Health & Fitness Tracker")
#     # def main():
#     #     st.title("Health & Fitness Tracker")
        
#         # Sidebar navigation
# menu = st.sidebar.selectbox("Select Option", 
#                         ["BMI Calculator", "Ideal Weight Calculator", "Calorie Tracker"])

# if menu == "BMI Calculator":
#     st.header("BMI Calculator")
#     weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
#     height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
    
#     if st.button("Calculate BMI"):
#         bmi = calculate_bmi(weight, height)
#         category = get_bmi_category(bmi)
        
#         st.success(f"Your BMI: {bmi:.1f} ({category})")
        
#         if category != "Normal weight":
#             st.warning(f"Recommendation: You should aim for a BMI between 18.5 and 25. "
#                     f"Consider consulting with a healthcare provider.")

# elif menu == "Ideal Weight Calculator":
#     st.header("Ideal Weight Calculator")
#     height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
#     gender = st.radio("Gender", ["Male", "Female"])
    
#     if st.button("Calculate Ideal Weight"):
#         ideal_min, ideal_max = calculate_ideal_weight(height, gender)
#         st.success(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")

# elif menu == "Calorie Tracker":
#     st.header("Calorie Tracker")
    
#     # Get user info for recommendations
#     col1, col2 = st.columns(2)
#     with col1:
#         weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
#     with col2:
#         height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
#     gender = st.radio("Gender", ["Male", "Female"], key="cal_gender")
    
#     # Calculate ideal weight for recommendations
#     ideal_min, ideal_max = calculate_ideal_weight(height, gender)
#     diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
    
#     # Food intake tracking
#     st.subheader("Track Your Daily Food Intake")
    
#     selected_foods = st.multiselect("Select foods you've eaten today", list(FOOD_CALORIES.keys()))
#     quantities = {}
    
#     for food in selected_foods:
#         quantities[food] = st.number_input(f"Quantity of {food} (servings)", min_value=0.1, max_value=10.0, value=1.0, key=f"qty_{food}")
    
#     if st.button("Calculate Total Calories"):
#         total_calories = sum(FOOD_CALORIES[food] * quantities[food] for food in selected_foods)
#         st.success(f"Total calories consumed today: {total_calories}")
        
#         # Estimate daily calorie needs (simplified)
#         if gender == "Male":
#             bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * 30)  # assuming age 30
#         else:
#             bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * 30)
        
#         activity_factor = 1.55  # moderately active
#         daily_needs = bmr * activity_factor
        
#         st.info(f"Estimated daily calorie needs: {daily_needs:.0f} (based on moderate activity)")
        
#         if total_calories > daily_needs:
#             st.warning(f"You've consumed {total_calories - daily_needs:.0f} calories more than your estimated needs.")
#         else:
#             st.warning(f"You've consumed {daily_needs - total_calories:.0f} calories less than your estimated needs.")
    
#     # Suggestions section
#     if st.button("Get Dietary Suggestions"):
#         st.subheader("Dietary Suggestions Based on Your Profile")
        
#         st.write(f"Your current weight: {weight} kg")
#         st.write(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
        
#         if diet_goal == "weight_loss":
#             st.success("Goal: Healthy Weight Loss")
#             st.write("To lose weight gradually, aim for a calorie deficit of 300-500 calories per day.")
#         elif diet_goal == "weight_gain":
#             st.success("Goal: Healthy Weight Gain")
#             st.write("To gain weight gradually, aim for a calorie surplus of 300-500 calories per day.")
#         else:
#             st.success("Goal: Weight Maintenance")
#             st.write("Maintain your current healthy weight with balanced nutrition.")
        
#         st.subheader("Recommended Foods:")
#         for food in FOOD_SUGGESTIONS[diet_goal]:
#             st.write(f"- {food}")
        
#         st.subheader("Additional Tips:")
#         if diet_goal == "weight_loss":
#             st.write("- Focus on high-fiber foods to feel full longer")
#             st.write("- Drink plenty of water before meals")
#             st.write("- Limit added sugars and processed foods")
#         elif diet_goal == "weight_gain":
#             st.write("- Eat more frequent, nutrient-dense meals")
#             st.write("- Include healthy fats in your diet")
#             st.write("- Combine with strength training to build muscle")
#         else:
#             st.write("- Maintain variety in your diet")
#             st.write("- Practice portion control")
#             st.write("- Stay physically active")



# def calorie_tracker_interface(conn= None):
#     st.title("Calorie Tracker")

# if __name__ == "__main__":
#     calorie_tracker_interface()
#     main()








'''import streamlit as st
import pandas as pd

def calorie_tracker_interface(conn=None):
    # Calorie database (simplified)
    FOOD_CALORIES = {
         "Apple": 52, "Banana": 89, "Orange": 47, "Grapes": 69,
         "Chicken Breast": 165, "Salmon": 208, "Egg": 68,
         "White Rice": 130, "Brown Rice": 111, "Whole Wheat Bread": 69,
         "Milk": 42, "Yogurt": 59, "Cheese": 113,
         "Broccoli": 34, "Carrot": 41, "Spinach": 23,
         "Potato": 77, "Pasta": 131, "Pizza": 266,
         "Hamburger": 295, "French Fries": 312, "Ice Cream": 207,
         "Chocolate": 546, "Nuts": 607, "Water": 0
    }
    
    FOOD_SUGGESTIONS = {
        "weight_loss": [
            "Vegetables (broccoli, spinach, carrots)",
            "Lean proteins (chicken breast, fish)",
            "Whole grains (brown rice, quinoa)",
            "Fruits (apples, berries)",
            "Legumes (lentils, chickpeas)"
        ],
        "weight_gain": [
            "Healthy fats (avocados, nuts, olive oil)",
            "Protein-rich foods (meat, dairy, legumes)",
            "Whole grains (oats, whole wheat bread)",
            "Dried fruits (dates, raisins)",
            "Starchy vegetables (potatoes, corn)"
        ],
        "weight_maintenance": [
            "Balanced meals with variety",
            "Portion-controlled servings",
            "Regular meal timing",
            "Hydration with water",
            "Moderate treats"
        ]
    }

    def calculate_bmi(weight, height):
        """Calculate BMI given weight in kg and height in meters"""
        return weight / (height ** 2)

    def calculate_ideal_weight(height, gender):
        """Calculate ideal weight range using Devine formula"""
        if gender == "Male":
            ideal = 50 + 2.3 * ((height * 100 / 2.54) - 60)
        else:  # Female
            ideal = 45.5 + 2.3 * ((height * 100 / 2.54) - 60)
        return (ideal * 0.9, ideal * 1.1)  # 10% range

    def get_bmi_category(bmi):
        """Return BMI category based on BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_diet_goal(current_weight, ideal_weight_range):
        """Determine diet goal based on current vs ideal weight"""
        avg_ideal = sum(ideal_weight_range) / 2
        if current_weight < ideal_weight_range[0]:
            return "weight_gain"
        elif current_weight > ideal_weight_range[1]:
            return "weight_loss"
        else:
            return "weight_maintenance"

    # Main interface
    st.title("🍏 Health & Fitness Tracker")
    
    # Sidebar navigation (local to this module)
    menu = st.sidebar.selectbox("Select Option", 
                               ["BMI Calculator", "Ideal Weight Calculator", "Calorie Tracker"])
    
    if menu == "BMI Calculator":
        st.header("BMI Calculator")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        
        if st.button("Calculate BMI"):
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            
            st.success(f"Your BMI: {bmi:.1f} ({category})")
            
            if category != "Normal weight":
                st.warning(f"Recommendation: You should aim for a BMI between 18.5 and 25. "
                          f"Consider consulting with a healthcare provider.")
    
    elif menu == "Ideal Weight Calculator":
        st.header("Ideal Weight Calculator")
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"])
        
        if st.button("Calculate Ideal Weight"):
            ideal_min, ideal_max = calculate_ideal_weight(height, gender)
            st.success(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
    
    elif menu == "Calorie Tracker":
        st.header("Calorie Tracker")
        
        # Get user info for recommendations
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"], key="cal_gender")
        
        # Calculate ideal weight for recommendations
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Food intake tracking
        st.subheader("Track Your Daily Food Intake")
        
        selected_foods = st.multiselect("Select foods you've eaten today", list(FOOD_CALORIES.keys()))
        quantities = {}
        
        for food in selected_foods:
            quantities[food] = st.number_input(f"Quantity of {food} (servings)", min_value=0.1, max_value=10.0, value=1.0, key=f"qty_{food}")
        
        if st.button("Calculate Total Calories"):
            total_calories = sum(FOOD_CALORIES[food] * quantities[food] for food in selected_foods)
            st.success(f"Total calories consumed today: {total_calories}")
            
            # Estimate daily calorie needs (simplified)
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * 30)  # assuming age 30
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * 30)
            
            activity_factor = 1.55  # moderately active
            daily_needs = bmr * activity_factor
            
            st.info(f"Estimated daily calorie needs: {daily_needs:.0f} (based on moderate activity)")
            
            if total_calories > daily_needs:
                st.warning(f"You've consumed {total_calories - daily_needs:.0f} calories more than your estimated needs.")
            else:
                st.warning(f"You've consumed {daily_needs - total_calories:.0f} calories less than your estimated needs.")
        
        # Suggestions section
        if st.button("Get Dietary Suggestions"):
            st.subheader("Dietary Suggestions Based on Your Profile")
            
            st.write(f"Your current weight: {weight} kg")
            st.write(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
            
            if diet_goal == "weight_loss":
                st.success("Goal: Healthy Weight Loss")
                st.write("To lose weight gradually, aim for a calorie deficit of 300-500 calories per day.")
            elif diet_goal == "weight_gain":
                st.success("Goal: Healthy Weight Gain")
                st.write("To gain weight gradually, aim for a calorie surplus of 300-500 calories per day.")
            else:
                st.success("Goal: Weight Maintenance")
                st.write("Maintain your current healthy weight with balanced nutrition.")
            
            st.subheader("Recommended Foods:")
            for food in FOOD_SUGGESTIONS[diet_goal]:
                st.write(f"- {food}")
            
            st.subheader("Additional Tips:")
            if diet_goal == "weight_loss":
                st.write("- Focus on high-fiber foods to feel full longer")
                st.write("- Drink plenty of water before meals")
                st.write("- Limit added sugars and processed foods")
            elif diet_goal == "weight_gain":
                st.write("- Eat more frequent, nutrient-dense meals")
                st.write("- Include healthy fats in your diet")
                st.write("- Combine with strength training to build muscle")
            else:
                st.write("- Maintain variety in your diet")
                st.write("- Practice portion control")
                st.write("- Stay physically active")

# This allows the file to be run standalone
if __name__ == "__main__":
    st.set_page_config(page_title="Calorie Tracker")  # Only for standalone use
    calorie_tracker_interface()'''
    
    
    
    
    
    
    
    
    
    
    
    
    










'''import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def calorie_tracker_interface(conn=None):
    # Calorie database (simplified)
    FOOD_CALORIES = {
        "Apple": 52, "Banana": 89, "Orange": 47, "Grapes": 69,
        "Chicken Breast": 165, "Salmon": 208, "Egg": 68,
        "White Rice": 130, "Brown Rice": 111, "Whole Wheat Bread": 69,
        "Milk": 42, "Yogurt": 59, "Cheese": 113,
        "Broccoli": 34, "Carrot": 41, "Spinach": 23,
        "Potato": 77, "Pasta": 131, "Pizza": 266,
        "Hamburger": 295, "French Fries": 312, "Ice Cream": 207,
        "Chocolate": 546, "Nuts": 607, "Water": 0
    }
    
    # Sample daily schedules based on goals
    DAILY_SCHEDULES = {
        "weight_loss": [
            {"time": "7:00 AM", "activity": "Wake up and drink warm water", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Morning walk (30 min)", "type": "exercise", "completed": False},
            {"time": "8:00 AM", "activity": "Breakfast: Oatmeal with berries", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Apple with almonds", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Grilled chicken with vegetables", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Greek yogurt", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Salmon with quinoa", "type": "meal", "completed": False},
            {"time": "8:00 PM", "activity": "Light stretching (15 min)", "type": "exercise", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ],
        "weight_gain": [
            {"time": "7:00 AM", "activity": "Wake up and protein shake", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Strength training (45 min)", "type": "exercise", "completed": False},
            {"time": "8:30 AM", "activity": "Breakfast: Scrambled eggs with toast and avocado", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Banana with peanut butter", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Beef with rice and vegetables", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Nuts and dried fruits", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Pasta with chicken", "type": "meal", "completed": False},
            {"time": "9:00 PM", "activity": "Protein shake before bed", "type": "meal", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ],
        "weight_maintenance": [
            {"time": "7:00 AM", "activity": "Wake up and lemon water", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Yoga or light exercise (30 min)", "type": "exercise", "completed": False},
            {"time": "8:00 AM", "activity": "Breakfast: Whole grain toast with eggs", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Fruit and nuts", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Balanced meal with protein and veggies", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Hummus with vegetables", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Fish with sweet potato", "type": "meal", "completed": False},
            {"time": "8:00 PM", "activity": "Evening walk (20 min)", "type": "exercise", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ]
    }
    FOOD_SUGGESTIONS = {
        "weight_loss": [
            "Vegetables (broccoli, spinach, carrots)",
            "Lean proteins (chicken breast, fish)",
            "Whole grains (brown rice, quinoa)",
            "Fruits (apples, berries)",
            "Legumes (lentils, chickpeas)"
        ],
        "weight_gain": [
            "Healthy fats (avocados, nuts, olive oil)",
            "Protein-rich foods (meat, dairy, legumes)",
            "Whole grains (oats, whole wheat bread)",
            "Dried fruits (dates, raisins)",
            "Starchy vegetables (potatoes, corn)"
        ],
        "weight_maintenance": [
            "Balanced meals with variety",
            "Portion-controlled servings",
            "Regular meal timing",
            "Hydration with water",
            "Moderate treats"
        ]
    }

    def calculate_bmi(weight, height):
        """Calculate BMI given weight in kg and height in meters"""
        return weight / (height ** 2)

    def calculate_ideal_weight(height, gender):
        """Calculate ideal weight range using Devine formula"""
        if gender == "Male":
            ideal = 50 + 2.3 * ((height * 100 / 2.54) - 60)
        else:  # Female
            ideal = 45.5 + 2.3 * ((height * 100 / 2.54) - 60)
        return (ideal * 0.9, ideal * 1.1)  # 10% range

    def get_bmi_category(bmi):
        """Return BMI category based on BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_diet_goal(current_weight, ideal_weight_range):
        """Determine diet goal based on current vs ideal weight"""
        avg_ideal = sum(ideal_weight_range) / 2
        if current_weight < ideal_weight_range[0]:
            return "weight_gain"
        elif current_weight > ideal_weight_range[1]:
            return "weight_loss"
        else:
            return "weight_maintenance"

    # Main interface
    st.title("🍏 Health & Fitness Tracker")
    
    # Sidebar navigation (local to this module)
    menu = st.sidebar.selectbox("Select Option", 
                               ["BMI Calculator", "Ideal Weight Calculator", "Calorie Tracker"])
    
    if menu == "BMI Calculator":
        st.header("BMI Calculator")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        
        if st.button("Calculate BMI"):
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            
            st.success(f"Your BMI: {bmi:.1f} ({category})")
            
            if category != "Normal weight":
                st.warning(f"Recommendation: You should aim for a BMI between 18.5 and 25. "
                          f"Consider consulting with a healthcare provider.")
    
    elif menu == "Ideal Weight Calculator":
        st.header("Ideal Weight Calculator")
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"])
        
        if st.button("Calculate Ideal Weight"):
            ideal_min, ideal_max = calculate_ideal_weight(height, gender)
            st.success(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
    
    elif menu == "Calorie Tracker":
        st.header("Calorie Tracker")
        
        # Get user info for recommendations
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"], key="cal_gender")
        
        # Calculate ideal weight for recommendations
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Food intake tracking
        st.subheader("Track Your Daily Food Intake")
        
        selected_foods = st.multiselect("Select foods you've eaten today", list(FOOD_CALORIES.keys()))
        quantities = {}
        
        for food in selected_foods:
            quantities[food] = st.number_input(f"Quantity of {food} (servings)", min_value=0.1, max_value=10.0, value=1.0, key=f"qty_{food}")
        
        if st.button("Calculate Total Calories"):
            total_calories = sum(FOOD_CALORIES[food] * quantities[food] for food in selected_foods)
            st.success(f"Total calories consumed today: {total_calories}")
            
            # Estimate daily calorie needs (simplified)
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * 30)  # assuming age 30
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * 30)
            
            activity_factor = 1.55  # moderately active
            daily_needs = bmr * activity_factor
            
            st.info(f"Estimated daily calorie needs: {daily_needs:.0f} (based on moderate activity)")
            
            if total_calories > daily_needs:
                st.warning(f"You've consumed {total_calories - daily_needs:.0f} calories more than your estimated needs.")
            else:
                st.warning(f"You've consumed {daily_needs - total_calories:.0f} calories less than your estimated needs.")
        
        # Suggestions section
        if st.button("Get Dietary Suggestions"):
            st.subheader("Dietary Suggestions Based on Your Profile")
            
            st.write(f"Your current weight: {weight} kg")
            st.write(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
            
            if diet_goal == "weight_loss":
                st.success("Goal: Healthy Weight Loss")
                st.write("To lose weight gradually, aim for a calorie deficit of 300-500 calories per day.")
            elif diet_goal == "weight_gain":
                st.success("Goal: Healthy Weight Gain")
                st.write("To gain weight gradually, aim for a calorie surplus of 300-500 calories per day.")
            else:
                st.success("Goal: Weight Maintenance")
                st.write("Maintain your current healthy weight with balanced nutrition.")
            
            st.subheader("Recommended Foods:")
            for food in FOOD_SUGGESTIONS[diet_goal]:
                st.write(f"- {food}")
            
            st.subheader("Additional Tips:")
            if diet_goal == "weight_loss":
                st.write("- Focus on high-fiber foods to feel full longer")
                st.write("- Drink plenty of water before meals")
                st.write("- Limit added sugars and processed foods")
            elif diet_goal == "weight_gain":
                st.write("- Eat more frequent, nutrient-dense meals")
                st.write("- Include healthy fats in your diet")
                st.write("- Combine with strength training to build muscle")
            else:
                st.write("- Maintain variety in your diet")
                st.write("- Practice portion control")
                st.write("- Stay physically active")

# This allows the file to be run standalone

    

    def update_completion_status(index):
        """Update completion status in session state"""
        st.session_state.current_schedule[index]['completed'] = st.session_state[f"completed_{index}"]

    def reset_schedule():
        """Reset all completion statuses to False"""
        if 'current_schedule' in st.session_state:
            for item in st.session_state.current_schedule:
                item['completed'] = False
                

if __name__ == "__main__":
    st.set_page_config(page_title="Calorie Tracker")  # Only for standalone use
    calorie_tracker_interface()

    # Main interface
    st.title("🍏 Health & Fitness Tracker")
    
    # Sidebar navigation (add new option)
    menu = st.sidebar.selectbox("Select Option", 
                               ["BMI Calculator", "Ideal Weight Calculator", 
                                "Calorie Tracker", "Daily Schedule"])
    
    if menu == "Daily Schedule":
        st.header("📅 Your Daily Health Schedule")
        
        # Get user info to determine goal
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"], key="schedule_gender")
        
        # Calculate ideal weight and determine goal
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Display the appropriate schedule
        st.subheader(f"Recommended {diet_goal.replace('_', ' ').title()} Schedule")
        
        # Initialize session state for schedule if not exists
        if 'current_schedule' not in st.session_state:
            st.session_state.current_schedule = DAILY_SCHEDULES[diet_goal]
        
        # Display schedule with checkboxes
        completed_count = 0
        for i, item in enumerate(st.session_state.current_schedule):
            col1, col2 = st.columns([1, 4])
            with col1:
                # Checkbox to mark completion
                completed = st.checkbox("", 
                                      value=item['completed'], 
                                      key=f"completed_{i}",
                                      on_change=update_completion_status,
                                      args=(i,))
                if completed:
                    completed_count += 1
            with col2:
                # Color code based on activity type
                if item['type'] == "meal":
                    st.markdown(f"🍽️ **{item['time']}**: {item['activity']}")
                elif item['type'] == "exercise":
                    st.markdown(f"🏋️ **{item['time']}**: {item['activity']}")
                else:
                    st.markdown(f"⏰ **{item['time']}**: {item['activity']}")
        
        # Progress tracking
        total_items = len(st.session_state.current_schedule)
        progress = completed_count / total_items
        st.progress(progress)
        st.caption(f"Completed {completed_count} of {total_items} tasks ({progress:.0%})")
        
        # Reset button
        if st.button("Reset Today's Progress"):
            reset_schedule()
            st.experimental_rerun()
    
# ... [Rest of your code] ...'''

















'''import streamlit as st
import time
from datetime import datetime, timedelta
import threading

# ... [keep all your existing imports and food databases] ...

def check_for_upcoming_activities():
    """Background thread to check for upcoming activities"""
    while True:
        if 'current_schedule' in st.session_state and 'notifications_enabled' in st.session_state:
            if st.session_state.notifications_enabled:
                now = datetime.now().strftime("%I:%M %p")
                for item in st.session_state.current_schedule:
                    if not item['completed'] and item['time'] == now:
                        show_notification(item)
        time.sleep(60)  # Check every minute

def show_notification(activity):
    """Display a notification for an upcoming activity"""
    notification = f"⏰ Reminder: It's time for {activity['activity']}!"
    st.session_state.notifications.append(notification)
    # Play a sound (optional)
    try:
        import winsound
        winsound.Beep(1000, 500)  # Windows only
    except:
        pass

def calorie_tracker_interface(conn=None):
    # ... [keep all your existing database and helper functions] ...
    
    # Initialize notifications in session state
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'notifications_enabled' not in st.session_state:
        st.session_state.notifications_enabled = False
    
    # Start notification thread (only once)
    if 'notification_thread' not in st.session_state:
        st.session_state.notification_thread = threading.Thread(
            target=check_for_upcoming_activities,
            daemon=True
        )
        st.session_state.notification_thread.start()
    
    # Main interface
    st.title("🍏 Health & Fitness Tracker")
    
    # Sidebar navigation
    menu = st.sidebar.selectbox("Select Option", 
                               ["BMI Calculator", "Ideal Weight Calculator", 
                                "Calorie Tracker", "Daily Schedule"])
    
    if menu == "Daily Schedule":
        st.header("📅 Your Daily Health Schedule")
        
        # Notification controls
        with st.expander("🔔 Notification Settings"):
            notifications_on = st.toggle("Enable Notifications", 
                                       value=st.session_state.notifications_enabled,
                                       key="notifications_toggle")
            st.session_state.notifications_enabled = notifications_on
            st.write("You'll get reminders when it's time for scheduled activities")
        
        # Display notifications
        if st.session_state.notifications:
            st.subheader("🔔 Notifications")
            for notification in st.session_state.notifications:
                st.warning(notification)
            if st.button("Clear Notifications"):
                st.session_state.notifications = []
                st.experimental_rerun()
        
        # ... [keep your existing schedule display code] ...
        
        # Add time check to each activity
        now = datetime.now().strftime("%I:%M %p")
        for i, item in enumerate(st.session_state.current_schedule):
            col1, col2, col3 = st.columns([1, 4, 2])
            with col1:
                completed = st.checkbox("", 
                                      value=item['completed'], 
                                      key=f"completed_{i}",
                                      on_change=update_completion_status,
                                      args=(i,))
            with col2:
                # Highlight upcoming activities (within 30 minutes)
                activity_time = datetime.strptime(item['time'], "%I:%M %p")
                current_time = datetime.strptime(now, "%I:%M %p")
                time_diff = (activity_time - current_time).total_seconds() / 60
                
                if 0 <= time_diff <= 30 and not item['completed']:
                    st.markdown(f"⏰ **{item['time']}**: {item['activity']}", 
                               help="Upcoming soon!")
                else:
                    if item['type'] == "meal":
                        st.markdown(f"🍽️ **{item['time']}**: {item['activity']}")
                    elif item['type'] == "exercise":
                        st.markdown(f"🏋️ **{item['time']}**: {item['activity']}")
                    else:
                        st.markdown(f"⏰ **{item['time']}**: {item['activity']}")
            
            with col3:
                if not item['completed']:
                    st.caption(f"Due at {item['time']}")
                else:
                    st.caption("✓ Completed")

# ... [keep all your remaining existing code] ...'''



















import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from plyer import notification

def calorie_tracker_interface(conn=None):
    # Calorie database (simplified)
    FOOD_CALORIES = {
        "Apple": 52, "Banana": 89, "Orange": 47, "Grapes": 69,
        "Chicken Breast": 165, "Salmon": 208, "Egg": 68,
        "White Rice": 130, "Brown Rice": 111, "Whole Wheat Bread": 69,
        "Milk": 42, "Yogurt": 59, "Cheese": 113,
        "Broccoli": 34, "Carrot": 41, "Spinach": 23,
        "Potato": 77, "Pasta": 131, "Pizza": 266,
        "Hamburger": 295, "French Fries": 312, "Ice Cream": 207,
        "Chocolate": 546, "Nuts": 607, "Water": 0
    }
    
    # Sample daily schedules based on goals
    DAILY_SCHEDULES = {
        "weight_loss": [
            {"time": "7:00 AM", "activity": "Wake up and drink warm water", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Morning walk (30 min)", "type": "exercise", "completed": False},
            {"time": "8:00 AM", "activity": "Breakfast: Oatmeal with berries", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Apple with almonds", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Grilled chicken with vegetables", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Greek yogurt", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Salmon with quinoa", "type": "meal", "completed": False},
            {"time": "8:00 PM", "activity": "Light stretching (15 min)", "type": "exercise", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ],
        "weight_gain": [
            {"time": "7:00 AM", "activity": "Wake up and protein shake", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Strength training (45 min)", "type": "exercise", "completed": False},
            {"time": "8:30 AM", "activity": "Breakfast: Scrambled eggs with toast and avocado", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Banana with peanut butter", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Beef with rice and vegetables", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Nuts and dried fruits", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Pasta with chicken", "type": "meal", "completed": False},
            {"time": "9:00 PM", "activity": "Protein shake before bed", "type": "meal", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ],
        "weight_maintenance": [
            {"time": "7:00 AM", "activity": "Wake up and lemon water", "type": "routine", "completed": False},
            {"time": "7:30 AM", "activity": "Yoga or light exercise (30 min)", "type": "exercise", "completed": False},
            {"time": "8:00 AM", "activity": "Breakfast: Whole grain toast with eggs", "type": "meal", "completed": False},
            {"time": "10:30 AM", "activity": "Snack: Fruit and nuts", "type": "meal", "completed": False},
            {"time": "1:00 PM", "activity": "Lunch: Balanced meal with protein and veggies", "type": "meal", "completed": False},
            {"time": "4:00 PM", "activity": "Snack: Hummus with vegetables", "type": "meal", "completed": False},
            {"time": "6:30 PM", "activity": "Dinner: Fish with sweet potato", "type": "meal", "completed": False},
            {"time": "8:00 PM", "activity": "Evening walk (20 min)", "type": "exercise", "completed": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "completed": False}
        ]
    }

    FOOD_SUGGESTIONS = {
        "weight_loss": [
            "Vegetables (broccoli, spinach, carrots)",
            "Lean proteins (chicken breast, fish)",
            "Whole grains (brown rice, quinoa)",
            "Fruits (apples, berries)",
            "Legumes (lentils, chickpeas)"
        ],
        "weight_gain": [
            "Healthy fats (avocados, nuts, olive oil)",
            "Protein-rich foods (meat, dairy, legumes)",
            "Whole grains (oats, whole wheat bread)",
            "Dried fruits (dates, raisins)",
            "Starchy vegetables (potatoes, corn)"
        ],
        "weight_maintenance": [
            "Balanced meals with variety",
            "Portion-controlled servings",
            "Regular meal timing",
            "Hydration with water",
            "Moderate treats"
        ]
    }

    def calculate_bmi(weight, height):
        """Calculate BMI given weight in kg and height in meters"""
        return weight / (height ** 2)

    def calculate_ideal_weight(height, gender):
        """Calculate ideal weight range using Devine formula"""
        if gender == "Male":
            ideal = 50 + 2.3 * ((height * 100 / 2.54) - 60)
        else:  # Female
            ideal = 45.5 + 2.3 * ((height * 100 / 2.54) - 60)
        return (ideal * 0.9, ideal * 1.1)  # 10% range

    def get_bmi_category(bmi):
        """Return BMI category based on BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_diet_goal(current_weight, ideal_weight_range):
        """Determine diet goal based on current vs ideal weight"""
        avg_ideal = sum(ideal_weight_range) / 2
        if current_weight < ideal_weight_range[0]:
            return "weight_gain"
        elif current_weight > ideal_weight_range[1]:
            return "weight_loss"
        else:
            return "weight_maintenance"

    def show_notification(activity):
        """Show desktop notification for activity"""
        try:
            notification.notify(
                title="Health Assistant Reminder",
                message=f"It's time for {activity['activity']}",
                app_name="Health Tracker",
                timeout=10
            )
            if 'notifications' not in st.session_state:
                st.session_state.notifications = []
            st.session_state.notifications.append(
                f"⏰ Reminder: It's time for {activity['activity']}"
            )
        except Exception as e:
            st.error(f"Could not show notification: {str(e)}")

    def check_for_upcoming_activities():
        """Background thread to check for upcoming activities"""
        while True:
            if 'current_schedule' in st.session_state and 'notifications_enabled' in st.session_state:
                if st.session_state.notifications_enabled:
                    now = datetime.now().strftime("%I:%M %p")
                    for item in st.session_state.current_schedule:
                        if not item['completed'] and item['time'] == now:
                            show_notification(item)
            time.sleep(60)  # Check every minute

    def update_completion_status(index):
        """Update completion status in session state"""
        st.session_state.current_schedule[index]['completed'] = st.session_state[f"completed_{index}"]

    def reset_schedule():
        """Reset all completion statuses to False"""
        if 'current_schedule' in st.session_state:
            for item in st.session_state.current_schedule:
                item['completed'] = False

    # Initialize notifications
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'notifications_enabled' not in st.session_state:
        st.session_state.notifications_enabled = False

    # Start notification thread (only once)
    if 'notification_thread' not in st.session_state:
        st.session_state.notification_thread = threading.Thread(
            target=check_for_upcoming_activities,
            daemon=True
        )
        st.session_state.notification_thread.start()

    # Main interface
    st.title("🍏 Health & Fitness Tracker")
    
    # Sidebar navigation
    menu = st.sidebar.selectbox("Select Option", 
                               ["BMI Calculator", "Ideal Weight Calculator", 
                                "Calorie Tracker", "Daily Schedule"])
    
    if menu == "BMI Calculator":
        st.header("BMI Calculator")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        
        if st.button("Calculate BMI"):
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            
            st.success(f"Your BMI: {bmi:.1f} ({category})")
            
            if category != "Normal weight":
                st.warning(f"Recommendation: You should aim for a BMI between 18.5 and 25. "
                          f"Consider consulting with a healthcare provider.")
    
    elif menu == "Ideal Weight Calculator":
        st.header("Ideal Weight Calculator")
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"])
        
        if st.button("Calculate Ideal Weight"):
            ideal_min, ideal_max = calculate_ideal_weight(height, gender)
            st.success(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
    
    elif menu == "Calorie Tracker":
        st.header("Calorie Tracker")
        
        # Get user info for recommendations
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"], key="cal_gender")
        
        # Calculate ideal weight for recommendations
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Food intake tracking
        st.subheader("Track Your Daily Food Intake")
        
        selected_foods = st.multiselect("Select foods you've eaten today", list(FOOD_CALORIES.keys()))
        quantities = {}
        
        for food in selected_foods:
            quantities[food] = st.number_input(f"Quantity of {food} (servings)", min_value=0.1, max_value=10.0, value=1.0, key=f"qty_{food}")
        
        if st.button("Calculate Total Calories"):
            total_calories = sum(FOOD_CALORIES[food] * quantities[food] for food in selected_foods)
            st.success(f"Total calories consumed today: {total_calories}")
            
            # Estimate daily calorie needs (simplified)
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * 30)  # assuming age 30
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * 30)
            
            activity_factor = 1.55  # moderately active
            daily_needs = bmr * activity_factor
            
            st.info(f"Estimated daily calorie needs: {daily_needs:.0f} (based on moderate activity)")
            
            if total_calories > daily_needs:
                st.warning(f"You've consumed {total_calories - daily_needs:.0f} calories more than your estimated needs.")
            else:
                st.warning(f"You've consumed {daily_needs - total_calories:.0f} calories less than your estimated needs.")
        
        # Suggestions section
        if st.button("Get Dietary Suggestions"):
            st.subheader("Dietary Suggestions Based on Your Profile")
            
            st.write(f"Your current weight: {weight} kg")
            st.write(f"Your ideal weight range: {ideal_min:.1f} kg to {ideal_max:.1f} kg")
            
            if diet_goal == "weight_loss":
                st.success("Goal: Healthy Weight Loss")
                st.write("To lose weight gradually, aim for a calorie deficit of 300-500 calories per day.")
            elif diet_goal == "weight_gain":
                st.success("Goal: Healthy Weight Gain")
                st.write("To gain weight gradually, aim for a calorie surplus of 300-500 calories per day.")
            else:
                st.success("Goal: Weight Maintenance")
                st.write("Maintain your current healthy weight with balanced nutrition.")
            
            st.subheader("Recommended Foods:")
            for food in FOOD_SUGGESTIONS[diet_goal]:
                st.write(f"- {food}")
            
            st.subheader("Additional Tips:")
            if diet_goal == "weight_loss":
                st.write("- Focus on high-fiber foods to feel full longer")
                st.write("- Drink plenty of water before meals")
                st.write("- Limit added sugars and processed foods")
            elif diet_goal == "weight_gain":
                st.write("- Eat more frequent, nutrient-dense meals")
                st.write("- Include healthy fats in your diet")
                st.write("- Combine with strength training to build muscle")
            else:
                st.write("- Maintain variety in your diet")
                st.write("- Practice portion control")
                st.write("- Stay physically active")
    
    elif menu == "Daily Schedule":
        st.header("📅 Your Daily Health Schedule")
        
        # Notification controls
        with st.expander("🔔 Notification Settings"):
            notifications_on = st.toggle("Enable Notifications", 
                                       value=st.session_state.notifications_enabled,
                                       key="notifications_toggle")
            st.session_state.notifications_enabled = notifications_on
            st.write("You'll get desktop reminders when it's time for scheduled activities")
        
        # Display notifications
        if 'notifications' in st.session_state and st.session_state.notifications:
            st.subheader("🔔 Notifications")
            for notification in st.session_state.notifications:
                st.warning(notification)
            if st.button("Clear Notifications"):
                st.session_state.notifications = []
                st.experimental_rerun()
        
        # Get user info to determine goal
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, key="schedule_weight")
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75, key="schedule_height")
        gender = st.radio("Gender", ["Male", "Female"], key="schedule_gender")
        
        # Calculate ideal weight and determine goal
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Display the appropriate schedule
        st.subheader(f"Recommended {diet_goal.replace('_', ' ').title()} Schedule")
        
        # Initialize session state for schedule if not exists
        if 'current_schedule' not in st.session_state:
            st.session_state.current_schedule = DAILY_SCHEDULES[diet_goal]
        
        # Display schedule with checkboxes
        completed_count = 0
        now = datetime.now().strftime("%I:%M %p")
        
        for i, item in enumerate(st.session_state.current_schedule):
            col1, col2, col3 = st.columns([1, 4, 2])
            with col1:
                # Checkbox to mark completion
                completed = st.checkbox("", 
                                      value=item['completed'], 
                                      key=f"completed_{i}",
                                      on_change=update_completion_status,
                                      args=(i,))
                if completed:
                    completed_count += 1
            with col2:
                # Highlight upcoming activities (within 30 minutes)
                activity_time = datetime.strptime(item['time'], "%I:%M %p")
                current_time = datetime.strptime(now, "%I:%M %p")
                time_diff = (activity_time - current_time).total_seconds() / 60
                
                if 0 <= time_diff <= 30 and not item['completed']:
                    st.markdown(f"⏰ **{item['time']}**: {item['activity']}", 
                               help="Upcoming soon!")
                else:
                    if item['type'] == "meal":
                        st.markdown(f"🍽️ **{item['time']}**: {item['activity']}")
                    elif item['type'] == "exercise":
                        st.markdown(f"🏋️ **{item['time']}**: {item['activity']}")
                    else:
                        st.markdown(f"⏰ **{item['time']}**: {item['activity']}")
            
            with col3:
                if not item['completed']:
                    st.caption(f"Due at {item['time']}")
                else:
                    st.caption("✓ Completed")
        
        # Progress tracking
        total_items = len(st.session_state.current_schedule)
        progress = completed_count / total_items
        st.progress(progress)
        st.caption(f"Completed {completed_count} of {total_items} tasks ({progress:.0%})")
        
        # Reset button
        if st.button("Reset Today's Progress"):
            reset_schedule()
            st.rerun()
        
        # Current time display
        st.markdown(f"🕒 Current time: {now}")

# This allows the file to be run standalone
if __name__ == "__main__":
    # st.set_page_config(
    #     page_title="Health & Fitness Tracker",
    #     page_icon="🍏",
    #     layout="wide"
    # )
    calorie_tracker_interface()