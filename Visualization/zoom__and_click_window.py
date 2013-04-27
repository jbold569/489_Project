import math
import pylab
import matplotlib
from matplotlib.pyplot import figure, show
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
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

figsrc = figure()

x = []
y = []
c = []
dist = []
dur = []
pace = []
calories = []
fuel = []

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
	
	
def find_center(points):
	total_x = 0
	total_y = 0
	for X in points:
		total_x += X[0]
		total_y += X[1]
	return [float(total_x)/len(points), float(total_y) / len(points)]
	
def to_pace(event):
	global aux_aux
	try:
		delaxes(aux_aux)
	except:
		None
	aux_aux = figsrc.add_subplot(224)
	aux_aux.hist(pace, bins = pace_buckets)
	title("Pace")
	xlabel("Duration (mi/min)")
	ylabel("Number of People")
	draw()
	
def to_dist(event):
	global aux_aux
	try:
		delaxes(aux_aux)
	except:
		None
	aux_aux = figsrc.add_subplot(224)
	aux_aux.hist(dist, bins = buckets)
	title("Distance")
	xlabel("Distance (km)")
	ylabel("Number of People")
	draw()
	
def to_dur(event):
	global aux_aux
	try:
		delaxes(aux_aux)
	except:
		None
	aux_aux = figsrc.add_subplot(224)
	aux_aux.hist(dur, bins = dur_buckets)
	title("Duration")
	xlabel("Duration (min)")
	ylabel("Number of People")
	draw()
	
def to_cal(event):
	global aux_aux
	try:
		delaxes(aux_aux)
	except:
		None
	aux_aux = figsrc.add_subplot(224)
	aux_aux.hist(calories, bins = cal_buckets)
	title("Calories")
	xlabel("Calories Burnt")
	ylabel("Number of People")
	draw()
	
def to_fuel(event):
	global aux_aux
	try:
		delaxes(aux_aux)
	except:
		None
	aux_aux = figsrc.add_subplot(224)
	aux_aux.hist(fuel, bins = fuel_buckets)
	title("Fuel")
	xlabel("Fuel Points")
	ylabel("Number of People")
	draw()
	
class Cluster_Manager:
	def __init__(self, master_X):
		self.master = master_X
		self.axsrc = figsrc.add_subplot(211, autoscale_on=True)	
		self.dist = True
		self.dur = True
		self.pace = True
		self.fuel = True
		self.cal = True
		self.__call__()
		self.Cluster()
	
	def __call__(self, event=None):
		if event == 'dist' : self.dist = not(self.dist)
		elif event == 'dur' : self.dur = not(self.dur)
		elif event == 'pace' : self.pace = not(self.pace)
		elif event == 'cal' : self.cal = not(self.cal)
		elif event == 'fuel' : self.fuel = not(self.fuel)
		print self.dist
		print self.dur
		print self.pace
		print self.fuel
		print self.cal
		print ""
		self.bool_vec = [self.dist,self.dur,self.pace,self.fuel,self.cal, ]
		
	def Cluster(self, event=None):
		global x,y,c,dist,dur,pace,calories,fuel,figsrc
		x=[]
		y=[]
		c=[]
		print self.bool_vec
		
		delaxes(self.axsrc)
		
		self.axsrc = figsrc.add_subplot(211, autoscale_on=True)			
		self.axsrc.set_title('Right Click to Zoom')
		
		def select(vec): return [elem for elem,b in zip(vec,self.bool_vec) if b]
		X = [ select(elem) for elem in self.master]
		print X[0]
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
			print "Center: "
			plot(cluster_center[0], cluster_center[1], 'o',
				markerfacecolor=color, markeredgecolor='k', markersize=7)
			title("Cluster View")

		self.master_lx_lim = self.axsrc.get_xlim()[0]
		self.master_ly_lim = self.axsrc.get_ylim()[0]
		self.master_ux_lim = self.axsrc.get_xlim()[1]
		self.master_uy_lim = self.axsrc.get_ylim()[1]
		self.af = AnnoteFinder(x,y,c,dist,dur,pace,calories,fuel, self.axsrc)
		figsrc.canvas.mpl_connect('button_press_event', self.af)
		
	def reset_area(self,event):
		self.axsrc.set_xlim(self.master_lx_lim, self.master_ux_lim)
		self.axsrc.set_ylim(self.master_ly_lim, self.master_uy_lim)
		draw()	

