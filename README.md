**1. UPLOAD CODE FOR ESP32 FOR OUTDOOR SENSOR**

  *1.1. Access the path: EE4348-G03-Final\CoAp\sensor_esp32
      - Upload code to ESP32
  *1.2. Connection Configuration
      - Set WiFi SSID under Example Configuration
      - Set WiFi Password
  *Copy the sta IP address to update in the code using for Home Center
  
**2. UPLOAD CODE FOR ESP32 FOR OUTDOOR PUMP**
  *1.1. Access the path: EE4348-G03-Final\CoAp\led_esp32/
      - Upload code to ESP32
  *1.2. Connection Configuration
      - Set WiFi SSID under Example Configuration
      - Set WiFi Password
  *Copy the sta IP address to update in the code using for Home Center

**3. UPLOAD CODE FOR ESP32 FOR INDOOR SENSOR**

  *1.1. Access the path: EE4348-G03-Final\MQTT\tcp_mqtt_transmit_test_2
      - Upload code to ESP32
  *1.2. Connection Configuration
      - Set WiFi SSID under Example Configuration
      - Set WiFi Password
  *Copy the TOPIC to update in the code using for Home Center
  
**4. UPLOAD CODE FOR ESP32 FOR OUTDOOR LED**
  *1.1. Access the path: EE4348-G03-Final\MQTT\ccch_mqtt
      - Upload code to ESP32
  *1.2. Connection Configuration
      - Set WiFi SSID under Example Configuration
      - Set WiFi Password
  *Copy the TOPIC to update in the code using for Home Center

**5. RUN HOMECENTER**
    - Run: EE4348-G03-Final\HomeCenter.exe
    - This code used for:
        + Send messages about data from sensors and status of pump and led to ThingsBoard
        + Send messages about signal control from ThingsBoard to sensors, pump, and led
        + Observing tracking log
