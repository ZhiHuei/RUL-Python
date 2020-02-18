class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)        
        
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
        self.canvas = FigureCanvasTkAgg(self.fig1, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        
        self.e1 = tk.Label(self,text="RUL",font = LARGE_FONT)
        self.e2 = tk.Entry(self)
        self.e1.place(x=520,y=10)
        self.e2.place(x=550,y=10)

 
        
    def on_click (self):
        self.ax3.plot(predicted_data)
        self.canvas.draw()
        self.e2.insert(10,"4350")
        
    
    
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
        button1.place(x=520,y=10)
        self.flash()
        
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        
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