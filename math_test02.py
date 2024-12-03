import streamlit as st
import json
import os
import random

# Initialize the leaderboard file
LEADERBOARD_FILE = "leaderboard.json"
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump([], f)

# Load the leaderboard
def load_leaderboard():
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

# Save the leaderboard
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

# Update the leaderboard
def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
    save_leaderboard(leaderboard)

# Title of the app
st.markdown("<h1 style='text-align: center; color: brown;'>Arjun, complete all questions for a chocolate!</h1>", unsafe_allow_html=True)

# Generate questions dynamically from 1+1 to 1+50
questions = [{"question": f"What is 1+{i}?\n(options: {i}, {i+1}, {i+2}, {i+3})", "answer": str(1 + i)} for i in range(1, 51)]

# Initialize session state variables
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'consecutive_correct' not in st.session_state:
    st.session_state.consecutive_correct = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

# Function to display the quiz
def display_quiz():
    st.sidebar.markdown("<h2 style='color: green; font-family: Impact; font-size: 30px;'>Leaderboard</h2>", unsafe_allow_html=True)
    leaderboard = load_leaderboard()
    for entry in leaderboard:
        st.sidebar.markdown(f"<p style='color: white; font-family: Ink Free; font-size: 20px;'>{entry['name']}: {entry['score']}</p>", unsafe_allow_html=True)

    st.write(f"Answer this, {st.session_state.user_name}!")
    st.write(f"Correct answers provided by you: {st.session_state.consecutive_correct}")
    
    question_data = st.session_state.shuffled_questions[st.session_state.current_question]
    st.write(f"Question {st.session_state.current_question + 1}: {question_data['question']}")
    user_answer = st.text_input("Your answer:", key=f"answer_{st.session_state.current_question}")

    submit_answer = st.button("Submit Answer", key=f"submit_{st.session_state.current_question}")
    
    if submit_answer:
        if user_answer.lower().strip() == question_data['answer'].lower().strip():
            st.success("Correct!")
            st.session_state.score += 1
            st.session_state.consecutive_correct += 1
            st.session_state.current_question += 1

            if st.session_state.current_question >= len(st.session_state.shuffled_questions):
                st.balloons()
                st.success(f"Quiz completed! Your score is {st.session_state.score}/{len(st.session_state.shuffled_questions)}")
                st.write(f"Consecutive correct answers: {st.session_state.consecutive_correct}")
                update_leaderboard(st.session_state.user_name, st.session_state.consecutive_correct)
                if st.button("Restart Quiz", key="restart_button"):
                    restart_quiz()
        else:
            st.error("Incorrect!")
            update_leaderboard(st.session_state.user_name, st.session_state.consecutive_correct)
            restart_quiz()

# Function to restart the quiz
def restart_quiz():
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.consecutive_correct = 0

# Input for user's name
if st.session_state.user_name == '':
    st.session_state.user_name = st.text_input("Enter your name:", key="name")

# Display the quiz if the user's name is provided
if st.session_state.user_name:
    display_quiz()
