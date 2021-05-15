
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

import os
import wx


def on_open(*args, **kwargs):
    wildcard = "Load segmentated file (*.png)|*.png"
    try:
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
        
        print (fullfilename)
        
        #gripy_app = wx.App.Get()
        #gripy_app.load_project_data(fullfilename)
    except Exception as e:
        print ('ERROR [on_open]:', str(e))
        raise


