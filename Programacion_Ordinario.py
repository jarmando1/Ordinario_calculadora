import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import math
import matplotlib.pyplot as plt

def calcular_distancia(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calcular_area(coordenadas):
    n = len(coordenadas)
    area = 0
    for i in range(n):
        x1, y1, _ = coordenadas[i]
        x2, y2, _ = coordenadas[(i + 1) % n]
        area += (x1 * y2) - (x2 * y1)
    return abs(area) / 2

def calcular_desnivel(coordenadas):
    desnivel_total = 0
    desniveles = []
    for i in range(len(coordenadas)):
        _, _, z1 = coordenadas[i]
        _, _, z2 = coordenadas[(i + 1) % len(coordenadas)]
        desnivel = abs(z2 - z1)
        desniveles.append(desnivel)
        desnivel_total += desnivel
    return desnivel_total, desniveles

def leer_archivo_csv(ruta_csv):
    df = pd.read_csv(ruta_csv)
    coordenadas = [(x, y, z) for x, y, z in zip(df['COORDENADA X'], df['COORDENADA Y'], df['Z'])]
    return coordenadas

def plot_terreno(coordenadas, tipo_calculo):
    x, y, _ = zip(*coordenadas)
    desnivel_total, desniveles = calcular_desnivel(coordenadas)

    fig, ax = plt.subplots()

    if tipo_calculo == "Distancia":
        ax.plot(x + (x[0],), y + (y[0],), color='blue')
        plt.title(f"Representación Gráfica del Terreno (Distancia total)")
    elif tipo_calculo == "Área":
        ax.plot(x + (x[0],), y + (y[0],), color='green')
        plt.title(f"Representación Gráfica del Terreno (Área del polígono)")
    elif tipo_calculo == "Desnivel":
        colores = ['green', 'yellow', 'red']
        
        for i, desnivel in enumerate(desniveles):
            color_idx = min(int(desnivel / desnivel_total * 2), 2)
            color = colores[color_idx]
            ax.plot([x[i], x[(i + 1) % len(coordenadas)]], [y[i], y[(i + 1) % len(coordenadas)]], color=color, linewidth=2)

        plt.title(f"Representación Gráfica del Terreno (Desnivel total)")
        
        legend_labels = [f'Rango {i+1}' for i in range(3)]
        legend_handles = [plt.Line2D([0], [0], color=colores[i], linewidth=2) for i in range(3)]
        plt.legend(legend_handles, legend_labels, loc='upper right')

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.show()

def mostrar_distancia():
    global resultado, coordenadas
    distancia_total = 0
    for i in range(len(coordenadas)):
        x1, y1, _ = coordenadas[i]
        x2, y2, _ = coordenadas[(i + 1) % len(coordenadas)]
        distancia = calcular_distancia(x1, y1, x2, y2)
        distancia_total += distancia

    resultado_text = f"Distancia total: {distancia_total:.2f} metros"
    resultado.set(resultado_text)
    messagebox.showinfo("Resultado", resultado_text)

def mostrar_area():
    global resultado, coordenadas
    area = calcular_area(coordenadas)
    resultado_text = f"Área del polígono: {area:.2f} metros cuadrados"
    resultado.set(resultado_text)
    messagebox.showinfo("Resultado", resultado_text)

def mostrar_desnivel():
    global resultado, coordenadas
    desnivel_total, _ = calcular_desnivel(coordenadas)
    resultado_text = f"Desnivel total: {desnivel_total:.2f} metros"
    resultado.set(resultado_text)
    messagebox.showinfo("Resultado", resultado_text)

def mostrar_grafico():
    global coordenadas
    if not coordenadas:
        messagebox.showinfo("Error", "No se han cargado coordenadas desde el archivo CSV.")
        return

    plot_terreno(coordenadas, "Distancia")
    plot_terreno(coordenadas, "Área")
    plot_terreno(coordenadas, "Desnivel")

ventana = tk.Tk()
ventana.title("Calculadora Topográfica")

resultado = tk.StringVar()
coordenadas = leer_archivo_csv("C:\\Users\\Colibecas\\Documents\\Armando\\LOS_AMIALES_PUNTOS.csv")

button_distancia = tk.Button(ventana, text="Calcular Distancia", command=mostrar_distancia)
button_distancia.pack(side=tk.LEFT, padx=5)

button_area = tk.Button(ventana, text="Calcular Área", command=mostrar_area)
button_area.pack(side=tk.LEFT, padx=5)

button_desnivel = tk.Button(ventana, text="Calcular Desnivel", command=mostrar_desnivel)
button_desnivel.pack(side=tk.LEFT, padx=5)

button_grafico = tk.Button(ventana, text="Mostrar Gráfico", command=mostrar_grafico)
button_grafico.pack(side=tk.LEFT, padx=5)

label_resultado = tk.Label(ventana, textvariable=resultado, wraplength=400)
label_resultado.pack()

ventana.mainloop()

