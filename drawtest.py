import matplotlib.pyplot as plt

plt.axes()


points1 = [[28, 115], [38, 115], [41, 143], [30, 143]]
points2 = [[14, 114], [26,111], [30,146], [18,148]]
line1 = plt.Polygon(points1,  fill=None, edgecolor='r')
line2 = plt.Polygon(points2,  fill=None, edgecolor='b')

plt.gca().add_patch(line1)
plt.gca().add_patch(line2)
plt.axis([0,50,80,160])
plt.show()