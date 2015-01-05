from __future__ import division
import numpy as np
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from PIL import Image
import PngImagePlugin
import ttk
import sys
from tkFileDialog import *
import os
#import pdb

pi=3.14159265359


    
def click(event):
    global gclick,s,width,height
    a = f.add_subplot(111)       
    x=event.xdata
    y=event.ydata
    r=str(np.around(x,decimals=2))+','+str(np.around(y,decimals=2))
    a.annotate(str(s),(x,y))
    a.plot(x,y,'b+')
    a.axis([0,width,0,height])
    a.axis('off')
    a.figure.canvas.draw()
       
    s=s+1
     
    gclick=np.vstack((gclick,np.array([x,y])))
    var_g_click.set(r)
    distance()
    return gclick,s
 
def reset():
    global image_diff,gclick,width,height,s       
    a = f.add_subplot(111)
    a.figure.clear()
    a = f.add_subplot(111)
    img=Image.open(image_diff)
    a.imshow(img,origin="lower")
    a.axis([0,width,0,height])
    a.axis('off')    
    a.figure.canvas.draw()
    s=1
    gclick=np.zeros((1,2))
    Listbox_d.delete(0,END)
    return s,gclick
    
    
def distance(): 
    global gclick,d,counter,x_calib
    for i in range(1,gclick.shape[0]):
        x=gclick[1,0]
        y=gclick[1,1]
        x1=gclick[i,0]
        y1=gclick[i,1]
        n=eval(n_entry.get())
        d=np.sqrt((x1-x)**2+(y1-y)**2)/n
        cal=calib_box.get()
        i=0
        if d==0:
            bet=0
        else:
            bet=np.arccos((y1-y)/(n*d))*180/pi
        for i in range(0,counter):
            if cal==str(x_calib[i]):
               
                d=eval(x_calib[i][4])/d
            
                
        
 
           
    if np.isinf(d)==0:
        Listbox_d.insert(END,(np.around(d,decimals=2),np.around(bet,decimals=2)))
    return d    
        
#################################################
### Fonction de calcul des distances interplanaires   
#########################################################
def distance_theo():
    global d
      
    a=eval(a_entry.get())
    b=eval(b_entry.get())
    c=eval(c_entry.get())
    alp=eval(alp_entry.get())
    bet=eval(bet_entry.get())
    gam=eval(gam_entry.get())
    e=eval(indice_entry.get())
    alp=alp*pi/180;
    bet=bet*pi/180;
    gam=gam*pi/180;
    Dist=np.zeros(((2*e+1)**3-1,5))
    G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
    Listbox_dist.delete(0,END)
    w=0
    for i in range(-e,e+1):
        for j in range(-e,e+1):
            for k in range(-e,e+1):
                if (i,j,k)!=(0,0,0):
                    di=1/(np.sqrt(np.dot(np.array([i,j,k]),np.dot(np.linalg.inv(G),np.array([i,j,k])))))
                    if di<(d+0.1) and di>(d-0.1):
                        
                        #if extinction(space_group_box.get(),i,j,k):
                        I=extinction(space_group_box.get(),i,j,k)
                        
                        Dist[w,:]=np.array([np.around(di,decimals=3),i,j,k,I])
                        w=w+1                    
                    
                    
    for k in range(0,w):                                   
        Listbox_dist.insert(END,(Dist[k,0],int(Dist[k,1]),int(Dist[k,2]),int(Dist[k,3]),Dist[k,4]))
    return 

##############################################################
# fonction pour quitter
#######################################################
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#############################################################
def init():
    global gclick,s,var_g_click
    s=1
    gclick=np.zeros((1,2))
    var_g_click=StringVar()
       
    return gclick,s,var_g_click
################################################################

root = Tk()
root.wm_title("Index")
root.geometry('1220x798+10+40')
root.configure(bg = '#BDBDBD')
#img = PhotoImage(file='index0.gif')
#root.tk.call('wm', 'iconphoto', root._w, img)

#root.resizable(0,0)
#s=ttk.Style()
#s.theme_use('clam')
style = ttk.Style()
theme = style.theme_use()
default = style.lookup(theme, 'background')




##########################################################################
def open_image():
    global width, height,image_diff,s,gclick
    
    a = f.add_subplot(111)    
    a.figure.clear()
    a=f.add_subplot(111)
    image_diff = askopenfilename() 
    img=Image.open(image_diff)
    a.imshow(img,origin="lower")
    f.suptitle(str(image_diff))
    width, height = img.size
    a.axis([0,width,0,height])    
    a.axis('off')
    a.figure.canvas.draw()
    Listbox_d.delete(0,END)
    s=1
    gclick=np.zeros((1,2))
    Listbox_d.delete(0,END)
    
        
    return s,gclick
   
    
