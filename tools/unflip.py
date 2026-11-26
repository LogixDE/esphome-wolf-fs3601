import cv2,numpy as np
P=np.load('allpads.npy').astype(np.float64)
def inv(M):
    A=np.vstack([M,[0,0,1]]); return np.linalg.inv(A)[:2]
def mapp(M,W):
    Mi=inv(M); q=(Mi[:,:2]@P.T).T+Mi[:,2]; q[:,0]=W-1-q[:,0]; return q
sw={5,3,4,8,7,9,21,25,29,28,27,20,6,14,24, 44,55,62,65,70,45,38,39,40,51,63,66,56,50}
seg={6,14,24,56,50}
def draw(img,q,scale,name):
    im=cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
    for i,(x,y) in enumerate(q*scale):
        x,y=int(x),int(y)
        col=(0,0,255) if i in seg else ((255,0,255) if i in sw else (0,200,255))
        r=int(14*scale/2) if scale>1 else 14
        cv2.circle(im,(x,y),r,col,3)
        t=str(i); fs=1.3 if i in sw else 1.0; th=3
        (tw,tht),_=cv2.getTextSize(t,cv2.FONT_HERSHEY_SIMPLEX,fs,th)
        px,py=x+r+3,y-r-3
        cv2.rectangle(im,(px-3,py-tht-4),(px+tw+3,py+5),(255,255,255),-1)
        cv2.putText(im,t,(px,py),cv2.FONT_HERSHEY_SIMPLEX,fs,col if i in sw or i in seg else (0,0,0),th)
    cv2.imwrite(name,im,[cv2.IMWRITE_JPEG_QUALITY,90])
s=cv2.imread('Loetseite_Scan.jpg')
draw(s,mapp(np.load('Mscan.npy'),s.shape[1]),2,'Unterseite_Scan_nummeriert.jpg')
u=cv2.imread('Platine_unten.jpg')
draw(u,mapp(np.load('Mreg.npy'),u.shape[1]),1,'Unterseite_Foto_nummeriert.jpg')
