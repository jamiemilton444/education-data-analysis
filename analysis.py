import pandas as pd

def analyze_school(school_name, df):
    school_row = df[df["school_name"].str.lower() == school_name.lower()]

    # CASE 1: School is found in dataset
    if not school_row.empty:
        percent_black = school_row["percent_black"].values[0]
        funding = school_row["funding_per_student"].values[0]
        test_score = school_row["test_score"].values[0]
    else:
        print(f"\nNo school found with the name '{school_name}'. Please enter your school’s information.")
        try:
            percent_black = float(input("Enter % of Black students at your school: "))
            if percent_black < 0 or percent_black > 100:
                raise ValueError("Percentage must be between 0 and 100.")
            funding = float(input("Enter per-student funding at your school ($): "))
            if funding < 0:
                raise ValueError("Funding must be a positive number.")
            test_score = float(input("Enter average test score at your school: "))
            if test_score < 0 or test_score > 100:
                raise ValueError("Test score must be between 0 and 100.")
            
        except ValueError:
            return "Invalid input. Please enter numeric values."

    # CASE 2: Determine peer group
    if percent_black >= 50:
        peer_group = df[df["percent_black"] >= 50]
    else:
        peer_group = df[df["percent_black"] < 50]

    avg_funding = peer_group["funding_per_student"].mean()
    avg_score = peer_group["test_score"].mean()

    funding_diff = avg_funding - funding
    score_gap = avg_score - test_score

    result = f"\nAnalyzing school data for '{school_name}'...\n"
    result += f"Your school has {percent_black}% Black students and receives ${funding:,.2f} per student.\n"

    if funding_diff > 0:
        result += f"That’s ${funding_diff:,.2f} less than similar schools on average.\n"
    elif funding_diff < 0:
        result += f"That’s ${abs(funding_diff):,.2f} more than similar schools on average.\n"
    else:
        result += "That’s the same as the average for similar schools.\n"

    result += f"Average test scores at similar schools: {avg_score:.1f}\n"
    result += f"Your school’s average test score: {test_score:.1f}\n"
    result += f"Score difference: {score_gap:.1f} points\n"

    return result

def main():
    # Load dataset
    try:
        df = pd.read_csv("school_data.csv")
    except FileNotFoundError:
        print("Error: school_data.csv not found. Please make sure the file is in the same folder.")
        return

    print("Welcome to the Education Equity Analyzer!\n")
    school_name = input("Enter your school name: ")

    # Analyze school and print results
    summary = analyze_school(school_name, df)
    print(summary)

if __name__ == "__main__":
    main()
