import plotly.plotly as plty
import plotly.graph_objs as go
from get_server_data import get_table_for_variable
flow_df = get_table_for_variable('1')

trace = go.Scatter(x=flow_df.index, y=flow_df['Value'])
data = [trace]

url = plty.plot(data, filename='flow data at storm drain')

