import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
import re
import time
from skimage import io
import os
import pydicom
import pandas as pd
import matplotlib.pyplot as plt
from pydicom import dcmread
from pydicom.data import get_testdata_file

DEBUG = True

NUM_ATYPES = 15
DEFAULT_FIG_MODE = "layout"
annotation_colormap = px.colors.qualitative.Light24
annotation_types = [
    "Silvio",
    "Cingulado",
    "Central",
    "Temporal superior",
    "Parito-occipital",
    "Frontal superior",
]
DEFAULT_ATYPE = annotation_types[0]

# prepare bijective type<->color mapping
typ_col_pairs = [
    (t, annotation_colormap[n % len(annotation_colormap)])
    for n, t in enumerate(annotation_types)
]
# types to colors
color_dict = {}
# colors to types
type_dict = {}
for typ, col in typ_col_pairs:
    color_dict[typ] = col
    type_dict[col] = typ

options = list(color_dict.keys())
columns = ["Type", "X0", "Y0", "X1", "Y1"]
# Open the readme for use in the context info
with open("assets/Howto.md", "r") as f:
    # Using .read rather than .readlines because dcc.Markdown
    # joins list of strings with newline characters
    howto = f.read()


def debug_print(*args):
    if DEBUG:
        print(*args)


def coord_to_tab_column(coord):
    return coord.upper()


def time_passed(start=0):
    return round(time.mktime(time.localtime())) - start


def format_float(f):
    return "%.2f" % (float(f),)


def shape_to_table_row(sh):
    return {
        "Type": type_dict[sh["line"]["color"]],
        "X0": format_float(sh["x0"]),
        "Y0": format_float(sh["y0"]),
        "X1": format_float(sh["x1"]),
        "Y1": format_float(sh["y1"]),
    }


def default_table_row():
    return {
        "Type": DEFAULT_ATYPE,
        "X0": format_float(10),
        "Y0": format_float(10),
        "X1": format_float(20),
        "Y1": format_float(20),
    }


def table_row_to_shape(tr):
    return {
        "editable": True,
        "xref": "x",
        "yref": "y",
        "layer": "above",
        "opacity": 1,
        "line": {"color": color_dict[tr["Type"]], "width": 4, "dash": "solid"},
        "fillcolor": "rgba(0, 0, 0, 0)",
        "fillrule": "evenodd",
        "type": "rect",
        "x0": tr["X0"],
        "y0": tr["Y0"],
        "x1": tr["X1"],
        "y1": tr["Y1"],
    }


def shape_cmp(s0, s1):
    """ Compare two shapes """
    return (
        (s0["x0"] == s1["x0"])
        and (s0["x1"] == s1["x1"])
        and (s0["y0"] == s1["y0"])
        and (s0["y1"] == s1["y1"])
        and (s0["line"]["color"] == s1["line"]["color"])
    )


def shape_in(se):
    """ check if a shape is in list (done this way to use custom compare) """
    return lambda s: any(shape_cmp(s, s_) for s_ in se)


def index_of_shape(shapes, shape):
    for i, shapes_item in enumerate(shapes):
        if shape_cmp(shapes_item, shape):
            return i
    raise ValueError  # not found


def annotations_table_shape_resize(annotations_table_data, fig_data):
    """
    Extract the shape that was resized (its index) and store the resized
    coordinates.
    """
    debug_print("fig_data", fig_data)
    debug_print("table_data", annotations_table_data)
    for key, val in fig_data.items():
        shape_nb, coord = key.split(".")
        # shape_nb is for example 'shapes[2].x0': this extracts the number
        shape_nb = shape_nb.split(".")[0].split("[")[-1].split("]")[0]
        # this should correspond to the same row in the data table
        # we have to format the float here because this is exactly the entry in
        # the table
        annotations_table_data[int(shape_nb)][
            coord_to_tab_column(coord)
        ] = format_float(fig_data[key])
        # (no need to compute a time stamp, that is done for any change in the
        # table values, so will be done later)
    return annotations_table_data


def shape_data_remove_timestamp(shape):
    """
    go.Figure complains if we include the 'timestamp' key when updating the
    figure
    """
    new_shape = dict()
    for k in shape.keys() - set(["timestamp"]):
        new_shape[k] = shape[k]
    return new_shape


