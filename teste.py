import streamlit as st
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Criar DataFrame com os dados fornecidos
data = {
    'Mês': ['ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO', 'JANEIRO', 'FEVEREIRO', 'MARÇO'],
    'Total Coletado Medido (kg)': [0, 0, 0, 0, 17800, 0, 27820, 0, 0, 0, 0, 0],
    'Material Vendido (kg)': [21341, 22446, 26758, 23408, 29973, 18916, 35849, 0, 0, 0, 0, 0],
    'Receita Gerada (R$)': [14128, 14598, 16086, 15984, 18537, 13885, 18421, 0, 0, 0, 0, 0],
    'Renda por Catador (R$)': [921, 1016, 1201, 1172, 1402, 1161, 1508, 0, 0, 0, 0, 0],
    'Geração RSD/Mês (kg)': [257400, 257400, 257400, 257400, 257400, 257400, 257400, 257400, 257400, 257400, 257400, 257400],
    'Coleta Seletiva/RSD (%)': [0, 0, 0, 0, 6.92, 0, 10.81, 0, 0, 0, 0, 0],
    'Valor Pago por Quilo Material Coletado (R$)': [0, 0, 0, 0, 0.94, 0, 0.60, 0, 0, 0, 0, 0],
}

df = pd.DataFrame(data)

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div(style={'backgroundColor': '#2E8B57', 'text-align':'center', 'font-size':'24px'}, children=[
    html.H1(children='Dashboard Projeto Lixo Rico', style={'color': 'white'}),
    
    dcc.Dropdown(
        id='dropdown-mes',
        options=[{'label': mes, 'value': mes} for mes in df['Mês']],
        value=df['Mês'][0],
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    
    html.Div(children=[
        dcc.Graph(
            id='grafico-barras-receita',
            style={'backgroundColor': 'white'},
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(children=[
        dcc.Graph(
            id='grafico-barras-renda-catador',
            style={'backgroundColor': 'white'},
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(children=[
        dcc.Graph(
            id='grafico-barras-material-vendido',
            style={'backgroundColor': 'white'},
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(id='cartoes-container', style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-top': '20px'}),
])

# Atualizar os gráficos e cartões com base no mês selecionado
@app.callback(
    [Output('grafico-barras-receita', 'figure'),
     Output('grafico-barras-renda-catador', 'figure'),
     Output('grafico-barras-material-vendido', 'figure'),
     Output('cartoes-container', 'children')],
    [Input('dropdown-mes', 'value')]
)
def update_dashboard(selected_month):
    selected_month_index = df.index[df['Mês'] == selected_month].tolist()[0]

    # Gráfico de Barras - Receita Gerada
    figure_receita = {
        'data': [{'x': df['Mês'], 'y': df['Receita Gerada (R$)'], 'type': 'bar', 'name': 'Receita Gerada (R$)'}],
        'layout': {'title': f'Receita Gerada por Mês - {selected_month}', 'xaxis': {'title': 'Mês'}, 'yaxis': {'title': 'Receita Gerada (R$)'}}
    }

    # Gráfico de Barras - Renda por Catador
    figure_renda_catador = {
        'data': [{'x': df['Mês'], 'y': df['Renda por Catador (R$)'], 'type': 'bar', 'name': 'Renda por Catador (R$)'}],
        'layout': {'title': f'Renda por Catador por Mês - {selected_month}', 'xaxis': {'title': 'Mês'}, 'yaxis': {'title': 'Renda por Catador (R$)'}}
    }

    # Gráfico de Barras - Material Vendido
    figure_material_vendido = {
        'data': [{'x': df['Mês'], 'y': df['Material Vendido (kg)'], 'type': 'bar', 'name': 'Material Vendido (kg)'}],
        'layout': {'title': f'Material Vendido por Mês - {selected_month}', 'xaxis': {'title': 'Mês'}, 'yaxis': {'title': 'Material Vendido (kg)'}}
    }

    # Cartões
    cartoes = []
    if df.loc[selected_month_index, 'Valor Pago por Quilo Material Coletado (R$)'] != 0:
        cartoes.append(html.Div(id='cartao-valor-pago', children=f'Valor Pago por Quilo Material Coletado: R$ {df.loc[selected_month_index, "Valor Pago por Quilo Material Coletado (R$)"]:.2f}', style={'padding': '10px', 'background-color': 'white', 'border-radius': '10px', 'width': '300px', 'margin-bottom': '10px'}))
    if df.loc[selected_month_index, 'Coleta Seletiva/RSD (%)'] != 0:
        cartoes.append(html.Div(id='cartao-coleta-seletiva', children=f'Porcentagem Coleta Seletiva/RSD: {df.loc[selected_month_index, "Coleta Seletiva/RSD (%)"]:.2f}%', style={'padding': '10px', 'background-color': 'white', 'border-radius': '10px', 'width': '300px', 'margin-bottom': '10px'}))

    return figure_receita, figure_renda_catador, figure_material_vendido, cartoes

# Rodar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)











