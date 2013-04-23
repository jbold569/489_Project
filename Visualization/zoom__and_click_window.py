import math
import pylab
import matplotlib
from matplotlib.pyplot import figure, show
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy
import matplotlib.lines as lines
import matplotlib.gridspec as gridspec
from pylab import *
from sklearn.utils import shuffle
from sklearn.utils import check_random_state
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn import decomposition
import matplotlib.cm as cm

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
	
def make_data(file):
    return np.genfromtxt(file, delimiter = ',')

class AnnoteFinder:

	def __init__(self, xdata, ydata, colordata, distdata, durdata, pacedata, caloriedata, fueldata,  axis=None, xtol=None, ytol=None):
		print len(xdata), len(ydata), len(colordata), len(distdata), len(durdata)
		self.data = zip(xdata, ydata, colordata, distdata, durdata, pacedata, caloriedata, fueldata)
		if xtol is None:
		  xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
		if ytol is None:
		  ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
		self.xtol = xtol
		self.ytol = ytol
		print xtol
		print ytol
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
			for x,y,c,di,du,pa,cal,fu in self.data:
			  if  clickX-self.xtol < x < clickX+self.xtol and  clickY-self.ytol < y < clickY+self.ytol :
				print "TRUE", x, y, c,di,du,pa,cal,fu
				global a
				global figsrc
				global n_clusters
				a.set_bbox(dict(facecolor=cm.spectral(float(c) / n_clusters, 1), alpha=.5))
				figsrc.canvas.draw()

random_state = np.random.RandomState(0)

master_lx_lim = None
master_ly_lim = None

master_ux_lim = None
master_uy_lim = None
n_clusters = 6				
	
figsrc = figure()
#left, bottom
a = figtext(.4,.4, "CLUSTER", bbox = dict(facecolor='red', alpha=.5)) 
#figsrc.subplots_adjust(bottom = .5, left = .05, right = .95, top = .95)
axsrc = figsrc.add_subplot(211, autoscale_on=True)	

#axsrc.set_visible(False)							
axsrc.set_title('Right Click to Zoom')
in_file = open("..\Exploratory Analysis\clean_data.txt", 'r')

X = []
x = []
y = []
c = []
dist = []
dur = []
pace = []
calories = []
fuel = []
import json
for line in in_file:
	data = json.loads(line)
	sum = np.zeros(5)
	invalid = False
	for workout in data['workouts']:
		try:
			sum += np.array(workout['basic'])
		except:
			invalid = True
	if invalid:
		continue
	else:
		#put this vector in annote finder. [distance in km, duration in minutes, average pace in min/mile, calories, fuel]
		vector = sum/float(len(data['workouts']))
		dist.append(vector[0])
		dur.append(vector[1])
		pace.append(vector[2])
		calories.append(vector[3])
		fuel.append(vector[4])
		X.append(vector)
X = np.array(X)

km = MiniBatchKMeans(k=n_clusters, init='random', n_init=10,
                     random_state=random_state).fit(X)

print X.shape
pca = decomposition.PCA(n_components=2)
pca.fit(X)
X = pca.transform(X)
print X.shape


def find_center(points):
    total_x = 0
    total_y = 0
    for X in points:
        total_x += X[0]
        total_y += X[1]
    return [float(total_x)/len(points), float(total_y) / len(points)]
        
for k in range(n_clusters):
    my_members = km.labels_ == k
    color = cm.spectral(float(k) / n_clusters, 1)
    x.extend(X[my_members, 0])
    y.extend(X[my_members, 1])
    for i in range(0,len(X[my_members])):
		c.append(k)
    plot(X[my_members, 0], X[my_members, 1], 'o', marker='.', c=color)
    #cluster_center = km.cluster_centers_[k]
    cluster_center = find_center(X[my_members])
    plot(cluster_center[0], cluster_center[1], 'o',
            markerfacecolor=color, markeredgecolor='k', markersize=6)
    title("Example cluster allocation with a single random init\n"
             "with MiniBatchKMeans")
#x,y,c = numpy.random.rand(3,2000)
master_lx_lim = axsrc.get_xlim()[0]
master_ly_lim = axsrc.get_ylim()[0]
master_ux_lim = axsrc.get_xlim()[1]
master_uy_lim = axsrc.get_ylim()[1]

v_line = axvline(x = .5, linewidth = 1, color='r')
h_line = axhline(y=.5, linewidth = 1, color = 'b')

af = AnnoteFinder(x,y,c,dist,dur,pace,calories,fuel, None, None, None)

figsrc.canvas.mpl_connect('button_press_event', af)
#left, bottom, width, height

speed_slider = axes([0.05, 0.1, 0.2, 0.03])
dist_slider = axes([0.05,0.14,0.2,0.03])
pace_ax = axes([.92,.31,.05,.05])
distance_ax = axes([.92,.24,.05,.05])
reset_ax = axes([.92,.75,.05,.05])
#emotion_ax = axes([0.05, 0.3, 0.1, 0.15])
#weather_ax = axes([.16,.3,.1,.15])
#terrain_ax = axes([.27, .3, .1, .15])
s_speed = Slider(speed_slider, "Pace", 0, 20, valinit = 9)
s_distance = Slider(dist_slider, "Distance", 0, 30, valinit = 5)
b_pace = Button(pace_ax, "Pace")
b_dist = Button(distance_ax, "Dist")
b_reset = Button (reset_ax, "Reset")
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
	
def reset_zoom(event):
	axsrc.set_xlim(master_lx_lim, master_ux_lim)
	axsrc.set_ylim(master_ly_lim, master_uy_lim)
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
b_reset.on_clicked(reset_zoom)
#emotion_radio.on_clicked(handle_emotion)
#weather_radio.on_clicked(handle_weather)
#terrain_radio.on_clicked(handle_terrain)

show()


