# written by Claude (with minor tweaks by me)

# I think this is kind of ugly...but it is mostly functional
# - I'd like to make the hard headers sticky at the top and only scroll inside.  My first attempt failed, so I reverted.

#shiny run --reload app.py

from pathlib import Path
from shiny import App, render, ui, reactive
from shinywidgets import render_widget, output_widget
import numpy as np

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
    
    ui.div({"class": "resizable-container"},
        ui.div({"class": "card-section survey-section", "id": "survey-panel"},
            ui.div({"class": "card-header"}, "Survey Questions"),
            ui.div({"class": "card-body"},
                ui.output_ui("survey_content"),
                ui.input_action_button("submit_button", "Submit", class_="btn btn-primary"),
                ui.input_action_button("reset_button", "Reset Survey", class_="btn btn-warning btn-reset"),
                # remove this when done testing
                ui.br(),ui.br(),
                ui.input_action_button("testing_button", "Test Random Responses", class_="btn btn-testing"),
            ),
        ),
        ui.div({"class": "divider", "id": "divider"}),
        ui.div({"class": "card-section viz-section"},
            ui.div({"class": "card-header"}, "Your EQ-5D Profile"),
            ui.div({"class": "card-body"},
                ui.output_ui("viz_message"),
                ui.div({"class": "viz-component"},
                    ui.output_ui("summary_viz_title"),
                    ui.output_ui("summary_viz_toggle"),
                    output_widget("summary_viz_plot"),
                ),
                ui.div({"class": "viz-component"},
                    ui.output_ui("dimensions_viz_title"),
                    ui.output_ui("dimensions_viz_toggle"),
                    output_widget("dimensions_viz_plot")
                ),
            )
        )
    )
)

