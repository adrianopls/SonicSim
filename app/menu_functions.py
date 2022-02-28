
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
from PIL import Image

from . import interface
from classes.uim import UIManager
from classes.om import ObjectManager
from solver.sg import staggeredGrid
from solver.crystal.crystal import Crystal


WAVELET_TYPES = OrderedDict()
WAVELET_TYPES['Ricker'] = 'ricker'

LATTICE_TYPES = OrderedDict()
LATTICE_TYPES['Square'] = 'square'
LATTICE_TYPES['Hexagonal'] = 'hex'

COLOR_TYPES = OrderedDict()
COLOR_TYPES['White'] = 'white'
COLOR_TYPES['Black'] = 'black'



def on_console(*args, **kwargs):
    
    UIM = UIManager()
    mwc = wx.App.Get().get_main_window_controller()
    UIM.create('console_controller', mwc.uid)



def on_create_1_layer_image(*args, **kwargs):
    OM = ObjectManager()
    UIM = UIManager()
    #
    dlg = UIM.create('dialog_controller', title='Create 1 layer image')
    ctn_model = dlg.view.AddCreateContainer('StaticBox', label='Image', orient=wx.VERTICAL, 
                                              proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    #
    box_name = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                        orient=wx.HORIZONTAL, proportion=1, 
                                        flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_name, label='Name:', proportion=1)
    dlg.view.AddTextCtrl(box_name, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                         widget_name='image_name', initial="My image") 
           
   
    #
    box_color = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                        orient=wx.HORIZONTAL, proportion=1,
                                        flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_color, label='Color:', proportion=1)
    dlg.view.AddChoice(box_color, proportion=1, flag=wx.ALIGN_LEFT, 
                       widget_name='color', options=COLOR_TYPES, initial=0)
    #  
    

    #
    box_width_pixels = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                        orient=wx.HORIZONTAL, proportion=1,
                                        flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_width_pixels, label='Width pixels:', proportion=1)    
    dlg.view.AddTextCtrl(box_width_pixels, proportion=1, flag=wx.ALIGN_LEFT, 
                         border=5, widget_name='width_pixels', initial=100)  
    
    #  

    #
    box_height_pixels = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                        orient=wx.HORIZONTAL, proportion=1,
                                        flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_height_pixels, label='Height pixels:', proportion=1)    
    dlg.view.AddTextCtrl(box_height_pixels, proportion=1, flag=wx.ALIGN_LEFT, 
                         border=5, widget_name='height_pixels', initial=100)  
    
    #  
  
    
    #    
    dlg.view.SetSize((400, 250))
    result = dlg.view.ShowModal()

    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating model. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()  
            print(results)
            
            
            width = int(results.get('width_pixels'))
            height = int(results.get('height_pixels')) 
            
            if results.get('color') == "white":
                data = np.ones((height, width), dtype=np.ubyte) 
                data *= 255
            else:
                data = np.zeros((height, width), dtype=np.ubyte)
            

            img = OM.new('image', data, name=results.get('image_name'))
            result = OM.add(img)

            
            
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)

            
            
            
            

