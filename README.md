🚀 Intelligent Image Classification & Robotic Navigation System

📖 Introduction
This project integrates Image Classification using TensorFlow's Inception Model and Robotic Orientation Control using ROS (Robot Operating System). It can classify objects in an image, process results, and align a robot's orientation towards a specified target object.

The system combines:

Machine Learning (Object Classification)
Data Processing (CSV Manipulation)
Robotics (Angular Navigation with ROS)
Whether you're a researcher, student, or tech enthusiast, this project aims to simplify complex AI-robotics integration.

🌟 Project Overview

Object Detection and Classification:

Classifies objects in an image using the Inception model.
Stores predictions in a CSV file.

Data Processing:
Cleans and processes the CSV data to extract relevant information.

Robot Navigation:
Adjusts a robot's orientation towards a target object based on classification results.

📝 Scripts Breakdown

📌 1. Image Classification Script (image_classification.py)

Purpose:
Classifies objects in a given image using TensorFlow's pre-trained Inception model and logs predictions into a CSV file.

Model Download & Setup:
Downloads the Inception model if not already present.

Inference Process:

Loads the model.
Processes the input image.
Outputs top predictions and writes them to a Predictions.csv file.

ROS Integration:

Subscribes to /rpy_angles for orientation data.
Logs yaw angles during image classification.

How to Run:
python image_classification.py --image_path=path_to_your_image.jpg

Expected Output:

Object predictions displayed on the terminal.
Predictions.csv file created with object names and their scores.

📌 2. CSV Data Cleaning Script (csv_cleaner.py)

Purpose:
Processes the raw Predictions.csv file to clean and extract meaningful data.

Empty Row Removal:
Removes any blank or invalid rows from Predictions.csv.

Column Filtering:
Keeps only the required columns.

Output File:
Creates a clean FilteredData.csv file.

How to Run:

python csv_cleaner.py
Expected Output:

A clean FilteredData.csv file ready for the robot navigation script.

📌 3. Robot Orientation Script (robot_orientation.py)

Purpose:
Controls a robot's yaw (angular rotation) based on the classified target object from FilteredData.csv.

Read Target Object:
Extracts the target object's yaw position from FilteredData.csv.

Orientation Adjustment:

Subscribes to /rpy_angles to receive live yaw updates.
Publishes angular velocity commands to align the robot towards the target.

How to Run:

roscore  # Start ROS core (if not already running)
python robot_orientation.py

Expected Output:
Robot rotates to align with the target object's yaw angle.

⚙️ Installation

Ensure you have the following installed:

Python 3.x
TensorFlow
ROS (Robot Operating System)
NumPy
Pandas
Install Dependencies:

pip install tensorflow numpy pandas rospy

Step 1: Run Image Classification Script
python image_classification.py --image_path=path_to_image.jpg

Step 2: Clean the CSV Data
python csv_cleaner.py

Step 3: Start ROS Core
roscore

Step 4: Run Robot Orientation Script
python robot_orientation.py

🔄 Workflow Explained

Image Classification:

Input an image and run the classification script.
Predictions are saved to Predictions.csv.

Data Processing:
Clean and refine prediction data into FilteredData.csv.

Robot Navigation:

Robot receives the target yaw position from the clean CSV.
Robot aligns itself with the target object.

🎯 Simple Diagram:
Image → TensorFlow Model → Predictions.csv → FilteredData.csv → Robot Navigation

🛠️ Troubleshooting

TensorFlow Import Errors:
Ensure TensorFlow is installed and matches your Python version.

CSV File Missing:
Verify that the scripts are executed in the correct order.

Robot Not Rotating:
Check if /rpy_angles topic is publishing yaw data.

🚀 Future Improvements

Add real-time image classification with a live camera feed.
Implement advanced robotics maneuvers.
Improve object detection accuracy using fine-tuned models.

Feel free to use, modify, and distribute it as long as you provide proper attribution.

🤝 Contributions
Pull requests, suggestions, and improvements are welcome!

Happy Coding! 🚀
