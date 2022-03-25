from importlib import resources
from flask import Flask, request, render_template, redirect, flash, session, template_rendered
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# survey_title = survey.title
# survey_instructions = survey.instructions
# questions = survey.questions
# q_index = 0
# question = questions[q_index]
# choices = []


# for question in questions:
#     choices.append(question.choices)

# choice = choices[q_index]


@app.get("/")
def go_home():
    session["responses"] = []
    return render_template("/survey_start.html", survey=survey)

@app.post("/begin")
def start_survey():
    return redirect(f"/questions/0")

@app.get("/questions/<int:index>")
def display_question(index):
    if index > len(session["responses"]):
        return redirect(f"/questions/{len(session['responses'])}")

    question = survey.questions[index]
    return render_template("/question.html", survey_question=question)

@app.post("/answer")
def submit_answer():

    answer = request.form["answer"]

    responses = session["responses"]
    responses.append(answer)
    session['responses'] = responses

    next_question = len(session["responses"])

    if next_question == len(survey.questions):
        return render_template("/completion.html")

    return redirect(f"/questions/{next_question}")

