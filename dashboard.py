from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import plotly.express as px
import pandas as pd
import requests
import os
from datetime import date
import dash

# Configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

app = Dash(__name__, suppress_callback_exceptions=True)

# Helper for dark charts
def dark_figure(fig):
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e2e8f0'},
        margin={'t': 40, 'l': 40, 'r': 10, 'b': 40}
    )
    return fig

# Layout Components

# 1. Login Container
login_container = html.Div(id='login-container', children=[
    html.H2("Health Monitor", style={'marginBottom': '30px', 'fontWeight': 'bold'}),
    html.Div([
        html.H4("Login", style={'color': '#94a3b8', 'marginBottom': '20px'}),
        dcc.Input(id='username-box', type='text', placeholder='Username'),
        dcc.Input(id='password-box', type='password', placeholder='Password'),
        html.Button('Sign In', id='login-button', n_clicks=0, style={'width': '100%', 'marginTop': '20px'}),
    ]),
    html.Div(id='login-output', style={'marginTop': '20px', 'color': '#f87171'})
])

# 2. Dashboard Container
dashboard_container = html.Div(id='dashboard-container', style={'display': 'none'}, children=[
    
    # Header
    html.Div(className='header-section card', children=[
        html.Div([
            html.H1("Health Dashboard", style={'margin': 0, 'fontSize': '1.5rem'}),
            html.H3(id='welcome-msg', children="Welcome!", style={'margin': 0, 'color': '#94a3b8', 'fontSize': '1rem', 'fontWeight': 'normal'})
        ]),
        html.Button('Logout', id='logout-button', n_clicks=0)
    ]),
    
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    
    # Visualizations Grid
    html.Div(className='dashboard-grid', children=[
        html.Div(className='card', children=[
            dcc.Graph(id='steps-bar-chart', config={'displayModeBar': False})
        ]),
        html.Div(className='card', children=[
            dcc.Graph(id='heart-rate-line-chart', config={'displayModeBar': False})
        ]),
        html.Div(className='card', children=[
            dcc.Graph(id='activity-pie-chart', config={'displayModeBar': False})
        ]),
        html.Div(className='card', children=[
            dcc.Graph(id='goal-gauge-chart', config={'displayModeBar': False})
        ])
    ]),
    
    # Data Management Section
    html.Div(className='dashboard-grid', style={'marginTop': '20px'}, children=[
        # Log Data Card
        html.Div(className='card', children=[
            html.H3("Log Health Data"),
            html.Div(style={'display': 'grid', 'gap': '10px'}, children=[
                dcc.Input(id='input-date', type='text', placeholder='YYYY-MM-DD', value=str(date.today())),
                dcc.Input(id='input-steps', type='number', placeholder='Steps'),
                dcc.Input(id='input-calories', type='number', placeholder='Calories'),
                dcc.Input(id='input-hr', type='number', placeholder='Heart Rate'),
                html.Button('Submit Entry', id='submit-metric-btn', n_clicks=0),
            ]),
            html.Div(id='metric-status', style={'marginTop': '10px'})
        ]),
        
        # Goals Card
        html.Div(className='card', children=[
            html.H3("Update Goals"),
            html.Div(style={'display': 'grid', 'gap': '10px'}, children=[
                dcc.Dropdown(
                    id='goal-type', 
                    options=[{'label': 'Steps', 'value': 'steps'}, {'label': 'Calories', 'value': 'calories'}], 
                    value='steps',
                    style={'color': 'black'} # Dropdown needs text color override for options
                ),
                dcc.Input(id='goal-value', type='number', placeholder='Target Value'),
                html.Button('Set New Goal', id='submit-goal-btn', n_clicks=0),
            ]),
            html.Div(id='goal-status', style={'marginTop': '10px'})
        ])
    ]),

    # Table Card
    html.Div(className='card', children=[
        html.H3("Recent Activity Log"),
        dash_table.DataTable(
            id='metrics-table',
            columns=[{"name": i, "id": i} for i in ['metric_id', 'date', 'steps', 'calories', 'heart_rate']],
            data=[],
            row_deletable=True,
            page_size=10,
            style_as_list_view=True,
            style_header={'backgroundColor': 'transparent', 'fontWeight': 'bold', 'color': 'white', 'borderBottom': '1px solid white'},
            style_cell={
                'backgroundColor': 'transparent',
                'color': '#e2e8f0',
                'border': 'none',
                'padding': '10px',
                'textAlign': 'left'
            },
        ),
        html.Div(id='delete-status', style={'marginTop': '10px', 'color': '#f87171'})
    ])
])

