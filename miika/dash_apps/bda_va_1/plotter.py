import plotly.express as px
import plotly.graph_objects as go

def gdp_plot(df, countries):
    # Subset by the selection of countries
    dff = df[countries]
    # Line graphs for every country
    fig = px.line(
        dff,
        x=df.index,
        y=dff.columns,
    )
    # Markers in the end of the line
    for country in countries:
        fig.add_scatter(
            x=[dff.index[-1]],  # Last year
            y=[dff[country].iloc[-1]],  # Last GDP value for this country
            mode='markers',
            marker=dict(size=10),
            showlegend=False,
        )
    # Annotation for China if it is selected
    if "China" in countries:
        annotation_text = """
        During the 2000s,<br>
        China began experiening rapid economic growth,<br>
        outpacing all other countries.
        """
        fig.add_annotation(
            text=annotation_text,
            x=45,
            y=df.loc["2005", "China"],
            axref="x domain",
            ax=-100,
            ayref="y domain",
            ay=-200,
            showarrow=True,
            arrowhead=2,
        )
    # Axis titles, legend and ticks
    fig.update_layout(
        xaxis_title="Year of Record",
        yaxis_title="GDP (in billions USD)",
        legend_title="",
        legend_yanchor="top",
        legend_y=0.99,
        legend_xanchor="left",
        legend_x=0.01,
        xaxis_tickmode="array",
        xaxis_tickvals=["1980","1990","2000","2010","2020"],
    )
    return fig