# 🇻🇳 Vietnamese Traffic Sign Recognition Using YOLOv8

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)
![Flask](https://img.shields.io/badge/Flask-Web_App-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Desktop_App-red)

A comprehensive computer vision project designed to detect and recognize **Vietnamese Traffic Signs** using the state-of-the-art **YOLOv8** object detection model. The project features two main interfaces: a Web Application for image upload processing and a Desktop Application capable of real-time screen capture detection.

## ✨ Features

- **High Accuracy Detection:** Utilizes YOLOv8 trained specifically on Vietnamese traffic signs, covering over 50 different classes.
- **Web Application (`app.py`):** A Flask-based web interface allowing users to upload images and instantly view the detection results with bounding boxes and Vietnamese labels.
- **Desktop Application (`desktop_app.py`):** An OpenCV-based screen capture tool that captures a specific region of your screen, allowing you to test detection on live videos (e.g., YouTube driving videos) by pressing a hotkey.
- **Detailed Presentation:** Includes presentation slides, scripts, and media assets summarizing the dataset, model architecture, training process, and results.

## 📂 Project Structure

```text
PE/
├── app.py                # Main script for the Flask Web Application
├── desktop_app.py        # Main script for the OpenCV Screen Capture Application
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation (this file)
├── .gitignore            # Git ignore configuration
├── models/               # Contains trained YOLOv8 weights (e.g., best_traffic_sign_model.pt)
├── data/                 # Datasets used for training and testing
├── runs/                 # YOLOv8 output directory (training logs, eval metrics, captures)
├── notebooks/            # Jupyter Notebooks for data exploration and model training
├── scripts/              # Python scripts for utility tasks (processing, augmentation)
├── templates/            # HTML templates for the Web Application (index.html)
├── static/               # Static assets for the Web Application (CSS, JS, UI images)
└── presentation/         # Presentation materials
    ├── assets/           # Images/Videos used in the presentation
    ├── presentation.html # Slide deck
    └── presentation_script.md # Speaker notes
```

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.8 or higher installed on your system. Setting up a virtual environment is highly recommended.

### 2. Installation

Clone this repository and navigate to the project directory:

```bash
git clone <your-repository-url>
cd <repository-name>
```

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Running the Applications

#### 🌐 Web Application (Flask)

The Web App allows you to upload an image from your computer and receive the predicted traffic signs drawn directly on the image.

To start the web server, run:
```bash
python app.py
```
Open your web browser and navigate to `http://localhost:5000` (or the URL provided in the terminal).

#### 🖥️ Desktop Application (Screen Capture)

The Desktop App creates a live view of your screen's center. This is highly useful for detecting signs on a driving video playing on your screen.

To launch the desktop capture tool, run:
```bash
python desktop_app.py
```
**Controls:**
- **`c`**: Capture the current frame and run YOLOv8 detection.
- **`q`**: Quit the application.
- *Any key*: Return to live view after a capture.
*(Captured images with bounding boxes are saved automatically to `runs/captures/`)*

## 🧠 Model Training

The model was trained using the Ultralytics YOLOv8 framework. If you wish to retrain or fine-tune the model:
1. Ensure your dataset is correctly formatted in the YOLO format and placed inside the `data/` folder.
2. Refer to the resources in the `scripts/` or `notebooks/` directory to start the training pipeline.
3. The new weights will be saved in `runs/detect/train/weights/best.pt`. Update the path in `app.py` and `desktop_app.py` if necessary.

## 👥 Authors

- **ThayBaiThatSon** - FPT University

---
*Created for PE - CPV301 (SU2026).*
