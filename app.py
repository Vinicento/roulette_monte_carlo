from flask import Flask, render_template, request
import plotly.graph_objects as go
import numpy as np
import simulations
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_div = None
    strategy_type = request.form.get('strategy_type', 'paroli_strategy')
    betting_type = request.form.get('betting_type',
                                    '1')  # Ensure this is a string, since HTML option values are strings
    scenario_numbers = request.form.get('scenario_numbers', '1')

    sequence_lenght = request.form.get('sequence_lenght', '20')

    max_break = 0
    average_break = 0
    max_profit = 0
    average_profit = 0
    if request.method == 'POST':
        simulator = simulations.Roulette_Monte_Carlo()
        curve, statistics = simulator.simulate_games(strategy_type, int(scenario_numbers), int(betting_type),
                                                     int(sequence_lenght))

        max_break = statistics[0]
        average_break = statistics[1]
        max_profit = statistics[2]
        average_profit = statistics[3]

        if curve is not None:
            plot_div = generate_plot(curve)

    return render_template('roulette_simulator.html', plot_div=plot_div,
                                  strategy_type=strategy_type,
                                  betting_type=betting_type,
                                  scenario_numbers=scenario_numbers,sequence_lenght=sequence_lenght,
                                  max_break=max_break,average_break=average_break,max_profit=max_profit,
                                  average_profit=average_profit)



def generate_plot(curves):
    fig = go.Figure()

    final_profit_color = '#26a69a'
    max_drawdown_color = '#ef5350'
    text_color = '#eceff1'
    background_color = '#263238'
    grid_color = '#37474f'

    for i in curves:
        fig.add_trace(go.Scatter(y=i, mode='lines', name='Profit Curve',
                                 ))

    fig.add_hline(y=0, line=dict(color=grid_color, width=3, dash='dash'))



    fig.update_layout(
        xaxis_title="Number of Bets",
        yaxis_title="Profit",
        margin=dict(l=20, r=20, t=25, b=80),  # Adjusted bottom margin to accommodate annotation
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        font=dict(color=text_color),
        xaxis=dict(showgrid=True, gridcolor=grid_color, title_standoff=25),  # Standoff to avoid overlap
        yaxis=dict(showgrid=True, gridcolor=grid_color),
        showlegend=False,
        height = 400  # Increase the height of the plot (default is usually around 400-500)

    )


    return fig.to_html(full_html=False)





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
