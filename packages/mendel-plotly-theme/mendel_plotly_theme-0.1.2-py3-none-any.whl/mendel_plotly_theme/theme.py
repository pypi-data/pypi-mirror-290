import plotly.graph_objects as go

# theme.py

def get_theme():
    return dict(
        layout=go.Layout(
            font=dict(
                family="Arial, sans-serif",
                size=16,
                color="#000000"
            ),
            title=dict(
                font=dict(
                    family="Arial, sans-serif",
                    size=24,
                    color="#333333"
                ),
                x=0.5,  # Center the title
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(
                    text="X Axis Title",
                    font=dict(
                        family="Arial, sans-serif",
                        size=18,
                        color="#333333"
                    )
                ),
                showgrid=True,
                gridcolor="#E5E5E5",
                zeroline=True,
                zerolinecolor="#E5E5E5",
                showline=True,
                linewidth=2,
                linecolor="#333333",
                ticks="outside",
                tickwidth=2,
                tickcolor="#333333",
                ticklen=5
            ),
            yaxis=dict(
                title=dict(
                    text="Y Axis Title",
                    font=dict(
                        family="Arial, sans-serif",
                        size=18,
                        color="#333333"
                    )
                ),
                showgrid=True,
                gridcolor="#E5E5E5",
                zeroline=True,
                zerolinecolor="#E5E5E5",
                showline=True,
                linewidth=2,
                linecolor="#333333",
                ticks="outside",
                tickwidth=2,
                tickcolor="#333333",
                ticklen=5
            ),
            margin=dict(
                l=50,  # Left margin
                r=50,  # Right margin
                t=50,  # Top margin
                b=50   # Bottom margin
            ),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
        )
    )

def apply_theme(fig):
    theme = get_theme()
    fig.update_layout(theme['layout'])
