# video colour summary

## Summarise a video into a single image
This script does not take shortcuts. Every pixel, of every frame, is taken into account.

Tested with
- `Windows 10`
- `Python 3.6.0`
- `Numpy 1.13.1`
- `OpenCV 3.3.0`
- `Only the provided Big Buck Bunny snippet as mp4`

### Getting Started
1. Place your video file in the `video` folder
2. Run `main.py`, and follow the printed menu system in the console
3. While processing, be patient - **it isn't very fast!** (It only looks at *every single pixel* of *every single frame*)
4. Any saved images will be in the `output` folder, having been announced in the console at the time of saving
5. Press `x`, as the menu states, to exit the script cleanly

#### Please Note
Generated files are named relative to the input file - to avoid files being overwritten, ensure every input file is named uniquely

#### Thanks
Big Buck Bunny Test Video Courtesy of https://peach.blender.org/
