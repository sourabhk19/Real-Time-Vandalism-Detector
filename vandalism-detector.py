from imutils.video import FileVideoStream
from imutils.video import WebcamVideoStream
import argparse
import imutils
import cv2
import time
import numpy as np
from skimage.measure import compare_ssim as ssim
def sliding_window(image, stepSize, windowSize):
	for y in xrange(0, image.shape[0], stepSize):
		for x in xrange(0, image.shape[1], stepSize):
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
def compare(a,b):
    count=0
    WHITE=[255,255,255]
    bordertype=cv2.BORDER_CONSTANT
    (winW, winH) = (30, 30)
    a=cv2.copyMakeBorder( a,winH, winH, winW, winW, bordertype, value=WHITE)
    b=cv2.copyMakeBorder( b, winH, winH, winW, winW, bordertype, value=WHITE)
    for (x, y, window) in sliding_window(a, stepSize=30, windowSize=(winW, winH)):
		if window.shape[0] != winH or window.shape[1] != winW:
			continue
                Box1=a[int(y):int(y+winH),int(x):int(x+winW)]
                Box2=b[int(y):int(y+winH),int(x):int(x+winW)]
                s =ssim(Box1,Box2)
                clone = b.copy()
		cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2) 
		#cv2.imshow("Window", clone)
		#cv2.waitKey(1)
		if(s<0.6):
                   count+=1
    return count
def selectRoi(frame):
    r = cv2.selectROI(frame)
    imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    return r
def Begin(Type):
        avg = None
        count=0
        flag=0
        cnt=0
        first=None
        detectflag=None
        while True:
                if Type==0:
                    frame=vs.read()
                elif Type==1:
                    if vs.more()==False:
                        break
                    frame=vs.read()
                if first is None:
                        frame = imutils.resize(frame, width=500)
                        r=selectRoi(frame)
                        frameroi=frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
                        grayf= cv2.cvtColor(frameroi, cv2.COLOR_BGR2GRAY)
                        grayfb = cv2.GaussianBlur(grayf, (21, 21), 0)
                        first=1
                text="Unoccupied"
                frame = imutils.resize(frame, width=500)
                frameroi=frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
                gray= cv2.cvtColor(frameroi, cv2.COLOR_BGR2GRAY)
                grayb = cv2.GaussianBlur(gray, (5, 5), 0)
                if avg is None:
                        print("[INFO] starting background model...")
                        avg = grayb.copy().astype("float")
                        continue
                cv2.accumulateWeighted(grayb, avg, 0.6)
                frameDelta = cv2.absdiff(grayb, cv2.convertScaleAbs(avg))
                thresh = cv2.threshold(frameDelta, 10, 255,
                        cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]                            
                for c in cnts:
                        (x, y, w, h) = cv2.boundingRect(c)
                        if w<20 or h<20:
                                continue
                        cv2.rectangle(frameroi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Occupied"
                        
                if len(cnts)!=0:
                        cnt+=1
                        flag=1
                        count=0
                        
                if len(cnts)==0:
                        count+=1
                if count>=100:
                    if flag==0:
                        grayf=gray
                        cnt=0
                    else: 
                                flag=0
                                if cnt>=50:
                                        grayfb=cv2.GaussianBlur(grayf, (21, 21), 0)
                                        grayb = cv2.GaussianBlur(gray, (21, 21), 0)
                                        frameD = cv2.absdiff(grayb, grayfb)
                                        threshd = cv2.threshold(frameD, 35, 255,cv2.THRESH_BINARY)[1]
                                        threshd = cv2.dilate(threshd, None, iterations=2)
                                    
                                        #cv2.imshow("thred",threshd)
                                        cntsd = cv2.findContours(threshd.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                                        cntsd = cntsd[0] if imutils.is_cv2() else cntsd[1]
                                        fram=frameroi.copy()
                                        #cv2.drawContours(fram, cntsd, -1, (0,255,0), 3)
                                        for c in cntsd:
                                                (x, y, w, h) = cv2.boundingRect(c)
                                                area=w*h
                                                if area<81:
                                                        continue
                                                
                                                cv2.rectangle(fram, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                image1=grayf[int(y):int(y+h),int(x):int(x+w)]
                                                image2=gray[int(y):int(y+h),int(x):int(x+w)]
                                                s=ssim(image1,image2)
                                                if  s<0.4 :
                                                    if detectflag==None:
                                                            print("object is detected")
                                                            detectflag=1
                                                    cv2.rectangle(frameroi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                    continue
                                                if area>2500:
                                                        
                                                        c=compare(image1,image2)
                                                        if c>=3:
                                                            if detectflag==None:
                                                                    print("object is detected")
                                                                    detectflag=1
                                                            cv2.rectangle(frameroi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                #cv2.imshow("Security", frame
                                        detectflag=None      
                                             
                                        cv2.imshow("Security", frameroi)
                                        #cv2.imshow("Sec", fram)
                                        cv2.waitKey(1)
                                        
                cv2.imshow("Security Feed", frameroi)
                cv2.imshow("thresh",thresh)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                        break



ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())


if args.get("video", None) is None:
	#"rtsp://192.168.1.235/h264"
	vs = WebcamVideoStream(src=0)
	vs.start()
	time.sleep(1)
	Begin(0)
	
else:
	
	vs = FileVideoStream(args["video"])
	vs.start()
	time.sleep(1)
        Begin(1)
#vs.release()
cv2.destroyAllWindows()
vs.stop()