# Main Layout
app.layout = html.Div([
    dcc.Store(id='auth-token', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    login_container,
    dashboard_container
])

# Callbacks (Logic remains mostly same, just updating chart styles)
# ... [Keeping helper functions and callbacks similar but applying dark theme to charts]

# Helpers
def get_user_info(token):
    if not token: return None
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/users/me", headers=headers)
        return response.json() if response.status_code == 200 else None
    except: return None

def fetch_data(token):
    if not token: return []
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/metrics", headers=headers, params={"limit": 100})
        return response.json() if response.status_code == 200 else []
    except: return []

def fetch_goal_progress(token):
    if not token: return []
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/goals/progress", headers=headers)
        return response.json() if response.status_code == 200 else []
    except: return []

# 1. Auth & View Management
@app.callback(
    [Output('auth-token', 'data'),
     Output('login-output', 'children'),
     Output('login-container', 'style'),
     Output('dashboard-container', 'style'),
     Output('welcome-msg', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('logout-button', 'n_clicks')],
    [State('username-box', 'value'),
     State('password-box', 'value'),
     State('auth-token', 'data')]
)
def manage_auth_and_view(login_clicks, logout_clicks, username, password, current_token):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Constants for styles
    SHOW_LOGIN = {'display': 'block'}
    HIDE_LOGIN = {'display': 'none'}
    SHOW_DASH = {'display': 'block'}
    HIDE_DASH = {'display': 'none'}

    # If logout
    if triggered_id == 'logout-button':
        return None, "", SHOW_LOGIN, HIDE_DASH, ""

    # If login attempt
    if triggered_id == 'login-button':
        if not username or not password:
             return dash.no_update, "Please enter credentials", dash.no_update, dash.no_update, dash.no_update
        try:
            res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
            if res.status_code == 200:
                token = res.json()["access_token"]
                user = get_user_info(token)
                name = user['username'] if user else "User"
                return token, "", HIDE_LOGIN, SHOW_DASH, f"Welcome, {name}!"
            else:
                return dash.no_update, "Invalid credentials", dash.no_update, dash.no_update, dash.no_update
        except:
            return dash.no_update, "Connection failed", dash.no_update, dash.no_update, dash.no_update

    # Initial Load check (persisted token)
    if current_token and not triggered_id:
         user = get_user_info(current_token)
         if user:
             return current_token, "", HIDE_LOGIN, SHOW_DASH, f"Welcome, {user['username']}!"
    
    # Default
    return dash.no_update, "", SHOW_LOGIN, HIDE_DASH, ""

# 2. Update Data & Charts & CRUD
@app.callback(
    [Output('steps-bar-chart', 'figure'),
     Output('heart-rate-line-chart', 'figure'),
     Output('activity-pie-chart', 'figure'),
     Output('goal-gauge-chart', 'figure'),
     Output('metrics-table', 'data'),
     Output('metric-status', 'children'),
     Output('goal-status', 'children'),
     Output('delete-status', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('auth-token', 'data'),
     Input('submit-metric-btn', 'n_clicks'),
     Input('submit-goal-btn', 'n_clicks'),
     Input('metrics-table', 'data_previous')],
    [State('input-date', 'value'),
     State('input-steps', 'value'),
     State('input-calories', 'value'),
     State('input-hr', 'value'),
     State('goal-type', 'value'),
     State('goal-value', 'value'),
     State('metrics-table', 'data')]
)
def update_dashboard_actions(n, token, sub_met, sub_goal, table_prev, date_val, steps, calories, hr, goal_type, goal_val, table_curr):
    if not token:
        e = dark_figure(px.bar(title="Waiting for Login..."))
        return e, e, e, e, [], "", "", ""

    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    stat_met, stat_goal, stat_del = "", "", ""

    # CRUD ACTIONS (Same logic as before)
    if trigger == 'submit-metric-btn' and steps:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"date": date_val or str(date.today()), "steps": int(steps), "calories": float(calories or 0), "heart_rate": int(hr or 0)}
            try: requests.post(f"{API_URL}/metrics", json=payload, headers=headers)
            except: pass
            stat_met = "Entry Added"
        except: stat_met = "Error"
    
    if trigger == 'submit-goal-btn' and goal_val:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"metric_type": goal_type, "target_value": int(goal_val)}
            try: requests.post(f"{API_URL}/goals", json=payload, headers=headers)
            except: pass
            stat_goal = "Goal Set"
        except: stat_goal = "Error"

    if trigger == 'metrics-table' and table_prev:
        if table_curr is None: table_curr = []
        prev = {r['metric_id'] for r in table_prev}
        curr = {r['metric_id'] for r in table_curr}
        diff = prev - curr
        for mid in diff:
            try: requests.delete(f"{API_URL}/metrics/{mid}", headers={"Authorization": f"Bearer {token}"})
            except: pass

    # FETCH DATA
    data = fetch_data(token)
    goals = fetch_goal_progress(token)

    if not data:
        e = dark_figure(px.bar(title="No Data Logged"))
        return e, e, e, e, [], stat_met, stat_goal, stat_del

    df = pd.DataFrame(data)

    # 1. Bar Chart
    fig_steps = dark_figure(px.bar(df, x='date', y='steps', title='Daily Steps'))
    fig_steps.update_traces(marker_color='#3b82f6')

    # 2. Line Chart
    fig_hr = dark_figure(px.line(df, x='date', y='heart_rate', title='Heart Rate'))
    fig_hr.update_traces(line_color='#f472b6', line_width=3)

    # 3. Pie Chart
    def cat_act(s): return "Low" if s<5000 else "Medium" if s<8000 else "High"
    df['Activity'] = df['steps'].apply(cat_act)
    ac = df['Activity'].value_counts().reset_index()
    ac.columns = ['Activity', 'Count']
    fig_pie = dark_figure(px.pie(ac, values='Count', names='Activity', title='Activity Distribution', color_discrete_sequence=px.colors.sequential.RdBu))

    # 4. Gauge
    import plotly.graph_objects as go
    g_step = next((g for g in goals if g['metric_type'] == 'steps'), None)
    if g_step:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = g_step['current_value'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Steps Goal", 'font': {'color': 'white'}},
            delta = {'reference': g_step['target_value'], 'primary': {'color': 'white'}},
            gauge = {
                'axis': {'range': [None, max(g_step['target_value'], g_step['current_value']*1.1)]},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, g_step['target_value']], 'color': "rgba(255, 255, 255, 0.1)"}],
                'threshold': {'line': {'color': "#f472b6", 'width': 4}, 'thickness': 0.75, 'value': g_step['target_value']}
            }
        ))
        fig_gauge = dark_figure(fig_gauge)
    else:
        fig_gauge = dark_figure(px.bar(title="No Steps Goal"))

    table_data = df.sort_values(by='date', ascending=False).to_dict('records')

    return fig_steps, fig_hr, fig_pie, fig_gauge, table_data, stat_met, stat_goal, stat_del

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
