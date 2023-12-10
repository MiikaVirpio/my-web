import plotly.graph_objects as go
import plotly.io as pio



def plot_graph(df, employees, permissions):
    
    # Subset by employees
    df = df.loc[employees, employees]
    
    def stringify_perms(cell):
        str_perms = ""
        for index, perm in enumerate(permissions):
            if cell[index] == 1:
                str_perms += perm + "<br>"
        return str_perms[:-4]
    
    fig = go.Figure(data=go.Heatmap(
                    # Z values are summed amounts of permissions.
                    # This would make easy to spot cases with a lot of
                    # permissions among many employees.
                    z=df.applymap(lambda x: sum(x)).values,
                    x=df.columns,
                    y=df.index,
                    # String representation added to cells to check what
                    # permissions there exactly is.
                    text=df.applymap(stringify_perms).values,
                    texttemplate='%{text}',
                    # Color bar with just 0-3 permissions is a bit funny,
                    # but with 10+ permissions it would make better sense.
                    colorbar=dict(
                        title="Permission count",
                        titleside="right",
                        dtick=1,
                    ),
                    colorscale=[[0, "#1a0933"], [1, "#ffc107"]]))
    fig.update_layout(
        title="Access to data permissions across organization",
        xaxis_title="Data To",
        yaxis_title="Data From",
        template=pio.templates["VAPOR"],
    )
    return fig
