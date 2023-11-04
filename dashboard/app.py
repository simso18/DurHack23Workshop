from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly

from ..common import HockeyTeamResults


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash("HockeyTeamResults", external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H4("Hockey Team Results"),
        html.Br(),
        dash_table.DataTable(id="data-table", page_size=25),
        html.Br(),
        "Choose a team:",
        dcc.Dropdown(id="selected-team", persistence=True),
        dcc.Graph(id="team-time-series"),
        dcc.Interval(
            id="interval-component",
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@callback(Output("data-table", "data"), Input("interval-component", "n_intervals"))
def update_data_table(n):
    return HockeyTeamResults().get_data()

@callback(Output("selected-team", "options"), Input("interval-component", "n_intervals"))
def update_team_options(n):
    data = HockeyTeamResults().get_data()
    return {result["TeamName"] for result in data}

@callback(
    Output("live-update-graph", "figure"),
    Input("interval-component", "n_intervals"),
    Input("selected-team", "value"),
)
def update_graph_live(n, team: str):
    data = HockeyTeamResults().get_data()
    team_data = [data_point for data_point in data if data_point["TeamName"] == team]

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=3, cols=2, vertical_spacing=0.2)
    fig["layout"]["margin"] = {
        "l": 30, "r": 10, "b": 30, "t": 10
    }
    fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

    for i, stat in enumerate(["Wins", "Losses", "OTLosses", "WinPct", "GoalsFor", "GoalsAgainst"]):
        fig.append_trace({
            "x": [datapoint["Year"] for datapoint in team_data],
            "y": [datapoint[stat] for datapoint in team_data],
            "name": stat,
            "mode": "lines+markers",
            "type": "scatter"
        }, *divmod(i, 2))

    return fig


if __name__ == "__main__":
    app.run(debug=True)