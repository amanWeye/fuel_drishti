# Pre-requisites
- python3.9 or above

# Setup
- Install all dependencies from requirements.txt
```
pip install -r requirements.txt
```

# Usage
- Run using
    ```
    python vehicle_dynamic_plot.py
    ```
- Enter vehicle Id and Start/Stop time in the specified format(Epoch time is also supported)
- Select which fields to visualize from Fuel, Frequency, and Speed
- Click on plot to visualize
- Matplotlib tools are available for zoom and pan options


# Additional points
- If Vehicle list is fixed, you can enter that in vehicle_list.json with vehicle number and vehicle id and the list would be shown in the dropdown menu. Further modification can be made to fetch vehicle id from vehicle name in the window itself.
- Modifications can be made to visualize detected events on the same plot.
