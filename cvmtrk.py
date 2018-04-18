import cv2
import sys
(major_ver,minor_ver,subminor_ver)=(cv2.__version__).split('.')
print('cv version=',major_ver, minor_ver, subminor_ver)
if __name__ == '__main__' :
# Set up tracker.
# Instead of MIL, you can also use
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MULTI']
    tracker_type = tracker_types[6]

    if int(major_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MULTI':
	    tracker = cv2.MultiTracker_create()
    # Read video
    #video = cv2.VideoCapture("video/ksj3.mp4")
    video = cv2.VideoCapture(0)
 
    # Exit if video not opened.
    if not video.isOpened():
        print "Could not open video"
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print 'Cannot read video file'
        sys.exit()
    print('frame.shape=',frame.shape) 

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # create a CLAHE object (Arguments are optional).
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #gray = clahe.apply(gray)

    # Define an initial bounding box with face detector
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    #face_cascade = cv2.CascadeClassifier('lpb_cascade.xml') 
    #faces = face_cascade.detectMultiScale(frame, scaleFactor= 1.1, minNeighbors=8, minSize=(55, 55), flags=cv2.CASCADE_SCALE_IMAGE)
    print('type of faces = ', type(faces))
    no_faces = len(faces)
    while no_faces < 1:
        ok, frame = video.read()
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        no_faces = len(faces)
        print('no faces = ', no_faces)

    # Initialize multi-tracker with first frame and bounding box
    print('len(faces)=',len(faces))
    bbox = list(faces)
    no_faces = len(faces)
    for i in range(no_faces):
        print(faces[i])
        bbox[i] = tuple(faces[i])
        print('bbox[',i,']=',bbox[i])
        ok = tracker.add(cv2.TrackerBoosting_create(), frame, bbox[i])

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
        print('ok=',ok,'bbox=',bbox, 'no faces = ', len(bbox)) 
        if len(bbox) < 1: 
           faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        
        rno_faces = len(bbox)
        while not ok  :
	    ok, frame = video.read()
            ok, bbox = tracker.update(frame)
 	    rno_faces = len(bbox)
            print('ok=',ok,'bbox=',bbox, 'no faces = ', rno_faces) 

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # starting with here, treat with multiple face bbox
        for fbox in bbox:
        # Draw bounding box
            # Tracking success
            p1 = (int(fbox[0]), int(fbox[1]))
            p2 = (int(fbox[0] + fbox[2]), int(fbox[1] + fbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            cv2.putText(frame, "face"+str(i), (int(fbox[0]), int(fbox[1])), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
            # Tracking failure
            #cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
