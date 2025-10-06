import cv2
import numpy as np


class ImageProcessor:
    """
    Handles computer vision operations including video capture,
    image processing, and intersection detection.
    """
    
    def __init__(self, camera_index=0):
        """
        Initialize the image processor with camera configuration.
        
        Args:
            camera_index (int): Camera device index (default: 0)
        """
        self.camera_index = camera_index
        self.cap = None
        self.intersection_threshold = 0.80
        self.tracking_center_min = 210
        self.tracking_center_max = 430
        
    def initialize_camera(self):
        """
        Initialize and configure the camera.
        
        Returns:
            bool: True if camera initialized successfully, False otherwise
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Error: Could not open video source.")
            return False
        else:
            width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(f"Camera initialized - Resolution: {width}x{height}")
            return True
    
    def capture_frame(self):
        """
        Capture a single frame from the camera.
        
        Returns:
            tuple: (success, frame) where success is bool and frame is numpy array
        """
        if self.cap is None:
            return False, None
        
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame.")
            return False, None
        
        return True, frame
    
    def preprocess_frame(self, frame):
        """
        Preprocess the frame for line tracking.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            tuple: (grayscale, binary, mask) processed images
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Create binary image
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
        # Create mask for white pixels
        low_b = np.uint8([200, 200, 200])  # Lower bound for white
        high_b = np.uint8([255, 255, 255])  # Upper bound for white
        mask = cv2.inRange(frame, low_b, high_b)
        
        return gray, binary, mask
    
    def find_line_center(self, mask):
        """
        Find the center of mass of white pixels in the mask.
        
        Args:
            mask: Binary mask image
            
        Returns:
            tuple: (center_x, center_y) coordinates of line center, or (None, None) if not found
        """
        contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Find the largest contour (main line)
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return cx, cy
        
        return None, None
    
    def is_intersection(self, binary_image):
        """
        Detect if the current frame shows an intersection.
        
        Args:
            binary_image: Binary processed image
            
        Returns:
            bool: True if intersection detected, False otherwise
        """
        h, w = binary_image.shape[:2]
        
        # Define region of interest (middle right section in 3x3 grid)
        roi = binary_image[int((1/3) * h):int((2/3) * h), int((2/3) * w):w-1]
        roi_area = roi.shape[0] * roi.shape[1]
        
        # Display ROI for debugging
        cv2.imshow("Region of Interest", roi)
        
        # Count white and black pixels in ROI
        number_of_black_pix = np.sum((roi >= 0) & (roi <= 50))
        number_of_white_pix = np.sum((roi >= 200) & (roi <= 255))
        
        # Calculate white pixel density
        white_pixel_density = number_of_white_pix / roi_area
        
        # Check if density exceeds threshold
        return white_pixel_density > self.intersection_threshold
    
    def determine_movement_command(self, center_x, center_y):
        """
        Determine movement command based on line center position.
        
        Args:
            center_x: X coordinate of line center
            center_y: Y coordinate of line center
            
        Returns:
            str: Movement command ('left', 'forward', 'right')
        """
        if center_x is None or center_y is None:
            return 'stop'
        
        if center_x >= self.tracking_center_max:
            return 'left'
        elif self.tracking_center_min < center_x < self.tracking_center_max:
            return 'forward'
        elif center_x <= self.tracking_center_min:
            return 'right'
        else:
            return 'stop'
    
    def draw_debug_info(self, binary_image, center_x, center_y):
        """
        Draw debugging information on the image.
        
        Args:
            binary_image: Binary image to draw on
            center_x: X coordinate of line center
            center_y: Y coordinate of line center
            
        Returns:
            numpy array: Image with debug information drawn
        """
        if center_x is not None and center_y is not None:
            cv2.circle(binary_image, (center_x, center_y), 5, (0, 0, 0), -1)
        
        return binary_image
    
    def release_camera(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print("Camera released")
    
    def __del__(self):
        """Destructor to ensure camera cleanup."""
        self.release_camera()
        cv2.destroyAllWindows()
