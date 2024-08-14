from typing import List
import dash_bootstrap_components as dbc
import dash
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from termcolor import cprint
import pandas as pd
from model import read_csv_with_metadata, get_bt_result_file_name



df_performance  = ''
df_para         = ''

def plot_all(df_list: List[pd.DataFrame]):
    fig = go.Figure()
    for df in df_list:
        fig.add_trace(go.Scatter(
            x       = df['datetime'], 
            y       = df['nav'], 
            mode    = 'lines', 
            name    = 'nav',
            line    = {'width': 2},
            customdata = [df.attrs['ref_tag']] * len(df),
            text    =   f'Ref: {df.attrs["ref_tag"]} <br>' +
                        f'total_trades: {df.attrs["performace_report"]["number_of_trades"]} <br>' +
                        f'win_rate: {df.attrs["performace_report"]["win_rate"]:.2f} <br>' +
                        f'total_cost: {df.attrs["performace_report"]["total_cost"]:,.2f} <br>' +
                        f'pnl $: {df.attrs["performace_report"]["pnl_trading"]:,.2f} <br>' +
                        f'roi %: {df.attrs["performace_report"]["roi_trading"]:.2%} <br>' +
                        f'mdd $: {df.attrs["performace_report"]["mdd_dollar_trading"]:,.2f} <br>' +
                        f'mdd %: {df.attrs["performace_report"]["mdd_pct_trading"]:.2%} <br>' +
                        f'roi(trading-B&H) %: {(df.attrs["performace_report"]["roi_trading"]-df.attrs["performace_report"]["roi_bah"]):.2%} <br>' +
                        f'mdd(trading-B&H) %: {(df.attrs["performace_report"]["mdd_pct_trading"]-df.attrs["performace_report"]["mdd_pct_bah"]):.2%} <br>',
            hoverinfo='text',
        ))

    fig.update_layout(
        height=None,
        showlegend=False,
        hovermode='closest',
        paper_bgcolor='#F8EDE3',
    )

    return fig

def plot_app(df_list: List[pd.DataFrame]):
    fig = plot_all(df_list)
    
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dash.dcc.Graph(figure=fig)



    app.run(debug=True)


if __name__ == "__main__":
    bt_result_file_names = get_bt_result_file_name('HSI')
    df_bt_result_list = [read_csv_with_metadata(file_name) for file_name in bt_result_file_names]
    plot_app(df_bt_result_list)

