#Campusly Flask App

#This file contains the Python backend for Campusly. Flask connects the
#HTML forms to Python functions so users can add courses, add tasks, and calculate their GPA.

#imports flask to help connect python backend with html frontend
from flask import Flask, render_template, request, redirect, url_for

#creates website using flask
app = Flask(__name__)

#these lists store user-entered data while the app is running.
#the data resets when the server restarts.
courses = []
tasks = []
gpa_rows = []

#grade scale for gpa calculation, each letter corresponds to a number of grade points (per credit hour)
GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0,
}

#function to calculate GPA based on grade and credits of each course
def calculate_gpa(rows):
    total_points = 0
    total_credits = 0

#loops through each course row to get grade, credits, and corresponding grade
    for row in rows:
        grade = row.get("grade")
        credits = int(row.get("credits", 0))
        points = GRADE_POINTS.get(grade)

        # only include rows that have a valid grade and credit value
        if points is not None and credits > 0:
            total_points += points * credits
            total_credits += credits

    if total_credits == 0: #if there is insufficient data to calculate GPA, return none
        return None

    return round(total_points / total_credits, 2) #rounds to 2 decimal places

#function to get unfinish tasks to be displayed on overview page and filters 
#keeping taks that are not marked as done
def get_unfinished_tasks():
    return [task for task in tasks if not task["done"]]

#what the user first sees when they open website
@app.route("/")
def overview():
    #display the overview page with GPA, courses, and tasks
    return render_template(
        "index.html",
        page="overview",
        courses=courses,
        tasks=tasks,
        unfinished_tasks=get_unfinished_tasks(),
        gpa=calculate_gpa(gpa_rows),
        grade_points=GRADE_POINTS,
    )

#displays gpa calculator page when user clicks on gpa tab
@app.route("/gpa")
def gpa_page():
    return render_template( #sends variables to HTML template to be displayed on the webpage
        "index.html", 
        page="gpa",
        courses=courses,
        tasks=tasks,
        unfinished_tasks=get_unfinished_tasks(),
        gpa_rows=gpa_rows,
        gpa=calculate_gpa(gpa_rows),
        grade_points=GRADE_POINTS,
    )


#when user submits a new course row in the gpa calculator, this function is called to the list of gpa rows
@app.route("/add-gpa-course", methods=["POST"])
def add_gpa_course():
    """Add one course row to the GPA calculator."""
    gpa_rows.append( #adds a new course row to list of gpa rows
        {
            "name": request.form.get("name", ""), #get coursse name
            "grade": request.form.get("grade", "A"), #get grade
            "credits": request.form.get("credits", "3"), #get credits
        }
    )
    return redirect(url_for("gpa_page")) #redirects user back to gpa page to update list of courses

#clears all courses from gpa calculator when user clicks clear button
@app.route("/clear-gpa", methods=["POST"])
def clear_gpa():
    gpa_rows.clear()
    return redirect(url_for("gpa_page"))

#navigates user to courses page
@app.route("/courses")
def courses_page(): #displays courses page when user clicks on courses tab
    return render_template( #sends variables to HTML template to be displayed on the webpage
        "index.html",
        page="courses",
        courses=courses,
        tasks=tasks,
        unfinished_tasks=get_unfinished_tasks(),
        gpa=calculate_gpa(gpa_rows),
        grade_points=GRADE_POINTS,
    )

#when user adds a course using the form on the courses page
@app.route("/add-course", methods=["POST"])
def add_course(): 
    #gets course name removing extra whitespace, if user doesn't enter anything it defaults to an empty string
    name = request.form.get("name", "").strip()

    #if the course name is not blank, add course to list
    if name:
        courses.append( #gets course information from form and adds it to list of courses
            {
                "name": name,
                "code": request.form.get("code", "").strip(),
                "credits": request.form.get("credits", "3"),
                "instructor": request.form.get("instructor", "").strip(),
                "grade": request.form.get("grade", "").strip(),
            }
        )

#after adding a course it redirects updating the courses page
    return redirect(url_for("courses_page"))

#goes to tasks page when user navigates to tasks tab
@app.route("/tasks")
#displays task page sending variables to HTML template
def tasks_page():
    """Display the to-do list page."""
    return render_template(
        "index.html",
        page="tasks",
        courses=courses,
        tasks=tasks,
        unfinished_tasks=get_unfinished_tasks(),
        gpa=calculate_gpa(gpa_rows),
        grade_points=GRADE_POINTS,
    )

#when user submits a new task 
@app.route("/add-task", methods=["POST"])
def add_task():
   #adds task and removes extra white space, if user doesn't enter anything it defaults to an empty string
    text = request.form.get("text", "").strip()

    # if there's a task add it to list of tasks with priority, due date, and done status
    if text:
        tasks.append(
            {
                "text": text,
                "priority": request.form.get("priority", "med"),
                "due": request.form.get("due", ""),
                "done": False,
            }
        )

#after adding a task, redirects user back to tasks page to update it
    return redirect(url_for("tasks_page"))

#runs when user checks/unchecks a task to mark it as done/not done
@app.route("/toggle-task/<int:index>", methods=["POST"])

#index indicates which task in list is being toggles
def toggle_task(index):
    #switches task between done and not done
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
#updates task page to reflect change in task status
    return redirect(url_for("tasks_page"))

#removes task from list
@app.route("/delete-task/<int:index>", methods=["POST"])
def delete_task(index):
    #checks if tasks exists and then removes it from the list
    if 0 <= index < len(tasks):
        tasks.pop(index)
#redirect back to task page to update and reflect change
    return redirect(url_for("tasks_page"))

#runs flask and runs the webpage
if __name__ == "__main__":
    app.run(debug=True)
