# Eye Tracking with MediaPipe and OpenCV

This project uses **MediaPipe** and **OpenCV** to track eye movements in real-time via webcam. It detects iris positions, logs data to a CSV, saves the video, and updates a live scatter plot of eye movement.

## 📸 Features

- Real-time iris tracking with MediaPipe
- Saves a video recording of the session
- Logs iris positions per frame in a CSV file
- Live scatter plot of eye movements

## 🧰 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- Matplotlib

## 🔧 Installation

```bash
git clone https://github.com/yourusername/eye-tracking-project.git
cd eye-tracking-project
pip install -r requirements.txt
```

## ▶️ How to Run

```bash
python eye_tracking.py
```

Press `ESC` to stop the capture.

## 📁 Output Files

- `eye_tracking_<timestamp>.avi` – Captured webcam footage
- `eye_tracking_<timestamp>.csv` – Iris coordinates per frame

## 📈 Live Plot

Green = Right Iris  
Red = Left Iris

## 🧠 Flowchart

See the flowchart below for a visual overview of how the system works.

![Flowchart](flowchart.png)

## 🤝 Contribution

Pull requests are welcome. For major changes, please open an issue first.

---

© 2025 Your Name or Organization
