import math
import pylab
import matplotlib
from matplotlib.pyplot import figure, show
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy
import matplotlib.lines as lines
import math
import matplotlib.gridspec as gridspec
from pylab import *

def get_speed(file):
	speed = []
	for line in file:
		speed.append(float(line))
	return speed

def get_dist(file):
	dist = []
	for line in file:
		dist.append(float(line))
	return dist


class AnnoteFinder:
	"""
	callback for matplotlib to display an annotation when points are clicked on.  The
	point which is closest to the click and within xtol and ytol is identified.

	Register this function like this:

	scatter(xdata, ydata)
	af = AnnoteFinder(xdata, ydata, annotes)
	connect('button_press_event', af)
	"""

	def __init__(self, xdata, ydata, axis=None, xtol=None, ytol=None):
		self.data = zip(xdata, ydata)
		if xtol is None:
		  xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
		if ytol is None:
		  ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
		self.xtol = xtol
		self.ytol = ytol
		print self.xtol
		print self.ytol
		if axis is None:
		  self.axis = pylab.gca()
		else:
		  self.axis= axis


	def distance(self, x1, x2, y1, y2):
		"""
		return the distance between two points
		"""
		return math.hypot(x1 - x2, y1 - y2)

	def __call__(self, event):
		if event.inaxes:
		  clickX = event.xdata
		  clickY = event.ydata
		  if self.axis is None or self.axis==event.inaxes:
			for x,y in self.data:
			  if  clickX-self.xtol < x < clickX+self.xtol and  clickY-self.ytol < y < clickY+self.ytol :
				print "TRUE", x, y

				
figsrc = figure()
#left, bottom
a = figtext(.4,.4, "TEST") 
a.set_text("PASSED")
#figsrc.subplots_adjust(bottom = .5, left = .05, right = .95, top = .95)
axsrc = figsrc.add_subplot(211, xlim=(0,1), ylim=(0,1), autoscale_on=False)	

#axsrc.set_visible(False)							
axsrc.set_title('Right Click to Zoom')
x,y,c = numpy.random.rand(3,20000)

v_line = axvline(x = .5, linewidth = 4, color='r')
h_line = axhline(y=.5, linewidth = 4, color = 'b')


axsrc.scatter(x,y,c=c)

af = AnnoteFinder(x,y, None, .0008,.0008)

figsrc.canvas.mpl_connect('button_press_event', af)
#left, bottom, width, height

speed_slider = axes([0.05, 0.1, 0.2, 0.03])
dist_slider = axes([0.05,0.14,0.2,0.03])
pace_ax = axes([.92,.31,.05,.05])
distance_ax = axes([.92,.24,.05,.05])
#emotion_ax = axes([0.05, 0.3, 0.1, 0.15])
#weather_ax = axes([.16,.3,.1,.15])
#terrain_ax = axes([.27, .3, .1, .15])
s_speed = Slider(speed_slider, "Pace", 0, 20, valinit = 9)
s_distance = Slider(dist_slider, "Distance", 0, 30, valinit = 5)
b_pace = Button(pace_ax, "Pace")
b_dist = Button(distance_ax, "Dist")
#emotion_radio = RadioButtons(emotion_ax, ('tired','so_so','great','injured','amped','unstopable'))
#weather_radio = RadioButtons(weather_ax, ('sunny','cloudy','partly_sunny','amped','rainy','snowy'))
#terrain_radio = RadioButtons(terrain_ax, ('trail','treadmill','beach','road','amped','track'))

buckets = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5]
speed_in = open("speed.txt",'r')
dist_in = open("dist.txt", 'r')
speed = get_speed(speed_in)
dist = get_dist(dist_in)
speed_in.close()
dist_in.close()


auxdist = None
auxpace = figsrc.add_subplot(224)
auxpace.hist(speed, bins = buckets)	

def update_speed(val):
	v_line.set_xdata(val)
	a.set_text(val)
	figsrc.canvas.draw()
	
def update_distance(val):
	h_line.set_ydata(val)
	figsrc.canvas.draw()
	
def to_pace(event):
	global auxdist,auxpace
	delaxes(auxdist)
	auxpace = figsrc.add_subplot(224)
	auxpace.hist(speed, bins = buckets)
	draw()
	
def to_dist(event):
	global auxdist,auxpace
	delaxes(auxpace)
	auxdist = figsrc.add_subplot(224)
	auxdist.hist(dist, bins = buckets)
	draw()
		
	
#def handle_emotion(label):
#	print label

#def handle_weather(label):
#	print label
	
#def handle_terrain(label):
#	print label
	
s_speed.on_changed(update_speed)
s_distance.on_changed(update_distance)
b_pace.on_clicked(to_pace)
b_dist.on_clicked(to_dist)
#emotion_radio.on_clicked(handle_emotion)
#weather_radio.on_clicked(handle_weather)
#terrain_radio.on_clicked(handle_terrain)

show()


