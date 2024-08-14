import dash_html_components as html
import dash_bio as dashbio
from dash import dcc
from .filters import filters_to_apply

### Sidebar Layout ###
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "white",
}

### Submission Box Layout ###
SUBMISSION_BOX_STYLE = {
    "position": "fixed",
    "top": 0,
    "bottom": 0,
    "left": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

### Submission Box ###
submission_box = html.Div(
    [
        html.H3("Submit", className="display-4"),
        html.Hr(),
        html.Div(id="submission-box-content", children=[
            html.P(
            "Submit your sequence here.", className="lead"
            ),
            dcc.Textarea(
                id='submission-box',
                value='HELLO',
                style={'width': '100%', 'height': 300},
            ),
            html.Button('Submit', id='submit-button', className='btn btn-primary')
            
        ]),
        html.Hr(),
        #button to run selected filters:
        html.Button('Run Selected Filters', id='run-filters-button', className='btn btn-primary'),
    ],
    style=SUBMISSION_BOX_STYLE,
)

sidebar = html.Div(
    [
        html.H3("Suggestions", className="display-4", 
                style={
                    'font-size': 'calc(10px + 2vmin)',
                    'max-width': '100%',
                    'margin': '0'
                    }),
        html.Hr(),
        html.Div(id="sidebar-content", children=[
            html.P(
            "Suggestions will be shown here.", className="lead"
            )
        ]),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(
    #here we riffle together the toggle switches in-line with the filters
    [ html.Div([
        dcc.Checklist(
            id=f'toggle-switch-{i}',
            options=[{'label': '', 'value': 'on'}],
            value=['on'],
            labelStyle={'display': 'inline-block'},
            style={'fontSize': '20px'}
        ),
        dashbio.SequenceViewer(
            id='default-sequence-viewer-{}'.format(i),
            sequence='AAA',
            toolbar=False,
            title=filters_to_apply[i].get_title(),
            badge=False,
            charsPerLine=90,
            search=False,
        ),
    ],style={'display': 'flex', 'flexDirection': 'row'}) for i in range(len(filters_to_apply)) ] + 
    [html.Div(id='output'),
     dashbio.FornaContainer(id='my-default-forna')],
    style=CONTENT_STYLE
)

