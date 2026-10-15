from google import genai

import os

from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("api_key")

client = genai.Client(api_key=api_key)

def get_diet_plan(response_data):

    monthly_total_calorie=response_data.get("monthly_total_calorie")

    meal_type_summary=response_data.get("meal_type_summary")

    meal_type_summary_text = ""

    for di in meal_type_summary:

        meal_type_summary_text += f".{di.get('meal_type')}:{di.get('total')}\n"

    print(meal_type_summary_text)

    prompt = f"""
            Act as an expert nutritionist and personalized diet planner.

            Food Diary Summary:
            - Total Monthly Calories: {monthly_total_calorie}
            - Meal-wise Calorie Breakdown:
            {meal_type_summary_text}

            Based on the user's food diary data, generate a personalized
            diet plan for 30 days.

            1. Food Analysis:
            Analyze the user's recorded calorie intake and meal distribution.
            Identify possible areas for improvement.

            2. Personalized Diet Plan:
            Create a balanced and varied 30-day diet plan with breakfast,
            lunch, dinner, and snacks. Suggest tasty meals, appropriate
            portions, and nutritious food combinations.

            3. Nutritional Balance:
            Include appropriate sources of protein, carbohydrates,
            healthy fats, fiber, vitamins, and minerals.

            4. Food Recommendations:
            Suggest healthy food alternatives and practical meal combinations
            that are easy to prepare and suitable for everyday life.

            5. Healthy Habits:
            Provide practical tips for hydration, portion control,
            meal consistency, and maintaining a balanced diet.

            6. FitWise Progress:
            Explain how the user can track daily calorie intake and
            monitor eating habits using the FitWise application.

            Important Instructions:
            - Personalize recommendations using only the available data.
            - Do not treat monthly calories as a daily calorie target.
            - Do not assume missing food entries mean skipped meals.
            - Do not prescribe extreme calorie restriction.
            - Do not claim that any diet guarantees specific health outcomes.
            - Use clear headings and meal-wise recommendations.
            - Make the plan practical, nutritious, and easy to follow.
            """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text
            