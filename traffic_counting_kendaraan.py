# #################################################################################### #
# README (Cofigurasi dan Cara Pakai)                                                   #         
# Program ini akan otomatis memakai VideoStream/WebCam sebagai parameter input         #
# F5 untuk mengeksekusi program dengan debbuging                                       # 
# Ctrl + F5 untuk mengeksekusi program tanpa debbuging                                 #     
# NOTE :                                                                               #   
# All syntax has been tested in Micosoft Visual Code                                   # 
# #################################################################################### #
# 
# Untuk membaca input file video 
#   Gunakan perintah ini :
# python traffic_counting_kendaraan.py --input videos/namavideo_01.mp4
#
# Untuk merekam video sebagai data train dan menyimpan di penyimpanan (disk/folder) 
#   Gunakan perintah ini :
# python traffic_counting_kendaraan.py --output output/namavideo_output.avi 
#
# Kombinasi untuk membaca file input dan merekamnya 
#   Gunakan perintah ini :
# python traffic_counting_kendaraan.py --input videos/namavideo_01.mp4 --output output/output_01.avi

#import library 
from __future__ import print_function
from imutils.video import WebcamVideoStream
from blobs.blob2 import Blob, get_centroid
from imutils.video import VideoStream
from imutils.video import FPS
from collections import OrderedDict
import contextlib
import datetime
import argparse
import imutils
import time
import os
import cv2
import math
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	help="pilih tempat penyimpanan untuk input file video")
ap.add_argument("-o", "--output", type=str,
    help="pilih tempat penyimpanan untuk output file video")
ap.add_argument("-p", "--picamera", type=int, default=-1,
    help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
	help="# of skip frames between detections")
args = vars(ap.parse_args())

# open log file
log_file_name = 'log.txt'
with contextlib.suppress(FileNotFoundError):
    os.remove(log_file_name)
log_file = open(log_file_name, 'a')
log_file.write('vehicle_id, count, datetime\n')
log_file.flush()

