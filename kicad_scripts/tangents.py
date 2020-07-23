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

    try:
        a = layer[0]
        layers = layer
    except:
        layers = [layer]*len(lines)

    print(f'Add traces on layers {layers}')

    for line, layer in zip(lines, layer):
        track = pcbnew.TRACK(board)
        config = board.GetDesignSettings()

        track.SetStart(pcbnew.wxPoint(*line[0]))
        track.SetEnd(pcbnew.wxPoint(*line[1]))
        track.SetWidth(config.GetCurrentTrackWidth()) #TODO: FIX
        track.SetLayer(layer) 

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

        if exists: 
            print(f'Skipping existing circle {r} at {x},{y}...')
            continue

        circle = pcbnew.DRAWSEGMENT(board)


        circle.SetShape(3)
        circle.SetCenter(pcbnew.wxPoint(x,y))
        circle.SetEnd(pcbnew.wxPoint(x+r,y))

        circle.SetWidth(int(width))
        circle.SetLayer(layer) #TODO: FIZ

        board.Add(circle)
    pcbnew.Refresh()

def add_arcs(center, arcs, board, force = False):
    """
    arcs of the form: radius, start_point, angle, layer, width, netcode
    """
    lines = []
    for radius, start_point, angle, layer, width, netcode in arcs:

        start_angle = math.atan2(*[start_point[i]-center[i] for i in [1,0]])
        mid_angle = start_angle + angle/2
        mid_point = [center[0]+radius*math.cos(mid_angle), center[1]+radius*math.sin(mid_angle)]

        hit = False
        print(f'Check hits at point {mid_point} of circle at {start_point} with radius {radius}')
        for track in board.GetTracks():
            if track.GetLayer() == layer and track.HitTest(pcbnew.wxPoint(*mid_point)):
                print(f'Got hit at track with net {track.GetNetname()}')
                hit = True
                break

        if hit and not force: continue

        #max deviation of line from center in nm
        max_dev = .001*1e6
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
            track.SetNetCode(netcode)
            
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
    if drw.GetLayer() in pcbnew.LSET_BackMask().Seq() or drw.GetLayerName()=='Eco2.User':
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
        tracks on this node. Format: [[r, start_point, angle, layer, width, net], ...]
        """
        result = []
        #0, 31 for copper
        side_map = self.side_map
        for rad, side, drw in zip(self.rads, self.sides, self.drws):
            hits = []
            #print(rad, side, drw)

            #Find matching end points
            for track in tracks:
                if side_map.get(side, None) != track.GetLayer(): continue
                start_point = track.GetStart()
                end_point = track.GetEnd()
                #print(f'Checking hit at {start_point} and {end_point}')
                start_hit = drw.HitTest(start_point)
                end_hit = drw.HitTest(end_point)
                if start_hit and not end_hit:
                    hits.append([start_point, end_point, track])
                elif end_hit and not start_hit:
                    hits.append([end_point, start_point, track])

            print(f'Hits: {hits}')

            if len(hits) != 2: continue

            #At this point, hits[track] contains a list of 
            #the point on the circle, 
            #the point off the circle,
            #the track object

            tresult = [rad, side_map[side]]

            #we arbitrarily choose index 0 as the start point of the curve
            start_point = hits[0][0]

            #we extract the starting angle and the stopping angle
            start_angle = self.get_angle(start_point)            
            stop_angle = self.get_angle(hits[1][0])

            #we unwrap the stop angle so it's larger than the start angle
            if stop_angle <= start_angle: stop_angle += math.pi*2

            #we compute the angle of this side of the arc
            angle = stop_angle-start_angle

            #we get the angle of the end point of the line and unwrap it as well
            bad_angle = self.get_angle(hits[0][1])
            if bad_angle <= start_angle: bad_angle += math.pi*2

            #if the lines are tangent, then the points off the circle should
            #have angles that don't lie on the arc.
            if bad_angle > start_angle and bad_angle < stop_angle:
                angle -= 2*math.pi

            nets = [x[2].GetNetCode() for x in hits]
            #print(nets)
            nets = list(set(filter(lambda x: x!= 0, nets)))
            netcode= 0
            if len(nets) == 1: netcode = nets[0]

            result.append([rad, start_point, angle, side_map[side], drw.GetWidth(), netcode])
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

