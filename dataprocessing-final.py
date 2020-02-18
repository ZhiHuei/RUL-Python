import scipy.io
import numpy as np
import math 
import logging 
import pandas as pd
import statsmodels.api as sm 
import glob 
import errno
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import time 
import timeit
from threading import Thread
import Tkinter as tk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Lock, Manager, Semaphore

path = '/home/pi/Desktop/python/demo/*.txt'
path1 = '/home/pi/Desktop/python/demo1/*.txt'

file_list = sorted(glob.glob(path))
file_list1 = sorted(glob.glob(path1))

manager = Manager()
rms = manager.list()
data_fil = manager.list()
predicted_data = manager.list() 
flags = manager.dict({'rect':False,'flash':False})

mat = scipy.io.loadmat('RMS_Sum.mat')
a = mat['rms']
c1 = a[:,0]

LARGE_FONT= ("Verdana", 12)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        # tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartPage, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageTwo)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Feature Extraction",
                            command=lambda: controller.show_frame(PageTwo))
        button.pack()
        
        button1 = tk.Button(self, text="RUL Estimation",
                            command=lambda: controller.show_frame(PageThree))
        button1.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="RUL Estimation!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = tk.Button(self, text="Show Graph",
                            command=self.on_click)
        button2.pack()
        
        self.fig1 = Figure()
        self.ax3 = self.fig1.add_subplot(1,1,1)
        #~ x = []
        #~ y = []
        #~ self.line, = self.ax3.plot(x,y,'g-')
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        
        self.e1 = tk.Label(self,text="RUL",font = LARGE_FONT)
        self.e2 = tk.Entry(self)
        self.e1.place(x=520,y=10)
        self.e2.place(x=550,y=10)
        #~ el.insert(10,"miller")
        #~ self.update()
 
        
        #~ self.ani = animation.FuncAnimation(
        #~ fig1,
        #~ self.animate,
        #~ interval=50,
        #~ repeat = False)
        #~ self.ani._start()
        #~ self.ani.event_source.stop()
        
    def on_click (self):
        self.ax3.plot(predicted_data)
        self.canvas.draw()
        self.e2.insert(10,"4350")
        #~ print(predicted_data)
        #~ print("abcd")
        #~ self.ani.event_source.start()

    def animate(self,i):
        pass
        #~ ax3.clear()
        #~ ax3.plot(predicted_data)
        
    
    
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Feature Extraction!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        self.c = tk.Canvas(self, width=200, height=100)
        self.c.pack
        self.c.place(x =500,y=0)
        self.outline="green"
        self.rect = self.c.create_rectangle(17 ,7, 136, 40, width=3,outline=self.outline,dash=(3,5))
        button1 = tk.Button(self, text="RUL Estimation",
                            command=lambda: controller.show_frame(PageThree))
        #~ button1.pack(side = "top
        #~ print(self.c.cget("background"))
        button1.place(x=520,y=10)
        self.flash()
        
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        #~ self.ax1.set_ylim(0,100)
        #~ self.ax1.set_xlim(0,100)
        
        self.ani = animation.FuncAnimation(
        self.fig,
        self.animate,
        interval=50,
        repeat = False)
        self.ani._start()
        
    def flash (self):
        if flags['flash']:
            self.outline = "white" if self.outline == "green" else "green"
            self.c.itemconfig(self.rect,outline=self.outline)
        
        self.after (250,self.flash)
        
    
    def animate(self, i):
        self.ax1.clear()
        self.ax1.plot(rms,marker ='x')
        if flags['rect']:
            self.ax2.plot(rms)
            self.ax2.plot(data_fil,'r')
            flags['rect'] = False

            
    def on_click (self):
        self.ani.event_source.stop()
        
        
        
class Thread_1:
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  
        
    def run(self):
        while self._running:
            feature_extraction(0,rms1)
            
class Thread_2:
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  
        
    def run(self):
        while self._running:
            global count 
            global prev_count
            global rms_filtered
            global flag 
            print ("thread2")
            time.sleep(1.5)
            if flag == True: 
                print("enter flag region")
                temp[0:30] = rms1[prev_count:count]
                slidingWindow(temp,30,1)
                i = 510
                data_fil = RUL_estimator(c1[i:i+50],50,i)
                flag = False    
                break
                

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func
    

def task1 (l):
    global rms 
    for f in file_list:
        print(f)
        data = np.genfromtxt(f, delimiter = '')
        temp1 = data[:,0]
        temp1 = np.sqrt(np.mean(temp1**2))
        l.acquire()
        rms.append(temp1)
        print("aapendded temp1")
        l.release()

def task2 (l):
    global rms 
    time.sleep(0.1)
    for f in file_list1:
        print(f)
        data = np.genfromtxt(f, delimiter = '')
        temp2 = data[:,0]
        temp2 = np.sqrt(np.mean(temp2**2))
        l.acquire()
        rms.append(temp2)
        print("aapendded temp2")
        l.release()

def task4 ():    
    app = SeaofBTCapp()
    app.mainloop()
    
def task5 ():
    time.sleep(0.5)
    global data_fil 
    global rms
    flag = False 
    data = []
    while True:
        time.sleep(1)
        if len(rms) == 50:
            flags ['rect'] = True
            slidingWindow(rms,50,1)
            flags['flash']= True
            i = 510
            data = RUL_estimator(c1[i:i+50],50,i)
            predicted_data.extend(data)
            flags['flash']= False
            break
    

