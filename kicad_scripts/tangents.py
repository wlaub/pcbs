import math
import os

import wx
import pcbnew


def get_tangents(xp, yp, r1, x1, y1, r2, x2, y2):
    """
    For a given intersection point:
    Return two pairs of points representing the two tangents between the two 
    given circles. Return also the corresponding angles on each circle.
    Ref http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    [[[x, y], [x,y]] , [[x,y], [x,y]]], [[a1, a1], [a2,a2]]
    a  b  c  d
    x1 y1 x2 y2
    r0 -> r1 
    r1 -> r2
    Unfolded for easier implementation. Only god can judge.
    """ 

    #line, end, axis
    res = [[[0,0],[0,0]], [[0,0],[0,0]]]

    a = r1*r1*(xp-x1)
    b = r1*(yp-y1)*math.sqrt( (xp-x1)**2 + (yp-y1)**2 - r1**2 )
    c = (xp-x1)**2 + (yp-y1)**2

    #line, end, axis
    res[0][0][0] = x1+(a+b)/c
    res[1][0][0] = x1+(a-b)/c

    a = r1*r1*(yp-y1)
    b = -r1*(xp-x1)*math.sqrt( (xp-x1)**2 + (yp-y1)**2 - r1**2 )
    c = (xp-x1)**2 + (yp-y1)**2

    #line, end, axis
    res[0][0][1] = y1+(a+b)/c
    res[1][0][1] = y1+(a-b)/c

    a = r2*r2*(xp-x2)
    b = r2*(yp-y2)*math.sqrt( (xp-x2)**2 + (yp-y2)**2 - r2**2 )
    c = (xp-x2)**2 + (yp-y2)**2

    #line, end, axis
    res[0][1][0] = x2+(a+b)/c
    res[1][1][0] = x2+(a-b)/c

    a = r2*r2*(yp-y2)
    b = -r2*(xp-x2)*math.sqrt( (xp-x2)**2 + (yp-y2)**2 - r2**2 )
    c = (xp-x2)**2 + (yp-y2)**2

    #line, end, axis
    res[0][1][1] = y2+(a+b)/c
    res[1][1][1] = y2+(a-b)/c

    a = get_angles(res, x1, y1, x2, y2)

    return res, a

def get_point_tangents(r1, x1, y1, xp, yp):
    """
    Find the lines from xp, yp that are tangent to the circle of radius r1 at
    x1, y1
    Return same format as get_tangents
    """
    #line, end, axis
    res = [[[0,0],[0,0]], [[0,0],[0,0]]]

    a = r1*r1*(xp-x1)
    b = r1*(yp-y1)*math.sqrt( (xp-x1)**2 + (yp-y1)**2 - r1**2 )
    c = (xp-x1)**2 + (yp-y1)**2

    #line, end, axis
    res[0][0][0] = x1+(a+b)/c
    res[1][0][0] = x1+(a-b)/c

    a = r1*r1*(yp-y1)
    b = -r1*(xp-x1)*math.sqrt( (xp-x1)**2 + (yp-y1)**2 - r1**2 )
    c = (xp-x1)**2 + (yp-y1)**2

    #line, end, axis
    res[0][0][1] = y1+(a+b)/c
    res[1][0][1] = y1+(a-b)/c

    res[0][1][0] = xp
    res[1][1][0] = xp

    #line, end, axis
    res[0][1][1] = yp
    res[1][1][1] = yp

    a = get_angles(res, x1, y1, x1, y1)

    return res, a


def get_angles(res, x1, y1, x2, y2):
    """
    Return angles for the given lines
    """
    #circle, line
    a = [[0,0,],[0,0]]

    dx = res[0][0][0] - x1
    dy = res[0][0][1] - y1

    #circle, line
    a[0][0] = math.atan2(dy, dx)

    dx = res[0][1][0] - x1
    dy = res[0][1][1] - y1

    #circle, line
    a[0][1] = math.atan2(dy, dx)

    dx = res[1][0][0] - x2
    dy = res[1][0][1] - y2

    #circle, line
    a[1][0] = math.atan2(dy, dx)

    dx = res[1][1][0] - x2
    dy = res[1][1][1] - y2

    #circle, line
    a[1][1] = math.atan2(dy, dx)

    return a


