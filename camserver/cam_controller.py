import io
import time
import picamera
from PIL import Image
import zbar
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from pymongo import MongoClient
import datetime

def insertAtDB(content,x,y):
    server = MongoClient("159.89.231.140")
    db = server.container
    post = { "contains":content,
             "x":x,
             "y":y,
             "datetime":datetime.datetime.utcnow()
             }
    detected = db.detected
    post_with_id = detected.insert_one(post).inserted_id
             

def readQR(frame):
    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(cv2_im)
    scanner = zbar.ImageScanner()
    pil = pil.convert('L')
    width, height = pil.size
    raw = pil.tobytes()
    # configure the reader
    scanner.parse_config('enable')
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        return symbol.data


def saveData(frame, x, x1, y, y1):
    qr_text = readQR(frame[y:y1, x:x1])
    if qr_text is not None:
        print('%s at coordinate %i, %i' % (qr_text, x, y))
        insertAtDB(qr_text,x,y)
        

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=5000, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.25)

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])
    # initialize the first frame in the video stream

firstFrame = None
# loop over the frames of the video
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the current frame and initialize the occupied/unoccupied
    # text
    # frame = camera.read()
    frame = image.array

    rawCapture.truncate(0)

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    changeFrame = None
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        saveData(frame, x, x + w, y, y + h)


    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    if changeFrame is not None:
        cv2.imshow("change", changeFrame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
# camera.release()
cv2.destroyAllWindows()


