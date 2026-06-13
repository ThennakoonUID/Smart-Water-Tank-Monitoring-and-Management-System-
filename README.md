# Smart Water Tank Monitoring and Management System

## Overview
[cite_start]This project is a low-cost, IoT-based smart water tank monitoring and management system. [cite: 33] [cite_start]Traditional unmonitored water tanks often lead to water overflow, unknown water quality, and a lack of daily usage data. [cite: 6, 13, 20, 30] [cite_start]This system solves these issues by using a Raspberry Pi 4 to monitor water levels, assess water purity, and measure water consumption in real-time. [cite: 8, 35, 36, 37] [cite_start]All sensor data is transmitted to a smartphone via the Blynk IoT platform, providing a remote dashboard and critical push notifications. [cite: 39, 220]

## Key Features
* [cite_start]**Real-Time Water Level Monitoring:** Uses an ultrasonic sensor to calculate the tank's water capacity and prevent overflow or emergency shortages. [cite: 11, 35, 105]
* [cite_start]**Water Purity Checking:** Integrates a pH sensor with an ADS1115 Analog-to-Digital Converter to continuously monitor the acidity or alkalinity of the storage water. [cite: 36, 123, 124]
* [cite_start]**Consumption Tracking:** Measures the exact volume of water used via a Hall Effect water flow sensor, utilizing hardware interrupts for precise calculations. [cite: 37, 156, 157, 171]
* [cite_start]**Mobile Dashboard & Alerts:** Proactively pushes data to a Blynk mobile app every 5 seconds. [cite: 195, 217] [cite_start]It features automated lock-screen push notifications when the water level drops critically low. [cite: 219, 220]

## Hardware Architecture
* [cite_start]Raspberry Pi 4 Model B [cite: 61]
* [cite_start]JSN-SR04T Ultrasonic Sensor (Time-of-Flight) [cite: 62, 87]
* [cite_start]E-201-C pH Sensor [cite: 63]
* [cite_start]HZ21WA Water Flow Sensor [cite: 64]
* [cite_start]ADS1115 Analog-to-Digital Converter (16-bit) [cite: 65]

## Software & Libraries
* [cite_start]**Language:** Python 3 [cite: 71]
* [cite_start]**Key Libraries:** `RPi.GPIO`, `time`, `BlynkLib`, `board`, `busio`, `adafruit_ads1x15.ads1115` [cite: 75, 76, 77, 80, 81]

## Future Improvements
* [cite_start]**Enhanced Water Quality Parameters:** Integrating TDS (Total Dissolved Solids) and Turbidity sensors to detect suspended particles and mineral concentrations. [cite: 222, 225, 228]
* [cite_start]**Closed-Loop Automation:** Adding a 5V relay module to automatically switch the water pump on/off based on tank capacity without human intervention. [cite: 230, 233, 234]
* [cite_start]**Machine Learning Leak Detection:** Implementing an AI model on the Raspberry Pi to learn normal household usage patterns and trigger alerts for unusual flow rates indicating leaks. [cite: 236, 239, 240]

## Project Team (Group BM4)
* A.D.T.M.S.H. [cite_start]Tennekone [cite: 1, 2]
* U.I.D. [cite_start]Thennakoon [cite: 1]
* W.M.I.R. [cite_start]Wanninayaka [cite: 1]