def get_outer_tangents(r1, x1, y1, r2, x2, y2):
    """
    Return two pairs of points representing the two outer tangents between
    the two given circles. Return also the corresponding angles on each circle.
    Ref http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    [[[x, y], [x,y]] , [[x,y], [x,y]]], [[a1, a1], [a2,a2]]
    """
    
    #todo: case when radii equal.
    if r1 == r2:
        a = math.atan2(y2-y1,x2-x1)
        rs = r1*math.sin(a)
        rc = r1*math.cos(a)
        res = [
            [[x1+rs, y1-rc], [x2+rs, y2-rc]],
            [[x1-rs, y1+rc], [x2-rs, y2+rc]],
        ]
        return res, get_angles(res, x1, y1, x2, y2)

    if r2 > r1:
        r1, r2 = r2, r1
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    xp = (x2*r1-x1*r2)/(r1-r2)
    yp = (y2*r1-y1*r2)/(r1-r2)  

    return get_tangents(xp, yp, r1, x1, y1, r2, x2, y2)

def get_inner_tangents(r1, x1, y1, r2, x2, y2):
    """
    Return two pairs of points representing the two outer tangents between
    the two given circles. Return also the corresponding angles on each circle.
    Ref http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    [[[x, y], [x,y]] , [[x,y], [x,y]]], [[a1, a1], [a2,a2]]
    First line is under first circle, second is over?
    """

    if r2 > r1:
        r1, r2 = r2, r1
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    xp = (x2*r1+x1*r2)/(r1+r2)
    yp = (y2*r1+y1*r2)/(r1+r2)

    return get_tangents(xp, yp, r1, x1, y1, r2, x2, y2)

def get_nearest_tangent(lines, xp, yp):
    """
    Return the index of the line having an endpoint nearest the given point
    xp, yp
    """
    best = -1
    best_dist = -1
    for idx, points in enumerate(lines):
        for x, y in points:
            dist = (x-xp)**2 + (y-yp)**2
            if best_dist == -1 or dist < best_dist:
                best = idx
                best_dist = dist
    return best

def get_trace(r1, x1, y1, r2, x2, y2, over1, over2):
    """
    Given a circle of radius r1 at 0,0
    A circle of radius r2 at dx, dy
    over1 = 0 if the tangent is under r1
    over1 = 1 if the tangent is over r1
    over2 = 0 if the tangent is under r2
    over2 = 1 if the tangent is over r2
    """
    if over1 != over2:
        lines, angles = get_inner_tangents(r1, x1, y1, r2, x1, y1)
    else:
        lines, angles = get_outer_tangents(r1, x1, y1, r2, x1, y1)
    
    #index of the highest endpoint
    idx = 0
    if lines[0][1] < lines[1][1]:
        idx = 1
    if over1 == 0: idx = 1-idx
    return lines[idx], [angles[0][idx], angles[1][idx]]

def get_pads(board):
    sel = []
    for drw in board.GetPads():
        if drw.IsSelected():
            sel.append(drw)
    return sel

def get_all_circles(board):
    result = []
    for drw in board.GetDrawings():
        if drw.Type() == 5 and drw.GetShapeStr() == 'Circle':
            result.append(drw)

    return result

def extract_selection(stuff):
    return list(filter(lambda x: x.IsSelected(), stuff))

def get_circles(board):

    sel = extract_selection(get_all_circles(board))

    result = []
    for circle in sel:
        result.append([circle.GetRadius(), *circle.GetCenter()])

    return result, sel

def add_trace_tangents(board):
    circles, _ = get_circles(board)
    if len(circles) != 2:
        print('Need circles')
        return

    lines, angles = get_inner_tangents(*circles[0], *circles[1])
    lines2, angles2 = get_outer_tangents(*circles[0], *circles[1])
    lines.extend(lines2)
    add_traces(lines, board)

def add_traces(lines, layer, board):

    for line in lines:
        track = pcbnew.TRACK(board)
        config = board.GetDesignSettings()

        track.SetStart(pcbnew.wxPoint(*line[0]))
        track.SetEnd(pcbnew.wxPoint(*line[1]))
        track.SetWidth(config.GetCurrentTrackWidth())
        track.SetLayer(layer) #TODO: FIX

        board.Add(track) 
    pcbnew.Refresh()

def add_circles(circles, width, layer, board):
    """
    Circles of the form r, x, y
    """
    config = board.GetDesignSettings()
    drws = get_all_circles(board)

    for r,x,y in circles:
        exists = False
        for drw in drws:
            if drw.GetLayer() == layer and drw.HitTest(pcbnew.wxPoint(x+r, y)):
                exists = True

        if exists: continue

        circle = pcbnew.DRAWSEGMENT(board)


        circle.SetShape(3)
        circle.SetCenter(pcbnew.wxPoint(x,y))
        circle.SetEnd(pcbnew.wxPoint(x+r,y))

        circle.SetWidth(int(width))
        circle.SetLayer(layer) #TODO: FIZ

        board.Add(circle)
    pcbnew.Refresh()