def on_create_2_layers_image(*args, **kwargs):
    
    OM = ObjectManager()
    UIM = UIManager()
    #
    dlg = UIM.create('dialog_controller', title='Create 2 layers image')
    #

    ctn_image = dlg.view.AddCreateContainer('StaticBox', label='Image', 
            orient=wx.VERTICAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    #
    box_name = dlg.view.AddCreateContainer('BoxSizer', ctn_image, 
            orient=wx.HORIZONTAL, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_name, label='Name:', proportion=1)
    dlg.view.AddTextCtrl(box_name, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                         widget_name='image_name', initial="") 
    #
    box_lattice = dlg.view.AddCreateContainer('BoxSizer', ctn_image, 
                                              orient=wx.HORIZONTAL, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_lattice, label='Lattice:', proportion=1)
    dlg.view.AddChoice(box_lattice, proportion=1, flag=wx.ALIGN_LEFT, 
                       widget_name='lattice', options=LATTICE_TYPES, initial=0)
    #   
    box_width = dlg.view.AddCreateContainer('BoxSizer', ctn_image, 
            orient=wx.HORIZONTAL, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_width, label='Width (pixels):', proportion=1)
    dlg.view.AddTextCtrl(box_width, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                         widget_name='image_width', initial="200") 
    #
    box_height = dlg.view.AddCreateContainer('BoxSizer', ctn_image, 
            orient=wx.HORIZONTAL, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_height, label='Height (pixels):', proportion=1)
    dlg.view.AddTextCtrl(box_height, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                         widget_name='image_height', initial="200") 
    #
    box_diameter = dlg.view.AddCreateContainer('BoxSizer', ctn_image, 
            orient=wx.HORIZONTAL, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
    dlg.view.AddStaticText(box_diameter, label='Circle diameter (pixels):', proportion=1)
    dlg.view.AddTextCtrl(box_diameter, proportion=1, flag=wx.ALIGN_LEFT, 
                         border=5, widget_name='diameter', initial=10) # 10px
    #    
    #
    

    
    dlg.view.SetSize((400, 380))
    result = dlg.view.ShowModal()

    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating image. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()  
            print(results)
            #filename='crystal_777.png'
            crystal = Crystal(ngrains=1, 
                  #seed_minimum_distance=float(results.get('seed_min_dist')), 
                  lattice = results.get('lattice'),
                  atom_diameter=float(results.get('diameter')),
                  xsize= float(results.get('image_width')), 
                  ysize=float(results.get('image_height')))

            crystal.grow_crystal()
            
            input_vec = crystal.plot_crystal(linewidth=0) #, filename=filename)


            print("\n\n")
            
            print ("\n\nfilename: ", results.get('image_name'))
            
            #input_vec = plt.imread(fullfilename)


            print(input_vec.shape)
            print(input_vec.dtype)
            
            
            ny, nx, ncolor = input_vec.shape
            
            new_vec = np.zeros((ny, nx), dtype=np.ubyte) 
            
            if (input_vec.shape[2] == 4):
                # RGBA
                for y in range(ny):
                    for x in range(nx):
                        
                        #print("haha: ", (input_vec[y, x, 0], input_vec[y, x, 1], input_vec[y, x, 2], input_vec[y, x, 3]))
                        
                        #a, b, c = input_vec[y, x]
                        r = int(input_vec[y, x, 0])
                        b = int(input_vec[y, x, 1])
                        g = int(input_vec[y, x, 2]) 
                        soma = r + g + b
                        
                        # print((input_vec[y, x, 0], input_vec[y, x, 1], input_vec[y, x, 2]), (input_vec[y, x, 0] + input_vec[y, x, 1] + input_vec[y, x, 2]))
                        # print(type(r), type(g), type(soma), soma)
                        
                        # print(int(r), int(g), int(soma))
                        
                        print(soma/3)
                        
                        if (soma/3) > 128:
                            new_vec[y, x] = 255
                            
                        else:
                            new_vec[y, x] = 0
                        

                
                
                #new_vec = np.array(Image.open(fullfilename).convert('L'))
                
                print(new_vec)
                #print(new_vec[100,100])
                values = np.unique(new_vec)
        
                print("\n\nVALUES.SIZE: ", values.size)
                
                input_vec = new_vec
            
            print(input_vec.shape)
            print(input_vec.dtype)
            
            
            img_obj = OM.new('image', input_vec, name=results.get('image_name'))

            result = OM.add(img_obj)
            
            
            
            # if (len(input_vec.shape) == 2):
            #     print(input_vec[100,100])
                
            # elif (len(input_vec.shape) == 3):    
                
            #     ny, nx, ncolor = input_vec.shape
                
            #     new_vec = np.zeros((ny, nx), dtype=np.int8)
                
            #     if (input_vec.shape[2] == 4):
            #         # RGBA
            #         for y in range(ny):
            #             for x in range(nx):
            #                 new_vec[y, x] = (input_vec[y, x, 0] + input_vec[y, x, 1] + 
            #                                  input_vec[y, x, 2] + input_vec[y, x, 3])/4  
                    
                    
            #         #new_vec = np.array(Image.open(fullfilename).convert('L'))
                    
            #         #print(new_vec)
            #         #print(new_vec[100,100])
            #         values = np.unique(new_vec)
            
            #         #print(values.size)
                    
            #         input_vec = new_vec
            #     #print(input_vec[100,100])




            # values = np.unique(input_vec)

            # am = OM.new('acoustic_2d_model', input_vec, 
            #             dx=results.get('x_spacing'), 
            #             dy=results.get('y_spacing'), 
            #             name=results.get('image_name'))
            # result = OM.add(am)
            
            # print ('result acoustic_2d_model:', result, args, kwargs)
    
    
            # layer1 = OM.new('geolayer', value=values[0], vp=results.get('matrix_vp'), rho=results.get('matrix_rho'), name="Layer 1")
            # result = OM.add(layer1, am.uid)
            # print ('result layer 1:', result)
            
            # if values.size == 2:
            #     layer2 = OM.new('geolayer', value=values[1], vp=results.get('pores_vp'), rho=results.get('pores_rho'), name="Layer 2")
            #     result = OM.add(layer2, am.uid)
            #     print ('result layer 2:', result)    
    
    
            # print(input_vec.shape)

            
            
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)




def on_load_image(*args, **kwargs):
    wildcard = "Load image file (*.png, *.tif)|*.png;*.tif"

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
    
    
    img = Image.open(fullfilename)
    data = np.asarray(img)
    
    
    
    print(data.shape)
    print(data.dtype)
    
    
    if (len(data.shape) == 2):
        print(data[100,100])
        
    # elif (len(input_vec.shape) == 3):    
        
    #     ny, nx, ncolor = input_vec.shape
        
    #     new_vec = np.zeros((ny, nx), dtype=np.int8)
        
    #     if (input_vec.shape[2] == 4):
    #         # RGBA
    #         for y in range(ny):
    #             for x in range(nx):
    #                 new_vec[y, x] = (input_vec[y, x, 0] + input_vec[y, x, 1] + 
    #                                  input_vec[y, x, 2] + input_vec[y, x, 3])/4  
            
            
    #         #new_vec = np.array(Image.open(fullfilename).convert('L'))
            
    #         print(new_vec)
    #         print(new_vec[100,100])
    #         values = np.unique(new_vec)
    
    #         print(values.size)
            
    #         input_vec = new_vec
    #     #print(input_vec[100,100])

    OM = ObjectManager()

    img_obj = OM.new('image', data, name=file_name)

    result = OM.add(img_obj)



def on_save_image(*args, **kwargs):
    
    OM = ObjectManager()
    UIM = UIManager()
    #
    images_od = OrderedDict()
    images = OM.list('image')
    for image in images:
        images_od[image.name] = image.uid    

    #
    dlg = UIM.create('dialog_controller', title='Save image file')
    ctn_image = dlg.view.AddCreateContainer('StaticBox', label='Select Image', 
                                            orient=wx.VERTICAL, proportion=0, 
                                            flag=wx.EXPAND|wx.TOP, border=5)


    dlg.view.AddChoice(ctn_image, proportion=0, flag=wx.EXPAND|wx.TOP, 
                       border=5, widget_name='images_choice', options=images_od,
                       initial=0) 
    #
    
    dlg.view.SetSize((300, 180))
    result = dlg.view.ShowModal()

  
    
    if result == wx.ID_OK:
        results = dlg.get_results()  
            
        print(results)    
    
        image_uid = results.get("images_choice")
    
    
        wildcard = "Save image file (*.png, *.tif)|*.png;*.tif"
    
        fdlg = wx.FileDialog(wx.App.Get().GetTopWindow(), 
                             "Save file", 
                             wildcard=wildcard, 
                             style=wx.FD_SAVE
        )
        
        if fdlg.ShowModal() == wx.ID_OK:
            file_name = fdlg.GetFilename()
            dir_name = fdlg.GetDirectory()
            fdlg.Destroy()
        else:
            fdlg.Destroy()
            return
        
        fullfilename = os.path.join(dir_name, file_name)        
        
        print("fullfilename: ", fullfilename)

        image = OM.get(image_uid)
        img = Image.fromarray(image.data)
        img.save(fullfilename)


    

def on_create_model(*args, **kwargs):
    
    OM = ObjectManager()
    UIM = UIManager()
    
    

    #
    images_od = OrderedDict()
    images = OM.list('image')
    for image in images:
        images_od[image.name] = image.uid    

    #
    dlg = UIM.create('dialog_controller', title='Chose image for model input')
    ctn_image = dlg.view.AddCreateContainer('StaticBox', label='Select Image', 
                                            orient=wx.VERTICAL, proportion=0, 
                                            flag=wx.EXPAND|wx.TOP, border=5)


    dlg.view.AddChoice(ctn_image, proportion=0, flag=wx.EXPAND|wx.TOP, 
                       border=5, widget_name='images_choice', options=images_od,
                       initial=0) 
    #
    
    dlg.view.SetSize((300, 180))
    result = dlg.view.ShowModal()

  
    
    if result == wx.ID_OK:
        results = dlg.get_results()  
            
        print(results)    
    
        image_uid = results.get("images_choice")    
        
        if not image_uid:
            return
        
        image = OM.get(image_uid)    
    
    
        values = np.unique(image.data)
        print(values)
        print(values.size)
    
        if values.size > 2:
            raise Exception("ERRO!")
    
    
        #
        dlg = UIM.create('dialog_controller', title='Create model')


        ctn_model = dlg.view.AddCreateContainer('StaticBox', label='Model', orient=wx.VERTICAL, 
                                                  proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
        #
        box_img_input = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                               orient=wx.HORIZONTAL, proportion=1, 
                                               flag=wx.EXPAND|wx.ALL, border=5)
        dlg.view.AddStaticText(box_img_input, label='Image input:', proportion=1)        
        dlg.view.AddTextCtrl(box_img_input, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                             widget_name='image_name', initial=image.name)         
        textctrl_image_name = dlg.view.get_object('image_name')
        textctrl_image_name.disable()        
        #
        box_name = dlg.view.AddCreateContainer('BoxSizer', ctn_model, 
                                               orient=wx.HORIZONTAL, proportion=1, 
                                               flag=wx.EXPAND|wx.ALL, border=5)
        dlg.view.AddStaticText(box_name, label='Name:', proportion=1)
        dlg.view.AddTextCtrl(box_name, proportion=1, flag=wx.ALIGN_LEFT, border=5, 
                             widget_name='model_name', initial="My model") 
        #
    
    
    # X Axis
    #
    def on_change_x_size(name, old_value, new_value, **kwargs):
        try:
            x_samples = float(dlg.view.get_object('x_samples').get_value())
            x_spacing = float(dlg.view.get_object('x_spacing').get_value())
            res = str(x_samples * x_spacing) 
        except:
            res = ""
        textctrl_x_size = dlg.view.get_object('x_size')
        textctrl_x_size.set_value(res)      
    #
    #
    ctn_x_axis = dlg.view.AddCreateContainer('StaticBox', label='X axis', 
        orient=wx.HORIZONTAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    #
    ctn_x_samples = dlg.view.AddCreateContainer('StaticBox', ctn_x_axis, 
            label='Samples(pixels)', orient=wx.VERTICAL, proportion=1, 
            flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_x_samples, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='x_samples', initial=image.width)
    textctrl_x_pixels = dlg.view.get_object('x_samples')
    textctrl_x_pixels.disable()
    #textctrl_x_samples.set_trigger(on_change_x_size)
    #
    ctn_x_spacing = dlg.view.AddCreateContainer('StaticBox', ctn_x_axis, 
                label='Spacing(m)', orient=wx.VERTICAL, proportion=1, 
                flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_x_spacing, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='x_spacing', initial=1)
    
    
    textctrl_x_spacing = dlg.view.get_object('x_spacing')
    textctrl_x_spacing.set_trigger(on_change_x_size)
    #
    ctn_x_size = dlg.view.AddCreateContainer('StaticBox', ctn_x_axis, 
                label='Size(m)', orient=wx.VERTICAL, proportion=1, 
                flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_x_size, proportion=1, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='x_size')
    textctrl_x_size = dlg.view.get_object('x_size')
    textctrl_x_size.disable()
    #
    on_change_x_size(None, None, None)
    #    
          
    
    # Y Axis
    #   
    def on_change_y_size(name, old_value, new_value, **kwargs):
        try:
            y_samples = float(dlg.view.get_object('y_samples').get_value())
            y_spacing = float(dlg.view.get_object('y_spacing').get_value())
            res = str(y_samples * y_spacing) 
        except:
            res = ""
        textctrl_y_size = dlg.view.get_object('y_size')
        textctrl_y_size.set_value(res)      
    #
    #
    ctn_y_axis = dlg.view.AddCreateContainer('StaticBox', label='Y axis', 
                                             orient=wx.HORIZONTAL, 
                                             proportion=0, 
                                             flag=wx.EXPAND|wx.TOP, border=5)
    #
    ctn_y_samples = dlg.view.AddCreateContainer('StaticBox', ctn_y_axis, 
                                                label='Samples(pixels)', 
                                                orient=wx.VERTICAL, 
                                                proportion=1, 
                                                flag=wx.EXPAND|wx.TOP, 
                                                border=5)
    dlg.view.AddTextCtrl(ctn_y_samples, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='y_samples', initial=image.height)
    textctrl_y_pixels = dlg.view.get_object('y_samples')
    textctrl_y_pixels.disable()
    #textctrl_y_samples.set_trigger(on_change_y_size)
    #
    ctn_y_spacing = dlg.view.AddCreateContainer('StaticBox', ctn_y_axis, 
                                                label='Spacing(m)', 
                                                orient=wx.VERTICAL, 
                                                proportion=1, 
                                                flag=wx.EXPAND|wx.TOP, 
                                                border=5)
    dlg.view.AddTextCtrl(ctn_y_spacing, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='y_spacing', initial=1)
    textctrl_y_spacing = dlg.view.get_object('y_spacing')
    textctrl_y_spacing.set_trigger(on_change_y_size)
    #
    ctn_y_size = dlg.view.AddCreateContainer('StaticBox', ctn_y_axis, 
                                                label='Size(m)', 
                                                orient=wx.VERTICAL, 
                                                proportion=1, 
                                                flag=wx.EXPAND|wx.TOP, 
                                                border=5)
    dlg.view.AddTextCtrl(ctn_y_size, proportion=1, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='y_size')
    textctrl_y_size = dlg.view.get_object('y_size')
    textctrl_y_size.disable()
    #
    on_change_y_size(None, None, None)
    #    
    
    if values[0] == 0:
        value_layer_1_text = "color: Black"
    elif values[0] == 255:    
        value_layer_1_text = "color: White"
    else:    
        value_layer_1_text = "value: " + str(values[0])
    
    ctn_prop_matrix = dlg.view.AddCreateContainer('StaticBox', 
            label="Layer 1 properties (" + value_layer_1_text + ")", 
            orient=wx.HORIZONTAL, proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
    #
    ctn_matrix_vp = dlg.view.AddCreateContainer('StaticBox', ctn_prop_matrix, 
                                                label='Vp(m/s)', orient=wx.VERTICAL, proportion=1, flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_matrix_vp, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='matrix_vp', initial=4000.0)  
    #
    ctn_matrix_rho = dlg.view.AddCreateContainer('StaticBox', ctn_prop_matrix, 
                                                label='Rho(m/s)', orient=wx.VERTICAL, proportion=1, flag=wx.EXPAND|wx.TOP, border=5)
    dlg.view.AddTextCtrl(ctn_matrix_rho, proportion=0, flag=wx.EXPAND|wx.TOP, 
                         border=5, widget_name='matrix_rho', initial=3.0)  
    #
    
    if values.size == 2:
        if values[1] == 0:
            value_layer_2_text = "color: Black"
        elif values[1] == 255:    
            value_layer_2_text = "color: White"
        else:    
            value_layer_2_text = "value: " + str(values[1])
            
        ctn_prop_pores = dlg.view.AddCreateContainer('StaticBox',
                label="Layer 2 properties (" + value_layer_2_text + ")", 
                orient=wx.HORIZONTAL, 
                proportion=0, flag=wx.EXPAND|wx.TOP, border=5)
        #          
        ctn_pores_vp = dlg.view.AddCreateContainer('StaticBox', ctn_prop_pores, 
                label='Vp(m/s)', orient=wx.VERTICAL, 
                proportion=1, flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_pores_vp, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='pores_vp', initial=2500.0)  
        #
        ctn_pores_rho = dlg.view.AddCreateContainer('StaticBox', ctn_prop_pores, 
                label='Rho(m/s)', orient=wx.VERTICAL, proportion=1, 
                flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_pores_rho, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='pores_rho', initial=2.2)  
        #    
    
    dlg.view.SetSize((400, 580))
    result = dlg.view.ShowModal()

    try:
        disableAll = wx.WindowDisabler()
        wait = wx.BusyInfo("Creating model. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()  
            
            print(results)


            am = OM.new('acoustic_2d_model', 
                        image_uid=image.uid,
                        dx=results.get('x_spacing'), 
                        dy=results.get('y_spacing'), 
                        name=results.get('model_name'))
            result = OM.add(am)
            
            print ('result acoustic_2d_model:', result, args, kwargs)
    

    
            layer1 = OM.new('geolayer', value=values[0], 
                    vp=results.get('matrix_vp'), rho=results.get('matrix_rho'),
                    name="Layer 1")
            result = OM.add(layer1, am.uid)
            print ('result layer 1:', result)
            
            
            if values.size == 2:
                layer2 = OM.new('geolayer', value=values[1], 
                    vp=results.get('pores_vp'), rho=results.get('pores_rho'), 
                    name="Layer 2")
                result = OM.add(layer2, am.uid)
                print ('result layer 2:', result)    
    
    

            
            
    except Exception as e:
        print ('ERROR [on_create_model]:', str(e))
        raise
    finally:
        del wait
        del disableAll
        UIM.remove(dlg.uid)





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
    
    
    print(input_vec.shape)
    print(input_vec.dtype)
    
    if (len(input_vec.shape) == 2):
        print(input_vec[100,100])
        
    elif (len(input_vec.shape) == 3):    
        
        ny, nx, ncolor = input_vec.shape
        
        new_vec = np.zeros((ny, nx), dtype=np.int8)
        
        if (input_vec.shape[2] == 4):
            # RGBA
            for y in range(ny):
                for x in range(nx):
                    new_vec[y, x] = (input_vec[y, x, 0] + input_vec[y, x, 1] + 
                                     input_vec[y, x, 2] + input_vec[y, x, 3])/4  
            
            
            #new_vec = np.array(Image.open(fullfilename).convert('L'))
            
            print(new_vec)
            print(new_vec[100,100])
            values = np.unique(new_vec)
    
            print(values.size)
            
            input_vec = new_vec
        #print(input_vec[100,100])
        
        
    
    
    values = np.unique(input_vec)
    
    print(values.size)
    
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
    
    
            layer1 = OM.new('geolayer', value=values[0], vp=results.get('vp1'),
                            rho=results.get('rho1'), name="Layer 1")
            result = OM.add(layer1, am.uid)
            print ('result layer 1:', result)
            
            if values.size == 2:
                layer2 = OM.new('geolayer', value=values[1],
                                vp=results.get('vp2'), rho=results.get('rho2'),
                                name="Layer 2")
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
        #disableAll = wx.WindowDisabler()
        #wait = wx.BusyInfo("Creating simulation. Wait...")
        if result == wx.ID_OK:
            results = dlg.get_results()          
            #print (results)
            
            
            dialog = wx.ProgressDialog("Staggered grid simulation", "Time remaining", 
                                int(results.get('sim_steps')),
                                style=wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME|wx.PD_REMAINING_TIME
            )
            
            wavefield, dx, dy, dt, cfl, c1 = staggeredGrid(results.get('model'),
                                                  results.get('wavelet'),
                                                  int(results.get('sim_steps')),
                                                  sou_x=int(results.get('soux')),
                                                  sou_y=int(results.get('souy')),
                                                  progress_dialog=dialog
            )
            #
            
            #
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
        #raise
        
    finally:
        dialog.Destroy()
        #del wait
        #del disableAll
        UIM.remove(dlg.uid)            
        
        
        
def on_create_teste(*args, **kwargs):
    OM = ObjectManager()
    UIM = UIManager()
    #        
    mwc = wx.GetApp().get_main_window_controller()
    tc = UIM.create('testeplot_controller', mwc.uid)      
                
                
                
                
                
                
                
                
                