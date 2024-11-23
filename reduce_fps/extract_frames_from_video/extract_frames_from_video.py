import cv2
import os
import numpy as np

# Configuration variables
input_video = '../data/output_video.mov'  # Replace with your video file path
output_dir = '../data/extracted_frames'  # Directory where frames will be saved
change_threshold = 10.0            # Percentage change threshold (configurable)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(input_video)

# Check if the video was successfully opened
if not cap.isOpened():
    print(f"Error: Cannot open video file {input_video}")
    exit()

previous_saved_frame = None
frame_count = 0
saved_frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    save_frame = False

    if previous_saved_frame is None:
        # Save the first frame by default
        save_frame = True
    else:
        # Calculate the percentage difference between current frame and previous saved frame
        diff = cv2.absdiff(frame, previous_saved_frame)
        non_zero_count = np.count_nonzero(diff)
        total_pixels = diff.size  # Total number of elements (height * width * channels)
        change_ratio = (non_zero_count / total_pixels) * 100

        if change_ratio > change_threshold:
            save_frame = True

    if save_frame:
        # Construct the filename for each frame
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:05d}.png')
        # Save the frame as an image file
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1
        # Update the previous saved frame
        previous_saved_frame = frame.copy()

    frame_count += 1

# Release the video capture object
cap.release()

print(f"Processed {frame_count} frames.")
print(f"Saved {saved_frame_count} frames to the folder '{output_dir}'.")
