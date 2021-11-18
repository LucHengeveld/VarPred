import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

app = dash.Dash(__name__)

vcf_list = []

# Saves the mutation information in a list
with open("vcf-test - kopie.vcf") as file:
    for line in file:
        if not line.startswith("#"):
            vcf_list.append(line.split("\t"))
file.close()

chrom_list = []
pos_list = []
ref_list = []
alt_list = []

# Loops through the vcf_list and saves the chromosome numbers and
# positions to a 2D list with the structure [chrom_list, pos_list]
for i in vcf_list:
    chrom_list.append(i[0])
    pos_list.append(i[1])
    ref_list.append(i[3])
    alt_list.append(i[4])
compare_list = [chrom_list, pos_list, ref_list, alt_list]

chrom_size = 248956422

x_list = []
for i in compare_list[1]:
    x_list.append(int(i))

y_list = []
for i in range(len(x_list)):
    y_list.append(0)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_list, y=y_list,
    mode='markers', marker_size=42.5, marker_symbol='line-ns',
    marker_line_color="black", marker_line_width=2
))
fig.update_xaxes(showgrid=False, fixedrange=False, range=[0, chrom_size],
                 tickfont_family="Arial Black", tickformat=',d')
fig.update_yaxes(showgrid=False, fixedrange=True,
                 zeroline=True, zerolinecolor='#04AA6D', zerolinewidth=60,
                 showticklabels=False)
fig.update_layout(height=260, plot_bgcolor='white', font_size=18)

app.layout = html.Div(children=[
    dcc.Graph(
        id='chromosome',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
