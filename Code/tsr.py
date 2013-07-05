import Image, cv
from colorsegm import *
from hough import *
from dstTransform import *
from dstCorrelation import *
import os

vid = cv2.VideoCapture("../Videos/street.mp4")
# vid = cv2.VideoCapture("../Videos/street2.avi")

nFrames = int(vid.get(cv.CV_CAP_PROP_FRAME_COUNT))
fwidth = int(vid.get(cv.CV_CAP_PROP_FRAME_WIDTH))
fheight = int(vid.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter("../Results/detection.avi", cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'), 29, (fwidth, fheight), 1)
aspect_ratio= fwidth*1.0/fheight

element1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
element2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
match_candidates= []

img = cv2.imread("template.jpg")
dst = getDstTrns(img)

for i in range(nFrames):
	cv_im = vid.read()[1]
	
	# Preprocess Image
	h, s = segmentRed(cv_im)
	h = cv2.dilate(h, element1)
	h = cv2.erode(h, element2)
	draw_im = cv_im
	
	# Find circles on edges
	edgeh = cv2.Canny(h, 128, 200)
	edgeCandidates = getCandidates(edgeh)
	# cur_dst = getDstTrns(cv_im)

	# Detect circles in the frame
	candidates = getCandidates(h)
	match_candidates, draw_im = getBestCandidates(candidates, edgeCandidates, match_candidates, cv_im)

	cv2.imwrite("../Temp/frame_"+str(i)+".jpg", draw_im)
	writer.write(draw_im)
	
	print "Processed frame", i