# Detect Red green and Blur Circles
# mask image is displayed for understanding purpose
import numpy as np
import argparse
import imutils
import cv2
import operator


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")

# Set default=0 to disable tail (deque)
ap.add_argument("-b", "--buffer", type=int, default=10,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries for the "green" "red" and "blue"
# Change the Values as per Requirement
# objects in the HSV model

redLower = (0, 100, 100)
redUpper = (10, 255, 255)

redLower2 = (160, 100, 100)
redUpper2 = (179, 255, 255)

# Kd's
#greenLower = (29, 100, 100)
#greenUpper = (50, 255, 255)


blueLower = (100, 100, 100)
blueUpper = (140, 255, 255)

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Load lower and upper boundaries into colorBoundaries array we later iterate it to find Objects of different colors
colorBoundaries = [[redLower, redUpper], [redLower2, redUpper2], [greenLower, greenUpper], [blueLower, blueUpper]]
#colorBoundaries = [[greenLower, greenUpper],[blueLower,blueUpper]]
print(colorBoundaries)

# If video path is not in arguments then start webcam

if not args.get("video", False):
    camera = cv2.VideoCapture(0)

else:
    camera = cv2.VideoCapture(args["video"])

# Main loop to captures frames and Process it. Will end if "q" is pressed
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we passed a video and we did not grab a frame,
    # It's end of video so we break (quit)
    if args.get("video") and not grabbed:
        break
    # Resizing frame, Apply Gaussian Blur to remove noise, Convert it to the HSV

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (53, 53), 69)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for lowers, uppers in colorBoundaries:
    #for i in range(5):
        #lowers = np.array([i,100,100])
        #uppers = np.array([i+36,255,255])
        mask = cv2.inRange(hsv, lowers, uppers)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # Show the mask  processing
        cv2.imshow("OUTPUT FRAME", mask)
        key = cv2.waitKey(1) & 0xFF

        # Find Circles
        countours = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,10,param1=1,param2=10, minRadius=10)
        try:
            countours = np.round(countours[0, :]).astype("int")

            # Go in if atleast one Circle was found
            if len(countours) > 0:
                # find the largest circle in the mask
                x ,y ,radius = max(countours, key=operator.itemgetter(2))
                #print(x,y,radius)

                # Draw circle of color depending on round object
                if lowers[0] == 0 or lowers[0] == 160:
                    cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                if lowers[0] == 100:
                    cv2.circle(frame, (x, y), radius, (255, 0, 0), 2)
                if lowers[0] == 29:
                    cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)

        except TypeError:
            print("Circles not found")

    # Show the frame after processing
    cv2.imshow("DetectedCircles",frame)
    key = cv2.waitKey(1) & 0xFF
    # If 'q' key is pressed, Exit Loop
    if key == ord("q"):
        break

# Release camera and close windows
camera.release()
cv2.destroyAllWindows()