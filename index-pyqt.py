from __future__ import division
import numpy as np
from PyQt4 import QtGui, QtCore
import sys
import random
import sys
import os
import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt
#import pdb

pi=np.pi


    
def click(event):
    global gclick,s,width,height
    a = figure.add_subplot(111)       
    x=event.xdata
    y=event.ydata
    r=str(np.around(x,decimals=2))+','+str(np.around(y,decimals=2))
    a.annotate(str(s),(x,y))
    a.plot(x,y,'b+')
    a.axis([0,width,height,0])
    a.axis('off')
    a.figure.canvas.draw()
       
    s=s+1
     
    gclick=np.vstack((gclick,np.array([x,y])))
    var_g_click=r
    distance()
    return gclick,s


 
def reset():
    global image_diff,gclick,width,height,s       
    a = figure.add_subplot(111)
    a.figure.clear()
    a = figure.add_subplot(111)
    img=Image.open(str(image_diff))
    img=np.array(img)
    figure.suptitle(str(image_diff))
    a.imshow(img,origin="upper")
    a.axis([0,width,height,0])
    a.axis('off')    
    a.figure.canvas.draw()
    s=1
    gclick=np.zeros((1,2))
    ListBox_d_2.setPlainText()
    return s,gclick
    
    
def distance(): 
    global gclick,d,counter,x_calib
    for i in range(1,gclick.shape[0]):
        x=gclick[1,0]
        y=gclick[1,1]
        x1=gclick[i,0]
        y1=gclick[i,1]
        n=np.int(n_entry.text())
        d=np.sqrt((x1-x)**2+(y1-y)**2)/n
        
        i=0
        if d==0:
            bet=0
        else:
            bet=180-np.arccos((y1-y)/(n*d))*180/pi
        d=eval(x_calib[Calib_box.currentIndex()][4])/d
            
                
        
 
           
    if np.isinf(d)==0:
        ListBox_d_2.appendPlainText('d (A):'+str(np.around(d,decimals=2))+',Inclination:'+str(np.around(bet,decimals=2)))
    return d    




#################################################
### Fonction de calcul des distances interplanaires   
#########################################################
def distance_theo():
    global d
      
    a=np.float(a_entry.text())
    b=np.float(b_entry.text())
    c=np.float(c_entry.text())
    alp=np.float(alpha_entry.text())
    bet=np.float(beta_entry.text())
    gam=np.float(gamma_entry.text())
    e=np.int(indice_entry.text())
    alp=alp*pi/180;
    bet=bet*pi/180;
    gam=gam*pi/180;
    Dist=np.zeros(((2*e+1)**3-1,5))
    G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
    ListBox_theo.clear()
    w=0
    for i in range(-e,e+1):
        for j in range(-e,e+1):
            for k in range(-e,e+1):
                if (i,j,k)!=(0,0,0):
                    di=1/(np.sqrt(np.dot(np.array([i,j,k]),np.dot(np.linalg.inv(G),np.array([i,j,k])))))
                    if di<(d+0.1) and di>(d-0.1):
                        
                        #if extinction(space_group_box.get(),i,j,k):
                        I=extinction(SpaceGroup_box.currentText(),i,j,k)
                        #print(SpaceGroup_box.currentText())
                        Dist[w,:]=np.array([np.around(di,decimals=3),i,j,k,I])
                        w=w+1                    
                    
                    
    for k in range(0,w):                                   
        ListBox_theo.appendPlainText('d(A):'+str(Dist[k,0])+', hkl:'+str(int(Dist[k,1]))+','+str(int(Dist[k,2]))+','+str(int(Dist[k,3]))+', I(a.u):'+str(Dist[k,4]))
    return 



