"""
#Another table style
patient_info= dbc.Card(
    id="patient info",
    children=[
        dbc.CardHeader(html.H4(id='tittle_card_1_output')),
        dbc.CardBody(
            dbc.Row([
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records')
                )

            ])
        )
    ]
)
"""


"""
image_annotation_card = dbc.Card(
    id="imagebox",
    children=[
        dbc.CardHeader(html.H4('ADC Imaging')),
        dbc.CardBody(
            [dbc.Row(

            ),
                dcc.Graph(
                    id="graph",
                    figure=fig,
                    config={'modeBarButtonsToAdd': ["drawrect", "drawclosedpath","eraseshape"],
                            'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian', 'hoverClosestCartesian']
                    }
                )
            ]
        ),
        dbc.CardFooter(
            [
                dbc.Row([

                    dbc.Button("Previous", id='previous_button',color="info", className="mr-1"),
                    dbc.Button('Next', id='next_button',color='info', className='mr-1')

                ]),

            ]
        ),
    ],
    color='info', outline= True
)

image_annotation_card2 = dbc.Card(
    id="imagebox2",
    children=[
        dbc.CardHeader(html.H4('3DT2 Imaging')),
        dbc.CardBody(
            [dbc.Row(

            ),
                dcc.Graph(
                    id="graph2",
                    figure=fig2,
                    config={'modeBarButtonsToAdd': ["drawrect", "drawclosedpath","eraseshape"],
                            'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian', 'hoverClosestCartesian']
                    }
                )
            ]
        ),
        dbc.CardFooter(
            [
                dbc.Row([

                    dbc.Button("Previous", id='previous_button2',color="info", className="mr-1"),
                    dbc.Button('Next', id='next_button2',color='info', className='mr-1')

                ]),

            ]
        ),
    ],
    color='info', outline= True
)

image_annotation_card3 = dbc.Card(
    id="imagebox3",
    children=[
        dbc.CardHeader(html.H4('Perfusion Imaging')),
        dbc.CardBody(
            [dbc.Row(

            ),
                dcc.Graph(
                    id="graph3",
                    figure=fig3,
                    config={'modeBarButtonsToAdd': ["drawrect", "drawclosedpath","eraseshape"],
                            'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian', 'hoverClosestCartesian']
                    }
                )
            ]
        ),
        dbc.CardFooter(
            [
                dbc.Row([

                    dbc.Button("Previous", id='previous_button3',color="info", className="mr-1"),
                    dbc.Button('Next', id='next_button3',color='info', className='mr-1')

                ]),

            ]
        ),
    ],
    color='info', outline= True
)
"""

"""
#OPTION SEPARATED ANNOTATION CARDS
annotated_data_card1 =dbc.Card([
        dbc.CardHeader(html.H2("Annotated Data coordinates")),
        dbc.CardBody([

            dbc.Row(
                dbc.Col(
                        [dash_table.DataTable(
                                id="annotations-table",
                                columns=[
                                    dict(
                                        name=n,
                                        id=n,
                                        presentation=(
                                            "dropdown" if n == "Type" else "input"
                                        ),
                                    )
                                    for n in columns
                                ],
                                editable=True,
                                style_data={"height": 40},
                                style_cell={
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                    "maxWidth": 0,
                                },
                                dropdown={
                                    "Type": {
                                        "options": [
                                            {"label": o, "value": o}
                                            for o in annotation_types
                                        ],
                                        "clearable": False,
                                    }
                                },
                                style_cell_conditional=[
                                    {"if": {"column_id": "Type"}, "textAlign": "left",}
                                ],
                                fill_width=True,
                            ),
                            dcc.Store(id="graph-copy", data=fig),
                            dcc.Store(
                                id="annotations-store",
                                data=dict(
                                    **{
                                        filename: {"shapes": []}
                                        for filename in filelist
                                    },
                                    **{"starttime": time_passed()}
                                ),
                            ),
                            dcc.Store(
                                id="image_files",
                                data={"files": filelist, "current_patient": 0, "current_technique":0},
                            ),
                        ],
                    ),
                ),

        ])

    ]
    )

annotated_data_card2=dbc.Card([
        dbc.CardHeader(html.H2("Create new annotation for")),
        dbc.CardBody([
            dbc.Row(
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="annotation-type-dropdown",
                                options=[
                                    {"label": t, "value": t} for t in annotation_types
                                ],
                                value=DEFAULT_ATYPE,
                                clearable=False,
                            ),
                        ],
                        align="center",
                    )
                ),
            ]
        ),
        dbc.CardFooter(
            [
                html.Div(
                    [
                        # We use this pattern because we want to be able to download the
                        # annotations by clicking on a button
                        html.A(
                            id="download",
                            download="annotations.json",
                            # make invisble, we just want it to click on it
                            style={"display": "none"},
                        ),
                        dbc.Button(
                            "Download annotations", id="download-button", outline=True,
                        ),
                        html.Div(id="dummy", style={"display": "none"}),
                        dbc.Tooltip(
                            "You can download the annotated data in a .json format by clicking this button",
                            target="download-button",
                        ),

                    ],
                )
            ]
        )
    ])

"""