def add_arcs(center, arcs, board):
    """
    arcs of the form: radius, start_point, angle, layer, width
    """
    lines = []
    for radius, start_point, angle, layer, width in arcs:

        start_angle = math.atan2(*[start_point[i]-center[i] for i in [1,0]])
        mid_angle = start_angle + angle/2
        mid_point = [center[0]+radius*math.cos(mid_angle), center[1]+radius*math.sin(mid_angle)]

        hit = False
        for track in board.GetTracks():
            if track.GetLayer() == layer and track.HitTest(pcbnew.wxPoint(*mid_point)):
                hit = True
                break

        if hit: continue

        #max deviation of line from center in nm
        max_dev = .005*1e6
        max_angle = 2*math.acos((radius-max_dev)/radius)
        N = math.ceil(abs(angle)/max_angle)
        print(f'{N} segments needed for radius {radius} and max_dev {max_dev} with max angle {max_angle} and angle {angle} = {angle/max_angle}')
        for i in range(N):
            sa = start_angle + i*angle/N
            start_point = [center[0]+radius*math.cos(sa), center[1]+radius*math.sin(sa)]
            ea = start_angle + (i+1)*angle/N
            end_point = [center[0]+radius*math.cos(ea), center[1]+radius*math.sin(ea)]

            track = pcbnew.TRACK(board)

            track.SetStart(pcbnew.wxPoint(*start_point))
            track.SetEnd(pcbnew.wxPoint(*end_point))
            track.SetWidth(width)
            track.SetLayer(layer)
            board.Add(track)
            
        """
        arc = pcbnew.DRAWSEGMENT(board)

        arc.SetShape(2)
        arc.SetCenter(center)
        arc.SetArcStart(start_point)
        arc.SetAngle(angle)
        
        arc.SetWidth(width)
        arc.SetLayer(layer)


        board.Add(arc)
        """

    pcbnew.Refresh()
    

def get_drawing_side(drw):
    if drw.GetLayer() in pcbnew.LSET_BackMask().Seq():
        return 'BOT'
    else:
        return 'TOP'

class BusNode():
    """
    Class for handling bus nodes comprising multiple concentric circles
    """
    side_map = {'TOP': 0, 'BOT': 31}

    def __init__(self):
        self.rads = []
        self.pos = []
        self.sides = []
        self.drws = []
        
    def add_rad(self, rad, drw):
        self.rads.append(rad)
        self.drws.append(drw)
        self.sides.append(get_drawing_side(drw))

    def sort(self):
        self.rads, self.sides, self.drws = zip(*sorted(zip(self.rads, self.sides, self.drws)))

    def get_side(self, sel_side):
        result = BusNode()
        for rad, side, drw in zip(self.rads, self.sides, self.drws):
            if side == sel_side:
                result.rads.append(rad)
                result.sides.append(side)
                result.drws.append(drw)
            result.pos = list(self.pos)
        return result

    def get_tangents(self, other, inner, side='BOTH'):
        """
        Return a list of pairs of circles that should be routed together for
        inner or outer tangents of the two bus nodes.
        """
        self.sort()
        other.sort()

        original = self
        if side != 'BOTH':
            other = other.get_side(side)
            original = self.get_side(side)

        print(side)
        other.print()
        original.print()

        if len(original.rads) <= len(other.rads):
            long_bus = other
            short_bus = original

        else:
            long_bus = original
            short_bus = other

        result = []
        for idx in range(len(short_bus.rads)):
            other_idx = idx
            if inner: other_idx = len(short_bus.rads)-1-idx
            result.append([
            [short_bus.rads[idx], *short_bus.pos],
            [long_bus.rads[other_idx],  *long_bus.pos],
            ])

        return result

    def get_inner_tangents(self, other, side='BOTH'):
        return self.get_tangents(other, inner=True, side=side)

    def get_outer_tangents(self, other, side='BOTH'):
        return self.get_tangents(other, inner=False, side=side)

    def get_angle(self, point):
        return math.atan2(point[1] - self.pos[1], point[0] - self.pos[0])

    def get_closing_arcs(self, tracks):
        """
        Given a list of tracks, generate closing arcs for all the pairs of
        tracks on this node. Format: [[r, start_point, angle, layer, width], ...]
        """
        result = []
        #0, 31 for copper
        side_map = self.side_map
        for rad, side, drw in zip(self.rads, self.sides, self.drws):
            hits = []
            print(rad, side, drw)

            #Find matching end points
            for track in tracks:
                if side_map.get(side, None) != track.GetLayer(): continue
                start_point = track.GetStart()
                end_point = track.GetEnd()
                start_hit = drw.HitTest(start_point)
                end_hit = drw.HitTest(end_point)
                if start_hit and not end_hit:
                    hits.append([start_point, end_point, track])
                elif end_hit and not start_hit:
                    hits.append([end_point, start_point, track])

            if len(hits) != 2: continue
            
            tresult = [rad, side_map[side]]

            start_point = hits[0][0]

            start_angle = self.get_angle(start_point)            
            stop_angle = self.get_angle(hits[1][0])

            bad_angle = self.get_angle(hits[0][1])
            if stop_angle < start_angle: stop_angle += math.pi*2

            angle = stop_angle-start_angle

            if bad_angle > start_angle and bad_angle < stop_angle:
                angle -= 2*math.pi

            result.append([rad, start_point, angle, side_map[side], drw.GetWidth()])
            #result.append([rad, start_point, 1800*angle/math.pi, 37, drw.GetWidth()])
        return result


    def print(self):
        print(f"node at {self.pos} with radii {self.rads}" )

