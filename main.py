import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def main():
    print("WELCOME TO THE AI WORKOUT GENERATOR\n")
    goal = input("WHAT IS YOUR GOAL?(BUILD MUSCLE, LOSE WEIGHT, ETC): ")
    days = input("HOW MANY DAYS A WEEK? OR HOW LONG OF A PERIOD (In Days): ")
    experience = input("WHAT IS YOUR EXPERIENCE LEVEL?(BEGINNER, MID, ADVANCED)?: ")
    print("\nGenerating..\n")
    workout_plan = generate_workout(goal, days, experience)
    print(workout_plan)
def generate_workout(goal, days, experience):
    prompt = (
        "Can you make a {} day gym workout plan for someone who is {} "
        "with their goal being {}. Include sets, reps, exercises, and scheduled rest days if needed."
    ).format(days, experience, goal)
    model = GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.75,
            "max_output_tokens": 2020,
        },
    )
    return response.text
if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    vertexai.init(project="finalproject-458201", location="us-central1")
    
    main()
