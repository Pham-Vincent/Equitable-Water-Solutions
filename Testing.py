import plotly.graph_objects as go

# Sample data
x = [1, 2, 3, 4, 5]
y1 = [10, 12, 15, 13, 17]
y2 = [5, 8, 10, 7, 11]

# Create the area chart
fig = go.Figure()

# First area fill to the x-axis
fig.add_trace(go.Scatter(
    x=x, y=y1,
    fill='tozeroy', # Fill to the x-axis
    mode='none', # No line or markers
    name='Series 1',
    fillcolor='rgba(0, 100, 80, 0.2)' # Custom fill color with opacity
))

# Second area fill to the previous y value
fig.add_trace(go.Scatter(
    x=x, y=y2,
    fill='tonexty', # Fill to the next y value
    mode='none', # No line or markers
    name='Series 2',
    fillcolor='rgba(0, 176, 246, 0.2)' # Custom fill color with opacity
))

# Update layout
fig.update_layout(
    title='Area Chart Example',
    xaxis_title='X Axis Title',
    yaxis_title='Y Axis Title'
)

# Show the figure
fig.show()
