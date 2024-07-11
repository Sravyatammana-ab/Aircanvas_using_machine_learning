import cv2
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the image
image_path = os.path.join(script_dir, 'CLEAR ALL.png')

# Load the image from file
image = cv2.imread(image_path)

# Check if image is None (failed to load)
if image is None:
    print("Error: Failed to load image.")
else:
    # Check if image has valid dimensions
    if image.shape[0] > 0 and image.shape[1] > 0:
        # Create a named window with a specific size
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image', 800, 600)  # Set window size (width, height)
        
        # Display the image
        cv2.imshow('Image', image)
        cv2.waitKey(0)  # Wait indefinitely until a key is pressed
        cv2.destroyAllWindows()  # Close all OpenCV windows
    else:
        print("Error: Image has invalid dimensions.")


