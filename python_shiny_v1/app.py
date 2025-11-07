# written by Claude (with minor tweaks by me)

# I think this is kind of ugly...but it is mostly functional
# - I'd like to make the hard headers sticky at the top and only scroll inside.  My first attempt failed, so I reverted.

#shiny run --reload app.py

from pathlib import Path
from shiny import App, render, ui, reactive
from shinywidgets import render_widget, output_widget
import plotly.graph_objects as go

from eq5d import *
from plots import *

app_dir = Path(__file__).parent

# UI Definition
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.include_css(app_dir / "www/styles.css")
    ),
    ui.include_js("www/ui.js"),
    ui.h1("EQ-5D-5L Health Questionnaire Dashboard"),
    ui.hr(),
    
    ui.div(
        {"class": "header-controls"},
        ui.output_ui("completion_status")
    ),
    
    ui.div(
        {"class": "resizable-container"},
        ui.div(
            {"class": "survey-section", "id": "survey-panel"},
            ui.div({"class": "card-header"}, "Survey Questions"),
            ui.output_ui("survey_content"),
            ui.input_action_button("submit", "Submit", class_="btn btn-primary"),
            ui.input_action_button("reset", "Reset Survey", class_="btn btn-warning btn-reset"),

        ),
        ui.div({"class": "divider", "id": "divider"}),
        ui.div(
            {"class": "viz-section"},
            ui.div({"class": "card-header"}, "Your EQ-5D Profile"),
            ui.output_ui("vis_message"),
            output_widget("vis_plot")
        )
    )
)

# Server Logic
def server(input, output, session):
    
    # Track whether the survey is completed and submitted
    survey_completed = reactive.value(False)

    def update_completion_status():
        responses = [input[dim]() for dim in eq5d_questions.keys()]
        # Check if response exists and is not empty string
        completed = all(r is not None and r != "" for r in responses)
        survey_completed.set(completed)

    @reactive.Effect
    @reactive.event(input.reset)
    def _on_reset():
        for dimension in eq5d_questions.keys():
            ui.update_selectize(dimension, selected="")
        survey_completed.set(False)
    
    # When the user clicks submit:
    @reactive.effect
    @reactive.event(input.submit)
    def _on_submit():
        update_completion_status()

    @output
    @render.ui
    def completion_status():
        responses = [input[dim]() for dim in eq5d_questions.keys()]
        # Check if response exists and is not empty string
        completed = all(r is not None and r != "" for r in responses)
        answered = sum(1 for r in responses if r is not None and r != "")
        total = len(responses)
        
        if completed:
            badge_class = "completion-badge complete"
            text = f"✓ Survey Complete ({answered}/{total})"
        else:
            badge_class = "completion-badge incomplete"
            text = f"In Progress ({answered}/{total})"
        
        return ui.div({"class": badge_class}, text)
    
    @output
    @render.ui
    def survey_content():
        question_inputs = []
        for dim_key, dim_data in eq5d_questions.items():
            question_inputs.append(
                ui.div(
                    {"class": "question-group"},
                    ui.div({"class": "question-title"}, dim_data["question"]),
                    ui.input_selectize(
                        dim_key,
                        "",
                        choices={"": "-- Select your answer --", **{str(k): v for k, v in dim_data["options"].items()}},
                        selected=""
                    )
                )
            )
        
        return ui.div(*question_inputs)
    
    @output
    @render.ui
    def vis_message():
        if survey_completed.get():
             return ui.p("")
        else:
            return ui.div(
                {"style": "text-align: center; padding: 50px; color: #95a5a6;"},
                ui.h4("Please complete the survey to see your health profile visualization"),
                ui.p("Answer the questions on the left to see your results here.")
            )

    @output
    @render_widget
    def vis_plot():    
        if survey_completed.get():
            return survey_fig(eq5d_questions, input)
        else:
            return blank_fig()

app = App(app_ui, server)