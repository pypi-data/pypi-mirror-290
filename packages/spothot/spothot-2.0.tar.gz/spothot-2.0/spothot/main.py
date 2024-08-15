import os
import subprocess
import argparse
from spothot.app import run_flask

LOG_DIR = "/home/pi/"
LOG_FILE = os.path.join(LOG_DIR, "configure_hotspot.log")

# Ensure the necessary directories exist
def ensure_directory(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_log_directory():
    ensure_directory(LOG_FILE)

def log_message(message):
    ensure_log_directory()
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"Command '{command}' failed with error: {e}")

def is_wifi_connected():
    # Check if the system is connected to a Wi-Fi network
    result = subprocess.run(
        ['iwgetid'],
        capture_output=True,
        text=True
    )
    return "ESSID" in result.stdout

def connect_to_saved_wifi():
    log_message("Attempting to connect to saved Wi-Fi network...")
    
    # Stop the existing wpa_supplicant service
    run_command('sudo systemctl stop wpa_supplicant')
    
    # Remove the control interface file if it exists
    run_command('sudo rm -f /var/run/wpa_supplicant/wlan0')
    
    # Start wpa_supplicant with the specified configuration
    run_command('sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf')
    
    # Obtain an IP address via DHCP
    run_command('sudo dhclient wlan0')

    if is_wifi_connected():
        log_message("Connected to a saved Wi-Fi network.")
        return True
    else:
        log_message("Failed to connect to any saved Wi-Fi networks.")
        return False

def configure_network(ssid, password):
    log_message("Configuring network...")

    # Ensure directories exist before writing configuration files
    ensure_directory('/etc/hostapd')
    ensure_directory('/etc/dnsmasq.d')
    ensure_directory('/etc')

    # Create dhcpcd.conf configuration
    with open('/etc/dhcpcd.conf', 'w') as f:
        f.write("""
# Static IP configuration for wlan0
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
""")

    # Create dnsmasq.conf configuration
    with open('/etc/dnsmasq.conf', 'w') as f:
        f.write("""
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
""")

    # Create hostapd.conf configuration with optimized settings
    with open('/etc/hostapd/hostapd.conf', 'w') as f:
        f.write(f"""
# Interface and driver settings
interface=wlan0
driver=nl80211

# Wi-Fi settings
ssid={ssid}
hw_mode=g
channel=10

# Security settings
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# Additional settings
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wmm_enabled=1

# Enable IEEE 802.11n (high throughput)
ieee80211n=1

# Optional: Enable Short Guard Interval for 802.11n
ht_capab=[SHORT-GI-20][HT20]
""")

    # Unmask hostapd service
    run_command('sudo systemctl unmask hostapd')

    # Correct the DAEMON_CONF line in /etc/default/hostapd
    run_command('sudo sed -i \'s|#DAEMON_CONF=".*"|DAEMON_CONF="/etc/hostapd/hostapd.conf"|\' /etc/default/hostapd')
    run_command('sudo sed -i \'s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|g\' /etc/sysctl.conf')
    run_command('sudo sysctl -p')
    run_command('sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
    run_command('sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"')

def restart_services():
    log_message("Restarting services...")
    run_command('sudo systemctl restart dhcpcd')
    run_command('sudo systemctl restart dnsmasq')
    run_command('sudo systemctl restart hostapd')

def start_flask_app():
    log_message("Starting Flask app...")
    run_flask()

def main():
    parser = argparse.ArgumentParser(description="Setup Raspberry Pi as a Wi-Fi hotspot")
    parser.add_argument('--ssid', required=True, help='SSID for the Wi-Fi hotspot')
    parser.add_argument('--password', required=True, help='Password for the Wi-Fi hotspot')
    args = parser.parse_args()

    if os.geteuid() != 0:
        log_message("Please run the script with sudo.")
        exit(1)

    log_message("Starting configuration...")

    # Try to connect to the saved Wi-Fi
    if not connect_to_saved_wifi():
        # If Wi-Fi connection fails, set up the hotspot
        configure_network(args.ssid, args.password)
        restart_services()

    # Start the Flask app in either case
    start_flask_app()

    log_message("Configuration completed.")

if __name__ == "__main__":
    main()
