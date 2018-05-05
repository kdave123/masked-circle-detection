# masked-circle-detection
Mask specific colours and find circular objects using inRange

Detecting circular objects of different colors
(Range set for 3 colors Red,green and blue)


1. Set Color Range for hsv model
hsv model allows us to set exact range of colors to detect (color,lightness,darkness)

2. Detect specifed color inRange and mask it

3. Apply Basic Morphological operations erode, dilate to remove noise and widen mask

4. Draw the circle if circular object detected of respective color around object

5. loop activites( masking, drawing specific colored circle if detected) for all detected Red, green, blue circular objects seperately.


Program starts with taking input frame and converting it to hsv model and one by one mask for each color(R-G-B) and check circular object for all three ranges (Red,green ,blue)
(Mask for red check circles than mask for green check circles draws if detected *loops over*). Detects Circles and tracks each one seperately.
