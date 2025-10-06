import cv2
from motor_controller import MotorController
from image_processor import ImageProcessor


class RobotController:
    """
    Main controller class that coordinates motor control and image processing
    to implement line-following robot behavior.
    """
    
    def __init__(self):
        """Initialize the robot controller with motor and image processing components."""
        self.motor_controller = MotorController()
        self.image_processor = ImageProcessor()
        self.is_running = False
    
    def initialize(self):
        """
        Initialize all robot components.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        print("Initializing robot controller...")
        
        if not self.image_processor.initialize_camera():
            print("Failed to initialize camera")
            return False
        
        print("Robot controller initialized successfully")
        return True
    
    def start_line_following(self):
        """
        Start the main line-following loop.
        """
        if not self.initialize():
            return
        
        self.is_running = True
        print("Starting line following mode...")
        print("Press 'q' to quit")
        
        try:
            while self.is_running:
                self._process_frame()
                
                # Check for quit command
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("Program interrupted by user")
        finally:
            self.stop()
    
    def _process_frame(self):
        """
        Process a single frame and execute appropriate movement.
        """
        # Capture frame
        success, frame = self.image_processor.capture_frame()
        if not success:
            return
        
        # Preprocess frame
        gray, binary, mask = self.image_processor.preprocess_frame(frame)
        
        # Find line center
        center_x, center_y = self.image_processor.find_line_center(mask)
        
        # Determine movement command
        command = self.image_processor.determine_movement_command(center_x, center_y)
        
        # Execute movement command
        self._execute_command(command)
        
        # Check for intersection
        if self.image_processor.is_intersection(binary):
            print("Intersection detected - turning right")
            self.motor_controller.turn_right()
        
        # Draw debug information
        debug_image = self.image_processor.draw_debug_info(binary, center_x, center_y)
        
        # Display processed frame
        cv2.imshow('Processed Frame', debug_image)
    
    def _execute_command(self, command):
        """
        Execute the specified movement command.
        
        Args:
            command (str): Movement command to execute
        """
        if command == 'left':
            print("Turn Left")
            self.motor_controller.turn_left()
        elif command == 'forward':
            print("On Track!")
            self.motor_controller.forward()
        elif command == 'right':
            print("Turn Right")
            self.motor_controller.turn_right()
        elif command == 'stop':
            print("Stop")
            self.motor_controller.stop()
    
    def stop(self):
        """Stop the robot and cleanup resources."""
        print("Stopping robot...")
        self.is_running = False
        self.motor_controller.stop()
        self.image_processor.release_camera()
        cv2.destroyAllWindows()
        print("Robot stopped")
    
    def cleanup(self):
        """Clean up all resources."""
        self.stop()
        self.motor_controller.cleanup()
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass  # Ignore errors during cleanup in destructor
