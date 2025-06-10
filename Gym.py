import streamlit as st
import requests
from datetime import datetime

# Define the weekly schedule for muscle groups
day_names = {
    1: "Chest",
    2: "Shoulders",
    3: "Back",
    4: "Legs",
    5: "Arms",
    6: "Abs",
    7: "Rest"
}

# Define muscle IDs for each day (based on wger.de API)
muscle_groups = {
    1: [1],  # Chest (Pectoralis major)
    2: [12],  # Shoulders (Deltoids)
    3: [2, 3, 4],  # Back (Latissimus dorsi, Trapezius, Erector spinae)
    4: [6, 7, 13, 8],  # Legs (Quadriceps, Hamstrings, Gluteus maximus, Gastrocnemius)
    5: [10, 11],  # Arms (Biceps, Triceps)
    6: [5],  # Abs (Rectus abdominis)
    7: []  # Rest
}

# Initialize session state for user inputs
if 'age' not in st.session_state:
    st.session_state.age = None
if 'gender' not in st.session_state:
    st.session_state.gender = None

# Streamlit App Title
st.title("Daily Weight Training Suggestion")

# User Input: Age
if st.session_state.age is None:
    age = st.number_input("Enter your age", min_value=1, max_value=120, value=30)
    if st.button("Save Age"):
        st.session_state.age = age
else:
    st.write(f"Age: {st.session_state.age}")

# User Input: Gender
if st.session_state.gender is None:
    gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
    if st.button("Save Gender"):
        st.session_state.gender = gender
else:
    st.write(f"Gender: {st.session_state.gender}")

# Get today's day (1-7, Monday=1, Sunday=7)
today = datetime.today().weekday() + 1

# Check if today is a rest day
if today == 7:
    st.write("Today is rest day. Enjoy your break!")
else:
    # User Input: Planned exercise time
    planned_time = st.selectbox("When do you plan to exercise today?", ["Morning", "Afternoon", "Evening"])

    # User Input: Food intake
    food_intake = st.selectbox("Have you eaten in the last 2 hours?", ["Yes", "No"])
    if food_intake == "Yes":
        meal_size = st.selectbox("What size was your meal?", ["Small", "Medium", "Large"])
    else:
        meal_size = None

    # Fetch exercises for today's muscle group
    muscles = muscle_groups[today]
    exercises = []
    for muscle in muscles:
        url = f"https://wger.de/api/v2/exercise/?muscle={muscle}&category=1&limit=5"  # Category 1 = Strength
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            exercises.extend(data['results'])

    # Fetch images for each exercise
    exercise_with_images = []
    for ex in exercises:
        ex_id = ex['id']
        img_url = f"https://wger.de/api/v2/exerciseimage/?exercise={ex_id}&limit=1"
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            img_data = img_response.json()
            if img_data['results']:
                image = img_data['results'][0]['image']
            else:
                image = None
        else:
            image = None
        exercise_with_images.append((ex['name'], image, ex.get('description', 'No description available')))

    # Display today's workout
    st.title(f"Today's Workout: {day_names[today]}")
    for name, img, desc in exercise_with_images:
        st.subheader(name)
        if img:
            st.image(img, width=300)
        st.write(desc)

    # Provide notes based on age and food intake
    if st.session_state.age and st.session_state.age > 50:
        st.write("Since you're over 50, ensure proper form and start with lighter weights to avoid injury.")
    if meal_size == "Large":
        st.write("Since you've had a large meal recently, consider waiting 30 minutes before starting intense exercise to prevent discomfort.")
    elif meal_size in ["Small", "Medium"]:
        st.write("You've eaten recently, so you should have enough energy for your workout. Ensure proper hydration.")
    elif food_intake == "No":
        st.write("Since you haven't eaten recently, consider a small snack before exercising to boost energy levels.")

    # Provide a tip based on planned exercise time
    if planned_time == "Morning":
        st.write("Morning workouts can boost your metabolism and energy for the day.")
    elif planned_time == "Afternoon":
        st.write("Afternoon workouts can provide a great energy boost midway through the day.")
    elif planned_time == "Evening":
        st.write("Evening workouts can help you unwind and promote better sleep.")