import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import time
from datetime import datetime
from plot_fuel import plot_graph, read_json_as_dict  # Import plot_graph and vehicle_data

def detect_time_format(time_str):
    try:
        # Try parsing as epoch (integer)
        int(time_str)
        return 'epoch'
    except ValueError:
        # If parsing fails, assume it's in datetime string format
        return 'datetime'

def convert_to_epoch(time_str):
    if detect_time_format(time_str) == 'epoch':
        return int(time_str)
    else:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())

def on_plot_button_click():
    global canvas, toolbar  # Declare canvas and toolbar as global
    selected_vehicle = vehicle_dropdown.get()
    custom_vehicle_id = custom_vehicle_entry.get()
    start_time_str = start_time_entry.get()
    end_time_str = end_time_entry.get()

    # Handle custom vehicle ID
    if custom_vehicle_id:
        vehicle_id = custom_vehicle_id
    else:
        vehicle_id = vehicle_data.get(selected_vehicle)

    # Convert time strings to epoch
    try:
        start_time = convert_to_epoch(start_time_str)
        end_time = convert_to_epoch(end_time_str)
    except ValueError:
        print("Invalid date-time format. Please use 'YYYY-MM-DD HH:MM:SS' or epoch time.")
        return

    print(f"Selected vehicle ID: {vehicle_id}")
    try:
        fig = plot_graph(
            id=vehicle_id,
            start_time=start_time,
            end_time=end_time,
            show_fuel=show_fuel.get(),
            show_frequency=show_frequency.get(),
            show_speed=show_speed.get()
        )
        if canvas.get_tk_widget() is not None:
            canvas.get_tk_widget().destroy()  # Remove old canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Remove old toolbar if exists
        if hasattr(on_plot_button_click, 'toolbar'):
            on_plot_button_click.toolbar.pack_forget()
            on_plot_button_click.toolbar.destroy()

        # Add toolbar for interactive features
        on_plot_button_click.toolbar = NavigationToolbar2Tk(canvas, root)
        on_plot_button_click.toolbar.update()
        on_plot_button_click.toolbar.pack()

    except ValueError as e:
        print(f"Error: {e}")

def on_close():
    print("Closing the application...")
    if canvas.get_tk_widget() is not None:
        canvas.get_tk_widget().destroy()  # Clean up the canvas
    root.quit()  # Stop the Tkinter main loop
    root.destroy()  # Destroy the Tkinter root window

def on_vehicle_change(event):
    # Trigger plot update when the vehicle is changed
    on_plot_button_click()

# Create the main window
root = tk.Tk()
root.title("Vehicle Data Plotter")

# Read Default vehicle list
vehicle_data = read_json_as_dict("vehicle_list.json")

# Create a dropdown menu
vehicle_dropdown = ttk.Combobox(root, values=list(vehicle_data.keys()))
vehicle_dropdown.bind("<<ComboboxSelected>>", on_vehicle_change)
vehicle_dropdown.pack(padx=10, pady=10)

# Create an entry field for custom vehicle ID
tk.Label(root, text="Custom Vehicle ID (leave blank to use dropdown selection)").pack(padx=10, pady=5)
custom_vehicle_entry = tk.Entry(root)
custom_vehicle_entry.pack(padx=10, pady=5)

# Create checkboxes for data selection
show_fuel = tk.BooleanVar(value=True)
show_frequency = tk.BooleanVar(value=True)
show_speed = tk.BooleanVar(value=True)

fuel_checkbox = tk.Checkbutton(root, text="Show Fuel", variable=show_fuel)
fuel_checkbox.pack()

frequency_checkbox = tk.Checkbutton(root, text="Show Frequency", variable=show_frequency)
frequency_checkbox.pack()

speed_checkbox = tk.Checkbutton(root, text="Show Speed", variable=show_speed)
speed_checkbox.pack()

# Time input fields
tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM:SS or epoch)").pack(padx=10, pady=5)
start_time_entry = tk.Entry(root)
start_time_entry.pack(padx=10, pady=5)

tk.Label(root, text="End Time (YYYY-MM-DD HH:MM:SS or epoch)").pack(padx=10, pady=5)
end_time_entry = tk.Entry(root)
end_time_entry.pack(padx=10, pady=5)

# Create a plot button
plot_button = tk.Button(root, text="Plot", command=on_plot_button_click)
plot_button.pack(pady=10)

# Sample time values
epoch_now = int(time.time())
epoch_one_day_ago = epoch_now - 86400

# Set default values for start and end time in entry fields
start_time_entry.insert(0, datetime.fromtimestamp(epoch_one_day_ago).strftime("%Y-%m-%d %H:%M:%S"))
end_time_entry.insert(0, datetime.fromtimestamp(epoch_now).strftime("%Y-%m-%d %H:%M:%S"))

# Initial plot
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
