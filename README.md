# Smart Water Tank Monitoring and Management System

## Overview
This project is a low-cost, IoT-based smart water tank monitoring and management system. Traditional unmonitored water tanks often lead to water overflow, unknown water quality, and a lack of daily usage data. This system solves these issues by using a Raspberry Pi 4 to monitor water levels, assess water purity, and measure water consumption in real-time. All sensor data is transmitted to a smartphone via the Blynk IoT platform, providing a remote dashboard and critical push notifications.

## Key Features
* **Real-Time Water Level Monitoring:** Uses an ultrasonic sensor to calculate the tank's water capacity and prevent overflow or emergency shortages.
* **Water Purity Checking:** Integrates a pH sensor with an ADS1115 Analog-to-Digital Converter to continuously monitor the acidity or alkalinity of the storage water.
* **Consumption Tracking:** Measures the exact volume of water used via a Hall Effect water flow sensor, utilizing hardware interrupts for precise calculations.
* **Mobile Dashboard & Alerts:** Proactively pushes data to a Blynk mobile app every 5 seconds. It features automated lock-screen push notifications when the water level drops critically low.

## Hardware Architecture
* Raspberry Pi 4 Model B
* JSN-SR04T Ultrasonic Sensor (Time-of-Flight)
* E-201-C pH Sensor
* HZ21WA Water Flow Sensor
* ADS1115 Analog-to-Digital Converter (16-bit)

## Software & Libraries
* **Language:** Python 3
* **Key Libraries:** `RPi.GPIO`, `time`, `BlynkLib`, `board`, `busio`, `adafruit_ads1x15.ads1115`

## Future Improvements
* **Enhanced Water Quality Parameters:** Integrating TDS (Total Dissolved Solids) and Turbidity sensors to detect suspended particles and mineral concentrations.
* **Closed-Loop Automation:** Adding a 5V relay module to automatically switch the water pump on/off based on tank capacity without human intervention.
* **Machine Learning Leak Detection:** Implementing an AI model on the Raspberry Pi to learn normal household usage patterns and trigger alerts for unusual flow rates indicating leaks.

## Project Team (Group BM4)
* A.D.T.M.S.H. Tennekone
* U.I.D. Thennakoon
* W.M.I.R. Wanninayaka

## System Demo
🎥 **[Watch the full video demonstration on YouTube](https://youtu.be/YcRB5LZlO28)**
