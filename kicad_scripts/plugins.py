import math
import os

import wx
import pcbnew

from tangents import *

#MARKERS
#COLORS_DESIGN_SETTINGS
#
#
#

#test = [1,0,0,2,4,0]
#print(test)
#print(get_outer_tangents(*test))
#print(get_inner_tangents(*test))

class SpreadNets(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Spread Nets"
        self.category = "Routing"
        self.description = "For the given selection, fill unassigned nets with the net on other selected objects"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'connect_nets.png')

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()
        tracks = list(filter(lambda x: x.IsSelected(), board.GetTracks()))
        spread_nets(tracks)



class FlipECOMarkers(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Flip ECO"
        self.category = "Routing"
        self.description = "Swap Layers of Selection on ECO 1/2"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'flip_eco.png')

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()
        drws = list(filter(lambda x: x.IsSelected(), board.GetDrawings()))
        for drw in drws:
            if drw.GetLayer() == board.GetLayerID('Eco1.User'):
                drw.SetLayer(board.GetLayerID('Eco2.User'))
            elif drw.GetLayer() == board.GetLayerID('Eco2.User'):
                drw.SetLayer(board.GetLayerID('Eco1.User'))


class PlaceBusNode(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Place Bus Node"
        self.category = "Routing"
        self.description = "Place silkscreen markings for a bus node at the grid origin"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'bus_node.png')
        self.pattern = "1"
        self.default_side = 'Top'
        config = pcbnew.GetBoard().GetDesignSettings()
        self.default_clearance = config.GetSmallestClearanceValue()

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()

        dialog = BusNodeDialog(None, board, self)
        dialog.Show(True)


busnodeplugin = PlaceBusNode()

class BusNodeDialog(wx.Dialog):
    
    def __init__(self, parent, board, plugin):
        wx.Dialog.__init__(self, parent, title= "Bus Node Configuration")
        self.board = board
        config = board.GetDesignSettings()
        self.plugin = plugin

        unit_name, ToUnit, self.FromUnit = get_units()

        box = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self)

        self.text_boxes = {}

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        #left column
        ssbox = wx.BoxSizer(wx.VERTICAL)

        #pattern
        label = wx.StaticText(self.panel, label = "Bus positions")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.pattern = wx.TextCtrl(self.panel, value = plugin.pattern, size=(250, h*1.5))
        ssbox.Add(self.pattern,   proportion=0)

        subbox.Add(ssbox, 0, wx.RIGHT|wx.LEFT, 10)

        #right column
        ssbox = wx.BoxSizer(wx.VERTICAL)
        #layer
        label = wx.StaticText(self.panel, label = f"Board Side")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.layer_box = wx.ComboBox(self.panel, value = plugin.default_side, choices = ['Top', 'Bottom'], size=(120, h*1.5))
        ssbox.Add(self.layer_box,   proportion=0)

        subbox.Add(ssbox, 0)
        box.Add(subbox, 0, wx.TOP, 10)

        subbox = wx.BoxSizer(wx.HORIZONTAL)

        #left column
        ssbox = wx.BoxSizer(wx.VERTICAL)
        #width
        label = wx.StaticText(self.panel, label = f"Trace Width ({unit_name})")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.trace_width = wx.TextCtrl(self.panel, value = str(ToUnit(config.GetCurrentTrackWidth())), size=(120, h*1.5))
        ssbox.Add(self.trace_width,   proportion=0)
        
        #pad size
        xp, yp = board.GetGridOrigin()
        pad = board.GetPad(pcbnew.wxPoint(xp, yp))
        try:
            radius = pad.GetBoundingRadius()
        except:
            radius = 0

        label = wx.StaticText(self.panel, label = f"Pad Radius  ({unit_name})")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.radius = wx.TextCtrl(self.panel, value = str(ToUnit(radius)), size=(120, h*1.5))
        ssbox.Add(self.radius,   proportion=0)

        go_button = wx.Button(self.panel, label="Create", id=1)
        ssbox.Add(go_button,  proportion=0)

        subbox.Add(ssbox, 0, wx.RIGHT|wx.LEFT, 10)
        
        #right column

        ssbox = wx.BoxSizer(wx.VERTICAL)
        #clearance
        label = wx.StaticText(self.panel, label = f"Clearance ({unit_name})")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.clearance_width = wx.TextCtrl(self.panel, value = str(ToUnit(plugin.default_clearance)), size=(120, h*1.5))
        ssbox.Add(self.clearance_width,   proportion=0)

        #padding
        label = wx.StaticText(self.panel, label = f"Extra Padding  ({unit_name})")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.padding_width = wx.TextCtrl(self.panel, value = "0", size=(120, h*1.5))
        ssbox.Add(self.padding_width,   proportion=0)

        cancel_button = wx.Button(self.panel, label="Cancel", id=2)
        ssbox.Add(cancel_button,  proportion=0)

        subbox.Add(ssbox)
        box.Add(subbox)

        self.panel.SetSizer(box)
        self.Bind(wx.EVT_BUTTON, self.OnPress, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=2)

    def OnPress(self, event):
        board = self.board
        pattern = self.pattern.GetValue()
        trace_width = self.FromUnit(float(self.trace_width.GetValue()))
        clearance = self.FromUnit(float(self.clearance_width.GetValue()))
        radius = self.FromUnit(float(self.radius.GetValue()))
        padding = self.FromUnit(float(self.padding_width.GetValue()))

        self.plugin.default_clearance = clearance

        if self.layer_box.GetValue() == 'Top':
            #layer = board.GetLayerID('F.SilkS')
            layer = board.GetLayerID('Eco1.User')
        else:
            #layer = board.GetLayerID('B.SilkS')
            layer = board.GetLayerID('Eco2.User')
        self.plugin.default_side = self.layer_box.GetValue()

        self.plugin.pattern = pattern
        pattern = [float(x) for x in pattern.split(' ')]

        xp, yp = board.GetGridOrigin()
        pad = board.GetPad(pcbnew.wxPoint(xp, yp))
        if pad != None:
            xp, yp = pad.GetCenter()

        base_radius = radius + clearance + trace_width/2 + padding
        delta_radius = clearance+trace_width

        radii = [base_radius + (x-1)*delta_radius for x in pattern]
        circles = [[r, xp, yp] for r in radii]
        
        print(circles)

        add_circles(circles, trace_width, layer, board)

        self.Close()

    def OnCancel(self, event):
        self.Close()

