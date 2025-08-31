import random

# This dictionary holds all the static data for a problem.
# In a real app, this would come from a database.
PROBLEM_DATA = {
    "text": "2x + 5 = 15",
    "topic": "Mathematics - Linear Equations",
    "steps": [
        {
            "question": "What do you think is a good first move to start getting 'x' by itself?",
            "answer_keywords": ["subtract 5", "- 5"],
            "correct_response": "We now have `2x = 10`.",
            "hints": [
                "Think about how we can undo the operations being done to 'x'.",
                "We have a '+ 5' on the same side as the 'x'. What's the opposite of adding 5?",
                "Try subtracting 5 from both sides of the equation."
            ]
        },
        {
            "question": "What's the final step to isolate 'x'?",
            "answer_keywords": ["divide by 2", "/ 2"],
            "correct_response": "We get `x = 5`.",
            "hints": [
                "Now we have '2x'. What operation is happening between the '2' and the 'x'?",
                "To undo multiplication, we need to use its opposite operation.",
                "Try dividing both sides by 2."
            ]
        }
    ],
    "solution": "5",
}

POSITIVE_REINFORCEMENT = [
    "Excellent!",
    "That's exactly right!",
    "Great thinking!",
    "You're on the right track!",
    "Perfect!",
    "Awesome!"
]

def get_initial_state():
    """Returns the initial state for a new user session."""
    return {
        "mode": "STUDY",
        "current_step": 0,
        "hint_level": 0,
        "problem_solved": False
    }

def get_welcome_message():
    """Returns the initial messages for the user."""
    state = get_initial_state()
    question = PROBLEM_DATA['steps'][state['current_step']]['question']
    return [
        "Welcome to CogniTutor! I'm here to help you learn.",
        f"Let's work on this problem: Solve the equation `{PROBLEM_DATA['text']}`.",
        question
    ]

def process_message(user_input, session_state):
    """
    Processes a user's message and updates the session state.
    Returns a list of bot responses.
    """
    responses = []
    user_input = user_input.strip()

    # Handle mode switching first
    if user_input.upper() == "[MODE: EXAM]":
        session_state['mode'] = "EXAM"
        responses.append("Switched to EXAM mode. I will now wait for your final answer without providing hints.")
        responses.append(f"The problem is: `{PROBLEM_DATA['text']}`. What is the value of x?")
        return responses, session_state
    elif user_input.upper() == "[MODE: STUDY]":
        session_state['mode'] = "STUDY"
        # Reset progress when switching back to study
        session_state['current_step'] = 0
        session_state['hint_level'] = 0
        session_state['problem_solved'] = False
        question = PROBLEM_DATA['steps'][session_state['current_step']]['question']
        responses.append("Switched to STUDY mode. I will guide you step-by-step.")
        responses.append(question)
        return responses, session_state

    # Handle mode-specific logic
    if session_state['mode'] == 'STUDY':
        return _handle_study_mode(user_input, session_state)
    else: # EXAM mode
        return _handle_exam_mode(user_input, session_state)

def _handle_study_mode(user_input, session_state):
    responses = []
    if session_state.get('problem_solved', False):
        responses.append("We've already solved this one! Please refresh to start a new problem.")
        return responses, session_state

    step_info = PROBLEM_DATA['steps'][session_state['current_step']]

    if user_input.lower() == 'hint':
        hint, session_state = _give_hint(session_state)
        responses.append(hint)
        return responses, session_state

    if any(keyword in user_input.lower() for keyword in step_info['answer_keywords']):
        responses.append(f"{random.choice(POSITIVE_REINFORCEMENT)} {step_info['correct_response']}")
        session_state['current_step'] += 1
        session_state['hint_level'] = 0  # Reset hints

        if session_state['current_step'] < len(PROBLEM_DATA['steps']):
            next_step_info = PROBLEM_DATA['steps'][session_state['current_step']]
            responses.append(next_step_info['question'])
        else:
            responses.append("You've solved the problem! Nicely done.")
            responses.append(f"[TOPIC: {PROBLEM_DATA['topic']}]")
            session_state['problem_solved'] = True
    else:
        responses.append("Not quite. Try again, or say 'hint' if you're stuck.")

    return responses, session_state

def _give_hint(session_state):
    step_info = PROBLEM_DATA['steps'][session_state['current_step']]
    hints = step_info['hints']

    hint_level = session_state['hint_level']
    if hint_level < len(hints):
        hint = f"Hint: {hints[hint_level]}"
        session_state['hint_level'] += 1
    else:
        hint = f"Hint: {hints[-1]}" # Repeat last hint

    return hint, session_state

def _handle_exam_mode(user_input, session_state):
    responses = []
    if user_input.strip() == PROBLEM_DATA['solution']:
        responses.append("That is correct. Well done.")
    else:
        responses.append(f"That is not the correct answer. The correct solution is x = {PROBLEM_DATA['solution']}.")

    responses.append(f"[TOPIC: {PROBLEM_DATA['topic']}]")
    session_state['problem_solved'] = True
    return responses, session_state