def get_bus_nodes(board):
    """
    Find all the bus nodes in the selection
    """
    circles, drws = get_circles(board)
    centers = set(list(map(lambda x: (x[1], x[2]), circles)))
    result = []
    for center in centers:
        node = BusNode()
        result.append(node)
        node.pos = center
        for circle, drw in zip(circles, drws):
            if (circle[1], circle[2]) == center:
                node.add_rad(circle[0], drw)
        node.print()

    return result

def get_units():
    if pcbnew.GetUserUnits() == 0:
        to_func = pcbnew.ToMils
        from_func = pcbnew.FromMils
        name = pcbnew.uMils
    elif pcbnew.GetUserUnits() == 1:
        to_func = pcbnew.ToMM
        from_func = pcbnew.FromMM
        name = pcbnew.uMM

    return name, to_func, from_func

def dir_func(object):
    d = dir(object)
    d = list(filter(lambda x: callable(object.__dict__[x]), d))
    print(d)

def spread_nets(tracks):
    """
    Given a selection of tracks or objects having a net, if only one net is
    assigned, spread it to unassigned nets
    """
    nets = list(set(x.GetNetCode() for x in tracks))
    if not 0 in nets:
        print('No unfilled nets found')
        return

    if len(nets) > 2:
        print('Too many nets - net assignment ambiguous')
        return

    fill_net = max(nets) #Get the one that isn't 0
    
    for track in tracks:
        if track.GetNetCode() == 0:
            track.SetNetCode(fill_net)

    pcbnew.Refresh()

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


SpreadNets().register()

class PlaceBusNode(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Place Bus Node"
        self.category = "Routing"
        self.description = "Place silkscreen markings for a bus node at the grid origin"
        self.show_toolbar_button = True# Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'bus_node.png')
        self.pattern = "1"
        self.default_side = 'Top'

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()

        dialog = BusNodeDialog(None, board, self)
        dialog.Show(True)


busnodeplugin = PlaceBusNode()
busnodeplugin.register()        

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

        self.trace_width = wx.TextCtrl(self.panel, value = str(ToUnit(config.GetSmallestClearanceValue())), size=(120, h*1.5))
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

        self.clearance_width = wx.TextCtrl(self.panel, value = str(ToUnit(config.GetCurrentTrackWidth())), size=(120, h*1.5))
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

        if self.layer_box.GetValue() == 'Top':
            layer = board.GetLayerID('F.SilkS')
        else:
            layer = board.GetLayerID('B.SilkS')
        self.plugin.layer = self.layer_box.GetValue()

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

    def Run(self):
        board = pcbnew.GetBoard()
        config = board.GetDesignSettings()

        tracks = list(filter(lambda x: x.GetClass() == 'TRACK' and x.IsSelected, board.GetTracks()))
        layers = list(set(map(lambda x: x.GetLayer(), tracks)))
        track_map = {k: list(filter(lambda x: x.GetLayer() == k, tracks)) for k in layers}

        nodes = get_bus_nodes(board)

        for node in nodes:
            arcs = node.get_closing_arcs(tracks)
            import pprint
            pprint.pprint(arcs)
            add_arcs(pcbnew.wxPoint(*node.pos), arcs, board)
            


CompleteArcs().register()

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

RoutePointTangents().register()
RouteInnerTangents().register()
RouteOuterTangents().register()