def open_image():
    global width, height,image_diff,s,gclick
    
    a = figure.add_subplot(111)    
    a.figure.clear()
    a=figure.add_subplot(111)
    image_diff=QtGui.QFileDialog.getOpenFileName(Index,"Open image file", "", "*.png *.jpg *.bmp *.tiff *.tif *.jpeg")
    img=Image.open(str(image_diff))
    img=np.array(img)
    a.imshow(img,origin='upper')
    figure.suptitle(str(image_diff))
    print img.shape
    height,width = img.shape[0], img.shape[1]
    a.axis([0,width,height,0])    
    a.axis('off')
    a.figure.canvas.draw()
    ListBox_d_2.clear()
    s=1
    gclick=np.zeros((1,2))
    ListBox_d_2.clear()
    
        
    return s,gclick
   
    


###################################################



#####################################################
## Fonction de calcul des conditions de reflexions
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
        F=0
        a=np.float(a_entry.text())
        b=np.float(b_entry.text())
        c=np.float(c_entry.text())
        alp=np.float(alpha_entry.text())
        bet=np.float(beta_entry.text())
        gam=np.float(gamma_entry.text())
        e=np.int(self.lineEdit.text())
        alp=alp*pi/180;
        bet=bet*pi/180;
        gam=gam*pi/180;
        G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
        I=np.zeros((1,1))
        di=np.zeros((1,4))
        cont=np.zeros((1,1))
        space_group=SpaceGroup_box.currentText()
    
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
                    
                    for ii in range(s+1,rr):
                        f=eval(x_space[ii][0])
                        F=F+f*np.exp(2j*pi*(eval(x_space[ii][1])*di[dc,1]+eval(x_space[ii][2])*di[dc,2]+eval(x_space[ii][3])*di[dc,3]))        
                       
                    I=np.vstack((I,float(np.real(F*np.conj(F)))))
                    ff=float(np.real(F*np.conj(F)))                
                    if ff>0.0000001:
                        ann=str(int(di[dc,1]))+str(int(di[dc,2]))+str(int(di[dc,3]))
                        a2.text(di[dc,0],ff*1.05,ann, rotation='vertical')
        
        
        
                       
        a2.bar(di[:,0],I,0.01)
        plt.ylim((0,np.amax(I)*1.2))
        plt.xlabel('Interplanar distance (nm)')
        plt.ylabel('Intensity (a.u.)')
        self.canvas.draw()

    
                        
        

 

    
    
def extinction(space_group,h,k,l):
    global x_space
    F=0
    s=0
    
    
    for i in range(0,len(x_space)):
        if space_group==x_space[i][0]:
            s=i
       
    while (s<(len(x_space)-1) and (len(x_space[s+1])==4)):
        f=eval(x_space[s+1][0])
        F=F+f*np.exp(2j*pi*(eval(x_space[s+1][1])*h+eval(x_space[s+1][2])*k+eval(x_space[s+1][3])*l))        
        s=s+1
    #print(F)    
    I=np.around(float(np.real(F*np.conj(F))),decimals=2)
    #print(I) 
    #if np.abs(F)>0.000001:
    return I

####################################################    
f_space=open(os.path.join(os.path.dirname(__file__), 'space_group.txt'),"r")

x_space=[]

for line in f_space:
    x_space.append(map(str, line.split()))
    
list_space_group=[]
for i in range(0,len(x_space)):
    if len(x_space[i])==1:
        list_space_group.append(x_space[i][0])
        
f_space.close()






################################################
# Creation d'une zone pour tracer des graphiques
################################################


#f = plt.figure()
#canvas = FigureCanvasTkAgg(f, master=root)
#canvas.get_tk_widget().place(x=0,y=0,height=800,width=900)
#canvas.show()
#figure.canvas.mpl_connect('button_press_event', click)





##############################################
# Boutons
##############################################
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

app = QtGui.QApplication(sys.argv)
Index=QtGui.QMainWindow()
Index.setWindowTitle('Index')