class AnnoteFinder:

	def __init__(self, xdata, ydata, colordata, distdata, durdata, pacedata, caloriedata, fueldata,  axis=None):
		self.data = zip(xdata, ydata, colordata, distdata, durdata, pacedata, caloriedata, fueldata)
		if axis is None:
		  self.axis = pylab.gca()
		else:
		  self.axis= axis

	def distance(self, x1, x2, y1, y2):
		return math.hypot(x1 - x2, y1 - y2)

	def __call__(self, event):
		if event.inaxes:
		  clickX = event.xdata
		  clickY = event.ydata
		  closest_i = 0
		  closest_dist = 10000000
		  if self.axis is None or self.axis==event.inaxes:
			cluster_num = None
			for i in range(0,len(self.data)):
				potential = self.distance(clickX, self.data[i][0], clickY, self.data[i][1])
				if potential < closest_dist:
					closest_dist = potential
					closest_i = i
			x = self.data[closest_i][0]
			y = self.data[closest_i][1]
			c = self.data[closest_i][2]
			cluster_num = c
			di = self.data[closest_i][3]
			du = self.data[closest_i][4]
			pa = self.data[closest_i][5]
			cal = self.data[closest_i][6]
			fu = self.data[closest_i][7]
			a.set_bbox(dict(facecolor=cm.spectral(float(c) / n_clusters, 1), alpha=.5))
			dist_text.set_text ("DIST (km) = %.3f" % di)
			dur_text.set_text("DUR (min) = %.3f" % du) 
			pace_text.set_text ("PACE (min/mi) = %.3f" % pa)
			cal_text.set_text ("CAL = %.3f" % cal)
			fuel_text.set_text ("FUEL = %.3f" % fu)
			
			
			num = 0
			clust_di = 0
			clust_du = 0
			clust_pa = 0
			clust_cal = 0
			clust_fu = 0
			for item in self.data:
				if item[2] == cluster_num:
					num += 1
					clust_di+=item[3]
					clust_du+=item[4]
					clust_pa+=item[5]
					clust_cal+=item[6]
					clust_fu+=item[7]
			clust_di /= float(num)
			clust_du /= float(num)
			clust_pa /= float(num)
			clust_cal /= float(num)
			clust_fu /= float(num)
			
			clust_dist_text.set_text ("DIST (km) = %.3f" % clust_di)
			clust_dur_text.set_text("DUR (min) = %.3f" % clust_du) 
			clust_pace_text.set_text ("PACE (min/mi) = %.3f" % clust_pa)
			clust_cal_text.set_text ("CAL = %.3f" % clust_cal)
			clust_fuel_text.set_text ("FUEL = %.3f" % clust_fu)
			
			figsrc.canvas.draw()
		
random_state = np.random.RandomState(0)

master_lx_lim = None
master_ly_lim = None

master_ux_lim = None
master_uy_lim = None
n_clusters = 8
	
#left, bottom
a = figtext(.20,.40, "POINT INFORMATION", fontsize = 20, bbox = dict(facecolor='white', alpha=.5)) 
clust_title = figtext(.10, .35, "CLUSTER AVERAGE", fontsize = 16)
ind_title = figtext(.35, .35, "INDIVIDUAL POINT", fontsize = 16)
dist_text = figtext(.35,.30,"DIST (km) = n/a")
clust_dist_text = figtext(.10,.30,"DIST (km) = n/a")
dur_text = figtext(.35,.25,"DUR (min) = n/a") 
clust_dur_text = figtext(.10,.25,"DUR (min) = n/a") 
pace_text = figtext(.35,.20,"PACE (min/mi) = n/a")
clust_pace_text = figtext(.10,.20,"PACE (min/mi) = n/a")
cal_text = figtext(.35,.15,"CAL = n/a")
clust_cal_text = figtext(.10,.15,"CAL = n/a")
fuel_text = figtext(.35,.10,"FUEL = n/a")
clust_fuel_text = figtext(.10,.10,"FUEL = n/a")

#figsrc.subplots_adjust(bottom = .5, left = .05, right = .95, top = .95)

#axsrc.set_visible(False)					
in_file = open("..\Exploratory Analysis\clean_data.txt", 'r')

X = []


cluster_man = None

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
cluster_man = Cluster_Manager(X)

maxi = 0
for item in dur:
	if item > maxi:
		maxi = item
print "duration max: ", maxi

#centers = utils.canopy_clustering(0.5, 0.65, X, utils.cosine_simularity)
#print "Number of seeds: ", len(centers)

#left, bottom, width, height


pace_ax = axes([.92,.28,.05,.05])
dur_ax = axes([.92,.34,.05,.05])
cal_ax = axes([.92,.22,.05,.05])
fuel_ax = axes([.92,.16,.05,.05])
distance_ax = axes([.92,.40,.05,.05])
reset_ax = axes([.92,.75,.05,.05])

clust_ax = axes([.03,.65,.05,.05])
rax = axes([.03, .75, .05,.15])
check = CheckButtons(rax, ('dist','dur','pace','cal','fuel'),(True, True, True, True, True))


b_pace = Button(pace_ax, "Pace")
b_dist = Button(distance_ax, "Dist")
b_dur = Button(dur_ax, "Duration")
b_cal = Button(cal_ax, "Calories")
b_fuel = Button(fuel_ax, "Fuel")
b_reset = Button (reset_ax, "Reset")
b_reclust = Button(clust_ax, "Cluster")


buckets = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5,13,13.5,14,14.5]
pace_buckets = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5,13,13.5,14,14.5]
dur_buckets = [0.0,  5.0,10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0]
cal_buckets = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000.0,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
fuel_buckets = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000.0,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]

aux_aux = figsrc.add_subplot(224)
aux_aux.hist(dist, bins = buckets)
title("Distance")
xlabel("Distance (km)")
ylabel("Number of People")

b_pace.on_clicked(to_pace)
b_dist.on_clicked(to_dist)
b_dur.on_clicked(to_dur)
b_cal.on_clicked(to_cal)
b_fuel.on_clicked(to_fuel)
b_reset.on_clicked(cluster_man.reset_area)
b_reclust.on_clicked(cluster_man.Cluster)
check.on_clicked(cluster_man)

show()
