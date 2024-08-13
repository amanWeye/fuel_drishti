import matplotlib.dates as mdates
import mplcursors
from datetime import datetime
from helper.fetch_apis import fetch_raw_data
import matplotlib.pyplot as plt
import json

def read_json_as_dict(file_path) -> dict:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return {}

def plot_graph(id, start_time, end_time, show_fuel, show_frequency, show_speed):
    try:
        json_data = fetch_raw_data(vehicleId=id, fromTime=start_time, toTime=end_time)
        if 'data' not in json_data or 'rowData' not in json_data['data']:
            raise ValueError("Invalid data format received from API")

        row_data = json_data['data']['rowData']

        times = [datetime.fromtimestamp(item['time']) for item in row_data]
        fuel = [item['value'] for item in row_data]
        frequency = [item['frequency'] for item in row_data]
        speed = [item['speed'] for item in row_data]

        fig, ax1 = plt.subplots()

        if show_frequency:
            ax1.plot(times, frequency, marker='o', label='Frequency', color='blue')
            ax1.set_xlabel("Time")
            ax1.set_ylabel("Frequency", color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
            ax2 = ax1.twinx()
        else:
            ax2 = None

        if show_fuel or show_speed:
            if ax2 is None:
                if show_fuel:
                    ax1.plot(times, fuel, marker='o', label='Fuel', color='red')
                    ax1.set_ylabel("Fuel", color='red')
                    ax1.tick_params(axis='y', labelcolor='red')
                if show_speed:
                    ax1.plot(times, speed, marker='o', label='Speed', color='green')
                    ax1.set_ylabel("Speed", color='green')
                    ax1.tick_params(axis='y', labelcolor='green')
                ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
            else:
                if show_fuel:
                    ax2.plot(times, fuel, marker='o', label='Fuel', color='red')
                    ax2.set_ylabel("Fuel", color='red')
                    ax2.tick_params(axis='y', labelcolor='red')
                if show_speed:
                    ax2.plot(times, speed, marker='o', label='Speed', color='green')
                    ax2.set_ylabel("Speed", color='green')
                    ax2.tick_params(axis='y', labelcolor='green')
                ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
                ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3)

        fig.tight_layout()

        cursor = mplcursors.cursor([*ax1.lines, *ax2.lines] if ax2 else ax1.lines, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            try:
                index = int(sel.target.index)
                if 0 <= index < len(times):
                    time_str = times[index].strftime("%Y-%m-%d %H:%M:%S")
                    info = f"Time: {time_str}\n"
                    if show_frequency and len(frequency) > index:
                        info += f"Frequency: {frequency[index]}\n"
                    if show_fuel and len(fuel) > index:
                        info += f"Fuel: {fuel[index]}\n"
                    if show_speed and len(speed) > index:
                        info += f"Speed: {speed[index]}\n"
                    sel.annotation.set(text=info, bbox=dict(facecolor='white', alpha=0.8))
            except IndexError:
                pass

        return fig
    except Exception as e:
        raise ValueError(f"Error processing data: {e}")
