"""
This example shows how to connect events in one window, for example, a mouse
press, to another figure window.

If you click on a point in the first window, the z and y limits of the
second will be adjusted so that the center of the zoom in the second
window will be the x,y coordinates of the clicked point.

Note the diameter of the circles in the scatter are defined in
points**2, so their size is independent of the zoom
"""

import math
import pylab
import matplotlib
from matplotlib.pyplot import figure, show
import numpy

import math

import pylab
import matplotlib


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
axsrc = figsrc.add_subplot(211, xlim=(0,1), ylim=(0,1), autoscale_on=False)									
axsrc.set_title('Right Click to Zoom')
x,y,c = numpy.random.rand(3,20000)

axsrc.scatter(x,y,c=c)

af = AnnoteFinder(x,y, None, .0003,.0003)

figsrc.canvas.mpl_connect('button_press_event', af)
show()