# initialize the video stream and allow the cammera sensor to warmup
# if a video path was not supplied, grab a reference to the webcam
if not args.get("input", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, grab a reference to the video file
else:
	print("[INFO] opening video file...")
	vs = cv2.VideoCapture(args["input"])

#force 640x480 webcam resolution
#cap.set(3,640)
#cap.set(4,480)

# initialize the video writer (we'll instantiate later if need be)
writer = None

# initialize the frame dimensions (we'll set them as soon as we read
# the first frame from the video)
W = None
H = None

#use trained cars XML classifiers
blobs = OrderedDict()
blob_id = 1
frame_counter = 0
DETECTION_FRAME_RATE = 80
MAX_CONSECUTIVE_TRACKING_FAILURES = 15

# Buat fungsi blob dari 
def get_bounding_boxes(frame):
    fullbody_cascade = cv2.CascadeClassifier('cascade_baru_fix.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _bounding_boxes = fullbody_cascade.detectMultiScale(gray)
    return _bounding_boxes

# initialize trackers and create new blobs
frame = vs.read()
frame = frame[1] if args.get("input", False) else frame
initial_bboxes = get_bounding_boxes(frame)
for box in initial_bboxes:
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(box))
    _blob = Blob(box, tracker)
    blobs[blob_id] = _blob

totalFrames = 0
fps = FPS().start()

#read until video is completed
while True :
    alamat='http://localhost/PROGRAM_OPICK/index.php'

    # frame_counter = frame_counter + 1
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()

    # Cek input dari argsparse valid atau tidak
    frame = frame[1] if args.get("input", False) else frame
    if frame is None :
        print("kamera tidak terdeteksi")
        break
	# if we are viewing a video and we did not grab a frame then we
	# have reached the end of the video
    if args["input"] is not None and frame is None:
        break        
    frame = imutils.resize(frame, width=640)

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    f_height, f_width, _ = frame.shape
    # if we are supposed to be writing a video to disk, initialize
    # the writer
    if args["output"] is not None and writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 30,
            (W, H), True)
    # set counting line
    cl_y = round(4 / 5 * f_height)
    counting_line = [(0, cl_y), (f_width, cl_y)]
    vehicle_count = 0
    #convert video into gray scale of each frames
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # draw the timestamp on the frame
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 0, 255), 1)

        
# #################################################################################### #
    # update trackers
    for _id, blob in list(blobs.items()):
        success, box = blob.tracker.update(frame)
        if success:
            blob.num_consecutive_tracking_failures = 0
            blob.update(box)

            # draw and label bounding boxes
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'kendaraan_' + str(_id), (x, y - 2), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            blob.num_consecutive_tracking_failures += 1

        if blob.num_consecutive_tracking_failures >= MAX_CONSECUTIVE_TRACKING_FAILURES:
            del blobs[_id]

            # count vehicles
            if blob.centroid[1] >= cl_y and not blob.counted:
                blob.counted = True
                vehicle_count += 1

                # log count data to a file (vehicle_id, count, datetime)
                _row = '{0}, {1}, {2}\n'.format('kendaraan_' + str(_id), vehicle_count, datetime.datetime.now())
                log_file.write(_row)
                log_file.flush()     

    # rerun detection, add new blobs 
    if frame_counter >= DETECTION_FRAME_RATE:
        boxes = get_bounding_boxes(frame)
        
        for box in boxes:
            box_centroid = get_centroid(box)
            match_found = False
            for _id, blob in blobs.items():
                dist = np.linalg.norm(np.array(box_centroid) - np.array(blob.centroid))
                if dist <= 5: # 5 pixels
                    match_found = True
                    tracker = cv2.TrackerKCF_create()
                    tracker.init(frame, tuple(box))
                    blob.update(box, tracker)
                    break                    

            if not match_found:
                blob_id += 1
                tracker = cv2.TrackerCSRT_create()
                tracker.init(frame, tuple(box))
                _blob = Blob(box, tracker)
                blobs[blob_id] = _blob
            
            frame_counter = 0
    #detect cars in the video
    # cars = car_cascade.detectMultiScale(gray, 1.1, 1)   

    # #to draw arectangle in each cars 
    # for (x,y,w,h) in cars:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
    #     roi_gray = gray[y:y+h, x:x+w]
    #     roi_color = frame[y:y+h, x:x+w]

    # #draw the processing cars detect
    # counting = len(cars)
    # #if counting >= str(frame_no) :
    # counter = sum(map(len,cars))
    # count_cars = ('Processing %d : mobil terdeteksi : [%s]' % (frame_no,counting))
    # cv2.putText(frame, count_cars, (1, frame.shape[0] - 1), cv2.FONT_HERSHEY_SIMPLEX,
        # 0.35, (0, 255, 0), 1)            
    #print('Processing %d : mobil terdeteksi : [%s]' % (frame_no, len(cars)))        
    #print(sum(map(len,cars)))    
    #print(cars)
# #################################################################################### #


    # draw counting line
    cv2.line(frame, counting_line[0], counting_line[1], (0, 255, 0), 3)

    # display vehicle count
    cv2.putText(frame, 'Jumlah Mobil: ' + str(vehicle_count), (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
	
    # check to see if we should write the frame to disk
    if writer is not None:
        writer.write(frame)

    # show the output frame
    cv2.imshow("Traffic Counter System", frame)
    key = cv2.waitKey(1) & 0xFF
    frame_counter += 1

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break

    # update the FPS counter
    fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] rata-rata total FPS: {:.2f}".format(fps.fps()))
# check to see if we need to release the video writer pointer
if writer is not None:
	writer.release()

# if we are not using a video file, stop the camera video stream
if not args.get("input", False):
	vs.stop()
# otherwise, release the video file pointer
else:
	vs.release()
#close all the frames
cv2.destroyAllWindows()
