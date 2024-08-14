import math

# Function to calculate angle in degrees from reference_coord to mouse position
def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    radians = math.atan2(dy, dx)
    degrees = math.degrees(radians)
    return degrees

def get_direction(angle):
    if angle == 0:
        return []

    if -135 <= angle < -45:
        return [ 'top' ]

    if  angle >= 135 or angle < -135:
        return [ "left" ]

    if -45 <= angle < 45:
        return [ "right" ]

    if  45 <= angle < 135:
        return [ "bottom" ]
    
    return []

def get_direction_expanded(angle):
    if angle == 0:
        return []

    if -112.5 <= angle < -67.5:
        return [ 'top' ]

    if -157.5 <= angle < -112.5:
        return [ 'top', 'left', 'top-left' ]

    if -67.5 <= angle < -22.5:
        return [ 'top', 'right', 'top-right' ]

    if 67.5 <= angle < 112.5:
        return [ 'bottom' ]

    if 112.5 <= angle < 157.5:
        return [ 'bottom', 'left', 'bottom-left' ]

    if 22.5 <= angle < 67.5:
        return [ 'bottom', 'right', 'bottom-right' ]

    if angle >= 157.5 or  angle < -157.5:
        return [ 'left']
        
    if -22.5 <= angle < 22.5:
        return [ 'right']
    
    return []