# Server Logic
def server(input, output, session):
    
    # Shared reactive value controlling redraws 
    redraw_counter = reactive.value(0)

    # Track whether the survey is completed and submitted
    survey_completed = reactive.value(False)

    # Track whether the user has interacted with the sider
    slider_activated = reactive.Value(False)
    # Track if initialized (to avoid counting initialization for the slider activation)
    slider_initialized = reactive.Value(False)

    def collect_responses():
        # get all the survey responses, accounting for the slider
        responses = []
        for s_key, s_data in eq5d_questions.items():
            if s_data["type"] == "dropdown":
                responses.append(input[s_key]())
            if s_data["type"] == "slider":
                if (slider_activated.get()):
                    responses.append(input[s_key]())
                else:
                    responses.append(None)
        return responses

    def update_completion_status():
        # returns true if all responses are available
        responses = collect_responses()
        # Check if response exists and is not empty string
        completed = all(r is not None and r != "" for r in responses)
        survey_completed.set(completed)


    @reactive.Effect
    @reactive.event(input.reset_button)
    def _on_reset():
        # when user clicks reset, 
        # - set all the dropdowns to default unselected
        # - set survey completed to False
        for s_key, s_data in eq5d_questions.items():
            if s_data["type"] == "dropdown":
                ui.update_selectize(s_key, selected="")
        survey_completed.set(False)
        slider_activated.set(False)
        # re-hide the slider
        # according to the documentation, I should be able to send_custom_message
        # this doesn't seem to be working, so I will use send_input_message instead
        # session.send_custom_message("hide_sliders", {"reason": "user_reset"})
        session.send_input_message("js_command", {"action": "hide_sliders", "reason": "user_reset"})

    
    # When the user clicks submit:
    @reactive.effect
    @reactive.event(input.submit_button)
    def _on_submit():
        update_completion_status()
        redraw_counter.set(redraw_counter.get() + 1)

    # When the user touches the slider:
    @reactive.Effect
    @reactive.event(input.health_today)
    def _on_slider_interaction():
        # If it's the first call, ignore it
        if not slider_initialized.get():
            slider_initialized.set(True)  
            return  # Ignore first auto-trigger
        slider_activated.set(True)  

    # triggered from JS on resize
    @reactive.Effect
    @reactive.event(input.redraw_trigger)
    def _on_resize():
        redraw_counter.set(redraw_counter.get() + 1)


    # When the user clicks submit:
    @reactive.effect
    @reactive.event(input.testing_button)
    def _on_test():
        ui.update_numeric("mobility", value=np.random.randint(1, high=5))
        ui.update_numeric("selfcare", value=np.random.randint(1, high=5))
        ui.update_numeric("usual_activities", value=np.random.randint(1, high=5))
        ui.update_numeric("pain", value=np.random.randint(1, high=5))
        ui.update_numeric("anxiety", value=np.random.randint(1, high=5))
        ui.update_numeric("health_today", value=np.random.randint(0, high=100))
        slider_activated.set(True)  
        survey_completed.set(True)
        update_completion_status()

    @output
    @render.ui
    def completion_status():
        # update the div that has the completion badge with the number and fraction of questions completed
        responses = collect_responses()
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
        # populate the survey questions in the ui
        question_inputs = []
        for s_key, s_data in eq5d_questions.items():
            if s_data["type"] == "dropdown":
                question_inputs.append(
                    ui.div({"class": "question-group"},
                        ui.div({"class": "question-title"}, s_data["question"]),
                        ui.input_selectize(
                            s_key,
                            "",
                            choices={"": "-- Select your answer --", **{str(k): v for k, v in s_data["options"].items()}},
                            selected=""
                        )
                    )
                )
            if s_data["type"] == "slider":
                question_inputs.append(
                    ui.div({"class": "question-group"},
                        ui.div({"class": "question-title"}, s_data["question"]),
                        ui.input_slider(
                            s_key,  
                            s_data["instructions"], 
                            min=s_data["min_val"],  
                            max=s_data["max_val"],  
                            value=s_data["initial_val"],  
                            step=s_data["step"],
                        )
                    )
                )
        return ui.div(*question_inputs)
    
    @output
    @render.ui
    def viz_message():
        # populate the message in the viz side of the UI (only shows something if survey incomplete)
        if survey_completed.get():
            return ui.p("")
        else:
            return ui.div({"style": "text-align: center; padding: 50px; color: #95a5a6;"},
                ui.h4("Please complete the survey to see your health profile visualization"),
                ui.p("Answer the questions on the left to see your results here.")
            )

    ####### summary title, toggle and plot
    @output
    @render.ui
    def summary_viz_title():
        # populate the message in the viz side of the UI (only shows something if survey incomplete)
        if survey_completed.get():
            return ui.div(
                ui.h2("Overall Health Score"),
                ui.h3("The average value of your health dimensions.")
            )
        else:
            return ui.p("")
        
    @output
    @render.ui
    def summary_viz_toggle():
        #  Pill-shaped toggle for score display
        if survey_completed.get():
            return ui.div(
                ui.input_radio_buttons(
                    "summary_plot_type",
                    None,  # No label
                    choices={
                        "gauge": "Gauge |",
                        "number": "Number |",
                        "ring": "Ring"
                    },
                    selected="gauge",
                    inline=True
                ),
                class_="viz-toggle"
            )
        else:
            return ui.p("")
                    
    @output
    @render_widget
    def summary_viz_plot():
        # summary plot
        _ = redraw_counter.get()  # single reactive dependency for submit and resixe
        if survey_completed.get():
            if input['summary_plot_type']() == 'gauge':
                return survey_gauge_fig(eq5d_questions, input)
            else:
                return under_construction()
        else:
            return blank_fig()
        

    ####### dimensions title, toggle and plot
    @output
    @render.ui
    def dimensions_viz_title():
        # populate the message in the viz side of the UI (only shows something if survey incomplete)
        if survey_completed.get():
            return ui.div(
                ui.h2({"style": "margin-top:40px; margin-bottom:0"},"Health Dimensions"),
                ui.h3("Assessment across five key health areas."),
            )
        else:
            return ui.p("")

    @output
    @render.ui
    def dimensions_viz_toggle():
        #  Pill-shaped toggle for score display
        if survey_completed.get():
            return ui.div(
                ui.input_radio_buttons(
                    "dimensions_plot_type",
                    None,  # No label
                    choices={
                        "bar": "Bar |",
                        "radar": "Radar",
                    },
                    selected="bar",
                    inline=True
                ),
                class_="viz-toggle"
            )
        else:
            return ui.p("")

    @output
    @render_widget
    def dimensions_viz_plot():
        _ = redraw_counter.get()  # single reactive dependency for submit and resixe
        if survey_completed.get():
            if input['dimensions_plot_type']() == 'bar':
                return survey_bar_fig(eq5d_questions, input)
            else:
                return under_construction()
        else:
            return blank_fig()
        

        
app = App(app_ui, server)