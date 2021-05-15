
import logging

from classes.om.manager import ObjectManager
from .uim import UIManager
#
from .om.well import Well
#
from .uim import FrameController, Frame
from .uim import DialogController, Dialog
from .uim import TreeController, TreeView
#
from .uim import MainWindowController, MainWindow
from .uim import MenuBarController, MenuBarView
from .uim import MenuController, MenuView
from .uim import MenuItemController, MenuItemView
#
from .uim import ToolBarController, ToolBar
from .uim import ToolBarToolController
from .uim import StatusBarController, StatusBar
#
from .uim import CrossPlotController, CrossPlot
from .uim import WorkPageController, WorkPage                                          
from .uim import PropertyGridController, PropertyGridView
#                                            
from .uim import CanvasPlotterController, CanvasPlotter                
from .uim import TrackCanvasController, TrackCanvas   
from .uim import TrackLabelController, TrackLabel
                   



def register_app_classes():
    logging.debug("Registering ObjectManager classes...")
    register_OM_classes()
    logging.debug("ObjectManager classes registered successfully")
    logging.debug("Registering UIManager classes...")
    register_UIManager_classes()    
    logging.debug("UIManager classes registered successfully")
    
    
def register_OM_classes():
    ObjectManager.register_class(Well)
#     ObjectManager.register_class(CurveSet, Well)
#     ObjectManager.register_class(DataIndex, CurveSet)
#     ObjectManager.register_class(Log, CurveSet)
#     #
#     ObjectManager.register_class(Seismic)
#     ObjectManager.register_class(DataIndex, Seismic)
#     ObjectManager.register_class(DataIndexMap, Seismic)
#     #
#     ObjectManager.register_class(DataIndexMap, Log)
#     #
#     ObjectManager.register_class(Gather, Well)
#     ObjectManager.register_class(DataIndex, Gather)
#     ObjectManager.register_class(DataIndexMap, Gather)
#     #
#     ObjectManager.register_class(Spectogram, Log)
#     ObjectManager.register_class(Spectogram, Gather)
#     ObjectManager.register_class(Spectogram, Seismic)
#     ObjectManager.register_class(DataIndexMap, Spectogram)
#     ObjectManager.register_class(DataIndex, Spectogram)
#     #    
    
    """
#    ObjectManager.register_class(IndexSet, Well)
    ObjectManager.register_class(Core, Well)
    #
    
    #
    ObjectManager.register_class(Partition, Well)
    ObjectManager.register_class(Part, Partition)
    ObjectManager.register_class(Property, Partition)
    ObjectManager.register_class(Property, Part)
    ObjectManager.register_class(Partition) #remover apos alterar pra rocktbale
    ObjectManager.register_class(RockTable)
    ObjectManager.register_class(RockType, RockTable)
    ObjectManager.register_class(Inference, Well)
    ObjectManager.register_class(Part, Inference)
    ObjectManager.register_class(Rock)   #remover apos alterar pra rocktbale
    ObjectManager.register_class(Rock, Partition)   #remover apos alterar pra rocktbale
    ObjectManager.register_class(Rock, Well)   #remover apos alterar pra rocktbale
    ObjectManager.register_class(Fluid)																			   
    #
    ObjectManager.register_class(Seismic)
    
#    ObjectManager.register_class(IndexSet, Seismic)
    #
    ObjectManager.register_class(Scalogram, Seismic)
    ObjectManager.register_class(DataIndex, Scalogram)
#    ObjectManager.register_class(IndexSet, Scalogram)
    #
    
    ObjectManager.register_class(DataIndex, WellGather)  
#    ObjectManager.register_class(IndexSet, WellGather)

    ObjectManager.register_class(GatherSpectogram, Well)
    ObjectManager.register_class(DataIndex, GatherSpectogram)
#    ObjectManager.register_class(IndexSet, GatherSpectogram)
    #
    ObjectManager.register_class(GatherScalogram, Well)
    ObjectManager.register_class(DataIndex, GatherScalogram)
#    ObjectManager.register_class(IndexSet, GatherScalogram)
    #
    ObjectManager.register_class(Rock, Well)
    ObjectManager.register_class(Fluid, Well)
    #
#    ObjectManager.register_class(DataIndex, IndexSet)
    
    ObjectManager.register_class(Model1D, Well)
    ObjectManager.register_class(DataIndex, Model1D)
    #
#    ObjectManager.register_class(IndexSet, Model1D)
    #
    ObjectManager.register_class(ZoneSet, Well)
    ObjectManager.register_class(Zone, ZoneSet)
    ObjectManager.register_class(Property, Zone)
    #
    """
    
