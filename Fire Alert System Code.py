import cv2                                                  # To access camera.
import numpy as np                                          # To dectect the flame colour.
import playsound                                            # To play the Alert music
from twilio.rest import Client                              # To send message.


Fire_Reported = 0
Alarm_Status = False

def message():                                              # Message that will be sent to phone when fire will dectect.
    account_sid = "Your Account SID as in twilio"
    auth_token = "Your authority token as in twilio"
    client = Client(account_sid, auth_token)
    client.messages.create(from_="Sender Number with country code", body="FIRE!!! FIRE!!! FIRE!!!", to=["Receiver Number with country code"])




def play_audio():                                           #Alert music
    playsound.playsound("alert.wav",True)                  


video = cv2.VideoCapture(0)                                 # All camera to capture through pre-recorded or LIVE video.

while True:
    ret, frame = video.read()                               # To read the video.
    frame = cv2.resize(frame, (800,600))                    # Advesting the size of video.
    blur = cv2.GaussianBlur(frame,(15,15),0)                # Making video little bit blur.
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)             # HSV for detecting proper colour of flame.

    lower = [18,50,50]                                      # HSV color code of lower and upper portions of flame. 
    upper = [35,255,255] 

    lower = np.array(lower,dtype='uint8')                   # Converted the colours in numpy format.
    upper = np.array(upper,dtype='uint8')

    mask = cv2.inRange(hsv,lower,upper)                     # mask to search lower and upper colour of flame in HSV format.
    output = cv2.bitwise_and(frame,hsv,mask=mask)           # Storing the result of mask in output.

    size = cv2.countNonZero(mask)                           # To calculate the size of flame as per required.
    if int(size) > 500:
        Fire_Reported =Fire_Reported + 1                    # If fire detected then it increase the value of Fire_Dectected by +1.

        if Fire_Reported >= 1:
            if Alarm_Status == False:
                message()
                play_audio()
                Alarm_Status = True
           
    if ret == False:
        break

    cv2.imshow("Fire Security", output)                     # Output shown in frame.

    if cv2.waitKey(1) & 0xFF == ord("q"):                   # To stop the system on clicking "q"
        break


cv2.destroyAllWindows()
video.release()
