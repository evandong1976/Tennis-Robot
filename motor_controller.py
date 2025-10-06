import RPi.GPIO as GPIO
from time import sleep


class MotorController:
    """
    Handles all motor control operations for the robot.
    Manages GPIO pins and provides methods for robot movement.
    """
    
    def __init__(self):
        """Initialize motor controller with GPIO pin configuration."""
        # Motor pin definitions
        self.motor_A_in1 = 14  # GPIO 24
        self.motor_A_in2 = 15  # GPIO 23
        self.motor_B_in1 = 18  # GPIO 17
        self.motor_B_in2 = 23  # GPIO 27
        
        self._setup_gpio()
        self._initialize_motors()
    
    def _setup_gpio(self):
        """Configure GPIO pins for motor control."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_A_in1, GPIO.OUT)
        GPIO.setup(self.motor_B_in1, GPIO.OUT)
        GPIO.setup(self.motor_A_in2, GPIO.OUT)
        GPIO.setup(self.motor_B_in2, GPIO.OUT)
    
    def _initialize_motors(self):
        """Set default values for both motors (default: off)."""
        GPIO.output(self.motor_A_in1, GPIO.LOW)
        GPIO.output(self.motor_A_in2, GPIO.LOW)
        GPIO.output(self.motor_B_in1, GPIO.LOW)
        GPIO.output(self.motor_B_in2, GPIO.LOW)
    
    def forward(self):
        """Move the robot forward."""
        self.stop()
        GPIO.output(self.motor_A_in1, GPIO.HIGH)
        GPIO.output(self.motor_A_in2, GPIO.LOW)
        GPIO.output(self.motor_B_in1, GPIO.LOW)
        GPIO.output(self.motor_B_in2, GPIO.HIGH)
        print("Moving forward")
    
    def backward(self):
        """Move the robot backward."""
        self.stop()
        GPIO.output(self.motor_A_in1, GPIO.LOW)
        GPIO.output(self.motor_A_in2, GPIO.HIGH)
        GPIO.output(self.motor_B_in1, GPIO.HIGH)
        GPIO.output(self.motor_B_in2, GPIO.LOW)
        print("Moving backward")
    
    def turn_left(self):
        """Turn the robot left."""
        self.stop()
        GPIO.output(self.motor_A_in1, GPIO.HIGH)
        GPIO.output(self.motor_A_in2, GPIO.LOW)
        GPIO.output(self.motor_B_in1, GPIO.HIGH)
        GPIO.output(self.motor_B_in2, GPIO.LOW)
        print("Turning left")
    
    def turn_right(self):
        """Turn the robot right."""
        self.stop()
        GPIO.output(self.motor_A_in1, GPIO.LOW)
        GPIO.output(self.motor_A_in2, GPIO.HIGH)
        GPIO.output(self.motor_B_in1, GPIO.LOW)
        GPIO.output(self.motor_B_in2, GPIO.HIGH)
        print("Turning right")
    
    def stop(self):
        """Stop all motors (but keep them running)."""
        GPIO.output(self.motor_A_in1, GPIO.LOW)
        GPIO.output(self.motor_A_in2, GPIO.LOW)
        GPIO.output(self.motor_B_in1, GPIO.LOW)
        GPIO.output(self.motor_B_in2, GPIO.LOW)
    
    def cleanup(self):
        """Clean up GPIO resources and stop motors completely."""
        self.stop()
        GPIO.cleanup()
        print("GPIO Cleanup completed")
    
    def __del__(self):
        """Destructor to ensure cleanup when object is destroyed."""
        try:
            self.cleanup()
        except:
            pass  # Ignore errors during cleanup in destructor
