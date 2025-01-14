import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import BENCHMARK_RESULTS_URL, CLAUDE_MODEL_CARD_URL

# Set page config
st.set_page_config(
    page_title="AI Model Benchmark Comparison", page_icon="📊", layout="wide"
)

# Add title
st.title("AI Model Benchmark Comparison")


# Read the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv(BENCHMARK_RESULTS_URL)
    # Remove the 'source' column for plotting
    plot_df = df.drop("source", axis=1)
    return df, plot_df


df, plot_df = load_data()


# Function to clean percentage values
def clean_percentage(value):
    if pd.isna(value) or value == "-":
        return None
    return float(value.strip("%"))


# Process each row
for idx, row in plot_df.iterrows():
    test_name = row["name"]

    # Create data for plotting
    model_names = plot_df.columns[2:]  # Skip the test name and type columns
    values = [clean_percentage(row[col]) for col in model_names]

    # Filter out None values and create list of tuples for sorting
    valid_data = [
        (name, val) for name, val in zip(model_names, values) if val is not None
    ]
    if not valid_data:
        continue

    # Sort the data by values in descending order
    sorted_data = sorted(valid_data, key=lambda x: x[1], reverse=True)
    model_names, values = zip(*sorted_data)

    # Create bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=model_names,
                y=values,
                text=[f"{v:.1f}%" for v in values],
                textposition="auto",
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title=f"{test_name} Benchmark Results",
        xaxis_title="Models",
        yaxis_title="Score (%)",
        height=500,
        yaxis_range=[0, 100],
        xaxis_tickangle=-45,
        showlegend=False,
        margin=dict(t=50, b=100),  # Adjust margins to prevent label cutoff
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    benchmark_ref = df.loc[idx, "source"]
    source = CLAUDE_MODEL_CARD_URL
    st.markdown(f"[Benchmark]({benchmark_ref})")
    st.markdown(f"[Source]({source})")

    # Add a divider between charts
    st.divider()

# Add footer with information
st.markdown("""
---
This app visualizes performance comparisons across different AI models on various benchmarks.
Each bar represents a model's score on the given benchmark test.
""")

if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if get_script_run_ctx() is None:
        import sys

        from streamlit.web.cli import main

        sys.argv = ["streamlit", "run", __file__]
        main()
