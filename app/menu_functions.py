
"""
This is file is used as the main place to Menu Functions.

It's just a recomendation. With the callback system devoloped functions my
go everywhere.

Here there is an exemple of use. In the interface.py file we may have

    UIM.create('menu_item_controller', mc_model.uid, 
            label="&Load model", 
            help="Load a model from file",
            id=wx.ID_OPEN,
            callback='app.menu_functions.on_open'
    )   

...witch will call on_open function above.
"""

import logging
import os
from collections import OrderedDict

import wx
import numpy as np
import matplotlib.pyplot as plt

from . import interface
from classes.uim import UIManager
from classes.om import ObjectManager
from solver.sg import staggeredGrid


WAVELET_TYPES = OrderedDict()
WAVELET_TYPES['Ricker'] = 'ricker'



def on_console(*args, **kwargs):
    
    UIM = UIManager()
    mwc = wx.App.Get().get_main_window_controller()
    UIM.create('console_controller', mwc.uid)


def on_load_model(*args, **kwargs):
    wildcard = "Load segmentated file (*.png, *.tif)|*.png;*.tif"



    fdlg = wx.FileDialog(wx.App.Get().GetTopWindow(), 
                         "Choose file", 
                         wildcard=wildcard, 
                         style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST
    )
    if fdlg.ShowModal() == wx.ID_OK:
        file_name = fdlg.GetFilename()
        dir_name = fdlg.GetDirectory()
        fdlg.Destroy()
    else:
        fdlg.Destroy()
        return
    fullfilename = os.path.join(dir_name, file_name)    
    
    print("\n\n")
    print (fullfilename)
    
    input_vec = plt.imread(fullfilename)
    
    values = np.unique(input_vec)
    
    if values.size > 2:
        msg = "File {} is not a binary segmentated file!".format(file_name)
        logging.error(msg)
        raise Exception(msg)
        
    OM = ObjectManager()
    UIM = UIManager()
    #
    dlg = UIM.create('dialog_controller', title='Create 2 layers model')
    #
    ctn_name = dlg.view.AddCreateContainer('StaticBox', 
                                           label='New model name', 
                                           orient=wx.VERTICAL, 
                                           proportion=0, 
                                           flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_name, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='model_name', 
                         initial=file_name.split(".")[0])     
    #    
    #
    ctn_xaxis = dlg.view.AddCreateContainer('StaticBox', 
                                        label="X Axis spacing",
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_xaxis, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='dx', initial=0.000296)
    #
    ctn_yaxis = dlg.view.AddCreateContainer('StaticBox', 
                                            label="Y Axis spacing", 
                                            orient=wx.VERTICAL, 
                                            proportion=0, 
                                            flag=wx.EXPAND|wx.TOP, border=5) 
    dlg.view.AddTextCtrl(ctn_yaxis, proportion=0, flag=wx.EXPAND|wx.TOP,
                         border=5, widget_name='dy', initial=0.000296)
    #        
    #
    ctn_layer_1 = dlg.view.AddCreateContainer('StaticBox', 
                                label='Layer 1 - Value: ' + str(values[0]), 
                                orient=wx.VERTICAL, 
                                proportion=0, 
                                flag=wx.EXPAND|wx.TOP, border=5)
    #
    ctn_vp1 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_1, label='Vp(m/s)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_vp1, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='vp1', initial=2500.0)
    #
    ctn_rho1 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_1, label='Rho(g/cm3)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_rho1, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='rho1', initial=2.2)
    #    

    #
    if values.size == 2:
        ctn_layer_2 = dlg.view.AddCreateContainer('StaticBox', 
                                    label='Layer 2 - Value: ' + str(values[1]), 
                                    orient=wx.VERTICAL, 
                                    proportion=0, 
                                    flag=wx.EXPAND|wx.TOP, border=5)
        #
        ctn_vp2 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_2, label='Vp(m/s)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_vp2, proportion=0, flag=wx.EXPAND|wx.TOP,
                             border=5, widget_name='vp2', initial=4000.0)
        #
        ctn_rho2 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_2, label='Rho(g/cm3)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_rho2, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='rho2', initial=3.0)         
        #
    #    
    # ctn_layer_3 = dlg.view.AddCreateContainer('StaticBox', label='Layer 3', orient=wx.HORIZONTAL)
    # #
    # ctn_start3 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_3, label='Start', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_start3, proportion=0, flag=wx.EXPAND|wx.TOP, border=5, widget_name='start3', initial=200.0)       
    # #
    # ctn_vp3 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_3, label='Vp(m/s)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_vp3, proportion=0, flag=wx.EXPAND|wx.TOP, border=5, widget_name='vp3', initial=2645.0)
    # #
    # ctn_vs3 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_3, label='Vs(m/s)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_vs3, proportion=0, flag=wx.EXPAND|wx.TOP, border=5, widget_name='vs3', initial=1170.0)        
    # #
    # ctn_rho3 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_3, label='Rho(g/cm3)', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_rho3, proportion=0, flag=wx.EXPAND|wx.TOP, border=5, widget_name='rho3', initial=2.29)          
    # #    
    # ctn_q3 = dlg.view.AddCreateContainer('StaticBox', ctn_layer_3, label='Q', orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_q3, proportion=0, flag=wx.EXPAND|wx.TOP, border=5, widget_name='q3', initial=2000.0)   
    # #    
    dlg.view.SetSize((300, 550))
    result = dlg.view.ShowModal()

    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating model. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()  

            am = OM.new('acoustic_2d_model', input_vec, 
                        dx=results.get('dx'), 
                        dy=results.get('dy'), 
                        name=results.get('model_name'))
            result = OM.add(am)
            
            print ('result acoustic_2d_model:', result, args, kwargs)
    
    
            layer1 = OM.new('geolayer', value=values[0], vp=results.get('vp1'), rho=results.get('rho1'), name="Layer 1")
            result = OM.add(layer1, am.uid)
            print ('result layer 1:', result)
            
            if values.size == 2:
                layer2 = OM.new('geolayer', value=values[1], vp=results.get('vp2'), rho=results.get('rho2'), name="Layer 2")
                result = OM.add(layer2, am.uid)
                print ('result layer 2:', result)    
    
    
            print(input_vec.shape)
    

        
        
        
        # UIM = UIManager()      
        # mwc = wx.GetApp().get_main_window_controller()
        # cc = UIM.create('crossplot_controller', mwc.uid)        
        
        # xlim_max, ylim_max = input_vec.shape
        # # (left, right, bottom, top)
        # extent = (0, 0, xlim_max, ylim_max)

        # image = cc._main_panel.append_artist("AxesImage", 
        #                                      cmap="Greys") #,
        #                                      #extent=extent)
        # #cc._main_panel.add_image(image)
        # cc._main_panel.set_plot_lim('x', (0, xlim_max))
        # cc._main_panel.set_plot_lim('y', (ylim_max, 0))
        
        # print(xlim_max, ylim_max)
        
        # image.set_data(input_vec)
        # image.set_label('crossplot_controller')    
        
        
        # if image.get_clip_path() is None:
        #     # image does not already have clipping set, 
        #     # clip to axes patch
        #     image.set_clip_path(image.axes.patch)        
        
        #gripy_app = wx.App.Get()
        #gripy_app.load_project_data(fullfilename)
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)



