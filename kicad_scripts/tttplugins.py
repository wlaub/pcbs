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



class Teardrop(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Add Teardrops"
        self.category = "Routing"
        self.description = "Add teardrops to the via"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'teardrop.png')

    def Run(self):
        board = pcbnew.GetBoard()

        tracks = list(filter(lambda x: x.GetClass() == 'TRACK' and x.IsSelected(), board.GetTracks()))
        print(f'Selected Tracks: {tracks}')
        layers = list(set(map(lambda x: x.GetLayer(), tracks)))
        track_map = {k: list(filter(lambda x: x.GetLayer() == k, tracks)) for k in layers}

        vias = list(filter(lambda x: x.GetClass() == 'VIA' and x.IsSelected(), board.GetTracks()))
        print(f'Selected vias {vias}')
        via = vias[0]
        base_r = via.GetWidth()/2
        c = via.GetCenter()

        for track in tracks:
            r = base_r - track.GetWidth()/2

            s1 = track.GetStart()
            s2 = track.GetEnd()
            d1 = math.sqrt( (s1[0]-c[0])**2 + (s1[1]-c[1])**2 )
            d2 = math.sqrt( (s2[0]-c[0])**2 + (s2[1]-c[1])**2 )
            if d1 < r and d2 < r:
                print(f'Skipping - no external points')
                continue

            if d2 < d1:
                s = s2
                sx = s1
                D = d2
                end = 'end'
            else:
                s = s1
                sx = s2
                D = d1
                end = 'start'



            p = math.atan2(s[1]-sx[1], s[0]-sx[0])
            a = math.atan2(c[1]-s[1], c[0]-s[0])
            dpa = abs( math.pi - abs(abs(a-p) - math.pi) ) 
            print(f'Angles {p} - {a} = {dpa}')
            theta = math.pi/8

            lines = []

            angle1 = -(-a+dpa+math.pi/2)
            endpoint1 = shift(c, r, angle1)
            print(f'{angle1*180/math.pi}')

            L = r/math.tan(theta)
            print(L)


            #angle2 = -(math.pi-(-a+dpa+math.pi-theta))
            angle2 = angle1-math.pi+2*theta
            endpoint2 = shift(c, r, angle2)
            print(f'{angle2*180/math.pi}')


            anglex = angle1-math.pi/2
            lines.append([shift(endpoint1, L, anglex), endpoint2])


            angle2 = angle1+math.pi-2*theta
            endpoint2 = shift(c, r, angle2)
            anglex = angle1+math.pi/2
            lines.append([shift(endpoint1, L, anglex), endpoint2])

            add_traces(lines, track.GetLayer(), board)


        pcbnew.Refresh()



class ExtendToCircle(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Extend To Circle"
        self.category = "Routing"
        self.description = "Route lines to circles"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'extend_to_circle.png')

    def Run(self):
        board = pcbnew.GetBoard()

        circles, drws = get_circles(board)
        c = [circles[0][1], circles[0][2]]
        r = circles[0][0]

        if len(circles) != 1:
            print('Need exactly one circle')
            return

        tracks = list(filter(lambda x: x.GetClass() == 'TRACK' and x.IsSelected(), board.GetTracks()))
        print(f'Selected Tracks: {tracks}')
        layers = list(set(map(lambda x: x.GetLayer(), tracks)))
        track_map = {k: list(filter(lambda x: x.GetLayer() == k, tracks)) for k in layers}

        for track in tracks:
            s1 = track.GetStart()
            s2 = track.GetEnd()
            d1 = math.sqrt( (s1[0]-c[0])**2 + (s1[1]-c[1])**2 )
            d2 = math.sqrt( (s2[0]-c[0])**2 + (s2[1]-c[1])**2 )
            if d1 < r and d2 < r:
                print(f'Skipping - no external points')
                continue

            if d2 < d1:
                s = s2
                sx = s1
                D = d2
                end = 'end'
            else:
                s = s1
                sx = s2
                D = d1
                end = 'start'

            p = math.atan2(s[1]-sx[1], s[0]-sx[0])
            a = math.atan2(c[1]-s[1], c[0]-s[0])
            dpa = abs( math.pi - abs(abs(a-p) - math.pi) ) 
            print(f'Angles {p} - {a} = {dpa}')

            L = D*math.sin(dpa)
            print(f'Line radius = {pcbnew.ToMM(L)} mm')
            if r < L: 
                print(f'Skipping - no intersection')
                continue

            x = D*math.cos(dpa) - math.sqrt(r**2-L**2)
            dx = x*math.cos(p)
            dy = x*math.sin(p)
            ns = pcbnew.wxPoint(s[0]+dx, s[1]+dy)
            if end == 'end': track.SetEnd(ns)
            else: track.SetStart(ns)

        pcbnew.Refresh()