centralwidget = QtGui.QWidget(Index)
centralwidget.setObjectName(_fromUtf8("centralwidget"))
gridLayout_7 = QtGui.QGridLayout(centralwidget)
gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
gridLayout = QtGui.QGridLayout()
gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
gridLayout.setObjectName(_fromUtf8("gridLayout"))
groupBox = QtGui.QGroupBox(centralwidget)
groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
groupBox.setObjectName(_fromUtf8("groupBox"))
gridLayout_2 = QtGui.QGridLayout(groupBox)
gridLayout_2.setMargin(5)
gridLayout_2.setSpacing(5)
gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
space_group_label = QtGui.QLabel(groupBox)
space_group_label.setObjectName(_fromUtf8("space_group_label"))
gridLayout_2.addWidget(space_group_label, 17, 1, 1, 1)
Calib_box = QtGui.QComboBox(groupBox)
Calib_box.setObjectName(_fromUtf8("Calib_box"))
gridLayout_2.addWidget(Calib_box, 18, 2, 1, 3)
SpaceGroup_box = QtGui.QComboBox(groupBox)
SpaceGroup_box.setObjectName(_fromUtf8("SpaceGroup_box"))
gridLayout_2.addWidget(SpaceGroup_box, 17, 2, 1, 3)
spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
gridLayout_2.addItem(spacerItem, 25, 1, 1, 1)
c_entry = QtGui.QLineEdit(groupBox)
c_entry.setObjectName(_fromUtf8("c_entry"))
gridLayout_2.addWidget(c_entry, 9, 1, 1, 1)
b_label = QtGui.QLabel(groupBox)
b_label.setObjectName(_fromUtf8("b_label"))
gridLayout_2.addWidget(b_label, 5, 0, 1, 1)
n_label = QtGui.QLabel(groupBox)
n_label.setObjectName(_fromUtf8("n_label"))
gridLayout_2.addWidget(n_label, 15, 1, 1, 1)
n_entry = QtGui.QLineEdit(groupBox)
n_entry.setObjectName(_fromUtf8("n_entry"))
gridLayout_2.addWidget(n_entry, 15, 4, 1, 1)
d_label_var = QtGui.QLabel(groupBox)
d_label_var.setText(_fromUtf8(""))
d_label_var.setObjectName(_fromUtf8("d_label_var"))
gridLayout_2.addWidget(d_label_var, 11, 5, 1, 1)
beta_label = QtGui.QLabel(groupBox)
beta_label.setObjectName(_fromUtf8("beta_label"))
gridLayout_2.addWidget(beta_label, 5, 2, 1, 1)
spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
gridLayout_2.addItem(spacerItem1, 16, 1, 1, 1)
c_label = QtGui.QLabel(groupBox)
c_label.setObjectName(_fromUtf8("c_label"))
gridLayout_2.addWidget(c_label, 9, 0, 1, 1)
groupBox_9 = QtGui.QGroupBox(groupBox)
groupBox_9.setMaximumSize(QtCore.QSize(16777215, 16777215))
groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
gridLayout_10 = QtGui.QGridLayout(groupBox_9)
gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
ListBox_d_2 = QtGui.QPlainTextEdit(groupBox_9)
sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
sizePolicy.setHorizontalStretch(0)
sizePolicy.setVerticalStretch(0)
sizePolicy.setHeightForWidth(ListBox_d_2.sizePolicy().hasHeightForWidth())
ListBox_d_2.setSizePolicy(sizePolicy)
ListBox_d_2.setMaximumSize(QtCore.QSize(16777215, 120))
ListBox_d_2.setObjectName(_fromUtf8("ListBox_d_2"))
gridLayout_10.addWidget(ListBox_d_2, 0, 1, 1, 1)
gridLayout_2.addWidget(groupBox_9, 26, 1, 1, 4)
indice_label = QtGui.QLabel(groupBox)
indice_label.setObjectName(_fromUtf8("indice_label"))
gridLayout_2.addWidget(indice_label, 11, 1, 1, 1)
alpha_entry = QtGui.QLineEdit(groupBox)
alpha_entry.setObjectName(_fromUtf8("alpha_entry"))
gridLayout_2.addWidget(alpha_entry, 0, 4, 1, 1)
beta_entry = QtGui.QLineEdit(groupBox)
beta_entry.setObjectName(_fromUtf8("beta_entry"))
gridLayout_2.addWidget(beta_entry, 5, 4, 1, 1)
b_entry = QtGui.QLineEdit(groupBox)
b_entry.setObjectName(_fromUtf8("b_entry"))
gridLayout_2.addWidget(b_entry, 5, 1, 1, 1)
indice_entry = QtGui.QLineEdit(groupBox)
indice_entry.setObjectName(_fromUtf8("indice_entry"))
gridLayout_2.addWidget(indice_entry, 11, 4, 1, 1)
spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
gridLayout_2.addItem(spacerItem2, 19, 2, 1, 1)
a_label = QtGui.QLabel(groupBox)
a_label.setObjectName(_fromUtf8("a_label"))
gridLayout_2.addWidget(a_label, 0, 0, 1, 1)
Calib_label = QtGui.QLabel(groupBox)
Calib_label.setObjectName(_fromUtf8("Calib_label"))
gridLayout_2.addWidget(Calib_label, 18, 1, 1, 1)
a_entry = QtGui.QLineEdit(groupBox)
a_entry.setObjectName(_fromUtf8("a_entry"))
gridLayout_2.addWidget(a_entry, 0, 1, 1, 1)
alpha_label = QtGui.QLabel(groupBox)
alpha_label.setObjectName(_fromUtf8("alpha_label"))
gridLayout_2.addWidget(alpha_label, 0, 2, 1, 2)
Button_reset = QtGui.QPushButton(groupBox)
Button_reset.setObjectName(_fromUtf8("Button_reset"))
gridLayout_2.addWidget(Button_reset, 24, 1, 1, 4)
spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
gridLayout_2.addItem(spacerItem3, 10, 1, 1, 1)
gamma_entry = QtGui.QLineEdit(groupBox)
gamma_entry.setObjectName(_fromUtf8("gamma_entry"))
gridLayout_2.addWidget(gamma_entry, 9, 4, 1, 1)
gamma_label = QtGui.QLabel(groupBox)
gamma_label.setObjectName(_fromUtf8("gamma_label"))
gridLayout_2.addWidget(gamma_label, 9, 2, 1, 1)
gridLayout.addWidget(groupBox, 1, 1, 1, 2)
groupBox_5 = QtGui.QGroupBox(centralwidget)
groupBox_5.setMaximumSize(QtCore.QSize(300, 16777215))
groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
gridLayout_6 = QtGui.QGridLayout(groupBox_5)
gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
ListBox_theo = QtGui.QPlainTextEdit(groupBox_5)
sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
sizePolicy.setHorizontalStretch(0)
sizePolicy.setVerticalStretch(0)
sizePolicy.setHeightForWidth(ListBox_theo.sizePolicy().hasHeightForWidth())
ListBox_theo.setSizePolicy(sizePolicy)
ListBox_theo.setMaximumSize(QtCore.QSize(16777215, 350))
ListBox_theo.setObjectName(_fromUtf8("ListBox_theo"))
gridLayout_6.addWidget(ListBox_theo, 0, 0, 2, 1)
distance_button = QtGui.QPushButton(groupBox_5)
distance_button.setObjectName(_fromUtf8("distance_button"))
gridLayout_6.addWidget(distance_button, 2, 0, 1, 2)
spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
gridLayout_6.addItem(spacerItem4, 3, 0, 1, 1)
gridLayout.addWidget(groupBox_5, 2, 2, 1, 1)
gridLayout_7.addLayout(gridLayout, 0, 1, 1, 1)

