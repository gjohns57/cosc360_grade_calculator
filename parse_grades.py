from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from datetime import date


def lab_grade(grades: pd.DataFrame):
    exclude = {"Programming Assignment 9: Threaded Chat Server"}
    df = grades[((grades["Context"] == "Programming Assignments") | (grades["Context"] == "Lab Quizzes")) & (grades["Score"] != "-") & ~grades["Name"].isin(exclude)]

    if not grades[grades["Name"] == "Programming Assignment 9: Threaded Chat Server"].empty:
        bonus_lab_score = pd.to_numeric(grades[(grades["Name"] == "Programming Assignment 9: Threaded Chat Server") & (grades["Score"] != "-")]["Score"]).sum()

        min_lab_idx = pd.to_numeric(df["Score"]).idxmin()
        if int(bonus_lab_score) > int(pd.to_numeric(df.loc[min_lab_idx, "Score"])):
            print(df.loc[min_lab_idx, "Name"], "score of", df.loc[min_lab_idx, "Score"], "replaced with Lab 9 score of", bonus_lab_score)
            df.loc[min_lab_idx, "Score"] = str(bonus_lab_score)


    current = pd.to_numeric(df["Score"]).sum()
    total = pd.to_numeric(df["Out Of"]).sum()
    print("Programming Assignments:", current, "/", total, "=", current / total)

    return current / total

def exam_grade(grades: pd.DataFrame):
    exclude = {"Midterm Exam 1", "Midterm Exam 2", "Final Exam", "Final Exam Required"}
    df = grades[(grades["Context"] == "Exams") & (grades["Score"] != "-") & ~grades["Name"].isin(exclude)]
    current = pd.to_numeric(df["Score"]).sum()
    total = pd.to_numeric(df["Out Of"]).sum()
    print("Exams:", current, "/", total, "=", current / total)

    return current / total

def attendance_penalty(grades: pd.DataFrame):
    missed =  grades[(grades["Context"] == "Attendance Quizzes")]
    missed = missed[(pd.to_datetime(missed["Name"]) < date.today().strftime("%Y-%m-%d")) & (missed["Score"] == "-")]
    print("Attendance:", len(missed), "abcences", -0.05 * min(0, 5 - len(missed)), "penalty")

    return 0.05 * min(0, 5 - len(missed))

DIR = os.path.dirname(os.path.abspath(__file__))

def parse_html() -> pd.DataFrame:
    fname = None

    for file in os.listdir(DIR):
        if os.path.splitext(file)[1] == ".html":
            fname = os.path.join(DIR, file)
            break

    if fname == None:
        print("No grades html in directory")
        exit(1)

    with open(fname, "r", encoding="utf-8") as fin:
        contents = fin.read()

    soup = BeautifulSoup(contents, 'html.parser')


    assignments = soup.find_all(class_="student_assignment")

    grades = pd.DataFrame(columns=["Name", "Context", "Score", "Out Of"])

    for entry in assignments:
        title = entry.find(class_="title")
        if title == None:
            continue
        name_tag = title.find('a')
        if name_tag == None:
            continue

        context_tag = title.find(class_="context")
        if context_tag == None:
            continue

        grade_element = entry.find(class_="tooltip")
        if grade_element == None: continue

        score_element = grade_element.find(class_="grade")

        score = "-"
        if score_element != None:
            out_of_element = score_element.find_next_sibling()
            if out_of_element == None: continue

            score_match = re.search("-|[0-9]+", score_element.text)
            if score_match != None:
                score = score_match[0]


        new_row = [
            name_tag.text,
            context_tag.text,
            score,
            out_of_element.text.strip()[2:]
        ]


        grades.loc[len(grades)] = new_row

    grades.loc[len(grades)] = ["Final Exam Curved Score", "Exams", "-", "100"]
    grades.to_csv("grades.csv")
    return grades


if __name__ == "__main__":
    grades = None
    if os.path.isfile(os.path.join(DIR, "grades.csv")):
        grades = pd.read_csv("grades.csv")
    else:
        grades = parse_html()

    lab_score = lab_grade(grades)
    exam_score = exam_grade(grades)
    attendance = attendance_penalty(grades)
    total = lab_score * 0.4 + exam_score * 0.6 + attendance

    print("Total:", total)
