from .chart_gen import generate_chart, generate_scatter, generate_heat_map, generate_histogram, generate_histograph_mean
from .data_utils import clean_input, get_sleep_cgpa_correlation, convert_sleep_to_numeric
import pandas as pd
import numpy as np
import threading
import random

df = pd.read_csv("Student_Data_Updated.csv")
df["Sleep Duration"] = df["Sleep Duration"].apply(convert_sleep_to_numeric)
df["Study Environment"] = df["Study Environment"].replace({"Quiet": -1, "Moderate": 0, "Noisy": 1})
df = df.dropna(subset=["Sleep Duration", "CGPA"])

# Fixed dictionary — all keywords separated
KEYWORDS_TO_CHART = {
    "heatmap": ("heat_map", "Here's the heat map of correlations:"),
    "histogram": ("histogram", "Here's the histogram of CGPA:"),
    "histograph": ("histograph_mean", "Here's the histogram of CGPA with mean line:"),
    "sleep": ("sleep_duration", "Here's the sleep duration chart:"),
    "cgpa": ("cgpa_line", "Here's the CGPA trend:"),
    "study": ("study_environment", "Here's the breakdown of study environments:"),
    "city": ("city_distribution", "Here's how student count is distributed by city:"),
    "cities": ("city_distribution", "Here's how student count is distributed by city:")
}

def get_text_insights(user_input):
    user_input = user_input.lower()
    msg = user_input.lower().strip()

    greetings = ["hello", "hi", "good morning", "good afternoon", "good evening", "hey"]
    farewells = ["bye", "goodbye", "see you", "see ya", "take care"]
    how_are_you = ["how are you", "how's it going", "how are things"]
    thanks = ["thank you", "thanks", "appreciate it", "grateful"]

    if any(greet in msg for greet in greetings):
        return random.choice([
            "Hello! How can I assist you today?",
            "Hi there. How may I help you?",
            "Good to see you. What would you like to know?",
            "Welcome. Feel free to ask me anything related to your CGPA or performance."
        ])

    if any(bye in msg for bye in farewells):
        return random.choice([
            "Goodbye! If you have more questions later, I'll be here.",
            "Take care, and best of luck with your studies!",
            "See you soon. Don't hesitate to reach out again.",
            "Wishing you continued success. Bye for now!"
        ])

    if any(phrase in msg for phrase in how_are_you):
        return random.choice([
            "I'm doing well, thank you for asking. How can I support you today?",
            "I'm functioning smoothly. What would you like to discuss?",
            "All systems are running perfectly. Let me know how I can help."
        ])

    if any(phrase in msg for phrase in thanks):
        return random.choice([
            "You're very welcome.",
            "Glad I could help!",
            "Anytime. Let me know if there's anything else.",
            "Happy to assist."
        ])
    
    if "average cgpa" in user_input:
        avg = df["CGPA"].mean()
        return f"The average CGPA is {avg:.2f}."
    
    elif "most common city" in user_input or "most students" in user_input:
        top_city = df["City"].value_counts().idxmax()
        count = df["City"].value_counts().max()
        return f"The city with the most students is {top_city} with {count} students."
    
    elif "average sleep" in user_input or "sleep hours" in user_input:
        avg_sleep = df["Sleep Duration"].mean()
        return f"The average sleep duration is {avg_sleep:.1f} hours."
    
    elif "common study environment" in user_input:
        common_env = df["Study Environment"].mode().values[0]
        return f"The most common study environment is {common_env}."
    
    return None

def get_bot_response(user_input):
    user_input = user_input.lower()
    responses = []
    chart_paths = []

    if "scatter" in user_input and "cgpa" in user_input and "sleep" in user_input:
        chart_path = generate_scatter("Sleep Duration", "CGPA", "sleep_cgpa")
        responses.append("Here's the scatter plot of CGPA vs Sleep Duration:")
        chart_paths.append(chart_path)

    if "correlation" in user_input and "sleep" in user_input:
        responses.append(get_sleep_cgpa_correlation())

    text_insight = get_text_insights(user_input)
    if text_insight:
        responses.append(text_insight)

    for keyword, (chart_type, msg) in KEYWORDS_TO_CHART.items():
        if keyword in user_input:
            chart_path = generate_chart(chart_type)
            if chart_path:
                responses.append(msg)
                chart_paths.append(chart_path)

    if "cgpa analysis" in user_input or "full cgpa report" in user_input:
        cgpa_stats = df["CGPA"].describe()
        corr_sleep = df["CGPA"].corr(df["Sleep Duration"])
        corr_internet = df["CGPA"].corr(df["Internet Usage (hrs/day)"])
        corr_env = df["CGPA"].corr(df["Study Environment"])

        summary = (
            f"📊 **CGPA Summary Stats**:\n"
            f"- Mean: {cgpa_stats['mean']:.2f}\n"
            f"- Median: {df['CGPA'].median():.2f}\n"
            f"- Min: {cgpa_stats['min']:.2f}\n"
            f"- Max: {cgpa_stats['max']:.2f}\n\n"
            f"🔗 **Correlations**:\n"
            f"- Sleep Duration ↔ CGPA: {corr_sleep:.2f}\n"
            f"- Internet Usage ↔ CGPA: {corr_internet:.2f}\n"
            f"- Study Environment ↔ CGPA: {corr_env:.2f}\n"
        )

        scatter_path = generate_scatter("Sleep Duration", "CGPA", "sleep_cgpa")
        chart_paths.append(scatter_path)

        responses.append(summary)
        responses.append("Here's a scatter plot of CGPA vs Sleep Duration:")

    if responses:
        full_response = "\n".join(responses)
        return full_response, chart_paths

    return "Sorry, I didn't get that. Try asking about sleep duration, CGPA trend, city distribution, or study environments.", []
