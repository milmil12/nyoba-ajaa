# -*- coding: utf-8 -*-


# Import libraries yang digunakan


import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.io import show, output_notebook, push_notebook, curdoc

from bokeh.models import Quad, ColumnDataSource, HoverTool, CategoricalColorMapper, Panel, CustomJS, Dropdown, Select
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16, Spectral4

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

data = pd.read_csv('./data/world-happiness-report.csv')
data = data.rename(columns = lambda x : x.replace(' ','_'))
data = data.dropna().reset_index(drop = True)
data.columns = data.columns.str.lower()


available_countries = list(data.country_name.unique())

col_list = list(data.columns)

# To make a dataset ColumnDataSource to work with bokeh
def make_dataset(country_list, feature):

    
    xs = []
    ys = []
    colors = []
    labels = []

    for i, country in enumerate(country_list):

        df = data[data['country_name'] == country].reset_index(drop = True)
        
        x = list(df['year'])
        y = list(df[feature])
        
        xs.append(list(x))
        ys.append(list(y))

        colors.append(Category20_16[i])
        labels.append(country)

    new_src = ColumnDataSource(data={'x': xs, 'y': ys, 'color': colors, 'label': labels})

    return new_src

#Functiuon to make the plot from the data obtained/updated at each selection in the ColumnDataSource
def make_plot(src, feature):
    
    p = figure(plot_width = 700, plot_height = 400, 
            title = 'Progressions of factors defining the happiness of a nation year-wise',
            x_axis_label = 'Year', y_axis_label = 'Feature Selected')

    p.multi_line('x', 'y', color = 'color', legend_field = 'label', line_width = 2, source = src)

    return p

#Function to update the ColumnDataSource instance whenever new countries are selected in the app.
def update_country(attr, old, new):
    countries_to_plot = [country_selection.labels[i] for i in country_selection.active]

    
    new_src = make_dataset(countries_to_plot, feature_select.value)

    src.data.update(new_src.data)

#Function to update the ColumnDataSource instance whenever the feature to be plotted is selected.
def update_feature(attr, old, new):
    countries_to_plot = [country_selection.labels[i] for i in country_selection.active]
    
    feature = feature_select.value
    
    new_src = make_dataset(countries_to_plot, feature)

    src.data.update(new_src.data)

#Check boxes which help us in selecting the country
country_selection = CheckboxGroup(labels=available_countries, active = [0])
country_selection.on_change('active', update_country)

#range_select = RangeSlider(start = 2005, end = 2021, value = (2005,2020), step = 1, title = 'Years')
#range_select.on_change('value', update_country)

#Drop down list to select the feature which needs to be plotted for the countries
feature_select = Select(options = col_list[2:], value = 'life_ladder', title = 'Feature Select')
feature_select.on_change('value', update_feature)

#Default countries which are activated to be displayed on the graph.
initial_country = [country_selection.labels[i] for i in country_selection.active]

#Make default ColumnDataSource instance
src = make_dataset(initial_country, feature_select.value)

#Plot the default data
p = make_plot(src, feature_select.value)

# Put controls in a single element
controls = WidgetBox(feature_select, country_selection)

# Create a row layout
layout = row(controls, p)

#Adding the layout to the current document
curdoc().add_root(layout)
