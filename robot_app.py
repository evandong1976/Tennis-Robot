"""
Main application entry point for the line-following robot.
This module provides a clean interface to run the robot application.
"""

from robot_controller import RobotController


class RobotApp:
    """
    Main application class for the line-following robot.
    Handles application lifecycle and provides a clean interface.
    """
    
    def __init__(self):
        """Initialize the robot application."""
        self.robot_controller = RobotController()
        self.is_running = False
    
    def run(self):
        """
        Run the robot application.
        """
        print("=== Line Following Robot Application ===")
        print("Initializing robot components...")
        
        try:
            self.is_running = True
            self.robot_controller.start_line_following()
        except Exception as e:
            print(f"Error during robot operation: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """
        Shutdown the robot application and cleanup resources.
        """
        print("Shutting down robot application...")
        self.is_running = False
        self.robot_controller.cleanup()
        print("Robot application shutdown complete")


def main():
    """
    Main entry point for the robot application.
    """
    app = RobotApp()
    app.run()

if __name__ == "__main__":
    main()
