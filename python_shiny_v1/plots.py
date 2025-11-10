import plotly.graph_objects as go
import numpy as np

# Color mapping for severity levels
color_map = {
    1: "#3498db",  # Blue - No problems
    2: "#2ecc71",  # Green - Slight
    3: "#f39c12",  # Orange - Moderate
    4: "#e67e22",  # Dark Orange - Severe
    5: "#e74c3c"   # Red - Extreme/Unable
}

level_labels = {
    1: "No problems",
    2: "Slight",
    3: "Moderate",
    4: "Severe",
    5: "Extreme/Unable"
}

def get_responses(eq5d_questions, input):
    # Get all responses, filtering out empty strings
    responses = {}
    for s_key, s_data in eq5d_questions.items():
        val = input[s_key]()
        if val is not None and val != "":
            if s_data["type"] == "dropdown":
                responses[s_key] = int(val)
            if s_data["type"] == "slider":
                # normalize and flip
                responses[s_key] = (100 - int(val))/20.

    return responses


def survey_bar_fig(eq5d_questions, input):

    responses = get_responses(eq5d_questions, input)    

    # Create the horizontal bar chart
    fig = go.Figure()
    
    dimensions = list(eq5d_questions.keys())
    dimension_labels = [eq5d_questions[d]["question"].split("(")[0].strip().title()+"  " for d in dimensions]
    
    base = 0.05 #to allow the left corners to round
    # First, add background gray bars that extend to the full domain
    for i, dim in enumerate(dimensions):
        fig.add_trace(go.Bar(
            base=base, 
            x=[5 - base],  # Full width, but minus the base offset 
            y=[dimension_labels[i]],
            orientation='h',
            marker=dict(
                color='#f3f4f6', 
                cornerradius=15
            ),
            showlegend=False,
            hoverinfo='skip',
            width=0.6,
        ))
        
    for i, dim in enumerate(dimensions):
        if dim in responses:
            level = min(max(int(np.ceil(responses[dim])), 1), 5)
            color = color_map[level]
            label = level_labels[level]
            
            fig.add_trace(go.Bar(
                base=base,
                x=[responses[dim] - base],
                y=[dimension_labels[i]],
                orientation='h',
                marker=dict(
                    color=color,
                    cornerradius=15
                ),
                text=f"{label}",
                textposition='inside',
                textfont=dict(color="white", size=12, weight='bold'),
                hovertemplate=f"<b>{dimension_labels[i]}</b><br>{label}<extra></extra>",
                showlegend=False,
                width=0.6,
            ))
    
    fig.update_layout(
        xaxis=dict(
            title="",
            range=[0, 5],
            tickmode='array',
            tick0=1,
            dtick=1,
            tickvals=[0,1,2,3,4,5],    
            ticktext=["","← Better","","","Worse →",""],  
        ),
        yaxis=dict(title=""),
        height=400,
        bargap=0.1,
        barmode='overlay',
        margin=dict(l=200, r=150, t=50, b=100),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    
    fig.update_yaxes(categoryorder='array', categoryarray=dimension_labels[::-1])
    
    # Add background shading for severity zones
    # fig.add_vrect(x0=0, x1=1, fillcolor=color_map[1], opacity=0.1, layer="below", line_width=0)
    # fig.add_vrect(x0=1, x1=2, fillcolor=color_map[2], opacity=0.1, layer="below", line_width=0)
    # fig.add_vrect(x0=2, x1=3, fillcolor=color_map[3], opacity=0.1, layer="below", line_width=0)
    # fig.add_vrect(x0=3, x1=4, fillcolor=color_map[4], opacity=0.1, layer="below", line_width=0)
    # fig.add_vrect(x0=4, x1=5, fillcolor=color_map[5], opacity=0.1, layer="below", line_width=0)
     
    return fig

def survey_gauge_fig(eq5d_questions, input):
    # create a gauge plot with a summary score and text

    responses = get_responses(eq5d_questions, input)   

    # create an average value 
    mn = np.mean(list(responses.values()))
    level = min(max(int(np.ceil(mn)), 1), 5)
    color = color_map[level]
    label = level_labels[level]

    # note that you can include a delta to indicate a change from the previous visit

    fig = go.Figure(
        go.Indicator(
            mode="gauge",
            value=mn,  
            gauge={
                'axis': {
                    'range': [0, 5], 
                    'tickvals': [0, 5], 
                    'ticktext': ['Better', 'Worse']
                },
                'bar': {'color': 'black', 'thickness': 0.25},  # the current value
                'steps': [
                    {'range': [0, 1], 'color': color_map[1]},   
                    {'range': [1, 2], 'color': color_map[2]},  
                    {'range': [2, 3], 'color': color_map[3]},  
                    {'range': [3, 4], 'color': color_map[4]},   
                    {'range': [4, 5], 'color': color_map[5]},   
                ],
                'threshold': {
                    'line': {'color': 'black', 'width': 4},
                    'thickness': 0.75,
                    'value': mn  # show a threshold line at current value
                }
            }
        )
    )


    # Manually add the annotation (since I don't want to see the number)
    fig.add_annotation(
        text=label,
        x=0.5, y=0.2, 
        showarrow=False,
        font=dict(size=48, color=color)
    )

    fig.update_layout(
        height=300
    )

    return fig


def blank_fig():
    fig = go.Figure()
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        height=10,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig