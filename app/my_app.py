
import logging
import wx

from classes import class_register
from . import interface

from classes.uim import UIManager
from classes.om import ObjectManager


class MyApp(wx.App):
    
    # def __init__(self):
    #     #
    #     _redirect =  False
    #     _filename = None
    #     _useBestVisual = False
    #     _clearSigInt = True
    #     #
    #     super().__init__(_redirect, _filename, 
    #                                    _useBestVisual, _clearSigInt
    #     ) 
        
    def OnInit(self):
        logging.debug("Starting wxPython application...")
        self._mwc = None
        #
        logging.debug("Registering application classes...")
        class_register.register_app_classes()   
        logging.debug("Loading application interface...")
        self.load_app_interface()  
        return True           
 
    def load_app_interface(self):
        # Load app Interface
        self._mwc = interface.load()
        # 
        if self._mwc:
            # View-Controller app will bypass this call to self._mwc.view
            self._mwc.Show()    
            #
            self.SetTopWindow(self._mwc.view)      
            
    def get_main_window_controller(self):
        return self._mwc
              
    #TODO: REMOVER ISSO!!    
    def get_manager_class(self, obj_tid):
        if obj_tid in ObjectManager._types:
            return ObjectManager
        elif obj_tid in UIManager._types:
            return UIManager    
        raise Exception('App.gripy_app.get_manager_class: Class {} has a '+\
                        'unknown manager.'.format(obj_tid)
        )
            
            
            