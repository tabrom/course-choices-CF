import pandas 
import numpy as np 
from tkinter import *
from tkinter import filedialog

def browsefunc():
    root = Tk()
    root.withdraw()
    root.update()
    filename = filedialog.askopenfilename(filetypes=[('csv', '*.csv')])
    root.destroy()
    
    return filename

def start():
    print("Hi! \nChoose a file.\nBe aware that it has to be a csv file organized . In case it is not yet go to Excel or similar application and select \"save as\" and then csv.\nAdditionally, your table should contain a column with all the courses and another one with the student names so that each student appears as many times as they take courses (one time for each course).\nAll choices must be confirmed by pressing enter.")
    choices = browsefunc()
    if choices:
        separator(choices)
    else: 
        print("\nOops, something went wrong.\nDo you want to try again? Press \"y\" for yes or \"n\" to exit.")
        decision = input()
        if decision == "y":
            start()
        elif decision == "n":
            exit()
        else:
            print("\nOops, something went wrong again.")
            start()

def check_col_names(df):
    relev_col = ("naam", "omschrijving")
    for c in df.columns: 
        cLow = c.lower()
        if cLow in relev_col:
            newColname = c.lower()
            df.rename(columns = {c : newColname}, inplace = True) 

    if 'naam' and 'omschrijving' in df.columns:
        return df 
    else: 
        print("\nYour columns are not labelled as \"omschrijving\" for courses and \"naam\" for the student names. Please rename them and/or check the format of your file to work with this program.")
        exit()

def separator(choices): 
    print("\nA common problem is something called the sepearator: it is either \";\" or \",\". You can choose that now. If it doesnt work with what you have chose try the other option. I would recommend to try \";\" first if you saved it with Excel")
    sepa=input()
    df = pandas.read_csv(choices, sep=sepa)
    df = check_col_names(df)

    course_choice1(df)

def course_choice1(df): 
    print("\nNow you choose the first course you want to check. Press any key apart from enter and then enter to see a list of all courses.") 
    if input(): 
        uni_courses = np.unique(df['omschrijving'])
        counter = 1
        for i in uni_courses: 
            print(counter, ": ", i)
            counter += 1
        print("\nEnter the number corresponding with the first course you want to check.")
        choice = input()
        choice = int(choice) - 1
        course1 = uni_courses[choice]
        print("\nYour first course is:", course1,"\nIs that correct? Enter y for yes and n for no.")
        confirm_course(df, uni_courses, course1, course2=None)

def course_choice2(df, uni_courses, course1): 
    print("\nNow you choose the second course you want to check. Press any key apart from enter and then enter to see a list of all courses.") 
    if input(): 
        counter = 1
        for i in uni_courses: 
            print(counter, ": ", i)
            counter += 1
        print("\nEnter the number corresponding with the second course you want to check.")
        choice = input()
        choice = int(choice) - 1
        course2 = uni_courses[choice]
        print("\nYour second course is:", course2,"\nIs that correct? Enter y for yes and n for no.")
        confirm_course(df, uni_courses,course1, course2)

def confirm_course(df, uni_courses, course1, course2):
    decision = input()
    if decision == "y":
        if course2 == None:
            course_choice2(df, uni_courses, course1)
        else:
            compare(df, course1, course2)
    elif decision == "n":
        if course2 == None:
            course_choice1(df)
        else: 
            course_choice2(df, uni_courses, course1)
    else: 
        print("\nOops, something went wrong. Try again.")
        if course2 == None:
            course_choice1
        else: 
            course_choice2
        

def compare(df, course1, course2):
    first_course = np.where(df['omschrijving']== course1, df["naam"], "None")

    first_course = first_course[first_course != "None"]
    print("\nstudents of", course1, ":", first_course)

    second_course = np.where(df['omschrijving']== course2, df["naam"], "None")

    second_course = second_course[second_course != "None"]
    print("\nstudents of", course2, ":", second_course)

    comp = np.in1d(first_course,second_course)
    overlaps = np.where(comp == True)

    print("\nStudents taking both courses:")
    for i in overlaps[0]: 
        print(first_course[i])

    unique, counts = np.unique(comp, return_counts=True)
    print("\noverlap?")
    print((dict(zip(unique, counts))))
    final(df) 

def final(df):
    print("\nWhat do you want to do next? Press 1 for another comparison or 2 for exit.")
    decision = input()
    if decision == "1":
        course_choice1(df)
    elif decision == "2":
        exit 
    else: 
        print("\nOops, something went wrong. Try again.")
        final(df)


start()