################################################
# Creation d'une zone pour tracer des graphiques
################################################


f = plt.figure()
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(x=0,y=0,height=800,width=900)
canvas.show()
f.canvas.mpl_connect('button_press_event', click)




###################################################

init()

#####################################################
## Fonction de calcul des conditions de reflexions
###################################################

def pair(number):
    if number%2==0:
        return 1
def impair(number):
    if number%2==0:
        return 0


def spectre():
    global x_space
    f2=plt.figure()
    a2=f2.add_subplot(111)
    F=0
    a=eval(a_entry.get())
    b=eval(b_entry.get())
    c=eval(c_entry.get())
    alp=eval(alp_entry.get())
    bet=eval(bet_entry.get())
    gam=eval(gam_entry.get())
    alp=alp*pi/180;
    bet=bet*pi/180;
    gam=gam*pi/180;
    e=eval(indice_entry.get())
    G=np.array([[a**2,a*b*np.cos(gam),a*c*np.cos(bet)],[a*b*np.cos(gam),b**2,b*c*np.cos(alp)],[a*c*np.cos(bet),b*c*np.cos(alp),c**2]])    
    I=np.zeros((1,1))
    di=np.zeros((1,4))
    cont=np.zeros((1,1))
    space_group=space_group_box.get()
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
    
    print(I.shape,di.shape)
    top=Toplevel()
    top.wm_title("Spectre de diffraction")
    top.geometry('900x800')  
    
    canvas = FigureCanvasTkAgg(f2, master=top)
    canvas.get_tk_widget().place(x=0,y=0,height=800,width=900)
    toolbar = NavigationToolbar2TkAgg( canvas, top )
    toolbar.update()
        
    canvas.show()    
        
    a2.bar(di[:,0],I,0.01)
    plt.ylim((0,np.amax(I)*1.2))
    plt.xlabel('Interplanar distance (nm)')
    plt.ylabel('Intensity (a. u.)')
    a2.figure.canvas.draw()
    
    
    
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
    print(F)    
    I=np.around(float(np.real(F*np.conj(F))),decimals=2)
    print(I) 
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




space_group_box = ttk.Combobox (master=root,state="readonly",values=list_space_group)
space_group_box.place(relx=0.89,rely=0.28,relheight=0.03,relwidth=0.1)
space_group_box.configure(takefocus="")


##########################################################
#### Pre-definition de cristaux donnes
###################################################




##############################################
# Boutons
##############################################
button_trace = Button (master=root)
button_trace.place(relx=0.9,rely=0.09,height=21,width=55)
button_trace.configure(activebackground="#f9f9f9")
button_trace.configure(activeforeground="black")
button_trace.configure(background="#ff0000")
button_trace.configure(command=reset)
button_trace.configure(foreground="black")
button_trace.configure(highlightcolor="black")
button_trace.configure(pady="0")
button_trace.configure(text='''RESET''')

Cristal_label = Label (master=root)
Cristal_label.place(relx=0.79,rely=0.03,height=19,width=142)
Cristal_label.configure(text='''Crystal parameters''')

a_cristal_label = Label (master=root)
a_cristal_label.place(relx=0.8,rely=0.08,height=19,width=12)
a_cristal_label.configure(text='''a''')

b_cristal_label = Label (master=root)
b_cristal_label.place(relx=0.8,rely=0.11,height=19,width=12)
b_cristal_label.configure(activebackground="#f9f9f9")
b_cristal_label.configure(activeforeground="black")
b_cristal_label.configure(foreground="black")
b_cristal_label.configure(highlightcolor="black")
b_cristal_label.configure(text='''b''')

c_cristal_label = Label (master=root)
c_cristal_label.place(relx=0.8,rely=0.15,height=19,width=11)
c_cristal_label.configure(activebackground="#f9f9f9")
c_cristal_label.configure(activeforeground="black")
c_cristal_label.configure(foreground="black")
c_cristal_label.configure(highlightcolor="black")
c_cristal_label.configure(text='''c''')

alp_cristal_label = Label (master=root)
alp_cristal_label.place(relx=0.78,rely=0.19,height=19,width=38)
alp_cristal_label.configure(activebackground="#f9f9f9")
alp_cristal_label.configure(activeforeground="black")
alp_cristal_label.configure(foreground="black")
alp_cristal_label.configure(highlightcolor="black")
alp_cristal_label.configure(text='''alpha''')