class CompleteArcs(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Complete Arcs"
        self.category = "Routing"
        self.description = "For the selected bus nodes and tracks, find all tracks that have matching endpoints on a bus node and create arc tracks to complete them."
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'complete_arcs.png')
        self.force = False

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()

        tracks = list(filter(lambda x: x.GetClass() == 'TRACK' and x.IsSelected(), board.GetTracks()))
        print(f'Selected Tracks: {tracks}')
        layers = list(set(map(lambda x: x.GetLayer(), tracks)))
        track_map = {k: list(filter(lambda x: x.GetLayer() == k, tracks)) for k in layers}

        nodes = get_bus_nodes(board)

        for node in nodes:
            arcs = node.get_closing_arcs(tracks)
            import pprint
            pprint.pprint(arcs)
            add_arcs(pcbnew.wxPoint(*node.pos), arcs, board, self.force)
            
class ForceArcs(CompleteArcs):
    def defaults(self):
        self.name = "Force Arcs"
        self.category = "Routing"
        self.description = "As Complete Arcs, but will always route even if there is already copper present."
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'force_arcs.png')
        self.force = True


class RoutePointTangents(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Route Point Tangents"
        self.category = "Routing"
        self.description = "Route the two tangent lines between the grid origin and the selected circle"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'point_tangents.png')

    def Run(self):
        board = pcbnew.GetBoard()
        circles, drw = get_circles(board)
        if len(circles) != 1:
            print('Need exactly one circle')
            return
        circle = circles[0]

        side = get_drawing_side(drw[0])

        xp, yp = board.GetGridOrigin()

        lines = []
        angles = []
        tlines, tangles = get_point_tangents(*circle, xp, yp)
        lines.extend(tlines)
        angles.extend(tangles)

        add_traces(lines, BusNode.side_map[side], board)

class RouteInnerTangents(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Route Inner Tangents"
        self.category = "Routing"
        self.description = "Route the 2 inner tangents between the two selected bus nodes"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'inner_tangents.png')

    def Run(self):
        board = pcbnew.GetBoard()
        nodes = get_bus_nodes(board)
        if len(nodes) != 2:
            print('Need exactly two nodes')
            return
        xp, yp = board.GetGridOrigin()

        #start with a list of lines results, then find the index that gives the 
        #best distance on one, in order to select that one from each set.
        for side in ['TOP', 'BOT']:
            circle_pairs = nodes[0].get_inner_tangents(nodes[1], side)

            lines = []
            angles = []
            for left, right in circle_pairs:
                tlines, tangles = get_inner_tangents(*left, *right)
                lines.append(tlines)
                angles.append(tangles)

            if len(lines) == 0: continue

            line_idx = get_nearest_tangent(lines[0], xp, yp)
            flat_lines = []
            for tlines in lines:
                flat_lines.append(tlines[line_idx])

            print(flat_lines)

            add_traces(flat_lines, nodes[0].side_map[side], board)

class RouteOuterTangents(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Route Outer Tangents"
        self.category = "Routing"
        self.description = "Route the 2 outer tangents between the two selected bus nodes"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'outer_tangents.png')

    def Run(self):
        board = pcbnew.GetBoard()
        nodes = get_bus_nodes(board)
        if len(nodes) != 2:
            print('Need exactly two nodes')
            return

        xp, yp = board.GetGridOrigin()
        for side in ['TOP', 'BOT']:
            circle_pairs = nodes[0].get_outer_tangents(nodes[1], side)

            lines = []
            angles = []
            for left, right in circle_pairs:
                tlines, tangles = get_outer_tangents(*left, *right)
                lines.append(tlines)
                angles.append(tangles)

            if len(lines) == 0: continue

            line_idx = get_nearest_tangent(lines[0], xp, yp)
            flat_lines = []
            for tlines in lines:
                flat_lines.append(tlines[line_idx])

            add_traces(flat_lines, nodes[0].side_map[side], board)


SpreadNets().register()
FlipECOMarkers().register()
busnodeplugin.register()        
CompleteArcs().register()
ForceArcs().register()
RoutePointTangents().register()
RouteInnerTangents().register()
RouteOuterTangents().register()