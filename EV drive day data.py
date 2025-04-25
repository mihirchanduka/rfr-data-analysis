import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('coltrane.csv', skiprows=14, header=[0, 1])
    df.columns = [f'{name} ({unit})' if pd.notna(unit) else name for name, unit in df.columns]
    df = df.drop([0, 1])
    df = df.reset_index(drop=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    df['Wheel Speed FR (m/s)'] = df['Wheel Speed FR (km/h)'] * 0.277778

    psi_to_kpa = 900 * 6.895  #psi to kPa
    power_threshold = 15  #kW

    df['Time Difference (s)'] = df['Time (s)'].diff().fillna(0)
    df['Distance Traveled (m)'] = df['Wheel Speed FR (m/s)'] * df['Time Difference (s)']
    df['Cumulative Distance (m)'] = df['Distance Traveled (m)'].cumsum()

    fig, axs = plt.subplots(2, 2, figsize=(14, 12), constrained_layout=True)

    row_labels = df.columns
    cell_text = []
    for col in row_labels:
        cell_text.append([f"{df[col].min():.2f}", f"{df[col].max():.2f}"])
    axs[0, 0].axis('tight')
    axs[0, 0].axis('off')
    table = axs[0, 0].table(cellText=cell_text, rowLabels=row_labels, colLabels=['Min', 'Max'], loc='center')
    axs[0, 0].set_title('Min and Max Values', fontsize=14)

    plots = [
        (axs[0, 1], df['Brake Pressure Front (kPa)']/1000, df['Brake Pressure Rear (kPa)']/1000, 'Brake Pressure (1000s kPa)', 'Brake Pressure >= 900 psi (converted to kPa)'),
        (axs[1, 0], df['Engine Power (kW)'], None, 'Engine Power (kW)', 'Engine Power >= 15 kW'),
        (axs[1, 1], df['Cumulative Distance (m)'], None, 'Distance (m)', 'Cumulative Distance Traveled')
    ]

    for ax, y1, y2, ylabel, title in plots:
        ax.plot(df['Time (s)'], y1, label=y1.name, color='blue')
        if y2 is not None:
            ax.plot(df['Time (s)'], y2, label=y2.name, color='red')
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True)

    plt.show()

if __name__ == "__main__":
    main()
