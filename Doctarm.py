import time
from adafruit_ble import BLERadio
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.standard.health_thermometer import HealthThermometerService
from adafruit_ble.services.standard.heart_rate import HeartRateService

# Initialize BLE radio
ble = BLERadio()

# Scan for BLE devices and connect to the first found device
print("Scanning for BLE devices...")
while not ble.connected:
    for advertisement in ble.start_scan(timeout=5):
        if DeviceInfoService in advertisement.services:
            device_info = DeviceInfoService(ble.connect(advertisement))
            print(f"Connected to {device_info.model_number}")
            break
    ble.stop_scan()

# Initialize health thermometer service
thermometer_service = HealthThermometerService(ble)
heart_rate_service = HeartRateService(ble)

# Main loop to continuously read and display health data
def main():
    while True:
        # Read temperature in Celsius
        temperature = thermometer_service.read_temperature()
        print(f"Temperature: {temperature} °C")

        # Read heart rate
        heart_rate = heart_rate_service.measurement_values[1]
        print(f"Heart Rate: {heart_rate} bpm")

        time.sleep(2)  # Wait for 2 seconds between readings

if __name__ == "__main__":
    main()
