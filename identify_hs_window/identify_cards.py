import cv2 as cv
import numpy as np 

big_img = cv.imread("./hs_script/identify_hs_window/big_img.png")
small_img = cv.imread("./hs_script/identify_hs_window/test.png")

src_img = cv.cvtColor(big_img, cv.COLOR_BGR2GRAY)
target_img = cv.cvtColor(small_img, cv.COLOR_BGR2GRAY)
h, w, a = small_img.shape

# cv.imshow('big_img', src_img)
# cv.imshow('small_img', target_img)

res = cv.matchTemplate(src_img, target_img, cv.TM_CCOEFF_NORMED)

print("res", res)
threshold = 0.35

loc = np.where( res >= threshold)

print(loc)
for pt in zip(*loc[::-1]):
    print(pt)
    cv.rectangle(big_img, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
# cv.rectangle(big_img, (866, 422), (966, 522), (7, 249, 151), 2)
cv.imshow('new', big_img)
 
cv.waitKey(0)