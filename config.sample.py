# Configuration File

# This is the sample configuration file, that I (Hermann) am using for my setup.
# Copy it to 'config.py' and adapt it to your needs.

# InfluxDB address
influx_url = "http://gerty:8086/"

influx_database_name = "aqua"

# time interval for sending moisture measurements to the server (seconds)
send_measurements_interval = 300  # seconds

# number of measurements that should be aggregated before sending them to the server
aggregated_measurements_count = 6  # default: 6 per 5 minutes, i.e. measuring every 50 seconds
