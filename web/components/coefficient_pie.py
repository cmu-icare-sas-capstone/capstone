# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 20:20:05 2022

@author: mengy
"""

from l2.models.LR1 import model as lr
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# @st.cache
def plot_pie():
    lr_model, X_train, y_train, X_test, y_pred, lr_features= lr()
    total_coefficnet = lr_model.score(X_train, y_train)
    coefficient_array = lr_model.coef_
    intercept = lr_model.intercept_
    labels = lr_features
    values = [abs(i) for i in coefficient_array]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='Coefficients of LR model')
    st.plotly_chart(fig)


def main():
    plot_pie()

    
