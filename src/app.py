import streamlit as st
import pandas as pd

epoch_url = "https://epoch.ai/data/llm_benchmark_accuracies.csv"

df = pd.read_csv(epoch_url)

df