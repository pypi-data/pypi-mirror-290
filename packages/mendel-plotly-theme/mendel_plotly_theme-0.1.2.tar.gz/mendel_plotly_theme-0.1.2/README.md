# mendel-plotly-theme

This package provides a custom Plotly theme that can be easily applied to any Plotly figure.

## Installation

You can install the package using pip:

```bash
pip install my_plotly_themes
```

Example usage:
```python
import plotly.graph_objects as go
from mendel_plotly_theme import apply_theme

# Create a sample plot
fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines+markers'))

# Apply the custom theme
apply_theme(fig)

# Show the plot
fig.show()
```