bet_cristal_label = Label (master=root)
bet_cristal_label.place(relx=0.78,rely=0.23,height=19,width=38)
bet_cristal_label.configure(activebackground="#f9f9f9")
bet_cristal_label.configure(activeforeground="black")
bet_cristal_label.configure(foreground="black")
bet_cristal_label.configure(highlightcolor="black")
bet_cristal_label.configure(text='''beta''')

gam_cristal_label = Label (master=root)
gam_cristal_label.place(relx=0.77,rely=0.26,height=19,width=48)
gam_cristal_label.configure(activebackground="#f9f9f9")
gam_cristal_label.configure(activeforeground="black")
gam_cristal_label.configure(foreground="black")
gam_cristal_label.configure(highlightcolor="black")
gam_cristal_label.configure(text='''gamma''')

a_entry = Entry (master=root)
a_entry.place(relx=0.81,rely=0.08,relheight=0.03,relwidth=0.06)
a_entry.configure(background="white")
a_entry.configure(insertbackground="black")

b_entry = Entry (master=root)
b_entry.place(relx=0.81,rely=0.11,relheight=0.03,relwidth=0.06)
b_entry.configure(background="white")
b_entry.configure(foreground="black")
b_entry.configure(highlightcolor="black")
b_entry.configure(insertbackground="black")
b_entry.configure(selectbackground="#c4c4c4")
b_entry.configure(selectforeground="black")

c_entry = Entry (master=root)
c_entry.place(relx=0.81,rely=0.15,relheight=0.03,relwidth=0.06)
c_entry.configure(background="white")
c_entry.configure(foreground="black")
c_entry.configure(highlightcolor="black")
c_entry.configure(insertbackground="black")
c_entry.configure(selectbackground="#c4c4c4")
c_entry.configure(selectforeground="black")

alp_entry = Entry (master=root)
alp_entry.place(relx=0.81,rely=0.19,relheight=0.03,relwidth=0.06)
alp_entry.configure(background="white")
alp_entry.configure(foreground="black")
alp_entry.configure(highlightcolor="black")
alp_entry.configure(insertbackground="black")
alp_entry.configure(selectbackground="#c4c4c4")
alp_entry.configure(selectforeground="black")

bet_entry = Entry (master=root)
bet_entry.place(relx=0.81,rely=0.23,relheight=0.03,relwidth=0.06)
bet_entry.configure(background="white")
bet_entry.configure(foreground="black")
bet_entry.configure(highlightcolor="black")
bet_entry.configure(insertbackground="black")
bet_entry.configure(selectbackground="#c4c4c4")
bet_entry.configure(selectforeground="black")

gam_entry = Entry (master=root)
gam_entry.place(relx=0.81,rely=0.26,relheight=0.03,relwidth=0.06)
gam_entry.configure(background="white")
gam_entry.configure(foreground="black")
gam_entry.configure(highlightcolor="black")
gam_entry.configure(insertbackground="black")
gam_entry.configure(selectbackground="#c4c4c4")
gam_entry.configure(selectforeground="black")



Listbox_d = Listbox (master=root)
Listbox_d.place(relx=0.75,rely=0.53,relheight=0.16,relwidth=0.09)
Listbox_d.configure(background="white")


calib_label = Label (master=root)
calib_label.place(relx=0.85,rely=0.35,height=19,width=75)
calib_label.configure(activebackground="#f9f9f9")
calib_label.configure(activeforeground="black")
calib_label.configure(foreground="black")
calib_label.configure(highlightcolor="black")
calib_label.configure(text='''Calibrations''')


dexp_label = Label (master=root)
dexp_label.place(relx=0.75,rely=0.49,height=19,width=166)
dexp_label.configure(activebackground="#f9f9f9")
dexp_label.configure(activeforeground="black")
dexp_label.configure(foreground="black")
dexp_label.configure(highlightcolor="black")
dexp_label.configure(text='''d(angstroem), inclination''')


Listbox_dist = Listbox (master=root)
Listbox_dist.place(relx=0.87,rely=0.54,relheight=0.34,relwidth=0.1)

Listbox_dist.configure(background="white")

dtheo_label = Label (master=root)
dtheo_label.place(relx=0.89,rely=0.49,height=19,width=86)
dtheo_label.configure(activebackground="#f9f9f9")
dtheo_label.configure(activeforeground="black")
dtheo_label.configure(foreground="black")
dtheo_label.configure(highlightcolor="black")
dtheo_label.configure(text='''d(angstroem)''')


