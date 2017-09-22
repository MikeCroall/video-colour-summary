# Tested on Windows 10 using Python 3.6.0, with Numpy 1.13.1, and OpenCV 3.3.0

import sys
import numpy as np
try:
    import cv2
    print("Using OpenCV version " + cv2.__version__)
except ImportError:
    print("Could not import OpenCV")
    sys.exit(1)

file_name = "big_buck_bunny.mp4"

output_file = "output/{}.jpg".format(file_name)

vc = cv2.VideoCapture("video/{}".format(file_name))

if vc.isOpened():
    print("Video opened")

    keep_going, frame = vc.read()
    frame_count = 0
    rows, columns, channels = frame.shape
    total_pixels_in_frame = rows * columns
    total_frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

    if channels != 3:
        print("Video doesn't have exactly 3 colour channels, unexpected format")
        sys.exit(1)

    print("{} rows, {} columns, {} colour channels".format(rows, columns, channels))
    print("Reported frames: {}".format(total_frames))

    output_image = np.zeros((int(total_frames / 10), total_frames, 3), np.uint8)

    while keep_going:
        r, g, b = 0, 0, 0
        for y in range(rows):
            for x in range(columns):
                r += frame[y, x, 2]
                g += frame[y, x, 1]
                b += frame[y, x, 0]

        r /= total_pixels_in_frame
        g /= total_pixels_in_frame
        b /= total_pixels_in_frame
        r = round(r)
        g = round(g)
        b = round(b)

        output_image[:, frame_count] = (b, g, r)  # BGR, not RGB, because OpenCV

        keep_going, frame = vc.read()
        frame_count += 1
        if frame_count % 10 == 0:
            print("\rProgress: {}/{}".format(frame_count, total_frames), end="")

    vc.release()

    # frame_count was incremented regardless of keep_going, so check frame_count - 1
    if frame_count - 1 < total_frames:
        print("\nStopped at frame {}, cropping...".format(frame_count - 1))
        output_image = output_image[:, :frame_count-1]

    print("Saving output to {}".format(output_file))
    cv2.imwrite(output_file, output_image)

    cv2.imshow("output preview, press key to close", output_image)
    cv2.waitKey(0)

else:
    print("Video could not be opened")
