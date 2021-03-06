# Real-Time-Vandalism-Detector

![image 1](https://github.com/sourabhk19/Real-Time-Vandalism-Detector/blob/master/Readme_images/Vandalism.jpg)

## Objective 

- To build a light-weight real-time vandalism detector with Image processing techniques which can be run on small processors like Raspberry-pi. 
- The input is real-time surveillance footage.
- The system should immediately alert the user if vandalism is detected on the property monitored.

## Methodology
- We read each frame of the video in a parallel pipeline different from the image processing pipeline (Increases Frames per second for real-time operation).
- We apply Image enhancement techniques for removing noise, and converting the frame to gray scale. 
- To identify motion,we use Background Subtraction with Weighted Average.
- We detect contours if any in the image, and keep a contour counter.
- Once a buffer time and countour counter exceeds the threshold the frame is passed to detect Vandalism on the property.
- Sliding Window Approach is used to extract small windows which could potentially contain Vandalism.
- Every window is passed to SSIM and if the value is below a set threshold, alert is generated.

## How to Run
- Install Imutils, scikit-learn, numpy and OpenCV. (I suggest using Anaconda) 
- After downloading [this](https://github.com/sourabhk19/Real-Time-Vandalism-Detector/blob/master/vandalism-detector.py), Use command prompt to run ` python vandalism-detector.py `
  - #### Arguments
    - For passing a video file, use  ` python vandalism-detector.py -v "path to video file" `
    - For passing size of Monitoring Area, use  ` python vandalism-detector.py -a "Monitoring Area size " `. Default size is 500.
    - If no arguments are passed, the program automatically uses Webcam as default video source.
## References
- [SSIM](https://en.wikipedia.org/wiki/Structural_similarity)
- [Background Subtraction](https://en.wikipedia.org/wiki/Foreground_detection#Background_subtraction)
- [OpenCV documentation](https://docs.opencv.org/master/)
## Acknowledgements
[PyImageSearch](https://www.pyimagesearch.com/) tutorials have been extremely useful for utilizing various python libraries.
