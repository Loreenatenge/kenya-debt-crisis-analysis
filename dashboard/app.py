import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

st.set_page_config(page_title="Kenya Debt Crisis Analysis", layout="wide")

df = pd.read_csv("data/cleaned/kenya_debt.csv")