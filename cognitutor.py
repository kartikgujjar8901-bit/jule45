import time
import random

class CogniTutor:
    def __init__(self):
        self.mode = "STUDY"  # Default mode
        self.problem = None
        self.positive_reinforcement = [
            "Excellent!",
            "That's exactly right!",
            "Great thinking!",
            "You're on the right track!",
            "Perfect!",
            "Awesome!"
        ]
        self.load_problem()

    def load_problem(self):
        self.problem = {
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
            "current_step": 0,
            "hint_level": 0
        }

    def start(self):
        print("Welcome to CogniTutor! I'm here to help you learn.")
        print("You can type `[MODE: EXAM]` or `[MODE: STUDY]` to switch modes at any time.")
        print("If you're stuck in study mode, just say 'hint'.")
        print("-" * 20)
        self.introduce_problem()
        self.main_loop()

    def introduce_problem(self):
        # Reset problem state
        self.problem['current_step'] = 0
        self.problem['hint_level'] = 0
        print(f"Let's work on this problem: Solve the equation `{self.problem['text']}`.")
        if self.mode == "STUDY":
            first_step = self.problem['steps'][self.problem['current_step']]
            print(first_step['question'])

    def main_loop(self):
        while True:
            user_input = input("> ").strip()
            if user_input.upper() == "[MODE: EXAM]":
                self.mode = "EXAM"
                print("\nSwitched to EXAM mode. I will now wait for your final answer without providing hints.")
                print(f"The problem is: `{self.problem['text']}`. What is the value of x?")
                continue
            elif user_input.upper() == "[MODE: STUDY]":
                self.mode = "STUDY"
                print("\nSwitched to STUDY mode. I will guide you step-by-step.")
                self.introduce_problem()
                continue

            if self.mode == "STUDY":
                self.handle_study_mode(user_input)
            else:
                self.handle_exam_mode(user_input)

    def handle_study_mode(self, user_input):
        if self.problem['current_step'] >= len(self.problem['steps']):
            print("We've already solved this one! Let's restart for a new problem (feature coming soon).")
            return

        step_info = self.problem['steps'][self.problem['current_step']]

        if user_input.lower() == 'hint':
            self.give_hint()
            return

        if any(keyword in user_input.lower() for keyword in step_info['answer_keywords']):
            print(f"{random.choice(self.positive_reinforcement)} {step_info['correct_response']}")
            self.problem['current_step'] += 1
            self.problem['hint_level'] = 0  # Reset hint level for the next step

            if self.problem['current_step'] < len(self.problem['steps']):
                next_step_info = self.problem['steps'][self.problem['current_step']]
                print(next_step_info['question'])
            else:
                print("You've solved the problem! Nicely done.")
                print(f"[TOPIC: {self.problem['topic']}]")
        else:
            print("Not quite. Try again, or say 'hint' if you're stuck.")

    def give_hint(self):
        step_info = self.problem['steps'][self.problem['current_step']]
        hints = step_info['hints']

        if self.problem['hint_level'] < len(hints):
            print(f"Hint: {hints[self.problem['hint_level']]}")
            self.problem['hint_level'] += 1
        else:
            # If all hints are exhausted, repeat the last one.
            print(f"Hint: {hints[-1]}")

    def handle_exam_mode(self, user_input):
        if user_input.strip() == self.problem['solution']:
            print("That is correct. Well done.")
        else:
            print(f"That is not the correct answer. The correct solution is x = {self.problem['solution']}.")
        print(f"[TOPIC: {self.problem['topic']}]")
        print("You can switch back to [MODE: STUDY] or ask for a new problem (feature coming soon).")


if __name__ == "__main__":
    tutor = CogniTutor()
    tutor.start()
