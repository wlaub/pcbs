import math

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

    return res, a


def get_outer_tangents(r1, x1, y1, r2, x2, y2):
    """
    Return two pairs of points representing the two outer tangents between
    the two given circles. Return also the corresponding angles on each circle.
    Ref http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    [[[x, y], [x,y]] , [[x,y], [x,y]]], [[a1, a1], [a2,a2]]
    """

    xp = (x2*r1-x1*r2)/(r1-r2)
    yp = (y2*r1-y1*r2)/(r1-r2)

    return get_tangents(xp, yp, r1, x1, y1, r2, x2, y2)

def get_inner_tangents(r1, x1, y1, r2, x2, y2):
    """
    Return two pairs of points representing the two outer tangents between
    the two given circles. Return also the corresponding angles on each circle.
    Ref http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    [[[x, y], [x,y]] , [[x,y], [x,y]]], [[a1, a1], [a2,a2]]
    """

    xp = (x2*r1-x1*r2)/(r1+r2)
    yp = (y2*r1-y1*r2)/(r1+r2)

    return get_tangents(xp, yp, r1, x1, y1, r2, x2, y2)



test = [1,0,0,2,3,0]
print(test)
print(get_outer_tangents(*test))
print(get_inner_tangents(*test))

