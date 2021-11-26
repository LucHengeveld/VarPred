import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

app = dash.Dash(__name__)

vcf_list = []

# Saves the mutation information in a list
with open("vcf-test.vcf") as file:
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

print(compare_list)

x_list = []
pos_list = []
position_dict = {}

for i in range(len(compare_list[0])):
    if i == 0:
        pos_list.append(compare_list[1][i])

    elif compare_list[0][i] == compare_list[0][i-1]:
        pos_list.append(compare_list[1][i])
        if compare_list[1][i] == compare_list[1][-1]:
            position_dict[compare_list[0][i]] = pos_list

    elif compare_list[0][i] != compare_list[0][i-1]:
        position_dict[compare_list[0][i-1]] = pos_list
        pos_list = [compare_list[1][i]]
        if compare_list[1][i] == compare_list[1][-1]:
            position_dict[compare_list[0][i]] = pos_list

print(pos_list)
print(position_dict)