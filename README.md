# Line Following Robot

A line-following robot implementation using Raspberry Pi, OpenCV, and GPIO controls, refactored to follow Object-Oriented Programming principles with physical button controls.

## 🚀 Features

- **Object-Oriented Design**: Clean separation of concerns with dedicated classes for different functionalities
- **Computer Vision**: OpenCV-based line detection and intersection recognition
- **Motor Control**: Precise GPIO-based motor control for robot movement

## 📁 Project Structure

```
/Applications/Random/
├── README.md                    # This file
├── robot_app.py                 # Main application entry point
├── robot_controller.py          # Main robot controller (coordinates all components)
├── motor_controller.py          # Motor control and GPIO management
├── image_processor.py           # Computer vision and image processing
├── button_controller.py         # Physical button input handling
└── robot.py                     # Legacy entry point (backward compatibility)
```

### Class Hierarchy

```
RobotApp
└── RobotController
    ├── MotorController
    ├── ImageProcessor
    ├── ButtonController
    └── ButtonLED
```

### Key Classes

- **`RobotApp`**: Main application class that handles application lifecycle
- **`RobotController`**: Central controller that coordinates all robot components
- **`MotorController`**: Manages GPIO pins and motor movements (forward, backward, turn left/right)
- **`ImageProcessor`**: Handles camera capture, image processing, and line detection

## 🔧 Hardware Requirements

### Required Components

- Raspberry Pi (any model with GPIO pins)
- 2x DC Motors with motor driver (L298N recommended)
- USB Camera or Pi Camera
- Jumper wires
- Breadboard

### GPIO Pin Configuration

| Component         | GPIO Pin | Physical Pin | Function               |
| ----------------- | -------- | ------------ | ---------------------- |
| Motor A IN1       | 14       | Pin 8        | Left motor forward     |
| Motor A IN2       | 15       | Pin 10       | Left motor backward    |
| Motor B IN1       | 18       | Pin 12       | Right motor forward    |
| Motor B IN2       | 23       | Pin 16       | Right motor backward   |

## 📦 Installation

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python packages
pip install opencv-python numpy RPi.GPIO

# For camera support (if using Pi Camera)
sudo apt install python3-picamera
```

### 2. Enable GPIO and Camera

```bash
# Enable GPIO (usually enabled by default)
# Enable camera interface
sudo raspi-config
# Navigate to Interface Options > Camera > Enable
```

### 3. Hardware Setup

1. Connect motors to motor driver according to GPIO pin configuration
2. Connect buttons to designated GPIO pins with pull-up resistors
3. Connect LED to status LED pin (optional)
4. Connect USB camera or Pi Camera
5. Power up the Raspberry Pi

## 🔍 Computer Vision Parameters

The robot uses several configurable parameters for line detection:

- **Intersection Threshold**: 80% white pixel density in ROI
- **Tracking Center Range**: 210-430 pixels (adjustable based on camera resolution)
- **ROI (Region of Interest) Definition**: Middle-right section of 3x3 grid
- **Binary Threshold**: 128 (for grayscale to binary conversion)

## 🛠️ Customization

### Adjusting Motor Speed

Modify the `MotorController` class to add PWM control:

```python
# In motor_controller.py
def forward(self, speed=100):
    # Add PWM speed control
    pwm_a = GPIO.PWM(self.motor_A_in1, 1000)
    pwm_b = GPIO.PWM(self.motor_B_in2, 1000)
    # Implementation details...
```

## 📊 Performance Considerations

- **Frame Rate**: Typically 15-30 FPS depending on camera and processing
- **Latency**: Computation time
- **Battery**: As battery depletes, the strength of the motors decreases


## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- Raspberry Pi Foundation for GPIO libraries
- OpenCV community for computer vision tools
- Python community for excellent libraries and documentation
