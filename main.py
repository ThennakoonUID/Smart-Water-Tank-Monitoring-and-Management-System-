import RPi.GPIO as GPIO
import time
import BlynkLib
import statistics
import board, busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# --- Blynk and Sensor Setup ---

# Paste your Blynk Auth Token here
BLYNK_AUTH_TOKEN = "YOUR_TOKEN_HERE"

# Define Datastream Virtual Pins
V_WATER_LEVEL = 1      # V1 for water level in cm
V_PERCENTAGE = 2       # V2 for water percentage
V_STATUS = 3           # V3 for status messages
V_PH = 4               # V4 for pH value
V_PH_STATUS = 5        # V5 for pH health status

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)

# Define GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24

# --- Additional Hardware Pins ---
GREEN_LED = 17
RED_LED = 27
BUZZER = 22

# ----- Calibration -----
SLOPE = -10.87
INTERCEPT = 36.63

# ----- Setup ADS1115 -----
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
chan = AnalogIn(ads, 0)

# Tank dimensions (in cm)
TANK_HEIGHT_CM = 100.0  
MIN_ACCURATE_DISTANCE_CM = 25.0  # Ultrasonic blind spot

# Setup the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Setup for LEDs and Buzzer
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Turn off all indicators initially
GPIO.output(GREEN_LED, GPIO.LOW)
GPIO.output(RED_LED, GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)

# ----- Settings -----
SAMPLES = 20
DELAY = 0.5  # seconds between pH samples

def read_avg(n=SAMPLES, delay=DELAY):
    vals = []
    for _ in range(n):
        vals.append(chan.voltage)
        time.sleep(delay)
    return vals


# --- Functions ---
def measure_distance():
    """Measures the distance from the ultrasonic sensor."""
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start_time = time.time()
    pulse_end_time = time.time()

    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()
        if time.time() - timeout_start > 0.04:
            return None

    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()
        if time.time() - timeout_start > 0.04:
            return None

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2  # cm
    return distance


def blynk_connected(ping=None):
    print("Connected to Blynk Cloud")

blynk.on("connected", blynk_connected)


def read_sensor_and_update():
    """Measure water level and pH, send to Blynk."""
    print("Taking readings...")

    # --- Water Level Measurement ---
    air_gap = measure_distance()
    if air_gap is None:
        print("Sensor timeout or wiring error")
        blynk.virtual_write(V_STATUS, "Error: Sensor Timeout")
        return

    if air_gap < MIN_ACCURATE_DISTANCE_CM:
        water_level = TANK_HEIGHT_CM
        water_percent = 100.0
        status = "Tank Full"
        print(f"Tank Full | Level: {water_level} cm (100%)")
    else:
        air_gap_adj = air_gap - MIN_ACCURATE_DISTANCE_CM
        water_level = max(0.0, round(TANK_HEIGHT_CM - air_gap_adj, 2))
        water_percent = round((water_level / TANK_HEIGHT_CM) * 100, 1)
        status = "OK"
        print(f"Air Gap: {air_gap:.2f} cm | Level: {water_level:.2f} cm ({water_percent}%)")

    # --- LED & Buzzer for Water Level ---
    if water_percent >= 99:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(BUZZER, GPIO.LOW)
    elif water_percent <= 10:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(BUZZER, GPIO.LOW)
    else:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.LOW)

    # --- pH Sensor Measurement ---
    vals = read_avg()
    mean_v = statistics.mean(vals)
    stdev_v = statistics.pstdev(vals)
    mn = min(vals)
    mx = max(vals)

    ph = SLOPE * mean_v + INTERCEPT
    ph = max(0.0, min(14.0, ph))
    print(f"Voltage: {mean_v:.3f} V | pH: {ph:.2f}")

    # --- pH Status Check ---
    if 6.5 <= ph <= 8.5:
        ph_status = "Healthy"
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.LOW)
    else:
        ph_status = "Unhealthy"
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
        GPIO.output(BUZZER, GPIO.HIGH)
        print("ALERT: Water pH is not healthy!")
        time.sleep(2)
        GPIO.output(BUZZER, GPIO.LOW)

    # --- Send Data to Blynk ---
    blynk.virtual_write(V_WATER_LEVEL, water_level)
    blynk.virtual_write(V_PERCENTAGE, water_percent)
    blynk.virtual_write(V_STATUS, status)
    blynk.virtual_write(V_PH, ph)
    blynk.virtual_write(V_PH_STATUS, ph_status)


# --- Main Program Loop ---
print("Program starting...")
print(f"Tank Height: {TANK_HEIGHT_CM} cm | Blind Spot: < {MIN_ACCURATE_DISTANCE_CM} cm")
print("Press Ctrl + C to stop.")

last_update_time = 0
interval = 5  # seconds between readings

try:
    while True:
        blynk.run()
        current_time = time.time()
        if current_time - last_update_time >= interval:
            read_sensor_and_update()
            last_update_time = current_time

except KeyboardInterrupt:
    print("\nMeasurement stopped by user.")

finally:
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.output(BUZZER, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO pins cleaned up. Goodbye.")
