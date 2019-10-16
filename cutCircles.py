"""Cut Circles script.

Cuts circles on frames based on three different mouse clicks. Images already processed are moved to another folder. All file paths must be edited on code, for now.

Usage:
    python cutCircles.py <image/video>

Note that, for now, the image path must be changed on the code. A future version will be implemented, with args.
"""
import cv2
import numpy as np
import sys
import os
import glob as gl

if len(sys.argv) <= 1:
    print("Axlecutter script.\n")
    print("Cuts circles on frames based on three different mouse clicks. Images already processed are moved to another folder. All file paths must be edited on code, for now.\n")
    print("Usage:\n")
    print("python cutCircles.py <image/video>\n\n")
    exit(1)

# Paths
# video_src = "D:\\Videos\\Truck\\Lateral\\Balanca\\20160927100754-550.MP4"
img_src = "D:\\Data\\Images\\Truck"
img_dest = "D:\\Data\\Images\\Murilo1\\"
out = "D:\\Data\\Images\\Murilo2\\"

# Calculate the circle equation based on three points
def circleRadius(b, c, d):
    
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        return None

    # Center
    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det
    center = [int(cx), int(cy)]

    # Radius
    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5

    return center, int(radius)

# Listen to mouse events on the correct window
def clickCrop(event, x, y, flags, param):
   
    global center, radius    
    global coord         
   
    if event == cv2.EVENT_LBUTTONDOWN:

        coord = [x, y]
              
        cv2.circle(frame, (coord[0],coord[1]), 2, (0,255,0), -1)
        cv2.imshow('frame', frame)
     
    if event == cv2.EVENT_LBUTTONUP:
        coordList.append(coord)

#MAIN

decision = sys.argv[1]
coordList = []
axleCount = 0

if (decision == "video"):
    cap = cv2.VideoCapture(0)

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = np.ceil(cap.get(cv2.CAP_PROP_FPS))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #Printing general information
    print("OpenCV: ", cv2.__version__)
    print("Res:    ", size[0],"x" , size[1])
    print("FPS:    ", fps)
    print("Frames: ", frames)

    # cv2.namedWindow('frame')

    # frameno = 0 
    # pause = False

    # if cap.isOpened():   
    #     print("Abriu o video!")       
    #     ret, frame = cap.read()        
    #     while (ret):           
    #         cv2.imshow('frame', frame)            
    #         if not pause:
    #             frameno += 1
    #         else:
    #             frameCrop = frame.copy()
    #             while (pause):                   
    #                 cv2.setMouseCallback('frame', clickCrop)                    
    #                 if len(coordList) == 3:                        
    #                     print(coordList)
    #                     center, radius = circleRadius(coordList[0],coordList[1],coordList[2])                    
                        
    #                     #circle based on coords with transparency
    #                     overlay = frame.copy()  
    #                     cv2.circle(overlay, (center[0],center[1]), radius, (0,0,255), -1)
                        
    #                     #(overlay, alpha, source, beta, gama, output)
    #                     #overlay = draw stuff here
    #                     #alpha   = transparency percentage
    #                     #source  = original frame
    #                     #beta    = 1 - alpha
    #                     #gama    = changes gama applied to whole image
    #                     #output  = output frame
    #                     cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
                                        
    #                     coordList = []
                        
    #                     #cropped_axle = frame[center[0]-radius:center[1]-radius), center[0]+radius:center[1]+radius/2]    
    #                     cv2.rectangle(frame, (center[0]-radius, center[1]-radius), (center[0]+radius,center[1]+radius), (0, 255, 0), 2)
    #                     cv2.imshow('frame', frame)                
                        
    #                     #crops image on original frame
    #                     croppedAxle = frameCrop[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]  
    #                     cv2.imshow('crop', croppedAxle)
    #                     cv2.imwrite("axle"+str(axleCount)+".jpg",croppedAxle)
    #                     axleCount += 1
                    
    #                 k = 0xFF & cv2.waitKey(1)            
    #                 if k == 32: #space
    #                     pause = not pause
                
    #         cap.set(1, frameno)            
    #         ret, frame = cap.read()

    # else:
    #     print("Num abriu o video...", cap.isOpened())        
        
    # cap.release()
    # cv2.destroyAllWindows()

elif (decision == "image"):

    w_exit = False
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(img_src):
        for file in f:
            if '.jpg' in file:
                files.append(os.path.join(r, file))

    print("Found {} file(s)".format(len(files)))

    for f in files:

        if w_exit:
            break

        cropping = True

        print(f)
        
        frame = cv2.imread(f)
        cv2.imshow('frame', frame)
         
        frameCrop = frame.copy()

        while cropping:   
            cv2.setMouseCallback('frame', clickCrop)               
            if len(coordList) == 3: 

                print(coordList)
                center, radius = circleRadius(coordList[0],coordList[1],coordList[2])                    
                
                #circle based on coords with transparency
                overlay = frame.copy()  
                cv2.circle(overlay, (center[0],center[1]), radius, (0,0,255), -1)
                
                #(overlay, alpha, source, beta, gama, output)
                #overlay = draw stuff here
                #alpha   = transparency percentage
                #source  = original frame
                #beta    = 1 - alpha
                #gama    = changes gama applied to whole image
                #output  = output frame
                cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
                                
                coordList = []
                
                #cropped_axle = frame[center[0]-radius:center[1]-radius), center[0]+radius:center[1]+radius/2]    
                cv2.rectangle(frame, (center[0]-radius, center[1]-radius), (center[0]+radius,center[1]+radius), (0, 255, 0), 2)
                cv2.imshow('frame', frame)    

                fname = f[f.rfind("\\")+1:-4]           
                
                #crops image on original frame
                croppedAxle = frameCrop[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]  
                cv2.imshow('crop', croppedAxle)

                cv2.imwrite(out+fname+"_axle_"+str(axleCount)+".jpg",croppedAxle)
                axleCount += 1

            k = 0xFF & cv2.waitKey(1)            
            if k == 32: #SPACE
                cropping = not cropping

                if not os.path.exists(img_dest):
                    print("Directory", img_dest, " does not exist. Creating it now...")
                    os.mkdir(img_dest)

                fname = f[f.rfind("\\")+1:]

                with open(img_dest+"cut.dat","a") as log:
                    log.write(str(fname)+" "+str(axleCount)+"\n")

                os.rename(f,img_dest+fname)
                axleCount = 0

            if k == 27: #ESC
                w_exit = True
                break
    
    cv2.destroyAllWindows()