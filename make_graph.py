import PyGnuplot as pg
import pandas as pd
import scipy
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Users\time8\Desktop\program\2018.10")

G_set = pd.read_csv(r"Evaluate_data\G_set.csv")
N_set = pd.read_csv(r"Evaluate_data\N_set.csv")
G_set_R = pd.read_csv(r"Evaluate_data\G_set_R.csv")
N_set_R = pd.read_csv(r"Evaluate_data\N_set_R.csv")

x_value = list(range(1, 6))
plt.title("precision")
plt.plot(x_value, G_set.iloc[:, 0], label="G_set")
plt.plot(x_value, G_set_R.iloc[:, 0], label="G_set_R")
plt.plot(x_value, N_set.iloc[:, 0], label="N_set")
plt.plot(x_value, N_set_R.iloc[:, 0], label="N_set_R")
plt.legend()

print(os.getcwd())