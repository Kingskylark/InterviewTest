import streamlit as st
import pandas as pd
import time

# Load questions from the CSV file
df = pd.read_csv("ibom_air_recruitment_questions.csv")

# Shuffle questions only once when the app starts
if 'questions' not in st.session_state:
    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)

# Session state for managing test state and timer
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'time_left' not in st.session_state:
    st.session_state.time_left = 30 * 60  # 30 minutes in seconds

# Start Test button
if st.button("Start Test"):
    st.session_state.test_started = True
    st.session_state.start_time = time.time()
    st.session_state.time_left = 30 * 60  # Reset time left
    st.session_state.answers = {}  # Reset answers

# Timer logic
if st.session_state.test_started:
    elapsed_time = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, 30 * 60 - elapsed_time)  # Calculate time left

    if st.session_state.time_left <= 0:
        st.warning("Time is up! Please submit your answers.")
        st.session_state.test_started = False

    # Display remaining time
    mins, secs = divmod(int(st.session_state.time_left), 60)
    st.sidebar.write(f"Time Left: {mins:02d}:{secs:02d}")

    # Display questions and options
    for idx, row in st.session_state.questions.iterrows():
        st.subheader(f"Q{idx + 1}. {row['Question']}")
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        
        # Preserve previous selection if exists
        selected_option = st.session_state.answers.get(idx, None)

        # Safely get the index of the selected option, if it exists
        if selected_option in options:
            selected_index = options.index(selected_option)
        else:
            selected_index = None

        # Capture the selected option and store it
        answer = st.radio(
            "Choose an option:", 
            options, 
            key=f"q{idx}", 
            index=selected_index
        )
        
        # Store the letter corresponding to the selected option
        letter_answer = chr(65 + options.index(answer)) if answer in options else None  # 65 is ASCII for 'A'
        st.session_state.answers[idx] = letter_answer  # Update the answers dictionary

    # Submit answers button
    if st.button("Submit Answers"):
        score = 0
        total_questions = len(st.session_state.questions)
        for idx, row in st.session_state.questions.iterrows():
            correct_answer = row['Correct Answer']  # Assuming this is 'A', 'B', 'C', or 'D'
            user_answer = st.session_state.answers.get(idx, None)  # Get the user's letter answer
            
            # Display the user's answer and the correct answer
            st.write(f"Q{idx + 1}: Your answer: {user_answer}, Correct answer: {correct_answer}")

            if user_answer == correct_answer:
                score += 1
        
        st.success(f"Your score: {score}/{total_questions}")
        st.session_state.test_started = False  # Reset test state after submission

else:
    st.sidebar.write("Press the button above to start the test.")
