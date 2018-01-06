# Tested on Windows 10 using Python 3.6.0, with Numpy 1.13.1, and OpenCV 3.3.0

import sys, os, time  # Shouldn't fail, who runs python scripts on a non-existent system?

try:
    import numpy as np

    print("Using Numpy version {}".format(np.__version__))
except ImportError:
    print("Could not import Numpy, is it installed? Exiting...")
    sys.exit(1)

try:
    import cv2

    print("Using OpenCV version {}".format(cv2.__version__))
except ImportError:
    print("Could not import OpenCV, is it installed? Exiting...")
    sys.exit(1)


def strip_extension(file_name):
    base = os.path.basename(file_name)
    return os.path.splitext(base)[0]


def print_pre_video_commands():
    print("\nCommands (followed by enter to confirm)")
    print("\tv - load video file")
    print("\ti - load previously outputted image file")
    print("\tx - quit\n")


def print_video_processed_commands():
    print("\nCommands (on window, not in console this time)")
    print("\tm - merge all to single colour")
    print("\ts - select area to merge to single colour")
    print("\tx - quit")
    print("\nPress your chosen key on the image window\n")


def load_image(file):
    return cv2.imread("output/{}".format(file)), strip_extension(file)


def load_video(file):
    vc = cv2.VideoCapture("video/{}".format(file))

    if not vc.isOpened():
        print("Video could not be opened")
        return None
    else:
        print("Video opened")
        output_file = "output/{}.png".format(strip_extension(file))
        keep_going, frame = vc.read()
        frame_count = 1
        rows, columns, channels = frame.shape
        total_pixels_in_frame = rows * columns
        total_frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

        if channels != 3:
            print("Video doesn't have exactly 3 colour channels, unexpected format, exiting...")
            sys.exit(1)

        print("{} rows, {} columns, {} colour channels".format(rows, columns, channels))
        print("Reported frames: {}".format(total_frames))

        output_image = np.zeros((min(int(total_frames / 10), 200), total_frames, 3), np.uint8)
        start_time = time.time()

        while keep_going:
            print("\rProgress: {}/{} ({}%) Time elapsed: {} seconds".format(
                frame_count, total_frames, round(100 * frame_count / total_frames, 1), round(time.time() - start_time, 1)),
                end="")

            r, g, b = average_frame(frame)
            r = int(round(r))
            g = int(round(g))
            b = int(round(b))

            output_image[:, frame_count - 1] = (b, g, r)  # BGR, not RGB, because OpenCV

            keep_going, frame = vc.read()
            frame_count += 1

        vc.release()
        print()  # To prevent the Progress one line overwriting from being overwritten
        frame_count -= 1  # Account for final increment (could put it in an if keep_going: but that's slower than this)

        if frame_count < total_frames:
            print("Stopped at frame {}, cropping...".format(frame_count))
            output_image = output_image[:, :frame_count]  # Frame 1 at index 0, frame_count is 1 more than last index
            # (and the above splice is exclusive of the end index)

        print("Saving output to {}".format(output_file))
        cv2.imwrite(output_file, output_image)

        return output_image, strip_extension(file)


def merge_image(img, file_name):
    print("All pixels will be merged - although if output of this program only one row is needed")
    r, g, b = 0, 0, 0
    rows, columns, channels = img.shape

    output_image = np.zeros((400, 400, 3), np.uint8)

    if channels != 3:
        print("Image doesn't have exactly 3 colour channels, unexpected format, exiting...")
        sys.exit(1)

    r, g, b = average_frame(img)
    r = int(round(r))
    g = int(round(g))
    b = int(round(b))

    output_image[:, :] = (b, g, r)

    output_file = "merge/{} R{} G{} B{}.png".format(strip_extension(file_name), r, g, b)

    print("Saving output to {}".format(output_file))
    cv2.imwrite(output_file, output_image)

    cv2.imshow(output_file, output_image)


def average_frame(img):
    # img must be a numpy.array for the following code, which it always is in this script
    r = img[:, :, 2].mean()
    g = img[:, :, 1].mean()
    b = img[:, :, 0].mean()
    return r, g, b

def main():
    working_title = "no-file"
    working_image = None
    print_pre_video_commands()
    invalid_answer = True
    while invalid_answer:
        invalid_answer = False
        option = input("Option: ").lower().strip()
        if option == 'v':
            working_image, working_title = load_video(input("Video file to use: video/"))
        elif option == 'i':
            working_image, working_title = load_image(input("Image file to use: output/"))
        elif option == 'x':
            sys.exit(0)
        else:
            invalid_answer = True
            print_pre_video_commands()

    if working_image is None:
        print("Working image was unexpectedly null")
        sys.exit(1)
    else:
        keep_alive = True
        printed_commands = False
        while keep_alive:
            cv2.imshow("output preview, see console for commands", working_image)

            if not printed_commands:
                print_video_processed_commands()
                printed_commands = True

            key = cv2.waitKey(40) & 0xFF  # cv2.waitKey(0)

            if key == ord('x'):
                keep_alive = False
            elif key == ord('m'):
                merge_image(working_image, working_title)
                printed_commands = False
            elif key == ord('s'):
                print(
                    "Not yet implemented, for now use just the video/image section you want merged as input")  # TODO implement selection for merge
                # Automatically ignores invalid answers


if __name__ == "__main__":
    main()