# def on_open_model(*args, **kwargs):
#     UIM = UIManager()      
#     mwc = wx.GetApp().get_main_window_controller()
#     UIM.create('crossplot_controller', mwc.uid)
    
    
    
def create_properties_dialog(obj_uid, size=None):
    if not size:
        size = (300, 330)
    UIM = UIManager()
    try:      
        dlg = UIM.create('object_properties_dialog_controller')
        #print(dlg)
        dlg.obj_uid = obj_uid
        dlg.view.SetSize(size)
        dlg.view.ShowModal()            
    except Exception as e:
        print ('\nERROR create_properties_dialog:', e)
        raise
    finally:
        UIM.remove(dlg.uid)    
        
        
def on_create_wavelet(*args, **kwargs):
    OM = ObjectManager()
    UIM = UIManager()
    #
    dlg = UIM.create('dialog_controller', title='Create Wavelet')
    #
    ctn_wavelet = dlg.view.AddCreateContainer('StaticBox', label='Wavelet', 
                                              orient=wx.VERTICAL, proportion=0, 
                                              flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddChoice(ctn_wavelet, proportion=0, flag=wx.EXPAND|wx.TOP, 
                       border=5, widget_name='wavelet', options=WAVELET_TYPES,
                       initial=0)
    #
    ctn_f0 = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Base frequency (f0)', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_f0, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='f0', initial='10.0') 
    #
    ctn_amp = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Amplitude', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_amp, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='amp', initial='1.0') 
    #    
    ctn_name = dlg.view.AddCreateContainer('StaticBox', 
                                           label='New wavelet name', 
                                           orient=wx.VERTICAL, 
                                           proportion=0, 
                                           flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_name, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='wavelet_name', 
                         initial='My Ricker Wavelet')     
    #    
    
    
    dlg.view.SetSize((300, 400))
    result = dlg.view.ShowModal()
    #
    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating wavelet. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()          
            print (results)
            
            wavelet = OM.new('wavelet', _type="Ricker", 
                             f0=results.get('f0'), 
                             amp=results.get('amp'), 
                             name=results.get('wavelet_name'))
                             
            result = OM.add(wavelet)
            
            print ('result wavelet:', result, args, kwargs)            
            
            
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
        
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)        
        
        
def on_create_simulation(*args, **kwargs):
    OM = ObjectManager()
    UIM = UIManager()
    #
    models_od = OrderedDict()
    models = OM.list('acoustic_2d_model')
    for model in models:
        models_od[model.name] = model.uid    
    #
    wavelets_od = OrderedDict()
    wavelets = OM.list('wavelet')
    for wavelet in wavelets:
        wavelets_od[wavelet.name] = wavelet.uid    
    #
    dlg = UIM.create('dialog_controller', title='Create Staggered Grid Simulation')
    #
    ctn_models = dlg.view.AddCreateContainer('StaticBox', label='Select Model', 
                                              orient=wx.VERTICAL, proportion=0, 
                                              flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddChoice(ctn_models, proportion=0, flag=wx.EXPAND|wx.TOP, 
                       border=5, widget_name='model', options=models_od,
                       initial=0) 
    #
    ctn_wavelet = dlg.view.AddCreateContainer('StaticBox', label='Select Wavelet', 
                                              orient=wx.VERTICAL, proportion=0, 
                                              flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddChoice(ctn_wavelet, proportion=0, flag=wx.EXPAND|wx.TOP, 
                       border=5, widget_name='wavelet', options=wavelets_od,
                       initial=0)
    # #
    # ctn_dt = dlg.view.AddCreateContainer('StaticBox', 
    #                                 label='Wavelet Time Step (dt)', 
    #                                 orient=wx.VERTICAL, 
    #                                 proportion=0, 
    #                                 flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_dt, proportion=0, flag=wx.EXPAND|wx.TOP, 
    #                      border=5, widget_name='dt', initial='0.01') 
    # #

    # ctn_time_stop = dlg.view.AddCreateContainer('StaticBox', 
    #                                 label='Wavelet Time Stop', 
    #                                 orient=wx.VERTICAL, 
    #                                 proportion=0, 
    #                                 flag=wx.EXPAND|wx.TOP, border=5)
    # dlg.view.AddTextCtrl(ctn_time_stop, proportion=0, flag=wx.EXPAND|wx.TOP, 
    #                      border=5, widget_name='time_stop', initial='1.0') 
    # #   

    #
    ctn_soux = dlg.view.AddCreateContainer('StaticBox', 
                                    label='Source point X', 
                                    orient=wx.VERTICAL, 
                                    proportion=0, 
                                    flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_soux, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='soux', initial='0') 
    #
    ctn_souy = dlg.view.AddCreateContainer('StaticBox', 
                                    label='Source point Y', 
                                    orient=wx.VERTICAL, 
                                    proportion=0, 
                                    flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_souy, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='souy', initial='0') 
    #
    ctn_sim_steps = dlg.view.AddCreateContainer('StaticBox', 
                                    label='Simulation Steps', 
                                    orient=wx.VERTICAL, 
                                    proportion=0, 
                                    flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_sim_steps, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='sim_steps', initial='200') 
    #    
    
    #    
    ctn_name = dlg.view.AddCreateContainer('StaticBox', 
                                           label='Simulation name', 
                                           orient=wx.VERTICAL, 
                                           proportion=0, 
                                           flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_name, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='simulation_name', 
                         initial='Staggered Grid 2 Layers Model')     
    #    
    
    
    dlg.view.SetSize((300, 500))
    result = dlg.view.ShowModal()
    #
    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating simulation. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()          
            print (results)
            
            wavefield, dx, dy, dt, cfl, c1 = staggeredGrid(results.get('model'),
                                                  results.get('wavelet'),
                                                  int(results.get('sim_steps')),
                                                  sou_x=int(results.get('soux')),
                                                  sou_y=int(results.get('souy'))
                                                  )
            
            simulation = OM.new('simulation', wavefield,
                                dx=dx, dy=dy, dt=dt,
                                sou_x=int(results.get('soux')),
                                sou_y=int(results.get('souy')),            
                                model_uid= results.get('model'),
                                wavelet_uid= results.get('wavelet'),
                                name=results.get('simulation_name'),
                                cfl=cfl, 
                                c1=c1)
            
                                #_type="Ricker", 
            # wavelet = OM.new('wavelet', _type="Ricker", 
            #                  f0=results.get('f0'), 
            #                  amp=results.get('amp'), 
            #                  name=results.get('wavelet_name'))
                             
            result = OM.add(simulation)
            
            print ('result simulation:', result, args, kwargs)
            
            
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
        
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)            
        
        
        
def on_create_teste(*args, **kwargs):
    OM = ObjectManager()
    UIM = UIManager()
    #        
    mwc = wx.GetApp().get_main_window_controller()
    tc = UIM.create('testeplot_controller', mwc.uid)      
                
                
                
                
                
                
                
                
                