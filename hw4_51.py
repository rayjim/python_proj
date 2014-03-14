import matplotlib.pyplot as plt
import numpy as np
x = linspace(-4,4,100)
f1 = np.power(x,2)+ones(x.size)
plt.plot(x,f1,'r+')
lamb = linspace(1,8,3)
for i in range(lamb.size):
   f_lamb = (lamb[i]+1)*np.power(x,2)-6*lamb[i]*x+8*lamb[i]+1
   plt.plot(x,f_lamb,'-')

plt.axis([-5,6,0,20])
plt.show()