import pandas as pd
import plotly.graph_objects as go
import streamlit as st

colors = [
    "lightcoral",
    "lightsteelblue",
    "BurlyWood",
    "lightseagreen",
    "lightsalmon",
    "lightskyblue",
    "lightgreen",
    "lightpink",
    "lightgray",
    "lightblue",
]

def avg_price_fig(choosen_df):
    '''
    Make fugure Average Price by month
    INPUT: dataframe
    OUTPUT: figure, plotly.graph_objects
    '''
    fig = go.Figure()
    for m in set(choosen_df["Year"]):
        color = colors[m % 10]
        fig.add_trace(
            go.Bar(
                x=choosen_df["Month"],
                y=choosen_df[choosen_df["Year"] == m]["Average"],
                name=m,
                text=m,
                textposition="inside",
                insidetextanchor="start",
                hovertemplate="<br>Price: %{y}",
                marker_color=color,
                showlegend=False,
            )
        )

    fig.update_layout(
        barmode="group",
        title={
            "text": "Average Price",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        yaxis_title="Price ($)",
    )
    return fig

def diff_price_fig(choosen_df):
    '''
    Make fugure Percent of Original List Price
    INPUT: dataframe
    OUTPUT: figure, plotly.graph_objects
    '''
    fig = go.Figure()
    price_diff = [p - 100 for p in choosen_df[
                    "Percent of Original List Price Received"
                ]]
    for m in set(choosen_df["Year"]):
        color = colors[m % 10]
        fig.add_trace(
            go.Bar(
                x=choosen_df["Month"],
                y=[p - 100 for p in choosen_df[choosen_df["Year"] == m][
                    "Percent of Original List Price Received"
                ]],
                name=m,
                text=m,
                texttemplate='%{text}<br>%{y}%', 
                textposition='outside',
                insidetextanchor="start",
                marker_color=color,
                showlegend=False,
                cliponaxis=False,
            )
        )
    fig.update_layout(
        barmode="group",
        title={
            "text": "Percent of Original List Price",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    yaxis_title="Difference (%)",
    yaxis_range=[min(price_diff) - 3, max(price_diff) + 3]
)
    return fig

def new_listing_fig(choosen_df):
    '''
    Make fugure compare New Listings and Closed Sales
    INPUT: dataframe
    OUTPUT: figure, plotly.graph_objects
    '''
    fig = go.Figure()
    for m in set(choosen_df["Year"]):
        color = colors[m % 10]
        fig.add_trace(
            go.Bar(
                x=choosen_df["Month"],
                y=choosen_df[choosen_df["Year"] == m]["New Listings"],
                name=m,
                text=m,
                textposition="inside",
                insidetextanchor="start",
                offsetgroup=m,
                hovertemplate="<br>New Listings: %{y}",
                marker_color=color,
                showlegend=False,
                opacity=0.8,
            )
        )
        fig.add_trace(
            go.Bar(
                x=choosen_df["Month"],
                y=choosen_df[choosen_df["Year"] == m]["Closed Sales"],
                name=m,
                text=m,
                textposition="inside",
                insidetextanchor="start",
                offsetgroup=m,
                hovertemplate="<br>Closed Sales: %{y}",
                marker_color=color,
                showlegend=False,
                opacity=0.7,
            )
        )

    fig.update_layout(
        title={
            "text": "New Listings vs Closed Sales",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        yaxis_title="Sales",
    )
    return fig