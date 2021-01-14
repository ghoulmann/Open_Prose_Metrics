import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py

def spline(yseries, annotations, title):

    trace = go.Scatter(y = yseries, mode = 'line+markers', fill = 'tonexty', text = annotations, name = title, line=dict(shape='spline', smoothing=1.3))


    data = [trace]

    layout = go.Layout(xaxis=dict(autorange=True), yaxis=dict(autorange=True), height='50%')

    fig = go.Figure(data=data, layout=layout)

    #return offline.plot(fig, image='png', auto_open=False, image_filename='plot_image', output_type='file', filename='temp-plot.html', validate=False)
    div = offline.plot(fig, auto_open=False, image_filename='plot_image', validate=True, include_plotlyjs=True, show_link=False, output_type='div')



    return div

def bar_h(yseries, xseries):
    trace0 = go.Bar(orientation = 'h', x=xseries, y=yseries)
    layout = go.Layout(height='50%', title='Readability Scores', xaxis=dict(
        title='Grade Level',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        )), yaxis=dict(dict(
        title=False,
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'))))
    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    div = offline.plot(fig, auto_open=False, validate=True, include_plotlyjs=True, show_link=False, output_type='div')

    return div
