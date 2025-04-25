import pandas as pd
import matplotlib.pyplot as plt

def load_and_prepare_data(file_path):
    #Format Data
    df = pd.read_csv(file_path, skiprows=14, header=[0, 1])
    df.columns = [f'{name} ({unit})' if pd.notna(unit) else name for name, unit in df.columns]
    df = df.drop([0, 1]).reset_index(drop=True)
    # REMOVE NaN values
    df = df.apply(pd.to_numeric, errors='coerce')
    return df

def plot_data(df):
    time = df['Time (s)']

    temp_vars = ['Eng Oil Temp (C)', 'Gbox Oil Temp (C)', 'Coolant Temperature (C)']
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 15), sharex=True)

    for i, temp in enumerate(temp_vars):
        if temp in df.columns:
            axs[i].plot(time, df[temp], label=temp)
            axs[i].set_ylabel('Temperature (°C)')
            axs[i].legend()
            axs[i].grid(True)

    axs[-1].set_xlabel('Time (s)')
    plt.suptitle('Temperature Profile Over Time')

    plt.show()

def main():
    file_path = 'April23Szymon23.csv'
    df = load_and_prepare_data(file_path)
    plot_data(df)

if __name__ == "__main__":
    main()