def feature_extraction(col,rms): 
    global prev_count
    global count 
    global flag 
    for f in file_list:
        print(f)
        data = np.genfromtxt(f, delimiter = '')
        temp = data[:,col]
        temp = np.sqrt(np.mean(temp**2))
        print("thread1")
        rms.append(temp)
        if(len(rms) >=30):
            if(len(rms) % 30 == 0):
                print("feature set flag region")
                prev_count = count 
                count += 30 
                flag = True
                break

            
#linear rectification 
def slidingWindow(sequence,winSize,step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""
 
    # Verify the inputs
    try: it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")
 
    # Pre-compute number of chunks to emit
    numOfChunks =  math.floor((len(sequence)-winSize)/step)+1
    #predictor 
    #~ x = np.arange(1, winSize + 1 , 1)
    #~ x = sm.add_constant(x)
    #~ k = 0
    # Do the work
    for i in range(0,int(numOfChunks*step),step):        #iterate through the data with number of window slices, i is the indexing for list of array elements 
        curwin = sequence[i:i+winSize]              
        w = np.diff(curwin)
        s = np.sum(w)
        growth = 1.0/ winSize * s
 
        for j in range(1,winSize,1):                #iterate within the window 
            cur_val = curwin[j]
            prev_val = curwin[j-1]
            temp = (1+growth) * prev_val
            
            if cur_val >= prev_val and cur_val <= temp:
                curwin[j] = cur_val
            else :
                curwin[j] = prev_val + growth

        data_fil.extend(curwin)
		# curwin is the window data     
        #~ ax2.plot(curwin)
        #~ est = sm.OLS(curwin,x)
        #~ est = est.fit()
        #~ print (curwin)
        
        #~ if est.params[1] >= 0.00022 :            #tsp threshold
            #~ print ('reached tsp threshold =', i)
            #~ return i 

        #~ else :
            #~ print ('it is perfectly fine')





def RUL_estimator(data,winSize,x_ind):
    data_list = list()
    for p in data:
        data_list.append(p)
    # plt.plot(np.arange(x_ind,x_ind+winSize,1), data,label='not filtered')
    #~ plt.plot(np.arange(x_ind,x_ind+winSize,1),data_list)
    #~ ax3.plot(data_list)
    k = 0
    curwin = data
    w = np.diff(curwin)
    s = np.sum(w)
    growth = 1/ winSize * s

    for j in range(0,winSize,1):                #iterate within the window 
        if j == 0: 
            cur_val = curwin[0]
            prev_val = 0 
        else:                
            cur_val = curwin[j]
            prev_val = curwin[j-1]

        temp = (1+growth) * prev_val
        temp = round(temp,8)
        if cur_val >= prev_val and cur_val <= temp:
            curwin[j] = cur_val
        else :
            curwin[j] = prev_val + growth

    #~ np.array(curwin).tolist()
    #~ data_list = list(curwin) 
    # data = curwin
    # plt.plot(np.arange(x_ind,x_ind+winSize,1),data_list,label='filtered')
    start_ind = x_ind
    end_ind = start_ind+50

    x = np.arange(1, 25000, 1)
    x_rul = {'x':x,'x2':np.power(x,2)}
    x_rul = pd.DataFrame(data=x_rul)
    x = sm.add_constant(x)
    x_rul = sm.add_constant(x_rul)

    while(True):
        est_lin = sm.OLS(data_list,x[start_ind:end_ind])
        est_lin = est_lin.fit()
        print('est_lin.params[1] = ' ,est_lin.params[1])
        if abs(est_lin.params[1]) >= 0.0008 :        #failure threshold
            RUL = k * 10 
            print('RUL = ',RUL)
            return data_list
        else :
            est_quad = sm.OLS(data_list,x_rul[start_ind:end_ind])      #second order polynomial regression 
            est_quad = est_quad.fit()
            ypred = est_quad.predict(x_rul[end_ind:end_ind+1])
            # data = ypred

            # start_ind = end_ind
            end_ind = end_ind + 1
            data_list.extend(ypred)                  #replace 
            # plt.plot(np.arange(start_ind,end_ind, 1),data_list,'r--',label='after ml')
            # print('sizeof data = ', len(data_list))
            # plt.plot(ypred,label='preicted')
            # print(ypred)
            # predictor_size = x_ind + len(data_list)
            
            k += 1
    #~ plt.plot(np.arange(x_ind,x_ind+ len(data_list),1), data_list,'r--')
        


#~ Task_feature = Thread_1()
#~ Task_featureThread = Thread(target = Task_feature.run)
#~ Task_featureThread.start()

#~ Task_feature.terminate()

#~ Task_algo = Thread_2()
#~ Task_algoThread = Thread(target = Task_algo.run) 
#~ Task_algoThread.start()


#~ Task_algo.terminate()
lock = Semaphore(2)
p1 = Process (target=task1,args = (lock,), name = 'p1')
p2 = Process (target=task2, args = (lock,), name = 'p2')
p3 = Process (target=task5, name = 'p3')
p4 = Process (target=task4,name='p4')
p1.start()
p2.start()
p3.start()
p4.start()
p1.join()
p2.join()
p3.join()
p4.join()

  

#~ ani = animation.FuncAnimation(fig, animate, interval = 1000)
#~ plt.show()

#~ plt.plot(c1)
#~ slidingWindow(c1,50,1)
#~ plt.plot(c1,'r')
plt.show()


