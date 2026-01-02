# src/plotting.py
import plotly.graph_objects as go
import plotly.express as px

# ---------- dark sequential palettes ----------
DARK_SEQUENTIAL = ["#FFD166", "#06D6A0", "#118AB2", "#073B4C", "#EF476F"]
DARK_EARTH = [
    [0.0, "#0D1B2A"], [0.2, "#1B263B"], [0.4, "#415A77"],
    [0.6, "#778DA9"], [0.8, "#E0E1DD"], [1.0, "#F4D35E"]
]
FONT_HIGH   = dict(family="Segoe UI", size=14, color="#F4F4F4")
TITLE_FONT  = dict(family="Segoe UI", size=20, color="#FFD166")

def _update_layout(fig):
    fig.update_layout(font=FONT_HIGH, title_font=TITLE_FONT,
                      margin=dict(l=20, r=20, t=60, b=40),
                      paper_bgcolor="#0D1B2A", plot_bgcolor="#1B263B",
                      xaxis_gridcolor="#415A77", yaxis_gridcolor="#415A77",
                      xaxis_tickfont=FONT_HIGH, yaxis_tickfont=FONT_HIGH)
    return fig

def generate_bar_plot(data, info):
    switch, grp_by = list(info['grouping'].keys())[0], list(info['grouping'].values())[0]
    _x, _y = info['x'], grp_by if switch else info['y']
    y_lab = 'Categories' if 'Category' in _y else _y.split('_')[0] + 's'
    title = f"{'Top' if info['Top'] else 'Least'} 10 {y_lab} by {_x}"
    fig = px.bar(data, x=_x, y=_y, orientation='h', color=_x, color_continuous_scale=DARK_EARTH,
                 text=_x, template="plotly_white")
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside', marker_line_width=0)
    fig.update_layout(title=title, xaxis_title=_x, yaxis_title=y_lab, coloraxis_showscale=False)
    return _update_layout(fig)

def generate_heatmap(data, info):
    switch, grp_by = list(info['grouping'].keys())[0], list(info['grouping'].values())[0]
    _y, _x = info['x'], grp_by if switch else info['y']
    title = f"{_y} across {_x} groups"
    z = data.pivot_table(values=_y, index=data.index, columns=_x, aggfunc='sum', fill_value=0)
    fig = px.imshow(z, aspect="auto", color_continuous_scale=DARK_EARTH,
                    text_auto=".0f", template="plotly_white")
    fig.update_layout(title=title, xaxis_title=_x, yaxis_title=_y)
    return _update_layout(fig)

def generate_line_plot(data, tokens):
    _x, _y = 'Pub_Date', tokens['_by']
    channel = tokens['channel']
    category = (data['Category_Title'].mode().iloc[0]
                if 'Category_Title' in data.columns and not data['Category_Title'].isna().all()
                else 'Unknown')
    title = (f"{channel} – {_y} over time<br>"
             f"<sub style='font-size:14px;font-weight:300;'>Dominant category: {category}</sub>")
    fig = px.line(data, x=_x, y=_y, markers=True, template="plotly_white",
                  line_shape='spline', color_discrete_sequence=DARK_SEQUENTIAL,
                  hover_data={'Category_Title': True} if 'Category_Title' in data.columns else None)
    fig.update_traces(line_width=2.5, marker_size=5,
                      hovertemplate='<b>%{x}</b><br>' +
                                    f'{_y}: ' + '%{y:,.0f}<br>' +
                                    'Category: %{customdata[0]}<extra></extra>')
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title=_y)
    return _update_layout(fig)

def generate_boxplot(data, _by=None):
    if _by is None:
        _by = ['Views', 'Likes', 'Dislikes', 'Comments']
    fig = px.box(data, y=_by, template="plotly_white",
                 color_discrete_sequence=DARK_SEQUENTIAL)
    fig.update_layout(title="Distribution of Key Metrics",
                      xaxis_title="Metric", yaxis_title="Values")
    return _update_layout(fig)