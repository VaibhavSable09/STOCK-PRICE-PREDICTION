import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class StockVisualizer:
    @staticmethod
    def create_stock_chart(data, predictions=None):
        """Create an interactive stock price chart with optional predictions"""
        fig = make_subplots(rows=2, cols=1, 
                           shared_xaxes=True,
                           vertical_spacing=0.03,
                           row_heights=[0.7, 0.3])

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )

        # Add predictions if available
        if predictions is not None:
            fig.add_trace(
                go.Scatter(
                    x=predictions.index,
                    y=predictions.values,
                    mode='lines',
                    name='Predicted',
                    line=dict(color='#2E7D32', dash='dash'),
                ),
                row=1, col=1
            )

        # Volume bar chart
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color='rgba(30, 136, 229, 0.5)'
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            title_text="Stock Price & Volume Chart with Predictions",
            xaxis_rangeslider_visible=False,
            height=800,
            template="plotly",  # Changed to light theme
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            margin=dict(l=50, r=50, t=50, b=50),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Update axes for better visibility in light theme
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')

        return fig