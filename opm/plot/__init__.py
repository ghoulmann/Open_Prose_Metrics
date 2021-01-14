import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py

def spline(yseries, title):

    trace = go.Scatter(y = yseries, mode = 'line+markers', fill = 'tonexty', name = title, line=dict(shape='spline', smoothing=1.3))

    layout = go.Layout(xaxis=dict(autorange=True), yaxis=dict(autorange=True))

    fig = go.Figure(data=trace, layout=layout)

    offline.plot(fig, image='png', auto_open=False, image_filename='plot_image', output_type='file', filename='temp-plot.html', validate=False)
