import h5py
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
from matplotlib import use as matplotlib_backend
from pathlib import Path
matplotlib_backend("TkAgg")

# OPEN FILE
Tk().withdraw() 
directory = Path(askdirectory(title="Select data directory", initialdir='analysis'))
print(f"Analyzing: {directory}")
f = h5py.File(directory / 'height_maps.hdf5', 'r')

# DATA
fps         = int(f['fps'][0])
height_maps = f['height_maps']
cal         = f['calibration_factor'][0]

shape = height_maps[0].shape

# PLAY VIDEO
plt.ion()

fig, ax = plt.subplots()
for i, frame in enumerate(height_maps):
    ax.clear()
    ax.imshow(frame, cmap='RdBu', vmin=-4e-3, vmax=4e-3)
    ax.vlines(np.linspace(shape[0]/10, 9*shape[0]/10, 5), 0, shape[0], colors="k")
    ax.hlines(np.linspace(shape[0]/10, 9*shape[0]/10, 5), 0, shape[0], colors="k")
    ax.set_xlim(0, shape[0])
    ax.set_ylim(0, shape[0])
    fig.canvas.draw()
    fig.canvas.flush_events()  

plt.ioff()

f.close()

import cv2
 
# Open the video file
cap = cv2.VideoCapture("C:/Users/ssabb/Downloads/input.mp4")
 
# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
 
# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (frame_width, frame_height))
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break
 
    # Write the frame to the output video file
    out.write(frame)
 
    # Display the frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()