def register_UIManager_classes():
    UIManager.register_class(FrameController, Frame)
    UIManager.register_class(DialogController, Dialog)
    UIManager.register_class(TreeController, TreeView, FrameController) 
    UIManager.register_class(MainWindowController, MainWindow)    
    UIManager.register_class(TreeController, TreeView, MainWindowController) 
    UIManager.register_class(MenuBarController, MenuBarView, MainWindowController) 
    UIManager.register_class(MenuController, MenuView, MenuBarController)
    UIManager.register_class(MenuController, MenuView, MenuController)
    UIManager.register_class(MenuItemController, MenuItemView, MenuController)
    UIManager.register_class(ToolBarController, ToolBar, MainWindowController)     
    UIManager.register_class(ToolBarToolController, None, ToolBarController)  
#    UIManager.register_class(TreeController, TreeView, MainWindowController)
    UIManager.register_class(StatusBarController, StatusBar, MainWindowController)
    # 
    UIManager.register_class(WorkPageController, WorkPage, MainWindowController)
    UIManager.register_class(WorkPageController, WorkPage, FrameController)
    #
#    UIManager.register_class(WellPlotController, WellPlot, MainWindowController)
#    UIManager.register_class(WellPlotController, WellPlot, FrameController)
    #
    UIManager.register_class(CrossPlotController, CrossPlot, MainWindowController)
    UIManager.register_class(CrossPlotController, CrossPlot, FrameController)
    # 
#    UIManager.register_class(ConsoleController, Console, MainWindowController)
#    UIManager.register_class(ConsoleController, Console, FrameController)
    #    
#    UIManager.register_class(TrackController, TrackView, WellPlotController)
    # UIManager.register_class(TrackObjectController, None,
    #                           TrackController
    # )
    # UIManager.register_class(WellPlotEditorController, WellPlotEditor, 
    #                          WellPlotController
    # )
    #
    # UIManager.register_class(NavigatorController, Navigator, 
    #                          TrackObjectController
    # )
    #
    # UIManager.register_class(LineRepresentationController, 
    #                          LineRepresentationView, TrackObjectController
    # )
    # UIManager.register_class(IndexRepresentationController, 
    #                          IndexRepresentationView, TrackObjectController
    # )
    # UIManager.register_class(DensityRepresentationController, 
    #                          DensityRepresentationView, TrackObjectController
    # )
#    UIManager.register_class(PatchesRepresentationController,
#                              PatchesRepresentationView, TrackObjectController
#    )
#    UIManager.register_class(ContourfRepresentationController,  
#                              ContourfRepresentationView, TrackObjectController
#    )    
    #
    # UIManager.register_class(LPEWellPlotPanelController, LPEWellPlotPanel, 
    #                          WellPlotEditorController
    # )    
    # UIManager.register_class(LPETrackPanelController, LPETrackPanel, 
    #                          WellPlotEditorController
    # )
    # UIManager.register_class(LPEObjectsPanelController, LPEObjectsPanel, 
    #                          WellPlotEditorController
    # )
    # UIManager.register_class(PropertyGridController,
    #                          PropertyGridView, LPEObjectsPanelController
    # )
    #

    UIManager.register_class(CanvasPlotterController, CanvasPlotter, CrossPlotController) 
    
    #
    UIManager.register_class(FrameController, Frame, MainWindowController)
    #
    # UIManager.register_class(TrackCanvasController, TrackCanvas, TrackController)
    # UIManager.register_class(TrackLabelController, TrackLabel, TrackController)
    #
    # UIManager.register_class(ObjectPropertiesDialogController, 
    #                                              ObjectPropertiesDialog)
    # UIManager.register_class(PropertyGridController,
    #                          PropertyGridView, ObjectPropertiesDialogController
    # )    
    # UIManager.register_class(PropertyGridController,
    #                          PropertyGridView, LPEWellPlotPanelController
    # ) 
    #
    #UIManager.register_class(DataMaskController, DataMask, TrackObjectController)      
    # UIManager.register_class(LASHeaderController, LASHeader)
    # #
    # UIManager.register_class(WellImportFrameController, WellImportFrame, MainWindowController)    
    
    
    
    
    
    