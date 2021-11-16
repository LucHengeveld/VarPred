import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

app = dash.Dash(__name__)

x_list = [1, 930139, 930165, 930187, 930188, 930199, 248956422]
y_list = []
for i in range(len(x_list)):
    y_list.append(0)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_list, y=y_list,
    mode='markers', marker_size=42.5, marker_symbol='line-ns',
    marker_line_color="black", marker_line_width=2
))
fig.update_xaxes(showgrid=False, fixedrange=False,
                 tickfont_family="Arial Black", tickformat=',d')
fig.update_yaxes(showgrid=False, fixedrange=True,
                 zeroline=True, zerolinecolor='#04AA6D', zerolinewidth=60,
                 showticklabels=False)
fig.update_layout(height=260, plot_bgcolor='white', font_size=18)
# fig.show()

app.layout = html.Div(children=[
    dcc.Graph(
        id='chromosome',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
