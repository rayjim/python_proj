import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import cvxpy as cp
img = mpimg.imread('flowgray.png')
img_d = np.copy(img)
#plt.imshow(np.asarray(img),cmap=cm.binary_r)
m,n = img.shape
mask = np.random.rand(m,n)
known = np.zeros((m,n))
known = mask>0.5
x,y=np.where(mask>0.5)
###########
Ul2= cp.Variable(m,n)
constraints1=[Ul2[x[i],y[i]]==np.float(img[x[i],y[i]]) for i in range(x.size)]
Ux1 = Ul2[1:,1:]-Ul2[1:,0:n-1]
Uy1 = Ul2[1:,1:]-Ul2[0:m-1,1:]
objective1 = cp.Minimize(cp.norm2(cp.vstack(Ux1,Uy1)))
p1 = cp.Problem(objective1,constraints1)

#########################################
Utv= cp.Variable(m,n)
constraints2=[Utv[x[i],y[i]]==np.float(img[x[i],y[i]]) for i in range(x.size)]
Ux2 = Utv[1:,1:]-Utv[1:,0:n-1]
Uy2 = Utv[1:,1:]-Utv[0:m-1,1:]
objective2 = cp.Minimize(cp.norm(cp.vstack(Ux2,Uy2),1))
p2 = cp.Problem(objective2,constraints2)


p1.solve(verbose = True)
p2.solve(verbose = True)
plt.figure(1)
plt.set_cmap(cm.binary_r)
plt.subplot(221)
plt.imshow(img)
plt.subplot(222)
img_d[known]=1
plt.imshow(img_d)
plt.subplot(223)
plt.imshow(Ul2.value)
plt.subplot(224)
plt.imshow(Utv.value)
