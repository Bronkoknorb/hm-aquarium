# Configuration File

# This is the sample configuration file, that I (Hermann) am using for my setup.
# Copy it to 'config.py' and adapt it to your needs.

# Control Server WebSocket
server_websocket = "ws://gerty:8080/api/websocket"

# time interval for sending moisture measurements to the server (seconds)
send_measurements_interval = 60*3  # seconds

# number of measurements that should be aggregated before sending them to the server
aggregated_measurements_count = 6  # default: 6 measurements per 3 minutes, i.e. measuring every 30 seconds
