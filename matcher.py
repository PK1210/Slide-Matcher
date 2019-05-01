import cv2
import sys
import os
from numpy import inf

ROLLS = [ 20171086 ]
MAX_DISPLACEMENT = 16

# # Read the image. The first command line argument is the image
# # image = cv2.imread('Data/sample_test/slides/ppt1.jpg')
# image = cv2.imread('Data/sample_test/frames/0.jpg')
# print(image.shape)
# cv2.imshow("Image", image)
# cv2.waitKey(0)

def eval(frame, slide):
    # import matplotlib.pyplot as plt

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(frame,None)
    kp2, des2 = sift.detectAndCompute(slide,None)

    # Convert to coordinates
    points_1 = cv2.KeyPoint_convert(kp1)
    points_2 = cv2.KeyPoint_convert(kp2)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    count = 0
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            temp = points_1[m.queryIdx] - points_2[m.trainIdx]
            if abs(temp[0]) < MAX_DISPLACEMENT and abs(temp[1]) < MAX_DISPLACEMENT:
                count += 1

    # cv2.drawMatchesKnn expects list of lists as matches.
    # img3 = cv2.drawMatchesKnn(frame,kp1,slide,kp2,good,None,flags=2)
    # plt.imshow(img3),plt.show()
    # print(count)
    return count

def matcher(frame, slides):
    n = len(slides)
    max_val = -inf
    slide = 'a'
    for i in range(n):
        print(slides[i][1])
        val = eval(frame,slides[i][0])
        if val > max_val:
            slide = slides[i][1]
            max_val = val
    print(slide)
    return slide,max_val

def iter(PATH_FRAME, slides):
    files = os.listdir(PATH_FRAME)
    frames = []
    # print(files)
    for file in files:
        frame = cv2.imread(PATH_FRAME + file)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_info = [file,matcher(frame, slides)]
        frames.append(frame_info)
    return frames

def init():
    # if len(sys.argv) < 3:
    #     print("Please enter the path to slide and path to frames as arguments")
    #     exit(1)
    # PATH_SLIDE = argv[1]
    PATH_SLIDE = 'Testbench/Slides/'
    PATH_FRAME = 'Testbench/Frames/'
    slides = readSlides(PATH_SLIDE)
    mapping = iter(PATH_FRAME, slides)
    formatAnswer(mapping)

def readSlides(PATH_SLIDE):
    files = os.listdir(PATH_SLIDE)
    slides = []
    for img in files:
        slide = cv2.imread(PATH_SLIDE + img)
        slide = cv2.cvtColor(slide,cv2.COLOR_BGR2GRAY)
        slide = [slide, img]
        slides.append(slide)
    return slides

def formatAnswer(mapping):
    # mapping.sort()
    print(mapping)
    for roll in ROLLS:
        try:
            f = open(str(roll)+'.txt','w')
            for i in mapping:
                line = i[0] + ' ' + str(i[1][0]) + '\n'
                f.write(line)
            f.close()
        except error as e:
            print("Error in printing answer",Error)

if __name__ == "__main__":
    init()