#################
#################
#################

class ShiftClone(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Shift clone"
        self.category = "Routing"
        self.description = "Duplicate the select track and shift it orthogonally by a specified displacement and direction"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'shift_clone.png')
        self.default_direction = 0
        config = pcbnew.GetBoard().GetDesignSettings()
        self.default_distance = config.GetSmallestClearanceValue()+config.GetCurrentTrackWidth()

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()

        tracks = list(filter(lambda x: x.GetClass() == 'TRACK' and x.IsSelected(), board.GetTracks()))
        print(f'Selected Tracks: {tracks}')
        layers = list(set(map(lambda x: x.GetLayer(), tracks)))
        track_map = {k: list(filter(lambda x: x.GetLayer() == k, tracks)) for k in layers}


        dialog = ShiftCloneDialog(None, board, self, track_map)
        dialog.Show(True)


SpreadNets().register()
FlipECOMarkers().register()
busnodeplugin.register()        
CompleteArcs().register()
ForceArcs().register()
RoutePointTangents().register()
RouteInnerTangents().register()
RouteOuterTangents().register()
shiftcloneplugin = ShiftClone()
shiftcloneplugin.register()
ExtendToCircle().register()
Teardrop().register()

class ShiftCloneDialog(wx.Dialog):
    
    def __init__(self, parent, board, plugin, track_map):
        wx.Dialog.__init__(self, parent, title= "Shift Clone Configuration")
        self.board = board
        config = board.GetDesignSettings()
        self.plugin = plugin
        self.track_map = track_map

        unit_name, ToUnit, self.FromUnit = get_units()

        box = wx.BoxSizer(wx.VERTICAL)

        self.panel = wx.Panel(self)

        self.text_boxes = {}

        subbox = wx.BoxSizer(wx.HORIZONTAL)


        #left column
        ssbox = wx.BoxSizer(wx.VERTICAL)
        #displacement
        label = wx.StaticText(self.panel, label = f"Displacement ({unit_name})")
        ssbox.Add(label,   proportion=0)
        _,_,w,h = label.GetRect()

        self.distance = wx.TextCtrl(self.panel, value = str(ToUnit(plugin.default_distance)), size=(100, h*1.5))
        ssbox.Add(self.distance,   proportion=0)

        subbox.Add(ssbox, 0, wx.RIGHT|wx.LEFT, 10)
        
        #right column
        
        ssbox = wx.BoxSizer(wx.VERTICAL)
        #direction
        
        self.radio_buttons = []

        xpos = 250
        ypos = 50
        rad = 40
        size = (20,20)
        self.radio_buttons.append(wx.RadioButton(self.panel,11, pos = (xpos+rad,ypos), size=size, style = wx.RB_GROUP))
        self.radio_buttons.append(wx.RadioButton(self.panel,22, pos = (xpos,ypos+rad), size=size))

        self.radio_buttons.append(wx.RadioButton(self.panel,33, pos = (xpos-rad,ypos), size=size))
        self.radio_buttons.append(wx.RadioButton(self.panel,44, pos = (xpos,ypos-rad), size=size))
       
        self.radio_buttons[self.plugin.default_direction].SetValue(True)

        angles = []
        for layer in self.track_map.keys():
            for track in self.track_map[layer]:
                a = track.GetStart()
                b = track.GetEnd()
                dx = a[0] - b[0]
                dy = a[1] - b[1]
                angle = math.atan2(dy, dx)
                angles.append(angle)

        #[ssbox.Add(x) for x in self.radio_buttons[2:]]
        xpos += 12
        ypos += 10
        rad-=10
        def on_paint(event):
            dc = wx.PaintDC(event.GetEventObject())
            dc.Clear()
            dc.SetPen(wx.Pen("BLACK", 1))
            for a in angles:
                dc.DrawLine(xpos+rad*math.cos(a), ypos+rad*math.sin(a), xpos-rad*math.cos(a), ypos-rad*math.sin(a),)

        self.panel.Bind(wx.EVT_PAINT, on_paint)



        subbox.Add(ssbox, 0)
        box.Add(subbox)
        subbox = wx.BoxSizer(wx.HORIZONTAL)

        #left column
        ssbox = wx.BoxSizer(wx.VERTICAL)
        #go button

        go_button = wx.Button(self.panel, label="Dew it", id=1)
        ssbox.Add(go_button,  proportion=0)

        subbox.Add(ssbox, 0, wx.RIGHT|wx.LEFT, 10)

        #right column

        ssbox = wx.BoxSizer(wx.VERTICAL)

        #Cancel button

        cancel_button = wx.Button(self.panel, label="Do Not.", id=2)
        ssbox.Add(cancel_button,  proportion=0)

        subbox.Add(ssbox)
        box.Add(subbox)

        self.panel.SetSizer(box)
        self.Bind(wx.EVT_BUTTON, self.OnPress, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=2)

    def OnPress(self, event):
        board = self.board
        print('**Shift+Clone**')

        displacement = self.FromUnit(float(self.distance.GetValue()))
        self.plugin.default_displacement = displacement

        direction = [x.GetValue() for x in self.radio_buttons].index(True)
        self.plugin.default_direction = direction
        direction = math.pi*direction/2

        print(f'Shifting by distance of {displacement} in direction {direction}')


        lines = []
        layers = []
        for layer in self.track_map.keys():
            for track in self.track_map[layer]:
                a = track.GetStart()
                b = track.GetEnd()
                dx = a[0] - b[0]
                dy = a[1] - b[1]
                angle1 = math.atan2(dy, dx) + math.pi/2
                angle2 = math.atan2(dy, dx) - math.pi/2
                print(f'angles = {angle1}, {angle2} | direction = {direction}')
                da1 = math.pi - abs(abs(angle1 - direction) - math.pi); 
                da2 = math.pi - abs(abs(angle2 - direction) - math.pi); 
                
                if abs(da1-math.pi/2) < .01: continue

                if abs(da1) < abs(da2):
                    angle = angle1
                else:
                    angle = angle2

                dxx = displacement*math.cos(angle)
                dyy = displacement*math.sin(angle)

                nl = [(a[0]+dxx,a[1]+dyy),(b[0]+dxx,b[1]+dyy)]

                print(f'Shift line from {a} to {b}')
                print(f'Shift by {dxx}, {dyy}, angle = {angle}')
                print(f'Shift to {nl[0]} {nl[0]}')

                lines.append(nl)
                #layers.append(board.GetLayerID(layer))
                layers.append(layer)

        add_traces(lines, layers, board)

        #Get selected traces
            #Compute angle of trace
            #compute offset of trace
            #Compute new location of trace
            #create trace
            #drc?

        self.Close()

    def OnCancel(self, event):
        selections = [x.GetValue() for x in self.radio_buttons]
        print(selections)

        self.Close()
