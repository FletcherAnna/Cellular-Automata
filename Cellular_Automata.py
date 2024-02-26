import tkinter as tk
from tkinter import Frame,Label,Entry,Button
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


###
#TODO:
#move array operations to grid object
#implement GUI controls
#add file selector to save gif
###


def main():
    
    root = tk.Tk()
    root.geometry("900x600")
    root.resizable(False, False)
    app = Window(root)
    
    tk.mainloop()

def evolveGrid(x, rule, i):
    """Take a 2D array and rule and apply a single step. If the limit of the array has been reached, 
    rotate array and apply the step to the last row.
        
        Args:
        x (array): A 2D array.
        rule (int): Rule represented as an 8 bit binary
        i (int): index, the number of steps the autmomaton has evlolved
        
        Returns:
            x (array)
    """
    
    rule = np.array([int(x) for x in np.binary_repr(rule, 8)], dtype = np.int8)


    if i+1 < x.shape[0]:
       x[i + 1,:] = step(x[i,:], rule)
       
    else:
        x = np.roll(x, -1, axis=0)
        x[-1,:] = step(x[-2,:], rule)

    return x 


def step(x, rule):
    """Perform a single step with rule.
    
    Args:
        x (array): A single row of the grid.
        rule (int): Rule represented as an 8 bit binary
        
        Returns:
            x (array)
    """
    
    #select L, C, and R cells for each cell y then convert to three bit numbers
    lcr = np.vstack((np.roll(x, 1), x, np.roll(x, -1))).astype(np.int8)
    y = np.sum(lcr * np.array([[4], [2], [1]]) , axis=0).astype(np.int8)

    return rule[7-y]




class Window(Frame):
    __allAni = []
    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self._ani = animation


    def init_window(self):
        

        def animateThread(i):
            threading.Thread(target=animate, args=(i,)).start()
            
        def animate(i):
            
           self.grid = evolveGrid(self.grid, 169, i)
           self.image = self.ax.imshow(self.grid, interpolation='none', cmap=plt.cm.binary)
           return self.image

        self.master.title("Cellular Automata")
        self.pack(fill='both', expand=1)     

        #Controls

        self.labelRule = Label(self,text="Rule",width=12)
        self.labelRule.grid(row=0,column=1)
        
        self.labelInitCon = Label(self,text="Initial Conditions",width=12)
        self.labelInitCon.grid(row=0,column=2)

        self.textRule = Entry(self,width=12)
        self.textRule.grid(row=1,column=1)
        
        self.textInitCon = Entry(self,width=12)
        self.textInitCon.grid(row=1,column=2)
        
        def Plot():
            self.ani.pause()
        
        def Resume():
            self.ani.resume()
            

        self.buttonPlot = Button(self,text="Start",command=Plot,width=12)
        self.buttonPlot.grid(row=2,column=1)
        

        self.buttonClear = Button(self,text="Resume",command=Resume,width=12)
        self.buttonClear.grid(row=2,column=2)


        self.buttonClear.bind(lambda e:self.Plot)
        
        self.buttonClear.bind(lambda e:self.Clear)


        
        width = 10
        

        self.grid = np.zeros((width, width), dtype = np.int8)  
        
        #set random initial conditions
        self.grid[0,:] = np.random.rand(width) < .5

        #set up plot
        
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)  
        self.ax.set_axis_off()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0,row=4)
        
        self.ani = animation.FuncAnimation(self.fig, animateThread, np.arange(0, 200), interval=100, blit=False, repeat = False)





if __name__ == "__main__":
    main()

