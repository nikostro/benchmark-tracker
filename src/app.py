import pandas as pd
import plotly.express as px
import streamlit as st

epoch_url = "https://epoch.ai/data/llm_benchmark_accuracies.csv"

df = pd.read_csv(epoch_url)

gpqa_label = "GPQA (Diamond Set)"
gpqa_df = df[df["Benchmark"] == gpqa_label]

# Group by model name
grouped_df = (
    df.groupby("Name")
    .agg(
        {
            "Release date": "max",
            "Training compute (FLOP)": "mean",
            "Accuracy": "mean",
        }
    )
    .reset_index()
)

# Convert release date to datetime
grouped_df["Release date"] = pd.to_datetime(grouped_df["Release date"])

# Create plot with plotly express (works great with Streamlit)
fig = px.scatter(
    grouped_df,
    x="Release date",
    y="Accuracy",
    text="Name",
    title=f"Model Performance Over Time for {gpqa_label}",
)

# Customize layout
fig.update_traces(textposition="top center")
fig.update_layout(xaxis_title="Release Date", yaxis_title="Accuracy")

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Optionally show the data table below
st.dataframe(grouped_df)

st.write(gpqa_df)

if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if get_script_run_ctx() is None:
        import sys

        from streamlit.web.cli import main

        sys.argv = ["streamlit", "run", __file__]
        main()