external_stylesheets = [dbc.themes.BOOTSTRAP, "assets/image_annotation_style.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def fast_scandir_folder(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    im_folder = []
    im_folder.append(subfolders)
    return im_folder

path = 'assets/Base_de_Datos/'
filelist_patient = fast_scandir_folder(path)

patient_identification = [];
patient_dictionary = {}
for i in range(len(filelist_patient[0])):
    id = filelist_patient[0][i][21:]
    patient_identification.append(id)
    patient_dictionary[id] = i

patient_identification_default = patient_identification[0]

#ETIQUETAS metodos

def dictionary_function(vector):
    vector_dictionary = {}
    for i in range(len(vector)):
        id = vector[i]
        vector_dictionary[id] = i
    return vector_dictionary

techniques = ["3DT2", "ADC", "Perfusion"]
techniques_default = techniques[0]
techniques_dictionary = dictionary_function(techniques)


#Create a list of all the files
filelist= [os.path.join(r,file) for r,d,fl in os.walk(path) for file in fl]

#PARTE READER
#Create files_3DT2,  files_ADC, files_Perfusion, list of the name of the images inside the folder
filelist_3DT2=[]
filelist_ADC=[]
filelist_Perfusion=[]

def classificar(filelist):
    for i in range(len(filelist)):
        if '3DT2' in filelist[i]:
            filelist_3DT2.append(filelist[i])
        if 'ADC' in filelist[i]:
            filelist_ADC.append(filelist[i])
        if 'Perfusion' in filelist[i]:
            filelist_Perfusion.append(filelist[i])
    return filelist_3DT2,filelist_Perfusion,filelist_ADC

filelist_3DT2,filelist_Perfusion,filelist_ADC=classificar(filelist)



#list of the name of the images inside the folder
list_images_3DT2=[]
list_images_ADC=[]
list_images_Perfusion=[]

for i in range(len(filelist_3DT2)):
    id = filelist_3DT2[i][48:]
    list_images_3DT2.append(id)
for i in range(len(filelist_ADC)):
    id = filelist_ADC[i][47:]
    list_images_ADC.append(id)
for i in range(len(filelist_Perfusion)):
    id = filelist_Perfusion[i][53:]
    list_images_Perfusion.append(id)

#dictionary with keys method, elements Images
image_dictionary = {}
for i in range(len(list_images_3DT2)):
    id = '3DT2'
    image_dictionary[id] = list_images_3DT2
for i in range(len(list_images_ADC)):
    id='ADC'
    image_dictionary[id] = list_images_ADC
for i in range(len(list_images_Perfusion)):
    id='Perfusion'
    image_dictionary[id] = list_images_Perfusion

patient_info_dictionary = {}

path_initial = filelist[2]
ds = pydicom.dcmread(path_initial)

def patientinfodict(ds):
    pat_name = ds.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    for i in range(len(ds)):
        id = 'Patient Name'
        patient_info_dictionary[id] = [display_name]
        id = 'Patient ID'
        patient_info_dictionary[id] = [ds.PatientID]
        id = 'Date of birth'
        patient_info_dictionary[id] = [ds.PatientBirthDate]
        id = 'Modality'
        patient_info_dictionary[id] = [ds.Modality]
        id = 'Study Date'
        patient_info_dictionary[id] = [ds.StudyDate]
        id = 'Image Size'
        patient_info_dictionary[id] = [str(ds.Rows) + 'x' + str(ds.Columns)]

    return patient_info_dictionary


patient_info_dictionary = patientinfodict(ds)
df = pd.DataFrame.from_dict(patient_info_dictionary)

image_id_patient_before = -1
image_id_technique_before = -1
image_id_plane_before = -1

server = app.server

#Read the dicom file
path_initial=filelist[2]
ds = pydicom.dcmread(path_initial)
fig= px.imshow(pydicom.dcmread(path_initial).pixel_array, color_continuous_scale='gray')
fig.update_layout(
    newshape_line_color=color_dict[DEFAULT_ATYPE],
    margin=dict(l=0, r=0, b=0, t=0, pad=4),
    dragmode="pan",
)


# Buttons
button_gh = dbc.Button(
    "Learn more",
    id="howto-open",
    outline=True,
    color="secondary",
    # Turn off lowercase transformation for class .button in stylesheet
    style={"textTransform": "none"},
)

button_howto = dbc.Button(
    "View Code on github",
    outline=True,
    color="primary",
    href="https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-image-annotation",
    id="gh-link",
    style={"text-transform": "none"},
)

# Modal
modal_overlay = dbc.Modal(
    [
        dbc.ModalBody(html.Div([dcc.Markdown(howto, id="howto-md")])),
        dbc.ModalFooter(dbc.Button("Close", id="howto-close", className="howto-bn",)),
    ],
    id="modal",
    size="lg",
    style={"font-size": "small"},
)

# Cards
patient_info = dbc.Card(
    id="patient info",
    children=[
        dbc.CardBody(
            dbc.Row([
                dbc.Table.from_dataframe(df, striped=True, bordered=True

                                         )

            ])
        )
    ]
)

image_annotation_card = dbc.Card(
    id="imagebox",
    children=[
        dbc.CardHeader(html.H4(id="tittle_card_1_output")),
        dbc.CardBody(
            [
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
                dcc.Markdown(
                    "** Select patient and technique to choose an image ** \n\n"
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='patient_button',
                            options=[{'label': i, 'value': i} for i in patient_identification],
                            value=patient_identification_default,
                            clearable=False
                        ),
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='techniques_button',
                            options=[{'label': i, 'value': i} for i in image_dictionary.keys()],
                            value=techniques_default,
                            clearable=False

                        ),
                    ),
                    dbc.Button("Previous", id='previous_button',color="info", className="mr-1"),
                    dbc.Button('Next', id='next_button',color='info', className='mr-1')

                ]),

            ]
        ),
    ],
    color='info', outline= True
)

