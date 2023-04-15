import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = px.data.gapminder()

color_map = {country: 'red' if country == 'Mexico' else 'blue' for country in df['country'].unique()}

px.scatter_3d(df, 
              x="gdpPercap", 
              y="lifeExp", 
              z="continent",
              animation_frame="year", 
              animation_group="country",
              hover_name="country",
              log_x=True,
              size_max=55,
              range_x=[100,100000],
              range_y=[25,90],
              opacity=.3,
              color="country", 
              color_discrete_map=color_map)

############################################################################################################



def generate_cube_points_with_face_centers(center, side_length):
    offset = side_length / 2
    corner_points = np.array([
        [-offset, -offset, -offset],[-offset, -offset,  offset],
        [-offset,  offset, -offset],[-offset,  offset,  offset],
        [ offset, -offset, -offset],[ offset, -offset,  offset],
        [ offset,  offset, -offset],[ offset,  offset,  offset]])

    mid_points = np.array([
        [-offset, -offset, 0],[-offset,  offset, 0],
        [ offset, -offset, 0],[ offset,  offset, 0],
        [-offset, 0, -offset],[-offset, 0,  offset],
        [ offset, 0, -offset],[ offset, 0,  offset],
        [0, -offset, -offset],[0, -offset,  offset],
        [0,  offset, -offset],[0,  offset,  offset]])

    face_centers = np.array([
        [-offset, 0, 0],[ offset, 0, 0],
        [0, -offset, 0],[0,  offset, 0],
        [0, 0, -offset],[0, 0,  offset]])

    all_points = np.concatenate((corner_points, mid_points, face_centers), axis=0)
    return all_points + center

center = np.array([0, 0, 0])
side_length = 1

cube_points = generate_cube_points_with_face_centers(center, side_length)

df = pd.DataFrame(cube_points, columns=["v1", "v2", "v3"])




# Create the scatter plot with points
scatter = go.Scatter3d(
    x=df["v1"], 
    y=df["v2"], 
    z=df["v3"],
    mode="markers",
    marker=dict(size=6, color="blue", symbol="circle")
)

# Add lines connecting each point to the origin
lines = []
for _, row in df.iterrows():
    lines.append(
        go.Scatter3d(
            x=[0, row["v1"]],
            y=[0, row["v2"]],
            z=[0, row["v3"]],
            mode="lines",
            line=dict(color="black", width=1)
        )
    )

# Create a layout for the plot
layout = go.Layout(
    scene=dict(
        xaxis_title="v1",
        yaxis_title="v2",
        zaxis_title="v3",
    ),
    title="Scatter plot with lines connecting points to the origin",
    showlegend=False
)

# Combine the scatter plot and lines
data = [scatter] + lines

# Show the plot
fig = go.Figure(data=data, layout=layout)
fig.show()