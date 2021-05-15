
import logging
import wx

import app
from classes.uim import UIManager
from classes.om import ObjectManager

"""
Loads Application Initial Interface (MainWindow and it's children).
"""
def load():

    if wx.GetApp().get_main_window_controller():
        raise Exception("Main app Interface cannot be loaded again.")
    
    app = wx.GetApp()
    UIM = UIManager()
    
    
    mwc = UIM.create('frame_controller', 
                      icon='add.ico',  # Relative Path to icons dir
                      size=(800, 600),
                      pos=(100, 100),
                      #maximized=True,
                      title="That's My app!"
    )
 
    # OM = ObjectManager()    
    # well = OM.new('well', name="MEU POCO SINISTRO") 
    # print(well)
    # print(well.name)
        
    
    
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

   
    

  

