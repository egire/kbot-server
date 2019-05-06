# KBot
KBot Server - Controllable Autonomous Robot Server

## Purpose

Document serves to capture the hardware configuration of KBOT to facilitate software development.


## Designers



*   Software: Eric Gire 
    *   [https://www.linkedin.com/in/egr/](https://www.linkedin.com/in/egr/)
    *   [esgire@gmail.com](mailto:esgire@gmail.com)
    *   [https://github.com/egire](https://github.com/egire)


## Scope and Features

*   Hardware
    *   Telepresence/autonomous robot made from COTS and 3D printed components focusing on design for assembly and expandability
    *   [ROB0025: Baron - 4WD Arduino Mobile Platform with Encoder](https://www.dfrobot.com/product-261.html)
    *   High definition camera on servo operated pan/tilt mount.
    *   I2C - 4 channel motor driver
    *   I2C - 16 channel servo driver
    *   Ultrasonic proximity sensor for distance measurement and avoidance HC-SR04
    *   Compass Module 3-Axis HMC5883L for heading
    *   5 DOF 
*   Software
    *   JSON generated control interface
    *   CSV defined hardware configurations
    *   Python web server back-end (Web.py)
    *   Fully-exposed control interface (Android, Web, etc.)
    *   Interface data communication security (SSL)
    *   Login system (Multi-Factor Auth.)
    *   Responsive, real-time web control
    *   JSON sensor data encapsulation with sensor fusion
    *   Multi-modal control (partial control, full control, AI, ML, CV)
*   Control UI
    *   CONTROL: [http://th3ri5k.mynetgear.com/kbot/controls.html](http://th3ri5k.mynetgear.com/kbot/controls.html)
    *   LOGGING: [http://th3ri5k.mynetgear.com/kbot/log.html](http://th3ri5k.mynetgear.com/kbot/log.html)
    *   SENORS: [http://th3ri5k.mynetgear.com/kbot/sensors.html](http://th3ri5k.mynetgear.com/kbot/sensors.html)
    *   PIN EDITOR: [http://th3ri5k.mynetgear.com/kbot/editor.html](http://th3ri5k.mynetgear.com/kbot/editor.html)
    *   VIDEO: [http://th3ri5k.mynetgear.com/video](http://th3ri5k.mynetgear.com/video)
    *   LOGIN: [http://th3ri5k.mynetgear.com/kbot/](http://th3ri5k.mynetgear.com/kbot/)
    *   REGISTER: [http://th3ri5k.mynetgear.com/kbot/register.html](http://th3ri5k.mynetgear.com/kbot/register.html)
*   Login Credentials
    *   Username: test
    *   Password: test
    *   (or just register a new account)


## Bill of Materials (BOM)



1. [Camera Module V2](https://www.raspberrypi.org/products/camera-module-v2/)
2. [Raspberry Pi 2 B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
3. [Adafruit DC & Stepper Motor HAT](https://www.adafruit.com/product/2348)
4. [Adafruit 16-Channel PWM / Servo HAT](https://www.adafruit.com/product/2327)
5. [Dagu Rover 5 Robot Platform](https://www.sparkfun.com/products/10336)
6. [Compass Module 3-Axis HMC5883L](https://www.parallax.com/product/29133)
7. [SparkFun Triple Axis Accelerometer Breakout - ADXL345](https://www.sparkfun.com/products/9836)
8. [PING))) Ultrasonic Distance Sensor](https://www.parallax.com/product/28015) or similar generic
9. [https://www.dfrobot.com/product-261.html](https://www.dfrobot.com/product-261.html) (KBOT)
10. DF Robot Barron Platform Encoder information [https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_](https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_)


## Pin Assignments [https://pinout.xyz/pinout/](https://pinout.xyz/pinout/)


<table>
  <tr>
   <td><strong>Description</strong>
   </td>
   <td><strong>Pin # (hardware)</strong>
   </td>
   <td><strong>Name (software)</strong>
   </td>
   <td><strong>Notes</strong>
   </td>
  </tr>
  <tr>
   <td>I2C SDA1
   </td>
   <td>3
   </td>
   <td>SDA (data)/GPIO2
   </td>
   <td>Primary I2C bus
   </td>
  </tr>
  <tr>
   <td>I2C SCL1
   </td>
   <td>5
   </td>
   <td>SDL (data)/GPIO3
   </td>
   <td>Primary I2C bus
   </td>
  </tr>
  <tr>
   <td>Ultrasonic SIG
   </td>
   <td>32
   </td>
   <td>GPIO12 (in/out)
   </td>
   <td><a href="https://www.element14.com/community/community/stem-academy/blog/2014/12/21/ping-me">https://www.element14.com/community/community/stem-academy/blog/2014/12/21/ping-me</a>
   </td>
  </tr>
  <tr>
   <td>InfRARed
   </td>
   <td>IC2
   </td>
   <td>???
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Left Encoder
   </td>
   <td>16
   </td>
   <td>GPIO23
   </td>
   <td><a href="https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_">https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_</a>
   </td>
  </tr>
  <tr>
   <td>Right Encoder
   </td>
   <td>18
   </td>
   <td>GPIO24
   </td>
   <td><a href="https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_">https://wiki.dfrobot.com/Wheel_Encoders_for_DFRobot_3PA_and_4WD_Rovers__SKU_SEN0038_</a>
   </td>
  </tr>
  <tr>
   <td>Left Fore Motor
   </td>
   <td>IC2
   </td>
   <td>kit.motor1
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Right Fore Motor
   </td>
   <td>IC2
   </td>
   <td>kit.motor2
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Left Aft Motor
   </td>
   <td>IC2
   </td>
   <td>kit.motor3
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Right Aft Motor
   </td>
   <td>IC2
   </td>
   <td>kit.motor4
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Sensor Head Pan
   </td>
   <td>I2C
   </td>
   <td>kit.servo[0]
   </td>
   <td>left/right 180 degree rotation of arm base
   </td>
  </tr>
  <tr>
   <td>Sensor Head Tilt
   </td>
   <td>I2C
   </td>
   <td>kit.servo[1]
   </td>
   <td>up/down rotation at base
   </td>
  </tr>
</table>



## Interface Control Document (ICD)



*   4.7K pull ups required on SDA and SCL
*   I2C Addresses
    *   **0x40** (default) Library - [Adafruit 16-Channel PWM / Servo HAT](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/attach-and-test-the-hat#step-2-configure-your-pi-to-use-i2c-devices-6-3)
        *   sudo apt-get install python-smbus (required)
        *   sudo apt-get install i2c-tools (optional)
    *   **0x60** (default) Library - [Adafruit DC & Stepper Motor HAT](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software#python-installation-of-motorkit-library-4-3) 
        *   sudo pip3 install adafruit-circuitpython-motorkit
    *   **0X1E **[Compass Module 3-Axis HMC5883L ](https://www.parallax.com/product/29133)
    *   **0X53** [SparkFun Triple Axis Accelerometer Breakout - ADXL345](https://www.sparkfun.com/products/9836)
        *   NOTE: I2C mode is enabled if the CS pin is tied to high. There is no default mode if the CS pin is left unconnected, so it should always be tied high or driven by an external controller.
        *   [Raspi Tutorial](https://www.sunfounder.com/learn/super_kit_v2_for_raspberrypi/lesson-14-adxl345-super-kit-for-raspberrypi.html)
    *   [Ultrasonic tutorial ](https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/) digital read/write.
    *   **0x29 **VL53L0X Time of Flight distance sensor
        *   50 - 1200 mm
        *   [Tutorial ](https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/overview)
*   Motor configuration
    *   M1 = Left Fore (Red)
    *   M2 = Left Aft (Blue)
    *   M3 = Right Fore (Yellow)
    *   M4 = Right Aft (Green)
    *   Voltage: +4.5 to 6V MAX
    *   Current: 1200mA load
    *   Motor type: 130
    *   Rotational Speed: 10000 r / min
    *   Gearbox reduction ratio: 1:120
*   KBOT BATTERY INFO
    *   7.4 VDC NiMH
*   Ultrasonic Sensor: Parallax PING))) 2 cm (0.8 inches) to 3 meters (3.3 yards)
*   VL53L0X Time of Flight distance sensor
    *   50 - 1200 mm
    *   Tutorial [https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/overview](https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/overview)


## Raspi Provisioning Steps



1. Download image (torrent is fastest)
    1. [Raspbian Stretch with desktop and recommended software](https://www.raspberrypi.org/downloads/raspbian/)
2. Burn to SD with Etcher
3. Update OS when prompted
4. Enable camera interface, SSH, and wifi. `sudo raspi-config` 
5. Forward Ports
    2. 22 to KBOT Raspi for SSH
    3. 80 to KBOT Raspi Web front-end
    4. 8000 to KBOT Raspi Web.py back-end/front-end
6. Set DNS ANAME (th3ri5k.mynetgear.com) to resolve KBOT INET IP address
7. Install kbot following steps a-f and kbot.service in systemd to run start-kbot.sh on boot
    5. Installing KBot Server and Web Controller
        1. `sudo apt-get install python3.5`
        2. `python3 -m pip install web.py==0.40-dev1`
        3. `python3 -m pip install configparser`
        4. <code>git clone [https://github.com/egire/kbot-server.git](https://github.com/egire/kbot-server.git) ~/kbot/kbot-server</code>
        5. <code>git clone [https://github.com/egire/kbot-web](https://github.com/egire/kbot-web) ~/kbot/kbot-web</code>
        6. <code>cp -R ~kbot/kbot-server/scripts/ ~/</code>
    6. Add kbot.service to systemd 
        7. <code>sudo cp ~kbot/kbot-server/scripts/kbot.service /etc/systemd/system</code>
        8. <code>sudo reboot</code>
8. Installed RPi Cam web interface [https://elinux.org/RPi-Cam-Web-Interface](https://elinux.org/RPi-Cam-Web-Interface)
    7. install.sh main installation as used in step 4 above
    8. update.sh check for updates and then run main installation
    9. start.sh starts the software. If already running it restarts.
    10. stop.sh stops the software
    11. remove.sh removes the software
    12. debug.sh is same as start but allows raspimjpeg output to console for debugging
    13. Install Private key


## Running KBot



*   Default: Reboot RasPi or Restart kbot.service using systemctl Service (Provision steps have been followed)
*   Debug: Execute ~/kbot.sh  from kbot terminal (see server POSTs and GETs and Python Errors)

<!-- Docs to Markdown version 1.0β17 -->