annotated_data_card = dbc.Card(
    [
        dbc.CardHeader(html.H2("Annotated data")),
        dbc.CardBody(
            [
                dbc.Row(dbc.Col(html.H3("Coordinates of annotations"))),
                dbc.Row(
                    dbc.Col(
                        [
                            dash_table.DataTable(
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
                dbc.Row(
                    dbc.Col(
                        [
                            html.H3("Create new annotation for"),
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
        ),
    ],
color='info', outline= True
)


# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(
                                src=app.get_asset_url("dash-logo-new.png"),
                                height="30px",
                            ),
                            href="https://plot.ly",
                        )
                    ),
                    dbc.Col(dbc.NavbarBrand("DICOM Viewer")),
                ],
                align="center",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(
                            dbc.Nav(
                                [dbc.NavItem(button_howto)],
                                className="ml-auto",
                                navbar=True,
                            ),
                            id="navbar-collapse",
                            navbar=True,
                        ),
                        modal_overlay,
                    ]
                ),
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(image_annotation_card),
                        dbc.Col(
                            [dbc.Row(annotated_data_card),
                             dbc.Row(patient_info)])

                    ],
                ),
            ],
            fluid=True,
        ),
    ]
)

@app.callback(
    Output(component_id="tittle_card_1_output", component_property="children"),
    [
        Input(component_id="patient_button", component_property="value"),
        Input(component_id="techniques_button", component_property="value"),


    ]
)


def update_output_div(patient, techniques):
    return '{}, technique {} '.format(patient, techniques)

@app.callback(
    [Output("annotations-table", "data"), Output("image_files", "data")],
    [
        Input("patient_button", "value"),
        Input("techniques_button", "value"),
        Input("graph", "relayoutData")
    ],
    [
        State("annotations-table", "data"),
        State("image_files", "data"),
        State("annotations-store", "data"),
        State("annotation-type-dropdown", "value"),
    ],
)
def modify_table_entries(
    id_patient,
    id_techniques,
    graph_relayoutData,
    annotations_table_data,
    image_files_data,
    annotations_store_data,
    annotation_type,
):
    global image_id_patient_before, image_id_technique_before
    global patient_dictionary, techniques_dictionary

    cbcontext = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if cbcontext == "graph.relayoutData":
        debug_print("graph_relayoutData:", graph_relayoutData)
        debug_print("annotations_table_data before:", annotations_table_data)
        if "shapes" in graph_relayoutData.keys():
            # this means all the shapes have been passed to this function via
            # graph_relayoutData, so we store them
            annotations_table_data = [
                shape_to_table_row(sh) for sh in graph_relayoutData["shapes"]
            ]
        elif re.match("shapes\[[0-9]+\].x0", list(graph_relayoutData.keys())[0]):
            # this means a shape was updated (e.g., by clicking and dragging its
            # vertices), so we just update the specific shape
            annotations_table_data = annotations_table_shape_resize(
                annotations_table_data, graph_relayoutData
            )
        if annotations_table_data is None:
            return dash.no_update
        else:
            debug_print("annotations_table_data after:", annotations_table_data)
            return (annotations_table_data, image_files_data)

    image_id_patient = patient_dictionary[id_patient]
    image_id_technique = techniques_dictionary[id_techniques]


    #print('HOLaaaaaaaaaaaa', image_files_data["files"])
    # print('ADIOSSSSSSSSSSS', filelist)

    image_files_data["current_patient"] = image_id_patient
    image_files_data["current_technique"] = image_id_technique
    #image_files_data["current"] %= len(image_files_data["files"])

    if (image_id_patient != image_id_patient_before or image_id_technique != image_id_patient_before):
        image_id_patient_before = image_files_data["current_patient"]
        image_id_tecnique_before = image_files_data["current_technique"]

        # image changed, update annotations_table_data with new data
        annotations_table_data = []
        filename = image_files_data["files"][image_files_data["current_patient"]][image_files_data["current_technique"]]
        debug_print(annotations_store_data[filename])
        for sh in annotations_store_data[filename]["shapes"]:
            annotations_table_data.append(shape_to_table_row(sh))
        return (annotations_table_data, image_files_data)
    else:
        return dash.no_update


