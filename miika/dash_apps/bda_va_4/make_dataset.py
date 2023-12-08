import pandas as pd
import numpy as np
#from miika.settings import BASE_DIR

import plotly.graph_objs as go
import plotly.express as px

def make_dataset():
    column_names = ["From", "To" ,"Type" ,"Permission"]
    #df = pd.read_csv(os.path.join(BASE_DIR, 'miika/static/dash_apps/bda_va_4/data_permissions.csv'), names=column_names)
    df = pd.read_csv('../../static/dash_apps/bda_va_4/data_permissions.csv', names=column_names, header=0)
    df.describe()
    # We can see there is 10 From and 10 To, so one can assume those are our 10 employees
    employees = df["From"].unique()
    df["Type"].value_counts()
    # There is the Commercial with trailing space, let's fix that
    df["Type"] = df["Type"].str.strip()
    # Have our unique permissions in a list
    permissions = df[df["Type"] != "ALL/ANY"]["Type"].unique()
    # Create new dataframe with employees as rows and columns
    df_perm = pd.DataFrame(index=employees, columns=employees)
    # Method setting cell to be list of permissions by received rows in dataframe
    def set_perms(perms_df):
        # Set default permissions list to 0 in length of permissions
        perms = [0] * len(permissions)
        for index, row in perms_df.iterrows():
            # Set permission location by index in list and value by permission
            for perm in permissions:
                if row["Type"] == perm:
                    perms[np.where(permissions == perm)[0][0]] = 1 if row["Permission"] == "Yes" else 0
            # If however the permission is ALL/ANY, set all permissions to 1 or 0
            if row["Type"] == "ALL/ANY":
                print(row)
                # This will set everything even if there would be configurations before it.
                # One solution would be to order rows before setting or being aware of what is set already.
                # For the sake of speed we are naive this time.
                perms = [1,1,1] if row["Permission"] == "Yes" else [0,0,0]
        return perms
    
    for index, row in df_perm.iterrows():
        for column in df_perm.columns:
            df_perm.at[index, column] = set_perms(df.loc[(df["From"] == index) & (df["To"] == column)])
    
    def stringify_perms(cell):
        str_perms = ""
        for index, perm in enumerate(permissions):
            if cell[index] == 1:
                str_perms += perm + "<br>"
        return str_perms[:-4]
    
    text_df = df_perm.applymap(stringify_perms)
    
    fig = go.Figure(data=go.Heatmap(
                    z=df_perm.applymap(lambda x: sum(x)).values,
                    x=df_perm.columns,
                    y=df_perm.index,
                    text=text_df.values,
                    texttemplate='%{text}',
                    colorbar=dict(
                        title="Permission count",
                        titleside="right",
                        dtick=1,
                    ),))
    fig.update_layout(
        title="Access to data permissions across organization",
        width=800,
        height=800,
        xaxis_title="Data To",
        yaxis_title="Data From",
    )
        
    fig.show()
    
    
    
    
    return df
