import os
import sys
import argparse
import cv2

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-easyocr_path', type=str, required=True)
    parser.add_argument('-model_path', type=str, required=True)
    parser.add_argument('-user_network_path', type=str, required=True)
    parser.add_argument('-recog_network', type=str, required=True)
    return parser


def on_mouse(event,x,y,flags,params):

    global ix, iy, downdrawing, movedrawing, updrawing, rect, flag

    if event == cv2.EVENT_LBUTTONDOWN:
        downdrawing = True
        flag = False
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if downdrawing:
            movedrawing = True
            updrawing = True
            rect = (ix,iy,x,y)

    elif event == cv2.EVENT_LBUTTONUP:
        downdrawing = False
        updrawing = True
        flag = True
        rect = (ix,iy,x,y)


def BrightnessContrast(brightness = 0 ):
    # getTrackbarPos returns the current position of the specified trackbar.
    brightness = cv2.getTrackbarPos( 'Brightness' ,"frame" )
    contrast = cv2.getTrackbarPos( 'Contrast' ,"frame")
    effect = controller(grayFrame, brightness,contrast)
    return effect

def controller(img, brightness = 255 ,contrast = 127 ):
    brightness = int ((brightness - 0 ) * ( 255 - ( - 255 )) / ( 510 - 0 ) + ( - 255 ))
    contrast = int ((contrast - 0 ) * ( 127 - ( - 127 )) / ( 254 - 0 ) + ( - 127 ))
    if brightness != 0 :
        if brightness > 0 :
            shadow = brightness
            max = 50
        else :
            shadow = 0
            max = 50 + brightness
        al_pha = ( max - shadow) / 50
        ga_mma = shadow
        # The function addWeighted calculates the weighted sum of two arrays
        cal = cv2.addWeighted(img, al_pha, img, 0 , ga_mma)
    else :
        cal = img
    if contrast != 0 :
        Alpha = float ( 131 * (contrast + 127 )) / ( 127 * ( 131 - contrast))
        Gamma = 127 * ( 1 - Alpha)
        # The function addWeighted calculates the weighted sum of two arrays
        cal = cv2.addWeighted(cal, Alpha, cal, 0 , Gamma)

    return cal



if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    easyocr_path = namespace.easyocr_path
    model_path = namespace.model_path
    user_network_path = namespace.user_network_path
    recog_network = namespace.recog_network

    sys.path.insert(0,easyocr_path)
    import easyocr
    from easyocr import Reader
    #print(easyocr_path)
    #print(model_path)
    #print(user_network_path)
    #print(recog_network)
    reader = easyocr.Reader(['en'],
                        model_storage_directory=model_path, #здесь расположена модель custom_example.pth
                        user_network_directory=user_network_path,  #здесь расположены custom_example.py и custom_example.yaml
                        recog_network=recog_network,
                        gpu=False)  

    rect = (0,0,0,0)
    ix=-1
    iy=-1
    downdrawing = False
    movedrawing = False
    updrawing = False
    flag = False
  

    cap = cv2.VideoCapture(2)
    waitTime = 50
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    (grabbed, frame) = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('frame')
    cv2.createTrackbar( 'Brightness' ,'frame' , 255 , 2*255 , BrightnessContrast)
    # Contrast range -127 to 127
    cv2.createTrackbar( 'Contrast' , 'frame' ,  127 , 2*127 ,  BrightnessContrast) 


    while(cap.isOpened()):

        (grabbed, frame) = cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', on_mouse)  
        grayFrame2 = BrightnessContrast(0)
        cv2.imshow('gray', grayFrame2)
        #drawing rectangle
        if movedrawing == True and updrawing==True:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
        if flag:
            if rect[1]<=rect[3] and rect[0]<=rect[2]:
                ymin = rect[1]
                ymax = rect[3]
                xmin = rect[0]
                xmax = rect[2]
            elif rect[1]>=rect[3] and rect[0]<=rect[2]:
                ymin = rect[3]
                ymax = rect[1]
                xmin = rect[0]
                xmax = rect[2]            
            elif rect[1]<=rect[3] and rect[0]>=rect[2]:
                ymin = rect[1]
                ymax = rect[3]
                xmin = rect[2]
                xmax = rect[0]    
            elif rect[1]>=rect[3] and rect[0]>=rect[2]:
                ymin = rect[3]
                ymax = rect[1]
                xmin = rect[2]
                xmax = rect[0]  

            xDiff = abs(xmin - xmax) 
            yDiff = abs(ymin - ymax)
            area = xDiff * yDiff
         
            if area>20:
                region_propose = grayFrame2[ymin:ymax, xmin:xmax]  
                result = reader.readtext(region_propose)
            else:
                result = False     
            #print('result = ',result)
            if not result:
                predict = 'None'
                inf_acc = 'None'
            else:
                predict = str(result[0][1])
                inf_acc = str(float('{:.3f}'.format(result[0][2])))
                #print('predict = ', predict)
            cv2.putText(frame, predict+'    conf. score = '+inf_acc, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.imshow('frame',frame)

        key = cv2.waitKey(waitTime) 

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()