figure=plt.figure(facecolor='white',figsize=[2,2],dpi=100)
canvas=FigureCanvas(figure)
canvas.setMinimumSize(QtCore.QSize(640, 480))
canvas.setObjectName(_fromUtf8("canvas"))
gridLayout_7.addWidget(canvas, 0, 0, 1, 1)
Index.setCentralWidget(centralwidget)
menubar = QtGui.QMenuBar(Index)
menubar.setGeometry(QtCore.QRect(0, 0, 1152, 25))
menubar.setObjectName(_fromUtf8("menubar"))
menuSave = QtGui.QMenu(menubar)
menuSave.setObjectName(_fromUtf8("menuSave"))
menuStructure = QtGui.QMenu(menubar)
menuStructure.setObjectName(_fromUtf8("menuStructure"))
menuSpectrum = QtGui.QMenu(menubar)
menuSpectrum.setObjectName(_fromUtf8("menuSpectrum"))
menuResol = QtGui.QMenu(menubar)
menuResol.setObjectName(_fromUtf8("menuResol"))

Index.setMenuBar(menubar)
statusbar = QtGui.QStatusBar(Index)
statusbar.setObjectName(_fromUtf8("statusbar"))
Index.setStatusBar(statusbar)
actionSave_figure = QtGui.QAction(Index)
actionSave_figure.setObjectName(_fromUtf8("actionSave_figure"))
actionCalculate_spectrum = QtGui.QAction(Index)
actionCalculate_spectrum.setObjectName(_fromUtf8("actionCalculate_spectrum"))
menuSave.addAction(actionSave_figure)
menuSpectrum.addAction(actionCalculate_spectrum)
menubar.addAction(menuSave.menuAction())
menubar.addAction(menuStructure.menuAction())
menubar.addAction(menuSpectrum.menuAction())
menubar.addAction(menuResol.menuAction())

