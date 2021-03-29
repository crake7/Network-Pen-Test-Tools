import cv2
import os

ROOT  = '/home/kali/Documents/BlackHatPython2/virtual-env1/projects-python/pcap-processing/pictures'
FACES  = '/home/kali/Documents/BlackHatPython2/virtual-env1/projects-python/pcap-processing/faces'
TRAIN = '/home/kali/Documents/BlackHatPython2/virtual-env1/projects-python/pcap-processing/training'

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('.JPG'):
            continue
        fullname = os.path.join(srcdir, fname)
        newname  = os.path.join(tgtdir, fname)
        img = cv2.imread(fullname)
        if img is None:
            continue
        
        gray     = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load a detector(classifier trained in advance to detect faces in a front-facing orientation)
        training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml')
        cascade  = cv2.CasscadeClassifier(training)
        rects    = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            # Classifier return the coordinates of a rectangle to where the face is
            if rects.any():
                print('Got a selfie')
                rects[:, 2:] += rects[:, :2]
        
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue

        # highlight the faces in the image
        for x1, y1, x2, y2 in rects:
            # Coordinates(x2=x1+width, y2=y1+height)
            cv2.rectangle(img, (x1, y1), (x2,y2), (127,255,0), 2)
        cv2.imwrite(newname, img)

if __name__ == '__main__':
    detect()
    