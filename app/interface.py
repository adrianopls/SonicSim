
import logging
import wx

import app
from classes.om import ObjectManager
from classes.uim import UIManager


"""
Loads Application Initial Interface (MainWindow and it's children).
"""
def load():

    if wx.GetApp().get_main_window_controller():
        raise Exception("Main app Interface cannot be loaded again.")
    
    app = wx.GetApp()
    UIM = UIManager()
    
    
    # mwc = UIM.create('frame_controller', 
    #                   icon='add.ico',  # Relative Path to icons dir
    #                   size=(800, 600),
    #                   pos=(100, 100),
    #                   #maximized=True,
    #                   title="That's My app!"
    # )



    mwc = UIM.create('main_window_controller', 
                     icon='signal_32_32.bmp',
                     size=(1000, 800),
                     pos=(100, 100),
                     #maximized=True,
                     title="SonicSim 0.1b"
    )
    
    # Tree Controller                                                          
    UIM.create('tree_controller', mwc.uid)     

    # Menubar
    menubar_ctrl = UIM.create('menubar_controller', mwc.uid)
    
    
    mc_image = UIM.create('menu_controller', menubar_ctrl.uid, label=u"&Image")         

    UIM.create('menu_item_controller', mc_image.uid, 
            label="&Create 1 layer image", 
            #id=wx.ID_OPEN,
            callback="app.menu_functions.on_create_1_layer_image"
    )     

    UIM.create('menu_item_controller', mc_image.uid, 
            label="&Create 2 layers image", 
            callback="app.menu_functions.on_create_2_layers_image"
    )        

    UIM.create('menu_item_controller', mc_image.uid, 
            label="Load image", 
            callback="app.menu_functions.on_load_image"
    )  

    UIM.create('menu_item_controller', mc_image.uid, 
            label="Save image", 
            callback="app.menu_functions.on_save_image"
    )  
    
    UIM.create('menu_item_controller', mc_image.uid, 
                    kind=wx.ITEM_SEPARATOR
    )    
    UIM.create('menu_item_controller', mc_image.uid, 
            label=u'Exit', 
            help=u'Exits application.',
            id=wx.ID_EXIT#,
            #callback='app.menu_functions.on_exit'
    )      



    mc_model = UIM.create('menu_controller', menubar_ctrl.uid, 
                            label=u"&Model")            
    UIM.create('menu_item_controller', mc_model.uid, 
            label="&Create model", 
            help="Create a new model",
            #id=wx.ID_OPEN,
            callback="app.menu_functions.on_create_model"
    )       
    
    # UIM.create('menu_item_controller', mc_model.uid, 
    #         label="&Load model", 
    #         help="Load a model from file",
    #         id=wx.ID_OPEN,
    #         callback='app.menu_functions.on_load_model'
    # )        
       
    UIM.create('menu_item_controller', mc_model.uid, 
            label="&Save model", 
            help="Save a model into file",
            enabled=False
            #id=wx.ID_OPEN,
            #callback='app.menu_functions.on_open'
    )         
     
    
      
 
  
    mc_wavelet = UIM.create('menu_controller', menubar_ctrl.uid, 
                        label="Wavelet")      
    UIM.create('menu_item_controller', mc_wavelet.uid, 
            label="Create Wavelet", 
            callback='app.menu_functions.on_create_wavelet'
    )    

        
    mc_sim = UIM.create('menu_controller', menubar_ctrl.uid, 
                            label="Simulation type")                          
    UIM.create('menu_item_controller', mc_sim.uid, 
            label="Staggered grid",
            callback='app.menu_functions.on_create_simulation'
    )             
    UIM.create('menu_item_controller', mc_sim.uid, 
            label="Rotated Staggered grid",
            enabled=False
            #callback='app.menu_functions.on_open'
    )        

    
    mc_about = UIM.create('menu_controller', menubar_ctrl.uid, 
                    label="About")    
        
 
    UIM.create('menu_item_controller', mc_about.uid, 
            label="Console",
            callback='app.menu_functions.on_console'
    )   


    UIM.create('menu_item_controller', mc_about.uid, 
            label="Teste",
            callback='app.menu_functions.on_create_teste'
    )   


    
    # mwc = UIM.create('main_window_controller', 
    #                  icon='add.ico',  # Relative Path to icons dir
    #                  size=(800, 600),
    #                  pos=(100, 100),
    #                  #maximized=True,
    #                  title="That's My app!"
    # )
      
    # Tree Controller                                                          
    # UIM.create('tree_controller', mwc.uid)     

    # Menubar
    # menubar_ctrl = UIM.create('menubar_controller', mwc.uid)
        
    # mc_model = UIM.create('menu_controller', menubar_ctrl.uid, 
    #                         label=u"&Model")            
    # UIM.create('menu_item_controller', mc_model.uid, 
    #         label="&Load model", 
    #         help="Load a model from file",
    #         id=wx.ID_OPEN,
    #         callback='app.menu_functions.on_open_model'
    # )        
    # UIM.create('menu_item_controller', mc_model.uid, 
    #         label="&Create model", 
    #         help="Create a new model",
    #         enabled=False
    #         #id=wx.ID_OPEN,
    #         #callback='app.menu_functions.on_open'
    # )          
    # UIM.create('menu_item_controller', mc_model.uid, 
    #         label="&Save model", 
    #         help="Save a model into file",
    #         enabled=False
    #         #id=wx.ID_OPEN,
    #         #callback='app.menu_functions.on_open'
    # )         
    # UIM.create('menu_item_controller', mc_model.uid, 
    #                 kind=wx.ITEM_SEPARATOR
    # )    
    # UIM.create('menu_item_controller', mc_model.uid, 
    #         label=u'Exit', 
    #         help=u'Exits application.',
    #         id=wx.ID_EXIT#,
    #         #callback='app.menu_functions.on_exit'
    # )           
                 
            
    # Main ToolBar 
    # tbc = UIM.create('toolbar_controller', mwc.uid)
    # UIM.create('toolbartool_controller', tbc.uid,
    #                 label=u"New project", 
    #                 bitmap='new_file-30.png',
    #                 help='New project', 
    #                 long_help='Start a new Gripy project, closes existing',
    #                 callback='app.menu_functions.on_new'
    # )            
    # UIM.create('toolbartool_controller', tbc.uid,
    #                 label=u"Abrir projeto", 
    #                 bitmap='open_folder-30.png',
    #                 help='Abrir projeto', 
    #                 long_help='Abrir projeto GriPy',
    #                 callback='app.menu_functions.on_open'
    # )
    # UIM.create('toolbartool_controller', tbc.uid,
    #                 label=u"Salvar projeto", 
    #                 bitmap='save_close-30.png',
    #                 help='Salvar projeto', 
    #                 long_help='Salvar projeto GriPy',
    #                 callback='app.menu_functions.on_save'
    # )
    # UIM.create('toolbartool_controller', tbc.uid,
    #                 label=u"Well Plot", 
    #                 bitmap='oil_rig-30.png',
    #                 help='Well Plot', 
    #                 long_help='Well Plot',
    #                 callback='app.menu_functions.on_new_wellplot'
    # )
    # UIM.create('toolbartool_controller', tbc.uid,
    #                 label=u"Crossplot", 
    #                 bitmap='scatter_plot-30.png',
    #                 help='Crossplot', 
    #                 long_help='Crossplot',
    #                 callback='app.menu_functions.on_new_crossplot'
    # )               

    # StatusBar
    # UIM.create('statusbar_controller', mwc.uid, 
    #     label='Bem vindo ao ' + \
    #     app.gripy_app.GripyApp.Get()._gripy_app_state.get('app_display_name')
    # )  
        
    
    
    
    _LOADED = True
    return mwc

   
    

  

