# Real-Time-Vandalism-Detector

## Objective 

- To build a light-weight real-time vandalism detection with Image processing techniqies which can be run on modest processors like Raspberry-pi. 
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
- Make sure you have all the python libraries installed. (I suggest installing Anaconda) 
- On Windows, use command prompt to run ''' python vandalism-detector '''
  - #### Arguments
    - ''' python vandalism-detector -v "path to video file" '''
    - ''' python vandalism-detector -a "Monitoring Area size " '''
    
## Acknowledgements
[PyImageSearch](https://www.pyimagesearch.com/) tutorials have been extremely useful for utilizing various python libraries.
