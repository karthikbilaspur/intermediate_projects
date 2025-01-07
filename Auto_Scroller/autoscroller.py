import cv2
import numpy as np
import pyautogui
import time
from scipy.ndimage import gaussian_filter

# Set the color range for the scroll bar
lower_color = np.array([0, 0, 200])  # blue
upper_color = np.array([100, 100, 255])  # blue

# Set the region of interest (ROI) for the screen capture
x, y, w, h = 100, 100, 800, 600

# Set the scrolling speed
scrolling_speed = 10

# Set the smoothing factor
smoothing_factor = 0.5

# Initialize the previous scroll bar position
previous_scroll_bar_position = None

# Initialize the frame counter
frame_counter = 0

# Initialize the scroll bar position history
scroll_bar_position_history = []

while True:
    # Capture the screen
    screen = pyautogui.screenshot(region=(x, y, w, h))

    # Convert the screen to OpenCV format
    frame = np.array(screen)

    # Apply Gaussian filter to reduce noise
    frame = gaussian_filter(frame, sigma=1)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Detect the color of the scroll bar
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply morphological operations to refine the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find the contours of the detected color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours and find the one with the largest area
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # If a contour is found, track its center and simulate scrolling
    if max_contour is not None:
        M = cv2.moments(max_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Smooth the scroll bar position using exponential smoothing
        if previous_scroll_bar_position is not None:
            cx = int(smoothing_factor * cx + (1 - smoothing_factor) * previous_scroll_bar_position)
        previous_scroll_bar_position = cx

        # Add the current scroll bar position to the history
        scroll_bar_position_history.append(cx)

        # Simulate scrolling
        pyautogui.moveTo(cx, cy)
        pyautogui.scroll(-scrolling_speed)  # scroll down

    # Display the output
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    # Exit on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Limit the frame rate to 30 FPS
    frame_counter += 1
    if frame_counter % 30 == 0:
        time.sleep(1 / 30)

    # Save the scroll bar position history to a file
    if len(scroll_bar_position_history) > 100:
        np.savetxt('scroll_bar_position_history.txt', scroll_bar_position_history)
        scroll_bar_position_history = []

# Release resources
cv2.destroyAllWindows()