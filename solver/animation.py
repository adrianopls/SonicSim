
import numpy as np
import matplotlib

from classes.om import ObjectManager
from classes.uim import UIManager


class SGAnimation:
    
    def __init__(self, simulation_uid, cc_uid, *args, **kwargs):

        OM = ObjectManager()
        simulation = OM.get(simulation_uid)
        model = OM.get(simulation.model_uid)
        wavelet = OM.get(simulation.wavelet_uid)
             
        UIM = UIManager()
        cc = UIM.get(cc_uid)
        
        

        
        # layers = OM.list(parent_uid=model.uid)
        # geo_layer_1 = layers[0]
        # geo_layer_2 = layers[1]    
    
    
        # nx = input_vec.shape[0]  # Number of grid points in X
        # ny = input_vec.shape[1]  # Number of grid points in Y

        # dx = kwargs['dx']
        # dy = kwargs['dy']

        # f0 = kwargs['f0']
        # amp = kwargs['amp']
        
        # sou_x = kwargs['sou_x']    # Source position (in grid points) in X
        # sou_y = kwargs['sou_y']    # Source position (in grid points) in Y
        
        self.dt = simulation.dt       
        self.steps = simulation.nt

        vmax = kwargs['vmax']
        vmin = kwargs['vmin']


        #title = kwargs['title']



        # # Receiver Position
        self._xrec1 = kwargs.get('x_rec1') 
        self._yrec1 = kwargs.get('y_rec1')    # Position Reciever 1 (in grid points)
        
        self._xrec2 = kwargs.get('x_rec2') 
        self._yrec2 = kwargs.get('y_rec2')    # Position Reciever 2 (in grid points)
        
        self._xrec3 = kwargs.get('x_rec3') 
        self._yrec3 = kwargs.get('y_rec3')    # Position Reciever 3 (in grid points)



        self.main_ax = cc._main_panel.plot_axes

        sec_axes = cc._main_panel.get_secondary_axes()

        #
        #
        self.t = np.arange(0, self.dt*self.steps, self.dt)     # Time vector
        self.nt = np.arange(0, self.steps)
        #
        #
        
        


        if self._xrec1 and self._yrec1:
            rec1_color = 'black'
            self.ax0 = sec_axes[0]    
            self.ax0.set_xlabel('Step')
            self.ax0.set_ylabel('Amplitude')
            self.ax0.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
            self.ax0.set_yticks((vmin, 0, vmax))
            self.seis_line0 = matplotlib.lines.Line2D((0.0, 0.0), (0.0, 0.0), c=rec1_color)
            self.ax0.set_xlim(0, len(self.t))
            self.ax0.set_ylim(vmin, vmax)
            self.ax0.add_line(self.seis_line0)
            self.path_scatter1 = self.main_ax.scatter(self._xrec1, self._yrec1, s=30, c=rec1_color, marker="v") 
            #
            self.ax0.xaxis.labelpad = 1.0
            self.ax0.xaxis.label.update({'size': '8'})
            self.ax0.yaxis.labelpad = 1.0
            self.ax0.yaxis.label.update({'size': '8'})
            
            self.ax0.xaxis.labelpad = 1.0
            self.ax0.yaxis.labelpad = 1.0
            self.ax0.yaxis.set_tick_params(which="both", labelsize=8)
            self.ax0.xaxis.set_tick_params(which="both", labelsize=8)
            
        else:
            self.ax0 = None
            self.seis_line0 = None
            self.path_scatter1 = None


        if self._xrec2 and self._yrec2:
            rec2_color = 'red'
            self.ax1 = sec_axes[1]   
            self.ax1.set_xlabel('Step')
            self.ax1.set_ylabel('Amplitude')
            self.ax1.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
            self.ax1.set_yticks((vmin, 0, vmax))
            self.seis_line1 = matplotlib.lines.Line2D((0.0, 0.0), (0.0, 0.0), c=rec2_color)
            self.ax1.set_xlim(0, len(self.t))
            self.ax1.set_ylim(vmin, vmax)
            self.ax1.add_line(self.seis_line1)
            self.path_scatter2 = self.main_ax.scatter(self._xrec2, self._yrec2, s=30, c=rec2_color, marker="v")         
            #
            self.ax1.xaxis.labelpad = 1.0
            self.ax1.xaxis.label.update({'size': '8'})
            self.ax1.yaxis.labelpad = 1.0
            self.ax1.yaxis.label.update({'size': '8'})
            
            self.ax1.xaxis.labelpad = 1.0
            self.ax1.yaxis.labelpad = 1.0
            self.ax1.yaxis.set_tick_params(which="both", labelsize=8)
            self.ax1.xaxis.set_tick_params(which="both", labelsize=8)
            
            
        else:
            self.ax1 = None
            self.seis_line1 = None
            self.path_scatter2 = None


        if self._xrec3 and self._yrec3:
            rec3_color = 'teal'
            self.ax2 = sec_axes[2]                        
            self.ax2.set_xlabel('Step')
            self.ax2.set_ylabel('Amplitude')
            self.ax2.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
            self.ax2.set_yticks((vmin, 0, vmax))
            self.seis_line2 = matplotlib.lines.Line2D((0.0, 0.0), (0.0, 0.0), c=rec3_color)
            self.ax2.set_xlim(0, len(self.t))
            self.ax2.set_ylim(vmin, vmax)
            self.ax2.add_line(self.seis_line2)         
            self.path_scatter3 = self.main_ax.scatter(self._xrec3, self._yrec3, s=30, c=rec3_color, marker="v") 
            #
            self.ax2.xaxis.labelpad = 1.0
            self.ax2.xaxis.label.update({'size': '8'})
            self.ax2.yaxis.labelpad = 1.0
            self.ax2.yaxis.label.update({'size': '8'})
            
            self.ax2.xaxis.labelpad = 1.0
            self.ax2.yaxis.labelpad = 1.0
            self.ax2.yaxis.set_tick_params(which="both", labelsize=8)
            self.ax2.xaxis.set_tick_params(which="both", labelsize=8)
            
        else:
            self.ax2 = None
            self.seis_line2 = None
            self.path_scatter3 = None


        # No vetor grid, pontos com valor 1 estao associados a Fase 1 (rocha,
        # cor preta). Os pontos com valor 0 estao associados a Fase 2 (poros,
        # de cor branca).        
        # self.rho1 = 3.0
        # self.vp1 = 5000.0
        # #
        # self.rho2 = 2.2
        # self.vp2 = 3000.0


        cc.view._main_panel.draw()
        #super().draw(drawDC)

        self.main_ax = cc._main_panel.plot_axes




        # (left, right, bottom, top)
        extent = (0, simulation.nx, simulation.ny, 0)
        
        print("\n\n")
        print(extent)
        print("\n\n")
        
        
        
        # self.img_base = cc._main_panel.append_artist("AxesImage", 
        #                                       cmap="Greys",
        #                                       extent=extent)

        # self.img_base.set_data(model.data)
      
        
        



        # self.img_base = matplotlib.image.AxesImage(self.main_ax) #, *args, **kwargs)
        # self.main_ax.add_image(self.img_base)

    
        # self.img_base.set_data(model.data)
        #self.img_base.set_alpha(0.8)
        #self.img_base = main_ax.imshow(vec)
        #self.img_base.set_cmap("Greys")
        
        
                
        #self.img_wavefield = self.main_ax.imshow(simulation.data[0,:,:])
        
        self.img_wavefield = cc._main_panel.append_artist("AxesImage", 
                                              cmap="seismic_r",
                                              extent=extent)
        self.img_wavefield.set_data(simulation.data[0,:,:])        
        
        
        self.img_wavefield.set_cmap("seismic_r")
        #self.img_wavefield.set_cmap("RdBu")
        

        self.cpc = UIM.list('canvas_plotter_controller_jun21', cc.uid)[0]
        self.cpc.figure_titletext = simulation.name 
        
        # xlim = (0, simulation.nx)
        # cpc.xlim = xlim
        # cpc.set_plot_lim("x", xlim)
        
        # ylim = (simulation.ny, 0)
        # cpc.ylim = ylim
        # cpc.set_plot_lim("y", ylim)
        
        # print((0, simulation.nx), (simulation.ny, 0))





        # # self.main_ax.set_title(title)
        # # self.main_ax.set_xticks(range(0, nx+1, np.int(nx/5)))
        # # self.main_ax.set_yticks(range(0, ny+1, np.int(ny/5)))
        # # self.main_ax.set_xlabel('Grid-points in X axis')
        # # self.main_ax.set_ylabel('Grid-points in Y axis')
        
        
        # vmin = -0.2
        # vmax = 0.2
        
        self.img_wavefield.set_alpha(0.95)
        self.img_wavefield.set_clim(vmin, vmax)
        
        
        
        
        #self.img_wavefield.autoscale()
        # fig = self.main_ax.get_figure()
        
        # fig.colorbar(self.img_wavefield, ax=main_ax, orientation='horizontal', shrink=0.5) #, ticklocation='bottom')
               
                
        self._min_value = 0
        self._max_value = 0


        # # Output model parameter:
        # print('\n===========================================================')    
        # print('DX MODELO: ', dx)    
        # print("Model size: x:", dx*nx, "in m, y:", dy*ny, "in m")
        # print("Temporal discretization: ", self.dt," s")
        # print("Spatial discretization: ", dx, " m")
        # #print("Number of gridpoints per minimum wavelength: ", self.lampda_min/self._dx)
        # print("Wavefield Min-Max: ", np.min(wavefield), " - ",  np.max(wavefield))
        # print('===========================================================\n')   

        # model_size_text_template = "Model size - X: %.3fm (%d x %.6fm), Y: %.3fm (%d x %.6fm)"
        # model_size_text = main_ax.text(0.01, 0.97, '', transform=main_ax.transAxes)
        # model_size_text.set_text(model_size_text_template % (dx*nx, 
        #                                                 nx, dx,                      
        #                                                 dy*ny,
        #                                                 ny, dy))
        
        # wavelet_text_template = "Ricker wavelet: %.1fHz, Amplitude: %.1f"
        # wavelet_text = main_ax.text(0.01, 0.94, '', transform=main_ax.transAxes)
        # wavelet_text.set_text(wavelet_text_template % (f0, amp))

        # black_rock_text_template = 'Fase 1 (cinza) - Vp: %.1f m/s,  Rho: %.2f g/cm3'
        # black_rock_text = main_ax.text(0.01, 0.91, '', transform=main_ax.transAxes)
        # black_rock_text.set_text(black_rock_text_template % (self.vp1, self.rho1))

        # white_rock_text_template = 'Fase 2 (branco) - Vp: %.1f m/s,  Rho: %.2f g/cm3'
        # white_rock_text = main_ax.text(0.01, 0.88, '', transform=main_ax.transAxes)
        # white_rock_text.set_text(white_rock_text_template % (self.vp2, self.rho2))


        self.time_template = 'Step: %d/%d - Time: %.7fs'
        #self.time_text = main_ax.text(0.01, 0.85, '', transform=main_ax.transAxes)
        self.time_text = cc._main_panel.base_axes.title        
            
        
        sou_color = 'green'   
        # rec1_color = 'black'
        # rec2_color = 'red'
        # rec3_color = 'teal'
            
        

            
        self.main_ax.scatter(simulation.sou_x, simulation.sou_y, s=30, c=sou_color, marker=(5, 2))    
        
        # self.main_ax.scatter(self._xrec1, self._yrec1, s=30, c=rec1_color, marker="v")    
        # self.main_ax.scatter(self._xrec2, self._yrec2, s=30, c=rec2_color, marker="v")   
        # self.main_ax.scatter(self._xrec3, self._yrec3, s=30, c=rec3_color, marker="v")   
        
            
        # seis_ax0 = args[0]
        # seis_ax1 = args[1]
        # seis_ax2 = args[2]
        

        

        # #seis_ax0.set_title('Receiver 1 (' + rec1_color + ')')
        # seis_ax0.set_xlabel('Step')
        # seis_ax0.set_ylabel('Amplitude')
        # seis_ax0.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
        # seis_ax0.set_yticks((vmin, 0, vmax))
        # self.seis_line0 = matplotlib.lines.Line2D((0.0, 0.0), (0.0, 0.0), c=rec1_color)
        # seis_ax0.set_xlim(0, len(self.t))
        # seis_ax0.set_ylim(vmin, vmax)
        # seis_ax0.add_line(self.seis_line0)

        # #seis_ax1.set_title('Receiver 2 (' + rec2_color + ')')
        # seis_ax1.set_xlabel('Step')   
        # seis_ax1.set_ylabel('Amplitude')   
        # seis_ax1.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
        # seis_ax1.set_yticks((vmin, 0, vmax))
        # self.seis_line1 = matplotlib.lines.Line2D(self.t, wavefield[:, self._yrec2, self._xrec2], c=rec2_color)
        # seis_ax1.set_xlim(0, len(self.t))
        # seis_ax1.set_ylim(vmin, vmax)
        # seis_ax1.add_line(self.seis_line1)        

        # #seis_ax2.set_title('Receiver 3 (' + rec3_color + ')')
        # seis_ax2.set_xlabel('Step')   
        # seis_ax2.set_ylabel('Amplitude')  
        # seis_ax2.set_xticks((0, self.steps/4, self.steps/2, 3*self.steps/4, self.steps))
        # seis_ax2.set_yticks((vmin, 0, vmax))
        # self.seis_line2 = matplotlib.lines.Line2D(self.t, wavefield[:, self._yrec3, self._xrec3], c=rec3_color)
        # seis_ax2.set_xlim(0, len(self.t))
        # seis_ax2.set_ylim(vmin, vmax)
        # seis_ax2.add_line(self.seis_line2)    
        
        
        self.wavefield = simulation.data
        
 
        
    def init_func(self):    
        
        
        return self.img_wavefield, self.time_text, self.seis_line0, self.seis_line1, self.seis_line2

    

    def __call__(self, it, *args):
        


        # if (it % 10 == 0):     
        #     print('Animating SG [' + str(it+1) + '/' + str(self.steps) +']')        
        
        #self.cpc.axes_titletextcenter = self.time_template % (it+1, self.steps, it*self.dt)
        self.time_text.set_text(self.time_template % (it+1, self.steps, it*self.dt))
        
        

        self.img_wavefield.set_data(self.wavefield[it,:,:])
  
        self.seis_line0.set_data(self.nt[0:it], self.wavefield[0:it, self._yrec1, self._xrec1])
        self.seis_line1.set_data(self.nt[0:it], self.wavefield[0:it, self._yrec2, self._xrec2])
        self.seis_line2.set_data(self.nt[0:it], self.wavefield[0:it, self._yrec3, self._xrec3])
    
    
        return self.img_wavefield, self.time_text, self.seis_line0, self.seis_line1, self.seis_line2





