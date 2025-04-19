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
        df = pd.read_csv(f"data/{csv_path}")

        # Make sure we have enough data to plot
        if df.empty or df.shape[1] < 2:
            print("No sensor data to plot.")
            return

        # Limit to the last `max_points` rows
        df = df.tail(max_points)

        # Convert timestamp to string or readable format (optional)
        time_col = df.columns[0]
        x = df[time_col].astype(str).str[-8:].tolist() # Last 8 chars (like HH:MM:SS)

        # Clear previous plot
        plt.clear_figure()
        plt.title("Live Sensor Data")
        plt.xlabel("Time")

        # Plot each sensor
        for col in df.columns[1:]:
            plt.plot(x, df[col], label=col)

        plt.canvas_color("black")
        plt.axes_color("black")
        plt.ticks_color("white")
        plt.legend(loc="upper right")
        plt.show()
    except Exception as e:
        print(f"Plotting error: {e}")