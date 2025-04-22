import pandas as pd
import plotext as plt

def plot_sensor_data(csv_path, max_points=60):
    """
    Reads the sensor data CSV file and plots all available sensor data.
    
    Args:
        csv_path (str): Path to the CSV file.
        max_points (int): Max number of data points to show (rolling window).
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path, parse_dates= [0], dayfirst=True)

        # Make sure we have enough data to plot
        if df.empty or df.shape[1] < 2:
            print("No sensor data to plot.")
            return

        # Limit to the last `max_points` rows
        df = df.tail(max_points)

        # Convert timestamp to use as x-Axis
        
        plt.date_form(input_form='d/m/Y H:M:S', output_form='d/m/Y H:M:S')
        
        #time_labels = df["timestamp"].dt.strftime('%H:%M:%S').tolist()
        time_labels= plt.datetimes_to_string(df["timestamp"])
        
        # Clear previous plot
        plt.clear_figure()
        plt.title("Live Sensor Data")
        plt.xlabel("Time")

        # Plot each sensor
        plt.date_form('d/m/Y H:M:S')
        
        for col in df.columns[1:]:
            if col=="pressure":
                plt.plot(time_labels, df[col], label=col, yside="right")  
            else: 
                plt.plot(time_labels, df[col], label=col, yside="left")  
                
        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("white")
        plt.show()
    except Exception as e:
        print(f"Plotting error: {e}")