#Requiered Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button,CheckButtons

class fourier:
    #PARAMETERS OF WAVE FUNCTIONS
    def __init__(self,dim,Amplitude,Frequency,init_time,end_time,dt):
        self.dim = dim
        self.Amplitude = Amplitude
        self.Frequency = Frequency 
        self.init_time = init_time
        self.end_time = end_time
        self.dt = dt   

    #Sin/Cos Wave Function
    def wave(self):
        time_array = np.arange(self.init_time,self.end_time,self.dt)
            #[time_array,wave_points]
        return [time_array,(self.Amplitude)*np.sin(2*np.pi*(self.Frequency)*time_array)]

class wrap_plot: 
    def __init__(self,t,w_array,Amplitude_array,j):
        #PARAMETERS
        prec = 1/(1.1e3)
        freq_min = 1
        freq_max = 100
        freq_loop = np.linspace(freq_min,freq_max,5000)
        factor = 1/prec
        freq_wrap = 3
        #CENTER OF MASS
        wrap = np.sum(w_array,axis=0)*np.exp(2j*np.pi*t*freq_wrap)
        ms_sum = np.sum(wrap)/factor
        ms_abs = np.abs(ms_sum)
        ms_x = []
        ms_y = []
        #line plot of center mass
        for freq_wrap in freq_loop:
            arg = np.sum(w_array,axis=0)*np.exp(-2j*np.pi*t*freq_wrap)
            ms_x.append(freq_wrap)
            ms_y.append(np.abs(np.sum(arg.real)/factor+np.sum(arg.imag)/factor))



        # Create the figure and the line that we will manipulate
        plt.style.use('dark_background')
        fig, axs = plt.subplots(1,2)
        
        plt.subplots_adjust(bottom=.25)
        

        if j == 0:
            p1, = axs[0].plot(t,w_array[0],color = '#ae00ff',label='WAVE 1') # COMMA CONNECT WITH SLIDER
            p2, = axs[0].plot(t,w_array[1],color = '#ff8c00',label='WAVE 2') # COMMA CONNECT WITH SLIDER
            p, = axs[0].plot(t,np.sum(w_array,axis=0),color = 'white',label = 'SUM OF WAVES')
            w, = axs[1].plot(wrap.real,wrap.imag,color = 'white')
            ms, = axs[1].plot(ms_sum.real,ms_sum.imag,'ro')
            #PLOT 0:
            ax_slide1 = plt.axes([0.25, 0.15, 0.65, 0.03]) # CREATE THE SLIDER BAR 1
            ax_slide2 = plt.axes([0.25, 0.1, 0.65, 0.03]) # CREATE THE SLIDER BAR 2
            ax_slide_wrap = plt.axes([0.25, 0.05, 0.65, 0.03]) # CREATE THE SLIDER BAR 3
            freq1_factor = Slider(ax_slide1,"FREQ1",valmin=0.2,valmax=60.0,valinit=w_array[0].Frequency,color ='#ae00ff')
            freq2_factor = Slider(ax_slide2,"FREQ2",valmin=0.2,valmax=60.0,valinit=w_array[1].Frequency,color ='#ff8c00')
            freq_wrap_factor = Slider(ax_slide_wrap,"FREQ_WRAP",valmin=0.2,valmax=60.0,valinit=1,color ='white')
            axs[0].set_title('Harmonics Waves',fontsize = 16)
            axs[0].set_xlabel('Time Domain',fontsize = 13)
            axs[0].set_ylabel('Amplitude',fontsize = 13)
            axs[1].set_title('Wrapping the Unknown Wave',fontsize = 16)
            axs[1].set_xlabel('Real Axis',fontsize = 13)
            axs[1].set_ylabel('Imaginary Axis',fontsize = 13)
            axs[1].set_xlim(-2,2)
            axs[1].set_ylim(-2,2)

            ########################################
            #            BUTTONS
            # Make checkbuttons with all plotted lines with correct visibility
            lines = [p, p1, p2]
            col = (0.4,0.3,0.75,0.4)
            rax = plt.axes([0, 0, 0.15, 0.15],facecolor=col)
            labels = [str(line.get_label()) for line in lines]
            visibility = [line.get_visible() for line in lines]
            check = CheckButtons(rax, labels, visibility)

            def func(label):
                index = labels.index(label)
                lines[index].set_visible(not lines[index].get_visible())
                plt.draw()

            check.on_clicked(func)
            def update(val):
                f1 = freq1_factor.val
                f2 = freq2_factor.val
                freq_wrap = freq_wrap_factor.val
                p1.set_ydata(1*np.sin(2*np.pi*f1*t))
                p2.set_ydata(1*np.sin(2*np.pi*f2*t))
                p.set_ydata(1*np.sin(2*np.pi*f1*t) + 1*np.sin(2*np.pi*f2*t))
                y1 = Amplitude_array[0]*np.sin(2*np.pi*f1*t)
                y2 = Amplitude_array[1]*np.sin(2*np.pi*f2*t)
                arg = (y1+y2)*np.exp(-2j*np.pi*t*freq_wrap)
                w.set_xdata(arg.real)
                w.set_ydata(arg.imag)
                ms.set_xdata(np.sum(arg.real)/factor)
                ms.set_ydata(np.sum(arg.imag)/factor)

            freq1_factor.on_changed(update)
            freq2_factor.on_changed(update)
            freq_wrap_factor.on_changed(update)           
        else:
            w, = axs[0].plot(wrap.real,wrap.imag,color = 'white')
            ms, = axs[0].plot(ms_sum.real,ms_sum.imag,'ro')
            FT, = axs[1].plot(ms_sum.real,ms_sum.imag,'ro')
            msxy = axs[1].plot(ms_x,ms_y/np.max(ms_y),'#8c5eff')
            ax_slide_wrap = plt.axes([0.25, 0.05, 0.65, 0.03]) # CREATE THE SLIDER BAR 2
            freq_wrap_factor = Slider(ax_slide_wrap,"FREQ_WRAP",valmin=0.2,valmax=60.0,valinit=1,color ='white')
            axs[0].set_title('Wrapping the Unknown Wave',fontsize = 16)
            axs[0].set_xlabel('Real Axis',fontsize = 13)
            axs[0].set_ylabel('Imaginary Axis',fontsize = 13)
            axs[0].set_xlim(-2,2)
            axs[0].set_ylim(-2,2)
            axs[1].set_title('Fourier Transform',fontsize = 16)
            axs[1].set_xlabel('Frequency Domain',fontsize = 13)
            axs[1].set_ylabel('Weights',fontsize = 13)
            axs[1].set_xlim(0,100)
            axs[1].set_ylim(0,1)
            ######################################################
            def update(val):
                freq_wrap = freq_wrap_factor.val
                arg = np.sum(w_array,axis=0)*np.exp(-2j*np.pi*t*freq_wrap)
                FT.set_xdata(freq_wrap)
                FT.set_ydata(np.abs(np.sum(arg.real)/factor+np.sum(arg.imag)/factor))
                w.set_xdata(arg.real)
                w.set_ydata(arg.imag)
                ms.set_xdata(np.sum(arg.real)/factor)
                ms.set_ydata(np.sum(arg.imag)/factor)

            freq_wrap_factor.on_changed(update) 
        plt.show()

        


