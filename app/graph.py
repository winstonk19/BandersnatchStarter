from altair import Chart
import altair as alt
from pandas import DataFrame    

def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """
    Generate an Altair chart for visualizing relationships between features.
    """
    scatter_plot = Chart(df, title=f'{y.capitalize()} vs. {x.capitalize()}').mark_circle(size=60).encode(
        x=alt.X(x, title=f'{x.capitalize()}'),
        y=alt.Y(y, title=f'{y.capitalize()}'),
        color=alt.Color(target, legend=alt.Legend(title=f'{target.capitalize()}'),
                        scale=alt.Scale(scheme='category10')),  # Use a categorical color scheme
        tooltip=[x, y, target]
    ).properties(
        width=800,
        height=400,
        background='black',
        padding=10
    ).configure(
        background='#1E1E1E',
        axis=alt.AxisConfig(labelColor='white', titleColor='white'),
        legend=alt.LegendConfig(labelColor='white', titleColor='white')
    )
    return scatter_plot
