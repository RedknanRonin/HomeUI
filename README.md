
![image](https://github.com/user-attachments/assets/ea5b86a4-6324-4045-8793-de6635f60476)

**Project Overview**


This project is a web application that integrates various IoT devices and APIs to provide real-time data and control functionalities. 
It is built using Flask for the backend and JavaScript for the frontend. It includes features such as fetching and displaying RuuviTag sensor data, electricity prices, and Airthings data, as well as controlling Philips Hue lights.  

**Features**

RuuviTag Data: Fetches temperature data from RuuviTag sensors and displays it. 

Electricity Prices: Fetches and displays the latest electricity prices, including the current hour's price.

Airthings Data: Fetches Airthings sensor data every 30 minutes and stores it in a file.

Philips Hue Control: Provides endpoints to control Philips Hue lights.


**Technologies Used**

Backend: Flask, Python, asyncio

Frontend: JavaScript, HTML, CSS

Data Storage: JSON files

APIs: Airthings, Philips Hue, Porssisahko



**Usage**

Run the Flask application:  <pre>python main.py </pre>
Access the application: Open your web browser and navigate to http://localhost:5000.  



**Endpoints**

Home: /
Serve Static Files: /<path:filename>
Proxy for Electricity Prices: /proxy

Fetch RuuviTag Data: /ruuvitag_data

Fetch Airthings Data: /fetch_airthings_data

Control Philips Hue Lights:

Turn On Living Room Lights: /livingroomOn

Turn Off Living Room Lights: /livingroomOff

Set Living Room Evening Mode: /livingroomEvening



**Configuration**

RuuviTag Sensors: Add the MAC addresses of your RuuviTag sensors in the data/config.json file.

Airthings: Add your Airthings device ID, UID, and Auth Token in the data/config.json file.

Philips Hue: Add the URLs and Auth Token for controlling your Philips Hue lights in the data/config.json file.
