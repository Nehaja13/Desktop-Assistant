import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from plyer import notification
def calorie_tracker_interface(conn=None):
    # Calorie database (simplified) with health tags
    FOOD_CALORIES = {
        "Apple": {"calories": 52, "tags": ["diabetes", "heart"]},
        "Banana": {"calories": 89, "tags": ["heart"]},
        "Orange": {"calories": 47, "tags": ["diabetes", "heart"]},
        "Grapes": {"calories": 69, "tags": []},
        "Chicken Breast": {"calories": 165, "tags": ["diabetes", "heart"]},
        "Salmon": {"calories": 208, "tags": ["heart", "blood_pressure"]},
        "Egg": {"calories": 68, "tags": ["heart"]},
        "White Rice": {"calories": 130, "tags": []},
        "Brown Rice": {"calories": 111, "tags": ["diabetes"]},
        "Whole Wheat Bread": {"calories": 69, "tags": ["diabetes"]},
        "Milk": {"calories": 42, "tags": []},
        "Yogurt": {"calories": 59, "tags": ["diabetes"]},
        "Cheese": {"calories": 113, "tags": ["blood_pressure"]},
        "Broccoli": {"calories": 34, "tags": ["diabetes", "heart", "blood_pressure"]},
        "Carrot": {"calories": 41, "tags": ["diabetes", "heart"]},
        "Spinach": {"calories": 23, "tags": ["diabetes", "heart", "blood_pressure"]},
        "Potato": {"calories": 77, "tags": []},
        "Pasta": {"calories": 131, "tags": []},
        "Pizza": {"calories": 266, "tags": []},
        "Hamburger": {"calories": 295, "tags": []},
        "French Fries": {"calories": 312, "tags": []},
        "Ice Cream": {"calories": 207, "tags": []},
        "Chocolate": {"calories": 546, "tags": []},
        "Nuts": {"calories": 607, "tags": ["heart", "blood_pressure"]},
        "Water": {"calories": 0, "tags": ["all"]}
    }
    
    # Disease-specific recommendations
    DISEASE_RECOMMENDATIONS = {
        "diabetes": {
            "foods": ["Vegetables", "Whole grains", "Lean proteins", "Berries", "Nuts"],
            "avoid": ["Sugary foods", "White bread", "Fruit juices", "Processed snacks"],
            "tips": [
                "Monitor carbohydrate intake",
                "Eat at regular intervals",
                "Choose low glycemic index foods",
                "Stay hydrated with water"
            ]
        },
        "blood_pressure": {
            "foods": ["Leafy greens", "Berries", "Beets", "Oatmeal", "Bananas"],
            "avoid": ["High-sodium foods", "Processed meats", "Pickled foods", "Canned soups"],
            "tips": [
                "Limit salt intake",
                "Increase potassium-rich foods",
                "Maintain healthy weight",
                "Limit alcohol consumption"
            ]
        },
        "heart": {
            "foods": ["Fatty fish", "Nuts", "Berries", "Oats", "Dark chocolate"],
            "avoid": ["Trans fats", "Processed meats", "Fried foods", "Sugary drinks"],
            "tips": [
                "Choose healthy fats",
                "Increase fiber intake",
                "Exercise regularly",
                "Manage stress levels"
            ]
        }
    }

    # Base daily schedules
    BASE_SCHEDULES = {
        "weight_loss": [
            {"time": "7:00 AM", "activity": "Wake up and drink warm water", "type": "routine", "essential": True},
            {"time": "7:30 AM", "activity": "Morning walk (30 min)", "type": "exercise", "essential": False},
            {"time": "8:00 AM", "activity": "Breakfast: Oatmeal with berries", "type": "meal", "essential": True},
            {"time": "10:30 AM", "activity": "Snack: Apple with almonds", "type": "meal", "essential": False},
            {"time": "1:00 PM", "activity": "Lunch: Grilled chicken with vegetables", "type": "meal", "essential": True},
            {"time": "4:00 PM", "activity": "Snack: Greek yogurt", "type": "meal", "essential": False},
            {"time": "6:30 PM", "activity": "Dinner: Salmon with quinoa", "type": "meal", "essential": True},
            {"time": "8:00 PM", "activity": "Light stretching (15 min)", "type": "exercise", "essential": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "essential": True}
        ],
        "weight_gain": [
            {"time": "7:00 AM", "activity": "Wake up and protein shake", "type": "routine", "essential": True},
            {"time": "7:30 AM", "activity": "Strength training (45 min)", "type": "exercise", "essential": False},
            {"time": "8:30 AM", "activity": "Breakfast: Scrambled eggs with toast and avocado", "type": "meal", "essential": True},
            {"time": "10:30 AM", "activity": "Snack: Banana with peanut butter", "type": "meal", "essential": False},
            {"time": "1:00 PM", "activity": "Lunch: Beef with rice and vegetables", "type": "meal", "essential": True},
            {"time": "4:00 PM", "activity": "Snack: Nuts and dried fruits", "type": "meal", "essential": False},
            {"time": "6:30 PM", "activity": "Dinner: Pasta with chicken", "type": "meal", "essential": True},
            {"time": "9:00 PM", "activity": "Protein shake before bed", "type": "meal", "essential": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "essential": True}
        ],
        "weight_maintenance": [
            {"time": "7:00 AM", "activity": "Wake up and lemon water", "type": "routine", "essential": True},
            {"time": "7:30 AM", "activity": "Yoga or light exercise (30 min)", "type": "exercise", "essential": False},
            {"time": "8:00 AM", "activity": "Breakfast: Whole grain toast with eggs", "type": "meal", "essential": True},
            {"time": "10:30 AM", "activity": "Snack: Fruit and nuts", "type": "meal", "essential": False},
            {"time": "1:00 PM", "activity": "Lunch: Balanced meal with protein and veggies", "type": "meal", "essential": True},
            {"time": "4:00 PM", "activity": "Snack: Hummus with vegetables", "type": "meal", "essential": False},
            {"time": "6:30 PM", "activity": "Dinner: Fish with sweet potato", "type": "meal", "essential": True},
            {"time": "8:00 PM", "activity": "Evening walk (20 min)", "type": "exercise", "essential": False},
            {"time": "10:30 PM", "activity": "Sleep time", "type": "routine", "essential": True}
        ]
    }

    def get_disease_specific_schedule(base_schedule, diseases):
        """Modify schedule based on diseases"""
        modified_schedule = []
        
        for item in base_schedule:
            new_item = item.copy()
            
            # Modify meal suggestions for diseases
            if item["type"] == "meal":
                if "diabetes" in diseases and "sugar" in item["activity"].lower():
                    new_item["activity"] = item["activity"].replace("sugar", "stevia")
                
                if "blood_pressure" in diseases and "cheese" in item["activity"].lower():
                    new_item["activity"] = item["activity"].replace("cheese", "avocado")
                
                if "heart" in diseases and "fried" in item["activity"].lower():
                    new_item["activity"] = item["activity"].replace("fried", "grilled")
            
            modified_schedule.append(new_item)
        
        # Add disease-specific activities
        if "diabetes" in diseases:
            modified_schedule.append({
                "time": "9:00 PM",
                "activity": "Blood sugar check",
                "type": "health_check",
                "essential": True
            })
        
        if "blood_pressure" in diseases:
            modified_schedule.append({
                "time": "8:30 AM",
                "activity": "Blood pressure check",
                "type": "health_check",
                "essential": True
            })
        
        return modified_schedule

    def adjust_schedule_for_events(base_schedule, events):
        """Adjust schedule based on events"""
        adjusted_schedule = []
        
        for item in base_schedule:
            # Skip non-essential items during events
            if not item["essential"] and any(event["time"] == item["time"] for event in events):
                continue
                
            adjusted_schedule.append(item)
        
        # Add event items
        for event in events:
            adjusted_schedule.append({
                "time": event["time"],
                "activity": f"Event: {event['name']}",
                "type": "event",
                "essential": False
            })
        
        # Sort by time
        adjusted_schedule.sort(key=lambda x: datetime.strptime(x["time"], "%I:%M %p"))
        
        return adjusted_schedule

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
                        if not item.get('completed', False) and item['time'] == now:
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
    
    if menu == "Daily Schedule":
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
        
        # Get user info to determine goal and health conditions
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, key="schedule_weight")
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75, key="schedule_height")
        gender = st.radio("Gender", ["Male", "Female"], key="schedule_gender")
        
        # Health conditions
        st.subheader("Health Conditions")
        conditions = st.multiselect("Select any health conditions you have", 
                                  ["diabetes", "blood_pressure", "heart"])
        
        # Calculate ideal weight and determine goal
        ideal_min, ideal_max = calculate_ideal_weight(height, gender)
        diet_goal = get_diet_goal(weight, (ideal_min, ideal_max))
        
        # Event scheduling
        st.subheader("Today's Events")
        events = []
        with st.expander("Add Events/Appointments"):
            event_name = st.text_input("Event name")
            event_time = st.time_input("Event time")
            if st.button("Add Event"):
                events.append({
                    "name": event_name,
                    "time": event_time.strftime("%I:%M %p")
                })
        
        # Generate the customized schedule
        base_schedule = BASE_SCHEDULES[diet_goal]
        
        # Apply disease-specific modifications
        if conditions:
            base_schedule = get_disease_specific_schedule(base_schedule, conditions)
        
        # Apply event-based adjustments
        if events:
            base_schedule = adjust_schedule_for_events(base_schedule, events)
        
        # Initialize session state for schedule if not exists
        if 'current_schedule' not in st.session_state:
            st.session_state.current_schedule = base_schedule
        
        # Display health recommendations if conditions exist
        if conditions:
            st.subheader("Health Recommendations")
            for condition in conditions:
                with st.expander(f"Recommendations for {condition.replace('_', ' ').title()}"):
                    st.write("**Recommended Foods:**")
                    for food in DISEASE_RECOMMENDATIONS[condition]["foods"]:
                        st.write(f"- {food}")
                    
                    st.write("\n**Foods to Avoid:**")
                    for food in DISEASE_RECOMMENDATIONS[condition]["avoid"]:
                        st.write(f"- {food}")
                    
                    st.write("\n**Lifestyle Tips:**")
                    for tip in DISEASE_RECOMMENDATIONS[condition]["tips"]:
                        st.write(f"- {tip}")
        
        # Display the customized schedule
        st.subheader(f"Your Customized {diet_goal.replace('_', ' ').title()} Schedule")
        
        # Display schedule with checkboxes
        completed_count = 0
        now = datetime.now().strftime("%I:%M %p")
        
        for i, item in enumerate(st.session_state.current_schedule):
            col1, col2, col3 = st.columns([1, 4, 2])
            with col1:
                # Checkbox to mark completion
                completed = st.checkbox("", 
                                      value=item.get('completed', False), 
                                      key=f"completed_{i}",
                                      on_change=update_completion_status,
                                      args=(i,))
                if completed:
                    completed_count += 1
            with col2:
                # Style based on type
                if item['type'] == "meal":
                    icon = "🍽️"
                    color = "green"
                elif item['type'] == "exercise":
                    icon = "🏋️"
                    color = "blue"
                elif item['type'] == "health_check":
                    icon = "❤️"
                    color = "red"
                elif item['type'] == "event":
                    icon = "📅"
                    color = "purple"
                else:  # routine
                    icon = "⏰"
                    color = "orange"
                
                # Highlight upcoming activities (within 30 minutes)
                activity_time = datetime.strptime(item['time'], "%I:%M %p")
                current_time = datetime.strptime(now, "%I:%M %p")
                time_diff = (activity_time - current_time).total_seconds() / 60
                
                if 0 <= time_diff <= 30 and not item.get('completed', False):
                    st.markdown(f"<span style='color:red'>⏰ **{item['time']}**: {item['activity']}</span>", 
                               unsafe_allow_html=True, help="Upcoming soon!")
                else:
                    st.markdown(f"<span style='color:{color}'>{icon} **{item['time']}**: {item['activity']}</span>", 
                               unsafe_allow_html=True)
            
            with col3:
                if not item.get('completed', False):
                    st.caption(f"Due at {item['time']}")
                else:
                    st.caption("✓ Completed")
        
        # Progress tracking
        total_items = len(st.session_state.current_schedule)
        progress = completed_count / total_items if total_items > 0 else 0
        st.progress(progress)
        st.caption(f"Completed {completed_count} of {total_items} tasks ({progress:.0%})")
        
        # Reset button
        if st.button("Reset Today's Progress"):
            reset_schedule()
            st.rerun()
        
        # Current time display
        st.markdown(f"🕒 Current time: {now}")
        
        # Export schedule option
        '''st.subheader("Export/Import Schedule")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export Schedule to CSV"):
                df = pd.DataFrame(st.session_state.current_schedule)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="health_schedule.csv",
                    mime="text/csv"
                )
        with col2:
            uploaded_file = st.file_uploader("Import Schedule", type=["csv"])
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.current_schedule = df.to_dict('records')
                    st.success("Schedule imported successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error importing schedule: {str(e)}")'''
    
    elif menu == "Calorie Tracker":
        st.header("Calorie Tracker")
        
        # Get user info for recommendations
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        with col2:
            height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75)
        gender = st.radio("Gender", ["Male", "Female"], key="cal_gender")
        age = st.number_input("Age", min_value=10, max_value=100, value=30)
        activity_level = st.selectbox("Activity Level", [
            "Sedentary (little or no exercise)",
            "Lightly active (light exercise/sports 1-3 days/week)",
            "Moderately active (moderate exercise/sports 3-5 days/week)",
            "Very active (hard exercise/sports 6-7 days/week)",
            "Extra active (very hard exercise & physical job)"
        ])
        
        # Health conditions for food filtering
        conditions = st.multiselect("Any health conditions to consider?", 
                                  ["diabetes", "blood_pressure", "heart"])
        
        # Food intake tracking
        st.subheader("Track Your Daily Food Intake")
        
        # Get all food options, filtered by health conditions if any
        all_foods = list(FOOD_CALORIES.keys())
        if conditions:
            filtered_foods = [food for food in all_foods 
                            if any(tag in conditions for tag in FOOD_CALORIES[food]["tags"])]
        else:
            filtered_foods = all_foods
        
        selected_foods = st.multiselect("Select foods you've eaten today", filtered_foods)
        quantities = {}
        
        for food in selected_foods:
            quantities[food] = st.number_input(f"Quantity of {food} (servings)", 
                                             min_value=0.1, max_value=10.0, 
                                             value=1.0, key=f"qty_{food}")
        
        if st.button("Calculate Total Calories"):
            # Calculate total consumed calories
            total_calories = sum(FOOD_CALORIES[food]["calories"] * quantities[food] 
                           for food in selected_foods)
            
            # Calculate daily calorie needs (using Mifflin-St Jeor Equation)
            if gender == "Male":
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161
            
            # Apply activity factor
            activity_factors = {
                "Sedentary (little or no exercise)": 1.2,
                "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
                "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
                "Very active (hard exercise/sports 6-7 days/week)": 1.725,
                "Extra active (very hard exercise & physical job)": 1.9
            }
            daily_needs = bmr * activity_factors[activity_level]
            
            remaining_calories = daily_needs - total_calories
            
            # Display results
            st.success(f"Total calories consumed today: {total_calories}")
            st.info(f"Estimated daily calorie needs: {daily_needs:.0f}")
            
            if remaining_calories > 0:
                st.warning(f"You have {remaining_calories:.0f} calories remaining for today")
                
                # Suggest healthy food combinations based on remaining calories
                st.subheader("🍎 Healthy Food Suggestions")
                
                # Define healthy food combinations with approximate calories
                healthy_combinations = {
                    "Under 200 calories": [
                        "1 medium apple (95 cal) with 10 almonds (70 cal)",
                        "1 hard-boiled egg (70 cal) with cucumber slices (30 cal)",
                        "1 cup mixed berries (80 cal) with 1 tbsp Greek yogurt (20 cal)",
                        "1 small banana (90 cal) with 1 tsp peanut butter (30 cal)",
                        "1 cup carrot sticks (50 cal) with 2 tbsp hummus (70 cal)"
                    ],
                    "200-400 calories": [
                        "Whole wheat toast (100 cal) with avocado (120 cal) and poached egg (70 cal)",
                        "Greek yogurt (150 cal) with granola (100 cal) and honey (50 cal)",
                        "Salad with greens (30 cal), grilled chicken (150 cal), and olive oil dressing (100 cal)",
                        "Oatmeal (150 cal) with nuts (100 cal) and berries (50 cal)",
                        "Rice cake (60 cal) with almond butter (100 cal) and banana slices (80 cal)"
                    ],
                    "400-600 calories": [
                        "Grilled salmon (300 cal) with quinoa (150 cal) and steamed vegetables (100 cal)",
                        "Whole wheat pasta (200 cal) with marinara sauce (100 cal) and turkey meatballs (200 cal)",
                        "Stir-fry with tofu (200 cal), brown rice (200 cal), and mixed vegetables (100 cal)",
                        "Chicken wrap with whole wheat tortilla (200 cal), veggies (50 cal), and hummus (150 cal)",
                        "Sweet potato (150 cal) with black beans (150 cal), salsa (50 cal), and avocado (150 cal)"
                    ],
                    "600+ calories": [
                        "Balanced meal with protein (300 cal), complex carbs (300 cal), and healthy fats (200 cal)",
                        "Large salad with grilled chicken (300 cal), quinoa (200 cal), nuts (150 cal), and dressing (100 cal)",
                        "Bowl with brown rice (200 cal), beans (200 cal), veggies (100 cal), and guacamole (200 cal)",
                        "Whole grain sandwich with turkey (300 cal), cheese (200 cal), and veggies (100 cal)",
                        "Grilled fish (300 cal) with roasted potatoes (300 cal) and sautéed greens (100 cal)"
                    ]
                }
                
                # Determine which range the remaining calories fall into
                if remaining_calories < 200:
                    calorie_range = "Under 200 calories"
                elif 200 <= remaining_calories < 400:
                    calorie_range = "200-400 calories"
                elif 400 <= remaining_calories < 600:
                    calorie_range = "400-600 calories"
                else:
                    calorie_range = "600+ calories"
                
                st.write(f"**Suggested healthy combinations ({calorie_range}):**")
                for combo in healthy_combinations[calorie_range]:
                    st.write(f"- {combo}")
                
                # Macronutrient-balanced suggestions
                st.write("\n**Macronutrient-balanced options:**")
                if remaining_calories < 300:
                    st.write("- Focus on protein+fat or protein+carbs combos for satiety")
                    st.write("- Example: Greek yogurt with berries or apple with peanut butter")
                else:
                    st.write("- Aim for complete meals with protein, carbs, and healthy fats")
                    st.write("- Example: Grilled chicken with quinoa and roasted vegetables")
                
                # Time-based suggestions
                current_hour = datetime.now().hour
                if current_hour < 11:  # Morning
                    st.write("\n**Morning-appropriate suggestions:**")
                    st.write("- Oatmeal with nuts and fruit")
                    st.write("- Whole grain toast with avocado and egg")
                    st.write("- Smoothie with Greek yogurt, berries, and spinach")
                elif 11 <= current_hour < 16:  # Afternoon
                    st.write("\n**Lunch-appropriate suggestions:**")
                    st.write("- Salad with lean protein and whole grains")
                    st.write("- Whole grain wrap with hummus and veggies")
                    st.write("- Soup with beans and vegetables")
                else:  # Evening
                    st.write("\n**Dinner-appropriate suggestions:**")
                    st.write("- Grilled fish with roasted vegetables")
                    st.write("- Stir-fry with tofu and brown rice")
                    st.write("- Lentil curry with whole wheat naan")
                
                # Additional tips
                st.write("\n**Healthy eating tips:**")
                st.write("- Include protein in every meal/snack for satiety")
                st.write("- Choose whole foods over processed options")
                st.write("- Stay hydrated - sometimes thirst is mistaken for hunger")
                st.write("- Eat slowly and mindfully to recognize fullness cues")
                
            elif remaining_calories < 0:
                st.error(f"You've exceeded your daily needs by {-remaining_calories:.0f} calories")
                st.subheader("🔄 Balance Your Intake")
                
                st.write("**Exercise suggestions to offset excess calories:**")
                exercise_options = [
                    ("Walking (30 min)", 150),
                    ("Cycling (30 min)", 250),
                    ("Swimming (30 min)", 300),
                    ("Yoga (60 min)", 200),
                    ("HIIT workout (20 min)", 250)
                ]
                
                for exercise, calories in exercise_options:
                    st.write(f"- {exercise} burns ~{calories} calories")
                
                st.write("\n**Next meal adjustment suggestions:**")
                st.write("- Reduce portion sizes slightly at your next meal")
                st.write("- Choose lower-calorie density foods (more vegetables)")
                st.write("- Skip calorie-dense beverages and snacks")
                
            else:
                st.success("Perfect! You've met your daily calorie needs exactly.")
                st.write("**Maintenance tips:**")
                st.write("- Continue with your balanced eating pattern")
                st.write("- Stay active to maintain your current weight")
                st.write("- Monitor your intake to stay on track")
        
        # Disease-specific food suggestions
        if conditions:
            st.subheader("Food Recommendations for Your Conditions")
            for condition in conditions:
                with st.expander(f"Recommendations for {condition.replace('_', ' ').title()}"):
                    st.write("**Recommended Foods:**")
                    for food in DISEASE_RECOMMENDATIONS[condition]["foods"]:
                        st.write(f"- {food}")
                    
                    st.write("\n**Foods to Avoid:**")
                    for food in DISEASE_RECOMMENDATIONS[condition]["avoid"]:
                        st.write(f"- {food}")
                    
                    st.write("\n**Special Considerations:**")
                    for tip in DISEASE_RECOMMENDATIONS[condition]["tips"]:
                        st.write(f"- {tip}")
    
    elif menu == "BMI Calculator":
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

# This allows the file to be run standalone
if __name__ == "__main__":
    calorie_tracker_interface()


