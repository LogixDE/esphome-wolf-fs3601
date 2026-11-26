import cv2, numpy as np
U="./"  # Ordner mit den Originalfotos
names=["0b44a9ff","6c8aad03","3cc7fcd5","7f39bae1","5811e963","6b0f8870"]
I={f:cv2.imread(U+f+"-image.jpg") for f in names}
def prep(im):
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); return cv2.createCLAHE(3,(8,8)).apply(g)
sift=cv2.SIFT_create(6000)
F={f:sift.detectAndCompute(prep(I[f]),None) for f in names}
def aff(a,b,th=8):
    ka,da=F[a];kb,db=F[b]
    m=cv2.BFMatcher().knnMatch(da,db,k=2)
    good=[x for x,y in m if x.distance<0.8*y.distance]
    src=np.float32([ka[g.queryIdx].pt for g in good]); dst=np.float32([kb[g.trainIdx].pt for g in good])
    M,inl=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=th)
    return M,int(inl.sum()),np.hypot(M[0,0],M[1,0])
import itertools
for a,b in itertools.permutations(names,2):
    M,n,s=aff(a,b)
    if n>=10 and 0.9<s<1.1: print(a,b,n,round(s,3),np.round(M[:,2]),round(np.degrees(np.arctan2(M[1,0],M[0,0])),2))

def A3(M): return np.vstack([M,[0,0,1]])
T={}
T["3cc7fcd5"]=np.eye(3)
T["0b44a9ff"]=A3(aff("0b44a9ff","3cc7fcd5")[0])
T["6c8aad03"]=T["0b44a9ff"]@A3(aff("6c8aad03","0b44a9ff")[0])
T["7f39bae1"]=A3(aff("7f39bae1","3cc7fcd5")[0])
T["5811e963"]=T["7f39bae1"]@A3(aff("5811e963","7f39bae1")[0])
T["6b0f8870"]=A3(aff("6b0f8870","3cc7fcd5")[0])
# color normalize to reference stats (LAB)
ref=cv2.cvtColor(I["7f39bae1"],cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32)
rm,rs=ref.mean(0),ref.std(0)
def norm(im):
    l=cv2.cvtColor(im,cv2.COLOR_BGR2LAB).astype(np.float32)
    m,s=l.reshape(-1,3).mean(0),l.reshape(-1,3).std(0)
    l=(l-m)/s*rs+rm
    return cv2.cvtColor(np.clip(l,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR)
h,w=1080,1920
pts=[]
for f in names:
    c=np.float32([[0,0,1],[w,0,1],[0,h,1],[w,h,1]]).T
    pts.append((T[f]@c)[:2].T)
pts=np.vstack(pts); mn=pts.min(0); mx=pts.max(0)
off=np.array([[1,0,-mn[0]],[0,1,-mn[1]],[0,0,1]])
W,Hh=int(mx[0]-mn[0])+1,int(mx[1]-mn[1])+1
acc=np.zeros((Hh,W,3),np.float32); wsum=np.zeros((Hh,W),np.float32)
for f in names:
    im=norm(I[f]) if f in ("0b44a9ff","6c8aad03") else I[f]
    M=(off@T[f])[:2]
    wi=cv2.warpAffine(im,M,(W,Hh)).astype(np.float32)
    mask=np.zeros((h,w),np.uint8); mask[1:-1,1:-1]=255
    d=cv2.distanceTransform(mask,cv2.DIST_L2,3)
    wd=cv2.warpAffine(d,M,(W,Hh))
    wd=np.minimum(wd,60)
    acc+=wi*wd[...,None]; wsum+=wd
out=(acc/np.maximum(wsum,1e-3)[...,None]).astype(np.uint8)
out[wsum<1e-3]=0
cv2.imwrite("unten_gesamt.jpg",out); print(out.shape)
