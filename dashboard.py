"""
Boston Open Space Analysis - Bostonography Final Project
Aarav Sikriwal | INSH 2102

Data source: Analyze Boston open space dataset
Run: python dashboard.py
Open: http://127.0.0.1:8050
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output

# load the csv from the data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "open_space.csv")

df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

# rename columns to something easier to work with
df = df[["SITE_NAME", "DISTRICT", "TypeLong", "ACRES", "ADDRESS", "OWNERSHIP", "YearAcquired"]].rename(columns={
    "SITE_NAME":    "Name",
    "DISTRICT":     "Neighborhood",
    "TypeLong":     "Type",
    "ACRES":        "Acres",
    "ADDRESS":      "Address",
    "OWNERSHIP":    "Ownership",
    "YearAcquired": "Year",
})

df["Acres"] = pd.to_numeric(df["Acres"], errors="coerce").fillna(0)
df["Year"]  = pd.to_numeric(df["Year"],  errors="coerce")
df["Year"]  = df["Year"].where(df["Year"] > 0, other=None)

# shorten type names so they fit in charts
TYPE_SHORT = {
    "Parks, Playgrounds & Athletic Fields": "Parks & Playgrounds",
    "Malls, Squares & Plazas":             "Malls & Squares",
    "Parkways, Reservations & Beaches":    "Parkways & Beaches",
    "Urban Wilds":                         "Urban Wilds",
    "Cemeteries & Burying Grounds":        "Cemeteries",
    "Community Gardens":                   "Community Gardens",
    "Open Land":                           "Open Land",
}
df["TypeShort"] = df["Type"].map(TYPE_SHORT).fillna(df["Type"])

all_neighborhoods = sorted(df["Neighborhood"].dropna().unique())
all_types         = sorted(df["TypeShort"].dropna().unique())

app = Dash(__name__, title="Boston Open Space")

app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f5f5",
                              "padding": "20px", "maxWidth": "1100px", "margin": "0 auto"}, children=[

    # title
    html.H1("Boston Open Space Analysis",
            style={"color": "#2c2c2c", "borderBottom": "2px solid #4a7c3f",
                   "paddingBottom": "8px", "marginBottom": "4px"}),
    html.P("INSH 2102 — Bostonography | Data: Analyze Boston Open Space Dataset",
           style={"color": "#666", "fontSize": "13px", "marginTop": "0", "marginBottom": "20px"}),

    # quick summary numbers
    html.Div([
        html.Div([
            html.Div(f"{len(df)}", style={"fontSize": "26px", "fontWeight": "bold", "color": "#4a7c3f"}),
            html.Div("Total spaces", style={"fontSize": "12px", "color": "#666"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "12px 20px", "textAlign": "center", "flex": "1"}),
        html.Div([
            html.Div(f"{df['Acres'].sum():,.0f}", style={"fontSize": "26px", "fontWeight": "bold", "color": "#4a7c3f"}),
            html.Div("Total acres", style={"fontSize": "12px", "color": "#666"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "12px 20px", "textAlign": "center", "flex": "1"}),
        html.Div([
            html.Div(f"{len(all_neighborhoods)}", style={"fontSize": "26px", "fontWeight": "bold", "color": "#4a7c3f"}),
            html.Div("Neighborhoods", style={"fontSize": "12px", "color": "#666"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "12px 20px", "textAlign": "center", "flex": "1"}),
        html.Div([
            html.Div(f"{len(all_types)}", style={"fontSize": "26px", "fontWeight": "bold", "color": "#4a7c3f"}),
            html.Div("Space types", style={"fontSize": "12px", "color": "#666"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "12px 20px", "textAlign": "center", "flex": "1"}),
    ], style={"display": "flex", "gap": "12px", "marginBottom": "20px"}),

    # ---- neighborhood bar chart ----
    html.Div([
        html.H3("Spaces by Neighborhood", style={"marginTop": "0", "color": "#2c2c2c"}),
        html.P("Compare how open space is distributed across Boston's neighborhoods.",
               style={"fontSize": "13px", "color": "#666", "marginTop": "-8px"}),

        html.Div([
            html.Label("Show:  ", style={"fontSize": "13px", "marginRight": "6px"}),
            dcc.RadioItems(
                id="metric-toggle",
                options=[
                    {"label": "  Number of spaces  ", "value": "count"},
                    {"label": "  Total acres",        "value": "acres"},
                ],
                value="count",
                inline=True,
                inputStyle={"marginRight": "4px"},
                labelStyle={"marginRight": "18px", "fontSize": "13px"},
            ),
            html.Label("  Filter by type:  ", style={"fontSize": "13px", "marginLeft": "20px", "marginRight": "6px"}),
            dcc.Dropdown(
                id="type-filter-bar",
                options=[{"label": "All types", "value": "all"}] +
                        [{"label": t, "value": t} for t in all_types],
                value="all",
                clearable=False,
                style={"width": "230px", "fontSize": "13px", "display": "inline-block", "verticalAlign": "middle"},
            ),
        ], style={"marginBottom": "10px", "display": "flex", "alignItems": "center", "flexWrap": "wrap"}),

        dcc.Graph(id="bar-chart", config={"displayModeBar": False}),
    ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
              "padding": "16px", "marginBottom": "20px"}),

    # ---- two charts side by side ----
    html.Div([
        html.Div([
            html.H3("Type Breakdown", style={"marginTop": "0", "color": "#2c2c2c"}),
            html.P("What kinds of open spaces exist in Boston?",
                   style={"fontSize": "13px", "color": "#666", "marginTop": "-8px"}),
            dcc.Graph(id="donut-chart", config={"displayModeBar": False}, style={"height": "320px"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "16px", "flex": "1"}),

        html.Div([
            html.H3("10 Largest Spaces (acres)", style={"marginTop": "0", "color": "#2c2c2c"}),
            html.P("Which individual spaces take up the most land?",
                   style={"fontSize": "13px", "color": "#666", "marginTop": "-8px"}),
            dcc.Graph(id="top-chart", config={"displayModeBar": False}, style={"height": "320px"}),
        ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
                  "padding": "16px", "flex": "1"}),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px", "flexWrap": "wrap"}),

    # ---- data table ----
    html.Div([
        html.H3("Browse All Spaces", style={"marginTop": "0", "color": "#2c2c2c"}),
        html.P("Search and filter the full dataset. Click column headers to sort.",
               style={"fontSize": "13px", "color": "#666", "marginTop": "-8px"}),

        html.Div([
            dcc.Input(
                id="search-input", type="text",
                placeholder="Search name or address...",
                debounce=True,
                style={"padding": "7px 10px", "border": "1px solid #ccc", "borderRadius": "4px",
                       "fontSize": "13px", "width": "220px"},
            ),
            dcc.Dropdown(
                id="neighborhood-filter",
                options=[{"label": "All neighborhoods", "value": "all"}] +
                        [{"label": n, "value": n} for n in all_neighborhoods],
                value="all", clearable=False,
                style={"width": "210px", "fontSize": "13px"},
                placeholder="All neighborhoods",
            ),
            dcc.Dropdown(
                id="type-filter-table",
                options=[{"label": "All types", "value": "all"}] +
                        [{"label": t, "value": t} for t in all_types],
                value="all", clearable=False,
                style={"width": "190px", "fontSize": "13px"},
                placeholder="All types",
            ),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "10px", "flexWrap": "wrap",
                  "alignItems": "center"}),

        html.Div(id="results-count",
                 style={"fontSize": "12px", "color": "#888", "marginBottom": "6px"}),

        dash_table.DataTable(
            id="park-table",
            columns=[
                {"name": "Name",         "id": "Name"},
                {"name": "Neighborhood", "id": "Neighborhood"},
                {"name": "Type",         "id": "TypeShort"},
                {"name": "Acres",        "id": "Acres",  "type": "numeric",
                 "format": {"specifier": ".2f"}},
                {"name": "Est.",         "id": "Year"},
                {"name": "Ownership",    "id": "Ownership"},
            ],
            sort_action="native",
            page_size=20,
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "#eef2eb",
                "fontWeight": "bold",
                "fontSize": "13px",
                "borderBottom": "2px solid #ccc",
                "padding": "8px 10px",
            },
            style_cell={
                "fontSize": "13px",
                "padding": "7px 10px",
                "border": "1px solid #eee",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"},
            ],
        ),
    ], style={"background": "#fff", "border": "1px solid #ddd", "borderRadius": "6px",
              "padding": "16px", "marginBottom": "20px"}),

    html.P(f"Source: Analyze Boston Open Space Dataset  ·  {len(df)} total records",
           style={"textAlign": "center", "fontSize": "12px", "color": "#aaa"}),
])


# ---- callbacks ----

@app.callback(
    Output("bar-chart", "figure"),
    Input("metric-toggle",   "value"),
    Input("type-filter-bar", "value"),
)
def update_bar(metric, type_filter):
    data = df if type_filter == "all" else df[df["TypeShort"] == type_filter]

    if metric == "count":
        agg = data.groupby("Neighborhood").size().reset_index(name="Value")
        xlabel = "Number of open spaces"
    else:
        agg = data.groupby("Neighborhood")["Acres"].sum().reset_index(name="Value")
        agg["Value"] = agg["Value"].round(1)
        xlabel = "Total acres"

    agg = agg.sort_values("Value", ascending=True)

    fig = px.bar(
        agg, x="Value", y="Neighborhood",
        orientation="h",
        labels={"Value": xlabel, "Neighborhood": ""},
        color_discrete_sequence=["#4a7c3f"],
    )
    fig.update_layout(
        margin=dict(l=0, r=10, t=10, b=30),
        height=max(380, len(agg) * 34 + 60),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#eeeeee"),
    )
    return fig


@app.callback(
    Output("donut-chart", "figure"),
    Input("metric-toggle", "value"),
)
def update_donut(_):
    counts = df.groupby("TypeShort").size().reset_index(name="Count")

    fig = go.Figure(go.Pie(
        labels=counts["TypeShort"],
        values=counts["Count"],
        hole=0.5,
        textinfo="percent",
        hovertemplate="%{label}<br>%{value} spaces (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(font=dict(size=11), orientation="v"),
        paper_bgcolor="white",
    )
    return fig


@app.callback(
    Output("top-chart", "figure"),
    Input("metric-toggle", "value"),
)
def update_top(_):
    top = df[df["Acres"] > 0].nlargest(10, "Acres")[["Name", "Acres"]].copy()
    top["Label"] = top["Name"].apply(lambda n: n[:26] + "..." if len(n) > 26 else n)
    top = top.sort_values("Acres", ascending=True)

    fig = px.bar(
        top, x="Acres", y="Label",
        orientation="h",
        labels={"Acres": "Acres", "Label": ""},
        color_discrete_sequence=["#5b9e4e"],
    )
    fig.update_layout(
        margin=dict(l=0, r=10, t=10, b=30),
        height=320,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#eeeeee"),
    )
    return fig


@app.callback(
    Output("park-table",    "data"),
    Output("results-count", "children"),
    Input("search-input",        "value"),
    Input("neighborhood-filter", "value"),
    Input("type-filter-table",   "value"),
)
def update_table(search, neighborhood, type_filter):
    filtered = df.copy()

    if search:
        q = search.lower()
        filtered = filtered[
            filtered["Name"].str.lower().str.contains(q, na=False) |
            filtered["Address"].str.lower().str.contains(q, na=False)
        ]
    if neighborhood and neighborhood != "all":
        filtered = filtered[filtered["Neighborhood"] == neighborhood]
    if type_filter and type_filter != "all":
        filtered = filtered[filtered["TypeShort"] == type_filter]

    out = filtered[["Name", "Neighborhood", "TypeShort", "Acres", "Year", "Ownership"]].copy()
    out["Year"]  = out["Year"].apply(lambda y: str(int(y)) if pd.notna(y) else "-")
    out["Acres"] = out["Acres"].apply(lambda a: round(a, 2) if a > 0 else None)

    return out.to_dict("records"), f"Showing {len(out)} of {len(df)} spaces"


if __name__ == "__main__":
    print("\nBoston Open Space Explorer")
    print("Open http://127.0.0.1:8050 in your browser\n")
    app.run(debug=True)
    