import pandas as pd
import re

def convert_sleep_to_numeric(val):
    if isinstance(val, str):
        numbers = [float(num) for num in re.findall(r'\d+', val)]
        if numbers:
            return float(sum(numbers) / len(numbers)) 
    return None

pre_df = pd.read_csv("Student_Data_Updated.csv")
df = pre_df.copy()
df['Study Environment'] = df['Study Environment'].replace({
    'Quiet': -1,
    'Moderate': 0,
    'Noisy': 1
})
df['Sleep Duration Numeric'] = df['Sleep Duration'].apply(convert_sleep_to_numeric)

def clean_input(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) 
    text = re.sub(r'\s+', ' ', text) 
    return text.strip()

def get_sleep_cgpa_correlation():
    correlation = df["Sleep Duration Numeric"].corr(df["CGPA"])
    return f"The correlation between sleep duration and CGPA is {correlation:.2f}."