indice_entry = Entry (master=root)
indice_entry.place(relx=0.91,rely=0.19,relheight=0.02
,relwidth=0.04)
indice_entry.configure(background="white")
indice_entry.configure(insertbackground="black")

n_label = Label (master=root)
n_label.place(relx=0.75,rely=0.75,height=19,width=126)
n_label.configure(activebackground="#f9f9f9")
n_label.configure(activeforeground="black")
n_label.configure(foreground="black")
n_label.configure(highlightcolor="black")
n_label.configure(text='''Number of spots''')

n_entry = Entry (master=root)
n_entry.place(relx=0.81,rely=0.78,relheight=0.02
,relwidth=0.04)
n_entry.configure(background="white")
n_entry.configure(insertbackground="black")


indice_label = Label (master=root)
indice_label.place(relx=0.9,rely=0.16,height=19,width=78)
indice_label.configure(activebackground="#f9f9f9")
indice_label.configure(activeforeground="black")
indice_label.configure(foreground="black")
indice_label.configure(highlightcolor="black")
indice_label.configure(text='''Max indices''')

distance_button = Button (master=root)
distance_button.place(relx=0.9,rely=0.9,height=21,width=68)
distance_button.configure(activebackground="#f9f9f9")
distance_button.configure(activeforeground="black")
distance_button.configure(background="#00ff00")
distance_button.configure(command=distance_theo)
distance_button.configure(foreground="black")
distance_button.configure(highlightcolor="black")
distance_button.configure(pady="0")
distance_button.configure(text='''Calculate''')



space_group_label = Label (master=root)
space_group_label.place(relx=0.89,rely=0.24,height=19,width=118)
space_group_label.configure(activebackground="#f9f9f9")
space_group_label.configure(activeforeground="black")
space_group_label.configure(foreground="black")
space_group_label.configure(highlightcolor="black")
space_group_label.configure(text='''Space group''')



############################################################"
######## Importer les calib depuis un fichier txt: microscope, E(kV),longueur camera (cm), binning,px/A
#############################################################"
f_calib=open(os.path.join(os.path.dirname(__file__), 'calibrations.txt'),"r")

x_calib=[]

for line in f_calib:
    x_calib.append(map(str, line.split()))

f_calib.close()
counter=len(x_calib)

calib_box = ttk.Combobox (master=root,state="readonly",values=x_calib)
calib_box.place(relx=0.8,rely=0.40,relheight=0.03,relwidth=0.18)
calib_box.configure(takefocus="")
################################################################

menu = Menu(master=root)
filemenu = Menu(menu, tearoff=0)
openmenu=Menu(menu,tearoff=0)
menu.add_cascade(label="Open", menu=openmenu)
openmenu.add_command(label="Open an image", command=open_image)


spectremenu=Menu(menu,tearoff=0)
menu.add_cascade(label="Spectrum", menu=spectremenu)
spectremenu.add_command(label="Draw the spectrum", command=spectre)
######################################################################################################
######## importer des structures cristallines depuis un fichier Nom,a,b,c,alpha,beta,gamma,space group
######################################################################################################

def structure(i0):
    global x0
    
    a_entry.delete(0,END)
    a_entry.insert(1,eval(x0[i0][1]))
    b_entry.delete(0,END)    
    b_entry.insert(1,eval(x0[i0][2]))
    c_entry.delete(0,END)    
    c_entry.insert(1,eval(x0[i0][3]))
    alp_entry.delete(0,END)    
    alp_entry.insert(1,eval(x0[i0][4]))
    bet_entry.delete(0,END)    
    bet_entry.insert(1,eval(x0[i0][5]))
    gam_entry.delete(0,END)    
    gam_entry.insert(1,eval(x0[i0][6]))
    space_group_box.delete(0,END)
    space_group_box.set(x0[i0][7])

def createstructure(i):
    return lambda:structure(i)    
    
cristalmenu=Menu(menu,tearoff=0)
menu.add_cascade(label="Structures", menu=cristalmenu)
file_struct=open(os.path.join(os.path.dirname(__file__), 'structure.txt'),"r")

x0=[]
i=0
for line in file_struct:
    x0.append(map(str, line.split()))
    cristalmenu.add_command(label=x0[i][0], command=createstructure(i))
    i=i+1
  
file_struct.close()

#######################################################################################################

root.config(menu=menu)


indice_entry.insert(5,5)    




mainloop()
