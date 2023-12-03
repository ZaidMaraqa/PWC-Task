import streamlit as st
import requests


if not st.session_state.get('quiz_started', False):
    st.markdown("""
    ## Welcome to the Quiz Application! 

    Follow these simple steps to get started:

    - **Step 1**: Enter the *topic* for your quiz in the sidebar.
    - **Step 2**: Select the *difficulty level* of the quiz.
    - **Step 3**: Specify the *number of questions* you want in your quiz.
    - **Step 4**: Click '**Generate Quiz**' to start.
    - **Step 5**: Answer each question. Navigate through the quiz using the '**Next**' and '**Back**' buttons.
    - **Step 6**: After answering all questions, click '**Submit Quiz**' to see your score.
    - **Step 7**: Before final submission, you will be asked to confirm your action.

    Enjoy the quiz and test your knowledge!
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'confirm_submission' not in st.session_state:
    st.session_state.confirm_submission = False

# Define a function to fetch questions and handle errors
def fetch_questions(topic, difficulty, number_of_questions):
    questions = []
    for _ in range(number_of_questions):
        response = requests.get(f'http://127.0.0.1:8000/api/generate-quiz/{topic}/{difficulty}/')
        if response.status_code == 200:
            question_data = response.json()
            questions.append(question_data)
        else:
            st.error('Error fetching questions')
            return None  # Return None to indicate that an error occurred
    return questions




# Sidebar for user inputs
if not st.session_state.get('quiz_started', False):
    with st.sidebar:
        topic = st.text_input("Enter the topic for your quiz:", key="topic")
        difficulty = st.selectbox("Select the difficulty level:", ["Easy", "Medium", "Hard"], key="difficulty")
        number_of_questions = st.number_input("How many questions do you want?", min_value=1, max_value=10, step=1, key="num_questions")
        if st.button(f'Generate {topic} Quiz'):
            # Quiz generation logic
            if not topic.strip():  # Check if topic is empty or contains only whitespace
                st.error('Please enter a topic.')
            else:
                # Fetch the questions and check for errors
                fetched_questions = fetch_questions(topic, difficulty, number_of_questions)
                if fetched_questions is not None:  # Proceed only if no error occurred
                    st.session_state.questions = fetched_questions
                    st.session_state.current_question = 0
                    st.session_state.user_answers = {}
                    st.session_state.quiz_started = True
                    st.rerun()  # Force a re-render here after updating the session state

# Quiz navigation and display
# Display a single question at a time
if st.session_state.get('quiz_started', False) and not st.session_state.get('quiz_submitted', False):

    current_question = st.session_state.current_question
    q_data = st.session_state.questions[current_question]
    
    st.empty()
    st.subheader(f'Question {current_question + 1}')
    st.write(f"{q_data['question']}")  # Display the question text
    selected_option = st.radio("Select an answer", q_data['options'], key=f'answer_{current_question}')

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if current_question > 0 and st.button('Back'):
            st.session_state.current_question -= 1
            st.rerun()

    with col2:
        if current_question < len(st.session_state.questions) - 1:
            if st.button('Next'):
                # Store the answer and increment the question
                st.session_state.user_answers[current_question] = selected_option
                st.session_state.current_question += 1
                st.rerun()
        else:
            # Last question logic
            if st.button('Submit Quiz'):
                st.session_state.user_answers[current_question] = selected_option
                st.session_state.confirm_submission = True
                st.empty()
                st.rerun()

# Display confirmation options
if st.session_state.confirm_submission:

    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.markdown('---')
        st.markdown('### Are you sure you want to submit the quiz?')
        st.markdown('Please confirm your submission or cancel to review your answers.')

        # Create two buttons side by side for confirmation
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Confirm'):
                st.session_state.quiz_submitted = True
                st.session_state.confirm_submission = False
                st.rerun()
        with col2:
            if st.button('Cancel'):
                st.session_state.confirm_submission = False
                st.rerun()

        st.markdown('---')


if st.session_state.get('quiz_submitted', False):
    # Calculate the score
    score = 0
    for i, q_data in enumerate(st.session_state.questions, start=0):
        user_answer = st.session_state.user_answers.get(i, '').strip()  # Safely get the answer or an empty string
        correct_answer = q_data['correct_answer'].strip()

        if user_answer == correct_answer:
            score += 1
    
    # Display the score
    st.markdown(f"<h1 style='text-align: center;'>Your Score: {score}/{len(st.session_state.questions)}</h1>", unsafe_allow_html=True)

    # Create a table for the results
    st.markdown("## Detailed Results")
    for i, q_data in enumerate(st.session_state.questions, start=0):
        user_answer = st.session_state.user_answers.get(i, '').strip()
        correct_answer = q_data['correct_answer'].strip()
        
        # Color the text based on whether the answer was correct
        answer_color = "green" if user_answer == correct_answer else "red"
        
        # Use markdown to format the results as a table
        st.markdown(f"""
        <style>
        .reportview-container .main .block-container{{
            max-width: 800px;
        }}
        .big-font {{
            font-size: 20px !important;
            font-weight: bold;
            font-family: Monospace;
        }}
        </style>
        
        <div class="big-font" style="color: {answer_color};">
            Question {i + 1}: {q_data['question']}<br>
            Your answer: {user_answer} | Correct answer: {correct_answer}
        </div>
        """, unsafe_allow_html=True)

        # Optionally, display an explanation if provided in q_data
        if 'explanation' in q_data:
            st.markdown(f"##### Explanation: {q_data['explanation']}")
        
        st.markdown("---")  # Horizontal line for separation between questions

    # Button to restart the quiz
    if st.button('Restart Quiz'):
        st.session_state.quiz_started = False
        st.session_state.quiz_submitted = False
        st.rerun()