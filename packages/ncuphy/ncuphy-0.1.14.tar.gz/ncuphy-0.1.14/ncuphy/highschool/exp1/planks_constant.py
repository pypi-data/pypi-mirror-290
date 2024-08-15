from scipy.constants import c, e
from iminuit import Minuit
from iminuit.cost import LeastSquares
import matplotlib.pyplot as plt 
import numpy as np
from ..library import array


frequency = [int(c/632E-9), int(c/628E-9), int(c/519E-9), int(c/462E-9)]


def model(frequency, m, c):
    return (m / e) * frequency - c


def plot(frequency, voltage, error, filename="plot.png"):
    fontsize = 14
    
    plt.figure(figsize=(8, 6), dpi=300)
    plt.errorbar(frequency, voltage, yerr=error, fmt='o', label='Data', color='black')
    plt.xlabel("Frequency $(Hz)$", fontsize=fontsize)
    plt.ylabel("Voltage $(V)$", fontsize=fontsize)
    plt.grid()
    plt.savefig(filename)
    plt.clf()
    
    
def fit(frequency, voltage, error, m=1, c=0, filename="fit.png", eV=False):
    fontsize = 14
    
    frequency = np.array(frequency)
    voltage = np.array(voltage)
    error = np.array(error)
    
    ls = LeastSquares(frequency, voltage, error, model)
    m = Minuit(ls, m=m, c=c)
    m.migrad()
    m.hesse()
    
    fit_info = []
    parameters = ["Plank's Constant".ljust(24), "Heat Energy Contribution".ljust(24)]
    units = ["Js", "eV"]
    for p, v, e, u in zip(parameters, m.values, m.errors, units):
        fit_info.append(f"{p} = ${v:.2E} \\pm {e:.1E}$ {u}")

    
    plt.figure(figsize=(8, 6), dpi=300)
    plt.rcParams.update({"font.family": "monospace"})
    
    plt.errorbar(frequency, voltage, yerr=error, fmt='o', label='Data', color='black')
    plt.plot(frequency,  model(frequency, *m._values), label='Fit', color='grey', linestyle='--')
    
    if eV:
        plt.ylabel("Energy $(eV)$", fontsize=fontsize)
    else:
        plt.ylabel("Voltage $(V)$", fontsize=fontsize)
        
    plt.xlabel("Frequency $(Hz)$", fontsize=fontsize)
    plt.legend(title="\n".join(fit_info), fontsize=fontsize, title_fontsize=fontsize, frameon=False)
    
    plt.grid()
    plt.tick_params(axis='both', which='major', labelsize=fontsize, direction='in')
    plt.savefig(filename)
    plt.clf()
    
    