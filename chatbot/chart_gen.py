from .data_utils import df
import pandas as pd
import matplotlib
import seaborn as sns
matplotlib.use('Agg')

import os
import matplotlib.pyplot as plt
import os


def generate_chart(chart_type):
    df = pd.read_csv("Student_Data_Updated.csv")
    chart_dir = "static/charts"
    os.makedirs(chart_dir, exist_ok=True)

    if chart_type == "sleep_duration":
        sleep_counts = df['Sleep Duration'].value_counts().sort_index()
        plt.figure(figsize=(8, 5))
        sleep_counts.plot(kind='bar', color='mediumseagreen', edgecolor='black')
        plt.title("Distribution of Sleep Duration")
        plt.xlabel("Sleep Duration")
        plt.ylabel("Number of Students")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(chart_dir, "sleep_duration.png")
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    elif chart_type == "cgpa_line":
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['CGPA'], marker='o', linestyle='-', color='royalblue')
        plt.title("Line Graph of CGPA")
        plt.xlabel("Index")
        plt.ylabel("CGPA")
        plt.grid(True)
        plt.tight_layout()
        chart_path = os.path.join(chart_dir, "cgpa_line.png")
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    elif chart_type == "study_environment":
        study_env_counts = df['Study Environment'].value_counts()
        plt.figure(figsize=(7, 7))
        plt.pie(study_env_counts, labels=study_env_counts.index, autopct='%1.1f%%', startangle=140,
                colors=plt.cm.Pastel1.colors)
        plt.title("Study Environment Distribution")
        plt.axis('equal')
        chart_path = os.path.join(chart_dir, "study_environment.png")
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    elif chart_type == "city_distribution":
        city_counts = df['City'].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        plt.bar(city_counts.index, city_counts.values, color='coral', edgecolor='black')
        plt.title("Student Count by City")
        plt.xlabel("City")
        plt.ylabel("Number of Students")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(chart_dir, "city_distribution.png")
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    elif chart_type == "heat_map":
        return generate_heat_map()

    elif chart_type == "histogram":
        return generate_histogram()

    elif chart_type == "histograph_mean":
        return generate_histograph_mean()

    return None

def generate_scatter(x_col, y_col, label):
    plt.figure(figsize=(6, 4))
    plt.scatter(df[x_col], df[y_col], alpha=0.6, color='teal')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")
    filename = f"{label}_scatter.png"
    path = os.path.join("static", "charts", filename)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return "/" + path

def generate_heat_map():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    df = pd.read_csv("Student_Data_Updated.csv")
    
    
    # Load the dataset

    # Prepare data as a 2D array with one row (transposed column)
    activity_values = df[['Physical Activity (hrs/week)']].T

    # Plot single-variable heatmap
    plt.figure(figsize=(12, 2))
    sns.heatmap(activity_values, cmap="Oranges", cbar=True, linewidths=0.5)
    plt.title("Heatmap of Physical Activity (hrs/week) Across Students")
    plt.yticks(rotation=0)
    plt.xlabel("Student Index")
    plt.tight_layout()
    plt.tight_layout()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charts_dir = os.path.join(base_dir, "static", "charts")
    os.makedirs(charts_dir, exist_ok=True)
    plt.savefig(os.path.join(charts_dir, "heat_map.png"))
    plt.close()
    output_path = os.path.join("static", "charts", "heat_map.png")
    return output_path


def generate_histogram():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    df = pd.read_csv("Student_Data_Updated.csv")
    
    # Load the CSV file

    # Select only numeric columns
    numeric_df = df.select_dtypes(include='number')

    # Calculate Mean
    mean_values = numeric_df.mean()
    print("Mean:\n", mean_values)

    # Calculate Median
    median_values = numeric_df.median()
    print("\nMedian:\n", median_values)

    # Calculate Mode (can return multiple values, so take the first)
    mode_values = numeric_df.mode().iloc[0]
    print("\nMode:\n", mode_values)

    # Calculate Standard Deviation
    std_dev_values = numeric_df.std()
    print("\nStandard Deviation:\n", std_dev_values)




    # Load the CSV file

    # Count occurrences of each dietary habit
    diet_counts = df['Dietary Habits'].value_counts()

    # Plotting
    plt.figure(figsize=(8, 5))
    diet_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Distribution of Dietary Habits")
    plt.xlabel("Dietary Habit")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.tight_layout()
    plt.savefig("static/charts/histogram.png")
    plt.close()
    output_path = os.path.join("static", "charts", "histogram.png")
    return output_path


def generate_histograph_mean():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    df = pd.read_csv("Student_Data_Updated.csv")
    
    # Load the dataset

    # Select numeric columns
    numeric_df = df.select_dtypes(include='number')

    # Compute stats
    mean_vals = numeric_df.mean()
    median_vals = numeric_df.median()
    mode_vals = numeric_df.mode().iloc[0]  # first mode
    std_vals = numeric_df.std()

    # Create a DataFrame for plotting
    stats_df = pd.DataFrame({
        'Mean': mean_vals,
        'Median': median_vals,
        'Mode': mode_vals,
        'Standard Deviation': std_vals
    })

    # Plot grouped bar chart
    stats_df.plot(kind='bar', figsize=(12, 6), colormap='tab10')
    plt.title("Mean, Median, Mode & Standard Deviation of Numeric Columns")
    plt.ylabel("Value")
    plt.xlabel("Numeric Columns")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.legend(title="Statistics")
    plt.tight_layout()
    plt.savefig("static/charts/histograph_mean.png")
    plt.close()
    output_path = os.path.join("static", "charts", "histograph_mean.png")
    return output_path
