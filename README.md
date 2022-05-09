# Overview
<img src="assets/cover.png" width="350"/>

The project idea is to build a robot car that can receive a photo of an object so it can autonomously search and find it. An ultrasonic sensor is used
for close-range object detection to force stop the robot to avoid accidents. Finally, a pi v2 camera module is installed on the robot to help detect objects.

## Backend
A Node.js http and websocket server is running in the backend. The server communicates with the robot car
and sends/recieves information from the frontend web application as well.

## Frontend
A React.js frontend is used to communicate with the backend and create a dashboard to control the robot.

## AdaFruit
The python code also demonstrates communicating with AdaFruit using MQTT to send and recieve data which is used to create a cloud dashboard.

## Getting Started
Run npm install inside the backend and frontend folders. Running the command `npm run dev` with start the backend
and `npm run start` with start the frontend.