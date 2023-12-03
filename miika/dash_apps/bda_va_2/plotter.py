import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


def plot_structure(df, segments):
    # Make a subset of the dataframe
    subset_columns = [
        "Segment",
        "Gross Sales",
        "Profit",
        "Discounts Value",
        "Total Costs",
    ]
    # Subset of the dataframe where segments is in the list of segments
    df_structure = df[df["Segment"].isin(segments)][subset_columns]
    # Group by segment
    df_structure = df_structure.groupby("Segment").sum()
    # Calculate some percentages
    df_structure["Profit margin"] = np.round(
        (df_structure["Profit"] / df_structure["Gross Sales"]), 2
    )
    df_structure["Discount to Sales"] = np.round(
        (df_structure["Discounts Value"] / df_structure["Gross Sales"]), 2
    )
    df_structure["Discount to Profit"] = np.round(
        (df_structure["Discounts Value"] / df_structure["Profit"]), 2
    )
    df_structure["COGS %"] = np.round(
        (df_structure["Total Costs"] / df_structure["Gross Sales"]), 2
    )
    # Make a plotly figure
    fig_structure = go.Figure(
        data=[
            go.Bar(
                name="Profit",
                y=df_structure["Profit"],
                x=df_structure.index,
                text=df_structure["Profit margin"],
                textposition="auto",
            ),
            go.Bar(
                name="Discounts Value",
                y=df_structure["Discounts Value"],
                x=df_structure.index,
                text=df_structure["Discount to Sales"],
                textposition="auto",
            ),
            go.Bar(
                name="COGS",
                y=df_structure["Total Costs"],
                x=df_structure.index,
                text=df_structure["COGS %"],
                textposition="auto",
            ),
        ]
    )
    fig_structure.update_layout(
        title="Profit structure from Gross Sales",
        barmode="stack",
        template=pio.templates["VAPOR"],
    )
    return fig_structure


def plot_monthly(df, segments):
    df_sb_monthly = df[df["Segment"].isin(segments)].pivot_table(
        index="Month nbr", columns="Segment", values="Gross Sales", aggfunc="sum"
    )
    fig_monthly = px.line(df_sb_monthly, x=df_sb_monthly.index, y=df_sb_monthly.columns)
    fig_monthly.update_layout(
        title="Monthly Gross Saless",
        xaxis_title="Month",
        yaxis_title="Sales",
        legend_title="",
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="left",
        legend_x=0.01,
        template=pio.templates["VAPOR"],
    )
    return fig_monthly
