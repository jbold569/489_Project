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
import json

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
	
def reset_area(event):
	axsrc.set_xlim(master_lx_lim, master_ux_lim)
	axsrc.set_ylim(master_ly_lim, master_uy_lim)
	draw()
	
def update_graph(event):
	new_points = slider_tracker.update_graph()
	print new_points
	v_line.set_xdata(new_points[0])
	h_line.set_ydata(new_points[1])
	draw()
	
def reset_graph(event):
	s_speed.reset()
	s_distance.reset()
	s_cal.reset()
	s_fuel.reset()
	s_dur.reset()
	new_points = slider_tracker.update_graph()
	print new_points
	v_line.set_xdata(new_points[0])
	h_line.set_ydata(new_points[1])
	draw()
	
def init_graph():
	new_points = slider_tracker.update_graph()
	print new_points
	v_line.set_xdata(new_points[0])
	h_line.set_ydata(new_points[1])
	
def find_center(points):
    total_x = 0
    total_y = 0
    for X in points:
        total_x += X[0]
        total_y += X[1]
    return [float(total_x)/len(points), float(total_y) / len(points)]
	
def update_sliders(val):
	slider_tracker.update_pace(s_speed.val)
	slider_tracker.update_dist(s_distance.val)
	slider_tracker.update_dur(s_dur.val)
	slider_tracker.update_cal(s_cal.val)
	slider_tracker.update_fuel(s_fuel.val)
	
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
	
class slider_tracker:
	def __init__(self, data):
		self.origin = data
		self.origin_length = len(data)
		self. pace = 9
		self.dist = 5
		self.dur = 30
		self.cal = 300
		self.fuel = 1000
		self.pca = decomposition.PCA(n_components=2)
	def update_pace(self,data):
		self.pace = data
	def update_dist(self,data):
		self.dist = data
	def update_dur(self,data):
		self.dur = data
	def update_cal(self,data):
		self.cal = data
	def update_fuel(self,data):
		self.fuel = data
	def update_graph(self):
		vector = np.array([float(self.dist), float(self.dur), float(self.pace), float(self.cal), float(self.fuel)])
		new_data = [row[:] for row in self.origin]
		new_data.append(vector)
		new_data = np.array(new_data)
		self.pca.fit(new_data)
		new_data = pca.transform(new_data)
		return new_data[-1]

	def reset_graph(self):
		s_speed.reset()
		s_distance.reset()
		s_cal.reset()
		s_fuel.reset()
		s_dur.reset()	

class AnnoteFinder:

	def __init__(self, xdata, ydata, colordata, distdata, durdata, pacedata, caloriedata, fueldata,  axis=None, xtol=None, ytol=None):
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
				a.set_bbox(dict(facecolor=cm.spectral(float(c) / n_clusters, 1), alpha=.5))
				dist_text.set_text ("DIST (km) = %.3f" % di)
				dur_text.set_text("DUR (min) = %.3f" % du) 
				pace_text.set_text ("PACE (min/mi) = %.3f" % pa)
				cal_text.set_text ("CAL = %.3f" % cal)
				fuel_text.set_text ("FUEL = %.3f" % fu)
				figsrc.canvas.draw()

random_state = np.random.RandomState(0)

master_lx_lim = None
master_ly_lim = None

master_ux_lim = None
master_uy_lim = None
n_clusters = 6				
	
figsrc = figure()
#left, bottom
a = figtext(.35,.35, "CLUSTER", bbox = dict(facecolor='red', alpha=.5)) 
dist_text = figtext(.35,.30,"DIST (km) = n/a")
dur_text = figtext(.35,.25,"DUR (min) = n/a") 
pace_text = figtext(.35,.20,"PACE (min/mi) = n/a")
cal_text = figtext(.35,.15,"CAL = n/a")
fuel_text = figtext(.35,.10,"FUEL = n/a")
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
slider_tracker = slider_tracker(X)
X = np.array(X)

km = MiniBatchKMeans(k=n_clusters, init='random', n_init=10,
                     random_state=random_state).fit(X)

pca = decomposition.PCA(n_components=2)
pca.fit(X)
X = pca.transform(X)
        
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
master_lx_lim = axsrc.get_xlim()[0]
master_ly_lim = axsrc.get_ylim()[0]
master_ux_lim = axsrc.get_xlim()[1]
master_uy_lim = axsrc.get_ylim()[1]

v_line = axvline(x = 0, linewidth = 1, color='r')
h_line = axhline(y=0, linewidth = 1, color = 'b')

af = AnnoteFinder(x,y,c,dist,dur,pace,calories,fuel, None, .3, .3)

figsrc.canvas.mpl_connect('button_press_event', af)
#left, bottom, width, height

speed_slider = axes([0.05, 0.19, 0.2, 0.03])
dist_slider = axes([0.05,0.29,0.2,0.03])
cal_slider = axes([.05,.14,.2,.03])
dur_slider = axes([.05,.24,.2,.03])
fuel_slider = axes([.05,.09,.2,.03])
pace_ax = axes([.92,.31,.05,.05])
distance_ax = axes([.92,.24,.05,.05])
reset_ax = axes([.92,.75,.05,.05])

update_graph_ax = axes([.05,.02,.09,.05])
reset_cross_ax = axes([.16,.02,.09,.05])

s_speed = Slider(speed_slider, "Pace", 0, 20, valinit = 9)
s_distance = Slider(dist_slider, "Distance", 0, 30, valinit = 5)
s_cal = Slider(cal_slider, "Calories", 0, 5000, valinit = 300)
s_fuel = Slider(fuel_slider, "Fuel", 0, 14000, valinit = 1000)
s_dur = Slider(dur_slider, "Duration", 0, 1000, valinit = 30)
b_pace = Button(pace_ax, "Pace")
b_dist = Button(distance_ax, "Dist")
b_reset = Button (reset_ax, "Reset")
b_update_graph = Button(update_graph_ax, "Update Crosshairs")
b_reset_graph = Button(reset_cross_ax, "Reset Crosshairs")

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

s_speed.on_changed(update_sliders)
s_distance.on_changed(update_sliders)
s_cal.on_changed(update_sliders)
s_fuel.on_changed(update_sliders)
s_dur.on_changed(update_sliders)

b_pace.on_clicked(to_pace)
b_dist.on_clicked(to_dist)
b_reset.on_clicked(reset_area)
b_update_graph.on_clicked(update_graph)
b_reset_graph.on_clicked(reset_graph)
init_graph()
show()


