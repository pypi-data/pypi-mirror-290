import dash_ag_grid as dag
from dash import Dash, dcc, html
import pandas as pd

import os

app = Dash(__name__)


df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

columnDefs = [
    {
        "headerName": "Athlete",
        "children": [{"field": i} for i in ["athlete", "age", "country"]]
    },
    {
        "headerName": "Competition",
        "children": [{"field": "year"}, {"field": "date"}],
    },
    {"field": "sport"},
    {
        "headerName": "Medals",
        "children":  [{"field": i} for i in ["gold", "silver", "bronze", "total"]]
    },
]

defaultColDef = {
    "filter": True,
    "enableRowGroup": True,
    "enableValue": True,
    "enablePivot": True,
}

sideBar={
    "toolPanels": [
        {
            "id": "columns",
            "labelDefault": "Columns",
            "labelKey": "columns",
            "iconKey": "columns",
            "toolPanel": "agColumnsToolPanel",
        },
        {
            "id": "filters",
            "labelDefault": "Filters",
            "labelKey": "filters",
            "iconKey": "filter",
            "toolPanel": "agFiltersToolPanel",
        },
        {
            "id": "filters 2",
            "labelKey": "filters",
            "labelDefault": "More Filters",
            "iconKey": "menu",
            "toolPanel": "agFiltersToolPanel",
        },
    ],
    "position": "left",
    "defaultToolPanel": "filters",
}

app.layout = html.Div(
    [
        dcc.Markdown(
            """
        Demonstration of how to enable sidebar feature in a Dash AG Grid.    

        If the user sets `sideBar=True`, then the side bar is displayed with default configuration.
        The user can also set `sideBar` to `columns` or `filters` to display side bar with just one of Columns or Filters tool panels.
        """
        ),
        dag.AgGrid(
            id="sidebar-basic",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            dashGridOptions={"rowSelection": "multiple", "animateRows": False, "sideBar": True},
            defaultColDef=defaultColDef,
            enableEnterpriseModules=True,
            licenseKey=os.environ['AGGRID_ENTERPRISE'],
        ),
        dcc.Markdown(
            """
            A dictionary can be passed to allow detailed configuration of the side bar. Use this to configure the provided tool panels (e.g. pass parameters to the columns or filters panel) or to include custom tool panels.
            """
        ),

        dag.AgGrid(
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            dashGridOptions={"rowSelection": "multiple", "animateRows": False, "sideBar": sideBar},
            defaultColDef=defaultColDef,
            enableEnterpriseModules=True,
            licenseKey=os.environ['AGGRID_ENTERPRISE'],
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=False)
