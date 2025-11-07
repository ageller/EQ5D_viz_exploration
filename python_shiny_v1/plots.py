import plotly.graph_objects as go

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


def survey_fig(eq5d_questions, input):
    # Get all responses, filtering out empty strings
    responses = {}
    for dim in eq5d_questions.keys():
        val = input[dim]()
        if val is not None and val != "":
            responses[dim] = int(val) 
    
    # Create the horizontal bar chart
    fig = go.Figure()
    
    dimensions = list(eq5d_questions.keys())
    dimension_labels = [eq5d_questions[d]["question"].split("(")[0].strip() for d in dimensions]
    
    # Reverse order so first question appears at top
    dimensions = dimensions[::-1]
    dimension_labels = dimension_labels[::-1]
    
    for i, dim in enumerate(dimensions):
        if dim in responses:
            level = responses[dim]
            color = color_map[level]
            label = level_labels[level]
            
            fig.add_trace(go.Bar(
                x=[level],
                y=[dimension_labels[i]],
                orientation='h',
                marker=dict(
                    color=color,
                    cornerradius=15
                ),
                text=f"{label}",
                textposition='inside',
                textfont=dict(color='white', size=12),
                hovertemplate=f"<b>{dimension_labels[i]}</b><br>{label}<extra></extra>",
                showlegend=False
            ))
    
    fig.update_layout(
        xaxis=dict(
            title="",
            range=[0, 5],
            tickmode='array',
            tick0=1,
            dtick=1,
            tickvals=[0,1,2,3,4,5],    
            ticktext=["LEAST SEVERE","","","","","MOST SEVERE"],  
        ),
        yaxis=dict(title=""),
        height=600,
        bargap=0.3,
        margin=dict(l=200, r=50, t=50, b=100),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    
    # Add background shading for severity zones
    fig.add_vrect(x0=0, x1=1, fillcolor=color_map[1], opacity=0.1, layer="below", line_width=0)
    fig.add_vrect(x0=1, x1=2, fillcolor=color_map[2], opacity=0.1, layer="below", line_width=0)
    fig.add_vrect(x0=2, x1=3, fillcolor=color_map[3], opacity=0.1, layer="below", line_width=0)
    fig.add_vrect(x0=3, x1=4, fillcolor=color_map[4], opacity=0.1, layer="below", line_width=0)
    fig.add_vrect(x0=4, x1=5, fillcolor=color_map[5], opacity=0.1, layer="below", line_width=0)
     
    return fig


def blank_fig():
    fig = go.Figure()
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig