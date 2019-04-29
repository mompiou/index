from __future__ import division
import numpy as np
from PyQt4 import QtGui, QtCore
import sys
import random
import sys
import os
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt
import indexUI

######################
#
# click event control
#
######################



def onpress(event):
	global press,move
	press=True
def onmove(event):
	global press,move
	if press:
    		move=True
def onrelease(event):
	global press,move
	
	if press and not move:
    		click(event)
	press=False
	move=False
	

def click(event):
    global gclick,s,minx,maxx,miny,maxy
    
    a = figure.add_subplot(111)       
    minx,maxx=a.get_xlim()
    miny,maxy=a.get_ylim()  
    x=event.xdata
    y=event.ydata
    r=str(np.around(x,decimals=2))+','+str(np.around(y,decimals=2))
    a.annotate(str(s),(x,y))
    a.plot(x,y,'b+')
    a.axis('off')
    a.figure.canvas.draw()
    s=s+1
    gclick=np.vstack((gclick,np.array([x,y])))
    var_g_click=r
    distance()
    return gclick,s



#########################
#
# Reset points
#
############################

 
def reset_points():
    global image_diff,gclick,s,minx,maxx,miny,maxy 
    
    a = figure.add_subplot(111)
    a.figure.clear()
    a = figure.add_subplot(111)
    img=Image.open(str(image_diff))
    img=np.array(img)
    figure.suptitle(str(image_diff))
    a.imshow(img,origin="upper")
    a.axis([minx,maxx,miny,maxy])
    a.axis('off')    
    a.figure.canvas.draw()
    s=1
    gclick=np.zeros((1,2))
    ui.ListBox_d_2.setPlainText('')
    return s,gclick


######################
#
# reset view
#
#########################

def reset():
	global width, height, gclick,s, image_diff
	
	a = figure.add_subplot(111)
	a.figure.clear()
	a = figure.add_subplot(111)
	img=Image.open(str(image_diff))
	img=np.array(img)
	figure.suptitle(str(image_diff))
	a.imshow(img,origin="upper")
	minx=0
	maxx=width
	miny=height
	maxy=0
	a.axis([minx,maxx,miny,maxy])
	a.axis('off')    
	a.figure.canvas.draw()
	gclick=np.zeros((1,2))
	ui.ListBox_d_2.clear()
	s=1


#########################
#
# Get experimental interplanar distance
#
############################
    
    
def distance(): 
    global gclick,d,counter,x_calib
    for i in range(1,gclick.shape[0]):
        x=gclick[1,0]
        y=gclick[1,1]
        x1=gclick[i,0]
        y1=gclick[i,1]
        n=np.int(ui.n_entry.text())
        d=np.sqrt((x1-x)**2+(y1-y)**2)/n
        
        i=0
        if d==0:
            bet=0
        else:
            bet=180-np.arccos((y1-y)/(n*d))*180/np.pi
        d=eval(x_calib[ui.Calib_box.currentIndex()][4])/d
            
           
    if np.isinf(d)==0:
        ui.ListBox_d_2.appendPlainText('d (A):'+str(np.around(d,decimals=2))+',Inclination:'+str(np.around(bet,decimals=2)))
    return d    



#########################
#
# Get theoretical distance
#
############################

def distance_theo():
    global d
      
    a=np.float(ui.a_entry.text())
    b=np.float(ui.b_entry.text())
    c=np.float(ui.c_entry.text())
    alp=np.float(ui.alpha_entry.text())
    bet=np.float(ui.beta_entry.text())
    gam=np.float(ui.gamma_entry.text())
    e=np.int(ui.indice_entry.text())
    alp=alp*np.pi/180;
    bet=bet*np.pi/180;
    gam=gam*np.pi/180;
    Dist=np.zeros(((2*e+1)**3-1,5))
    G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
    ui.ListBox_theo.clear()
    w=0
    for i in range(-e,e+1):
        for j in range(-e,e+1):
            for k in range(-e,e+1):
                if (i,j,k)!=(0,0,0):
                    di=1/(np.sqrt(np.dot(np.array([i,j,k]),np.dot(np.linalg.inv(G),np.array([i,j,k])))))
                    if di<(d+0.1) and di>(d-0.1):
                        I=extinction(ui.SpaceGroup_box.currentText(),i,j,k)
                        Dist[w,:]=np.array([np.around(di,decimals=3),i,j,k,I])
                        w=w+1                    
                    
                    
    for k in range(0,w):                                   
        ui.ListBox_theo.appendPlainText('d(A):'+str(Dist[k,0])+', hkl:'+str(int(Dist[k,1]))+','+str(int(Dist[k,2]))+','+str(int(Dist[k,3]))+', I(a.u):'+str(Dist[k,4]))
    return 


#########################
#
# Open image
#
############################


def open_image():
    global width, height,image_diff,s,gclick,minx,maxx,miny,maxy,press,move
    press=False
    move=False
    a = figure.add_subplot(111)    
    a.figure.clear()
    a=figure.add_subplot(111)
    image_diff=QtGui.QFileDialog.getOpenFileName(Index,"Open image file", "", "*.png *.jpg *.bmp *.tiff *.tif *.jpeg")
    img=Image.open(str(image_diff))
    img=np.array(img)
    a.imshow(img,origin='upper')
    figure.suptitle(str(image_diff))
    height,width = img.shape[0], img.shape[1]
    a.axis([0,width,height,0])    
    a.axis('off')
    a.figure.canvas.draw()
    ui.ListBox_d_2.clear()
    s=1
    gclick=np.zeros((1,2))
    ui.ListBox_d_2.clear()
    minx=0
    maxx=width
    miny=height
    maxy=0
    return s,gclick
   
    

#####################################################
# 
# Get diffraction spectrum
#
###################################################

def pair(number):
    if number%2==0:
        return 1
def impair(number):
    if number%2==0:
        return 0

class Spect(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Spect, self).__init__(parent)
 
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
 
         
        self.toolbar = NavigationToolbar(self.canvas, self)
        
                
        gridLayout = QtGui.QGridLayout()
        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.label = QtGui.QLabel('Max indices')
        self.label.setObjectName(_fromUtf8("Max indices"))
        gridLayout.addWidget(self.label, 1, 0, 1, 2)
        
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        gridLayout.addWidget(self.canvas, 0, 0, 1, 3)
        gridLayout.addWidget(self.toolbar, 3, 0, 1, 3)
        
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.spectre)
              
        
        self.setLayout(gridLayout)
 
    
        
    def spectre(self):
        global x_space
        a2=self.figure.add_subplot(111)
        a2.clear()
        a=np.float(ui.a_entry.text())
        b=np.float(ui.b_entry.text())
        c=np.float(ui.c_entry.text())
        alp=np.float(ui.alpha_entry.text())
        bet=np.float(ui.beta_entry.text())
        gam=np.float(ui.gamma_entry.text())
        e=np.int(self.lineEdit.text())
        alp=alp*np.pi/180;
        bet=bet*np.pi/180;
        gam=gam*np.pi/180;
        G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
        
        di=np.zeros((1,4))
        cont=np.zeros((1,1))
        space_group=ui.SpaceGroup_box.currentText()
    
        for tt in range(0,len(x_space)):
            if space_group==x_space[tt][0]:
                s=tt
        rr=s+1
        
        while len(x_space[rr])==4:
           rr=rr+1        

        for h in range(-e,e+1):
                for k in range(-e,e+1):
                    for l in range(-e,e+1):
                        if (h,k,l)!=(0,0,0):
                            gg=0
                            
                            for c in range(0,cont.shape[0]):
                                if 1/(np.sqrt(np.dot(np.array([h,k,l]),np.dot(np.linalg.inv(G),np.array([h,k,l])))))>cont[c]-0.00000001 and 1/(np.sqrt(np.dot(np.array([h,k,l]),np.dot(np.linalg.inv(G),np.array([h,k,l])))))<cont[c]+0.00000001:
                                    gg=1
                                   
                            if gg==0: 
                                di=np.vstack((di,(1/(np.sqrt(np.dot(np.array([h,k,l]),np.dot(np.linalg.inv(G),np.array([h,k,l]))))),h,k,l)))
                                cont=np.vstack((cont,1/(np.sqrt(np.dot(np.array([h,k,l]),np.dot(np.linalg.inv(G),np.array([h,k,l])))))))
                          
        
        for dc in range(1,di.shape[0]):          
                    F=0
                    q=2*np.pi*1e-10/di[dc,0]
                    for ii in range(s+1,rr):
                    	f=str(x_space[ii][0])
                    	                    	
	    		for z in range(0,len(x_scatt)):
	    			
	    			if f==x_scatt[z][0]:
	    				f=eval(x_scatt[z][1])*np.exp(-eval(x_scatt[z][2])*(q/4/np.pi)**2)+eval(x_scatt[z][3])*np.exp(-eval(x_scatt[z][4])*(q/4/np.pi)**2)+eval(x_scatt[z][5])*np.exp(-eval(x_scatt[z][6])*(q/4/np.pi)**2)+eval(x_scatt[z][7])*np.exp(-eval(x_scatt[z][8])*(q/4/np.pi)**2)+eval(x_scatt[z][9])
	    			
                        
                        F=F+f*np.exp(2j*np.pi*(eval(x_space[ii][1])*di[dc,1]+eval(x_space[ii][2])*di[dc,2]+eval(x_space[ii][3])*di[dc,3]))        
                       
                    
                    ff=float(np.real(F*np.conj(F)))     
                    bar_width=1/np.shape(di)[0]         
                    if ff>0.0000001:
                        ann=str(int(di[dc,1]))+str(int(di[dc,2]))+str(int(di[dc,3]))
                        a2.text(di[dc,0],ff,ann, rotation='vertical')
                        a2.bar(di[dc,0],ff,width=bar_width,align='center')
        
    
        
        plt.xlabel('Interplanar distance (nm)')
        plt.ylabel('Intensity (a.u.)')
        self.canvas.draw()

#########################
#
# Compute extinction conditions
#
############################
    
    
def extinction(space_group,h,k,l):
    global x_space
    F=0
    s=0
    
    
    for i in range(0,len(x_space)):
        if space_group==x_space[i][0]:
            s=i
       
    while (s<(len(x_space)-1) and (len(x_space[s+1])==4)):
        f=eval(x_space[s+1][0])
        F=F+f*np.exp(2j*np.pi*(eval(x_space[s+1][1])*h+eval(x_space[s+1][2])*k+eval(x_space[s+1][3])*l))        
        s=s+1
    I=np.around(float(np.real(F*np.conj(F))),decimals=2)
    return I

#########################
#
# Get space group data from inpt file space_group.txt
#
############################

f_space=open(os.path.join(os.path.dirname(__file__), 'space_group.txt'),"r")

x_space=[]

for line in f_space:
    x_space.append(map(str, line.split()))
    
list_space_group=[]
for i in range(0,len(x_space)):
    if len(x_space[i])==1:
        list_space_group.append(x_space[i][0])
        
f_space.close()


##################################################
#
# Add matplotlib toolbar to zoom and pan
#
################################################### 


class NavigationToolbar(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Pan', 'Zoom')]
    def set_message(self, msg):
        pass
        
#############################################################
#
# Launch
#
#############################################################"
    
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
if __name__ == "__main__":
    
	app = QtGui.QApplication(sys.argv)
	Index = QtGui.QMainWindow()	
	ui = indexUI.Ui_Index()
	ui.setupUi(Index)
	figure=plt.figure()
	canvas=FigureCanvas(figure)
	ui.mplvl.addWidget(canvas)
	toolbar = NavigationToolbar(canvas, canvas)
	toolbar.setMinimumWidth(601)

############################################################"
#
# Import calibrations from txt files: microscope, E(kV),camera lebghth (cm), binning,px/A
#
#############################################################"

f_calib=open(os.path.join(os.path.dirname(__file__), 'calibrations.txt'),"r")

x_calib=[]

for line in f_calib:
    x_calib.append(map(str, line.split()))

f_calib.close()
counter=len(x_calib)

for i in range(counter):
    ui.Calib_box.addItem(x_calib[i][0]+' '+x_calib[i][1]+'keV '+x_calib[i][2]+'cm'+', Binning:'+x_calib[i][3])
    

    
 
#######################################################################################
#
# import crystal structures from un txt file Name,a,b,c,alpha,beta,gamma,space group
#
#######################################################################################

def structure(item):
    global x0, var_hexa, d_label_var, e_entry
    
    ui.a_entry.setText(str(item[1]))
    ui.b_entry.setText(str(item[2]))
    ui.c_entry.setText(str(item[3]))
    ui.alpha_entry.setText(str(item[4]))
    ui.beta_entry.setText(str(item[5]))
    ui.gamma_entry.setText(str(item[6]))
    ii=ui.SpaceGroup_box.findText(item[7])
    ui.SpaceGroup_box.setCurrentIndex(ii)
    
    
    
file_struct=open(os.path.join(os.path.dirname(__file__), 'structure.txt') ,"r")

x0=[]

for line in file_struct:
    x0.append(map(str, line.split()))

i=0
file_struct.close()            

for item in x0:
    entry = ui.menuStructure.addAction(item[0])
    Index.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: structure(item))
    ui.SpaceGroup_box.addItem(x0[i][7])
    i=i+1
    
f_scatt=open(os.path.join(os.path.dirname(__file__), 'scattering.txt'),"r")

x_scatt=[]

for line in f_scatt:
    x_scatt.append(map(str, line.split()))
    
	
f_scatt.close()		    
   

Index.connect(ui.actionSave_figure, QtCore.SIGNAL('triggered()'), open_image) 
#figure.canvas.mpl_connect('button_press_event', click)

figure.canvas.mpl_connect('button_press_event', onpress)
figure.canvas.mpl_connect('button_release_event', onrelease)
figure.canvas.mpl_connect('motion_notify_event', onmove)
press=False
move=False


ui.Button_reset.clicked.connect(reset_points)
ui.Button_reset_all.clicked.connect(reset)
ui.distance_button.clicked.connect(distance_theo)
dialSpect = Spect()
dialSpect.setWindowTitle("Spectrum")
Index.connect(ui.actionCalculate_spectrum, QtCore.SIGNAL('triggered()'), dialSpect.exec_)  

ui.n_entry.setText('1')
ui.indice_entry.setText('5')
s=1
gclick=np.zeros((1,2))
Index.show()
app.exec_()
