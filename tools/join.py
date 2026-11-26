import cv2, numpy as np
A=cv2.imread("unten_A.jpg"); B=cv2.imread("unten_B.jpg")
def prep(im):
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    return cv2.createCLAHE(3,(8,8)).apply(g)
sift=cv2.SIFT_create(8000)
ka,da=sift.detectAndCompute(prep(A),None); kb,db=sift.detectAndCompute(prep(B),None)
m=cv2.BFMatcher().knnMatch(da,db,k=2)
good=[x for x,y in m if x.distance<0.75*y.distance]
print("good",len(good))
src=np.float32([ka[g.queryIdx].pt for g in good]); dst=np.float32([kb[g.trainIdx].pt for g in good])
H,mask=cv2.findHomography(src,dst,cv2.RANSAC,5.0)
print("inliers",int(mask.sum())); print(H)
np.save("H.npy",H)