@app.callback(
    [Output("graph", "figure"), Output("annotations-store", "data")],
    [Input("annotations-table", "data"), Input("annotation-type-dropdown", "value"),
    Input("patient_button", "value"), Input("techniques_button", "value")],
    [State("image_files", "data"), State("annotations-store", "data")],
)
def send_figure_to_graph(
    annotations_table_data, annotation_type, num_patient, num_technique, image_files_data, annotations_store
):
    if annotations_table_data is not None:
        filename = image_files_data["files"][image_files_data["current_patient"]][image_files_data["current_technique"]]
        # convert table rows to those understood by fig.update_layout
        fig_shapes = [table_row_to_shape(sh) for sh in annotations_table_data]
        debug_print("fig_shapes:", fig_shapes)
        debug_print(
            "annotations_store[%s]['shapes']:" % (filename,),
            annotations_store[filename]["shapes"],
        )
        # find the shapes that are new
        new_shapes_i = []
        old_shapes_i = []
        for i, sh in enumerate(fig_shapes):
            if not shape_in(annotations_store[filename]["shapes"])(sh):
                new_shapes_i.append(i)
            else:
                old_shapes_i.append(i)
        # add timestamps to the new shapes
        for i in new_shapes_i:
            fig_shapes[i]["timestamp"] = time_passed(annotations_store["starttime"])
        # find the old shapes and look up their timestamps
        for i in old_shapes_i:
            old_shape_i = index_of_shape(
                annotations_store[filename]["shapes"], fig_shapes[i]
            )
            fig_shapes[i]["timestamp"] = annotations_store[filename]["shapes"][
                old_shape_i
            ]["timestamp"]
        shapes = fig_shapes
        debug_print("shapes:", shapes)
        fig= px.imshow(pydicom.dcmread(filename).pixel_array, color_continuous_scale='gray')
        fig.update_layout(
            shapes=[shape_data_remove_timestamp(sh) for sh in shapes],
            # reduce space between image and graph edges
            newshape_line_color=color_dict[annotation_type],
            margin=dict(l=0, r=0, b=0, t=0, pad=4),
            dragmode="drawrect",
        )
        annotations_store[filename]["shapes"] = shapes
        print("holaaaa")
        return (fig, annotations_store)
    return dash.no_update


@app.callback(
    Output("modal", "is_open"),
    [Input("howto-open", "n_clicks"), Input("howto-close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# set the download url to the contents of the annotations-store (so they can be
# downloaded from the browser's memory)
app.clientside_callback(
    """
function(the_store_data) {
    let s = JSON.stringify(the_store_data);
    let b = new Blob([s],{type: 'text/plain'});
    let url = URL.createObjectURL(b);
    return url;
}
""",
    Output("download", "href"),
    [Input("annotations-store", "data")],
)

# click on download link via button
app.clientside_callback(
    """
function(download_button_n_clicks)
{
    let download_a=document.getElementById("download");
    download_a.click();
    return '';
}
""",
    Output("dummy", "children"),
    [Input("download-button", "n_clicks")],
)


# TODO comment the dbc link
# we use a callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server()
