
import matplotlib.pyplot as plt

def integrate(dt):
	y = 0
	vy = 500
	lvy = 500
	t = 0
	ts = []
	ys = []

	ts.append(t)
	ys.append(y)
	while t < 1:
		vy -= 1000*dt
		y += (vy + lvy)*dt*0.5
		t += dt
		lvy = vy
		ts.append(t)
		ys.append(y)

	plt.plot(ts,ys)

integrate(0.016*4)
integrate(0.016)
integrate(0.016*0.25)
plt.show()
