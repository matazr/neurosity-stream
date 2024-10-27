from pylsl import StreamInlet, resolve_stream

# Resolve EEG streams on the network
print("Resolving EEG streams...")
streams = resolve_stream('type', 'EEG')

# Create an inlet to receive data
inlet = StreamInlet(streams[0])

print("Connected to EEG stream. Receiving data...")

# Receive data in a loop
while True:
    sample, timestamp = inlet.pull_sample()
    print(f"Timestamp: {timestamp}, Sample: {sample}")
