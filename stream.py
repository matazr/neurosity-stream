import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
import numpy as np
import mne

# Define the corrected channel names and types (assuming all EEG data)
channel_names = ['CP3', 'C3', 'F5', 'PO3', 'PO4', 'F6', 'C4', 'CP4']
channel_types = ['eeg'] * len(channel_names)
sfreq = 256  # Neurosity Crown sampling rate (256 Hz)

# Create MNE info object to store channel metadata
info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=channel_types)

# Resolve EEG streams (Neurosity Crown stream should be available via LSL)
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Initialize buffer for real-time plotting (5 seconds of data)
buffer_size = sfreq * 5  # Collecting 5 seconds of data
data_buffer = np.zeros((len(channel_names), buffer_size))  # Buffer to store data
current_index = 0  # Initialize current index

# Set up the real-time plot using Matplotlib
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

# Time axis: from -5 seconds to 0 (i.e., 5 seconds of data)
time_axis = np.linspace(-5, 0, buffer_size)

# Initialize lines for each channel in the plot
lines = [ax.plot(time_axis, data_buffer[i])[0] for i in range(len(channel_names))]

# Set plot limits and labels
ax.set_xlim(-5, 0)  # Time range from -5 to 0 seconds
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude (µV)')
ax.set_title('Real-Time EEG Data from Neurosity Crown')

plt.show()

# Start receiving and plotting data with dynamic scaling
try:
    while True:
        sample, timestamp = inlet.pull_sample()  # Get a new sample from LSL stream

        # Shift buffer to the left and append the new sample
        data_buffer = np.roll(data_buffer, -1, axis=1)
        data_buffer[:, -1] = sample[:len(channel_names)]  # Append new data to buffer

        # Update plot for each channel
        for i, line in enumerate(lines):
            line.set_ydata(data_buffer[i])

        # Dynamically adjust y-limits based on the data in the buffer
        current_min = np.min(data_buffer)
        current_max = np.max(data_buffer)

        # Set y-limits with some padding for better visualization
        if current_min < current_max:  # Ensure that min and max are valid
            ax.set_ylim(current_min - 10, current_max + 10)

        # Refresh the plot
        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    print("Real-time plotting stopped.")
    plt.close(fig)  # Close plot when stopped
