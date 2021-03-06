# -*- coding: UTF-8 -*-
'''
截取视频，识别结果可视化
'''
import numpy as np
import cv2 as cv
import os
from auto_sub import frame_to_time ,msec_to_timestring

def PPK_mask(hsv):
    lower_ray = np.array([56,178,189])
    upper_ray = np.array([67,193,207])
    mask = cv.inRange(hsv,lower_ray,upper_ray)
    res = mask
    #res = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return res
    
def PNT_mask(hsv):
    lower_ray = np.array([4,188,233])
    upper_ray = np.array([12,196,248])
    mask = cv.inRange(hsv,lower_ray,upper_ray)
    res = mask
    #res = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return res
    
def RAY_mask(hsv):
    lower_ray = np.array([173,163,219])
    upper_ray = np.array([178,173,230])
    mask = cv.inRange(hsv,lower_ray,upper_ray)
    res = mask
    #res = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return res
    
def RIO_mask(hsv):
    lower_rio = np.array([102,192,213])
    upper_rio = np.array([106,196,220])
    mask = cv.inRange(hsv,lower_rio,upper_rio)
    res = mask
    res = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return res
    
def BLACK_mask(hsv):
    lower_ray = np.array([1,5,1])
    upper_ray = np.array([255,255,43])
    mask = cv.inRange(hsv,lower_ray,upper_ray)
    res = mask
    res = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return res
    
def GRAY_mask(previous_hsv,hsv):
    signhsv = np.array(hsv,np.int16)
    signprevious_hsv = np.array(previous_hsv,np.int16)
    minus = np.subtract(signhsv,signprevious_hsv)
    lower_ray = np.array([-10,-25,-143])
    upper_ray = np.array([10,7,-49])
    mask = cv.inRange(minus,lower_ray,upper_ray)
    temp = np.array(mask,np.uint8)
    ret = cv.morphologyEx(temp, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    return ret
    
def WHITE_mask(hsv):
    lower_ray = np.array([0,0,252])
    upper_ray = np.array([255,4,255])
    ret = cv.inRange(hsv,lower_ray,upper_ray)
    return ret
    
def round_kernel_generator(radius):
    ret = np.ones((2*radius+1,2*radius+1),np.uint8)
    for x in range(2*radius+1):
        for y in range(2*radius+1):
            if (x-radius)**2 + (y-radius)**2 > radius**2:
                ret[x,y] = 0
    return ret
 
 
    
if __name__ == "__main__": 
    filelist = os.listdir() #在当前文件夹中查找扩展名为.mp4的文件
    select_list =[]
    for filename in filelist:
        if os.path.splitext(filename)[1]== '.webm' or os.path.splitext(filename)[1]== '.mp4' :
            select_list.append(filename)

    if len(select_list)>0:
        for i in range(len(select_list)):
            print(f'{i+1}: {select_list[i]}')
        chosen_one = int(input())-1
        VIDEO_FILENAME = select_list[chosen_one]
    else:
        VIDEO_FILENAME = input('请输入视频文件名（含扩展名）：\n')
    cap = cv.VideoCapture(VIDEO_FILENAME,cv.CAP_FFMPEG)
    FPS = cap.get(cv.CAP_PROP_FPS)
    frame_count = -1
    simple_kernel = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
    round_kernel = round_kernel_generator(40)
    previous_hsv = np.zeros((1080,1920,3))
    BLACK_new = np.zeros(1920*1080)
    while(cap.isOpened()):
        ret, img = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame_count += 1
        print(frame_count)      
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        if frame_count>=0:            
            small_img=cv.resize(img,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA)
            #GRAYmask=GRAY_mask(previous_hsv, hsv)
            RAYmask=RAY_mask(hsv)
            RIOmask=RIO_mask(hsv)
            current_frame_msec = cap.get(cv.CAP_PROP_POS_MSEC)
            #BLACKmask=BLACK_mask(hsv)
            #WHITEmask=WHITE_mask(hsv)
            #PPKmask=PPK_mask(hsv)
            #PNTmask=PNT_mask(hsv)
            #BLACKclosemask = cv.bitwise_xor(BLACKmask, cv.morphologyEx(BLACKmask, cv.MORPH_CLOSE, round_kernel))
            #BLACK_sur_WHITE = cv.bitwise_and(BLACKclosemask,WHITEmask)                
            if frame_count == 479 or frame_count == 770:
                #GRAYclosemask = cv.morphologyEx(GRAYmask, cv.MORPH_CLOSE, round_kernel)
                #GRAY_sur_WHITE = cv.bitwise_and(GRAYclosemask,WHITEmask)  
                cv.imshow(f'frame{VIDEO_FILENAME}', small_img)
                #cv.imshow('ponpoko', cv.resize(PPKmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))            
                #cv.imshow('peanuts', cv.resize(PNTmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow('gray', cv.resize(GRAYmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow(f'ray{VIDEO_FILENAME}', cv.resize(RAYmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))            
                #cv.imshow(f'rio{VIDEO_FILENAME}', cv.resize(RIOmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow('black',cv.resize(BLACKmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow('white',cv.resize(WHITEmask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow('BLACK_close_40',cv.resize(BLACKclosemask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow("BLACK close and white",cv.resize(BLACK_sur_WHITE,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow('GRAY_close_40',cv.resize(GRAYclosemask,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                #cv.imshow("GRAY close and white",cv.resize(GRAY_sur_WHITE,None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA))
                print("Frame count:%d"%frame_count)
                print(f"Current time:{msec_to_timestring(current_frame_msec)}")
                #print("RAY pxs:%d\tRIO pxs:%d\tBLACK pxs:%d"%(cv.countNonZero(RAYmask),cv.countNonZero(RIOmask),cv.countNonZero(BLACKmask)))
                #print("gray pxs:%d,white pxs:%d,GRAY_and_white:%d"%(cv.countNonZero(GRAYmask),cv.countNonZero(WHITEmask),cv.countNonZero(GRAY_sur_WHITE)))
                #print("ponpoko pxs:%d\tpeanuts pxs:%d"%(cv.countNonZero(PPKmask),cv.countNonZero(PNTmask)))
                KEY= cv.waitKey(0)
                if KEY == ord('q'):
                    break               
                elif KEY == ord('c'):
                    cv.imwrite(f"{VIDEO_FILENAME}{str(frame_count)}.bmp",img)
                cv.destroyAllWindows() 
        previous_hsv = hsv
            
    cap.release()
    cv.destroyAllWindows()        
            