QtCore.QMetaObject.connectSlotsByName(Index)
Index.setTabOrder(a_entry, b_entry)
Index.setTabOrder(b_entry, c_entry)
Index.setTabOrder(c_entry, alpha_entry)
Index.setTabOrder(alpha_entry, beta_entry)
Index.setTabOrder(beta_entry, gamma_entry)
Index.setTabOrder(gamma_entry, indice_entry)
Index.setTabOrder(indice_entry, n_entry)
Index.setTabOrder(n_entry, SpaceGroup_box)
Index.setTabOrder(SpaceGroup_box, Calib_box)
Index.setTabOrder(Calib_box, Button_reset)
Index.setTabOrder(Button_reset, ListBox_d_2)
Index.setTabOrder(ListBox_d_2, ListBox_theo)
Index.setTabOrder(ListBox_theo, distance_button)

   
Index.setWindowTitle(QtGui.QApplication.translate("Index", "Index", None, QtGui.QApplication.UnicodeUTF8))
groupBox_9.setTitle(QtGui.QApplication.translate("Index", "distance, inclination", None, QtGui.QApplication.UnicodeUTF8))
groupBox_5.setTitle(QtGui.QApplication.translate("Index", "Theo. distance", None, QtGui.QApplication.UnicodeUTF8))
distance_button.setText(QtGui.QApplication.translate("Index", "Calculate", None, QtGui.QApplication.UnicodeUTF8))
groupBox.setTitle(QtGui.QApplication.translate("Index", "Crystal Parameters", None, QtGui.QApplication.UnicodeUTF8))
space_group_label.setText(QtGui.QApplication.translate("Index", "Space group", None, QtGui.QApplication.UnicodeUTF8))
b_label.setText(QtGui.QApplication.translate("Index", "b", None, QtGui.QApplication.UnicodeUTF8))
n_label.setText(QtGui.QApplication.translate("Index", "Number of spots", None, QtGui.QApplication.UnicodeUTF8))
beta_label.setText(QtGui.QApplication.translate("Index", "beta", None, QtGui.QApplication.UnicodeUTF8))
c_label.setText(QtGui.QApplication.translate("Index", "c", None, QtGui.QApplication.UnicodeUTF8))
indice_label.setText(QtGui.QApplication.translate("Index", "Max Indices", None, QtGui.QApplication.UnicodeUTF8))
a_label.setText(QtGui.QApplication.translate("Index", "a", None, QtGui.QApplication.UnicodeUTF8))
alpha_label.setText(QtGui.QApplication.translate("Index", "alpha", None, QtGui.QApplication.UnicodeUTF8))
Button_reset.setText(QtGui.QApplication.translate("Index", "Reset", None, QtGui.QApplication.UnicodeUTF8))
gamma_label.setText(QtGui.QApplication.translate("Index", "gamma", None, QtGui.QApplication.UnicodeUTF8))
Calib_label.setText(QtGui.QApplication.translate("Index", "Calibrations", None, QtGui.QApplication.UnicodeUTF8))
menuSave.setTitle(QtGui.QApplication.translate("Index", "Open", None, QtGui.QApplication.UnicodeUTF8))
menuStructure.setTitle(QtGui.QApplication.translate("Index", "Structure", None, QtGui.QApplication.UnicodeUTF8))
menuSpectrum.setTitle(QtGui.QApplication.translate("Index", "Spectrum", None, QtGui.QApplication.UnicodeUTF8))
menuResol.setTitle(QtGui.QApplication.translate("Index", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
actionSave_figure.setText(QtGui.QApplication.translate("Index", "Open image", None, QtGui.QApplication.UnicodeUTF8))
actionCalculate_spectrum.setText(QtGui.QApplication.translate("Index", "Plot Spectrum", None, QtGui.QApplication.UnicodeUTF8))

############################################################"
######## Importer les calib depuis un fichier txt: microscope, E(kV),longueur camera (cm), binning,px/A
#############################################################"
f_calib=open(os.path.join(os.path.dirname(__file__), 'calibrations.txt'),"r")

x_calib=[]

for line in f_calib:
    x_calib.append(map(str, line.split()))

f_calib.close()
counter=len(x_calib)

for i in range(counter):
    Calib_box.addItem(x_calib[i][0]+' '+x_calib[i][1]+'keV '+x_calib[i][2]+'cm'+', Binning:'+x_calib[i][3])
    

################################################################

def resol(item):
    canvas.setMinimumSize(QtCore.QSize(np.int(item[0]), np.int(item[2])))
    canvas.update()
    Index.resize(np.int(item[0]), np.int(item[2]))
    
 
######################################################################################################
######## importer des structures cristallines depuis un fichier Nom,a,b,c,alpha,beta,gamma,space group
######################################################################################################

def structure(item):
    global x0, var_hexa, d_label_var, e_entry
    
    a_entry.setText(str(item[1]))
    b_entry.setText(str(item[2]))
    c_entry.setText(str(item[3]))
    alpha_entry.setText(str(item[4]))
    beta_entry.setText(str(item[5]))
    gamma_entry.setText(str(item[6]))
    ii=SpaceGroup_box.findText(item[7])
    SpaceGroup_box.setCurrentIndex(ii)
    
    
    
file_struct=open(os.path.join(os.path.dirname(__file__), 'structure.txt') ,"r")

x0=[]

for line in file_struct:
    x0.append(map(str, line.split()))

i=0
file_struct.close()            

for item in x0:
    entry = menuStructure.addAction(item[0])
    Index.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: structure(item))
    SpaceGroup_box.addItem(x0[i][7])
    i=i+1
    
    
file_resol=open(os.path.join(os.path.dirname(__file__), 'resolution.txt') ,"r")

xr=[]

for line in file_resol:
    xr.append(map(str, line.split()))

file_resol.close()            

for itemr in xr:
    entry = menuResol.addAction(itemr[0]+itemr[1]+itemr[2])
    Index.connect(entry,QtCore.SIGNAL('triggered()'), lambda itemr=itemr: resol(itemr))

   

#######################################################################################################


Index.connect(actionSave_figure, QtCore.SIGNAL('triggered()'), open_image) 
figure.canvas.mpl_connect('button_press_event', click)
Button_reset.clicked.connect(reset)
distance_button.clicked.connect(distance_theo)
dialSpect = Spect()
dialSpect.setWindowTitle("Spectrum")
Index.connect(actionCalculate_spectrum, QtCore.SIGNAL('triggered()'), dialSpect.exec_)  

n_entry.setText('1')
indice_entry.setText('5')
s=1
gclick=np.zeros((1,2))
Index.show()
app.exec_()
