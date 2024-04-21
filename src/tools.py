import math

def limitVector(vector, value):
    squared_mag = vector.magnitude() * vector.magnitude()
    if squared_mag > (value * value):
        vector.x = vector.x/math.sqrt(squared_mag)
        vector.y = vector.y/math.sqrt(squared_mag)
        vector.x = vector.x * value
        vector.y = vector.y * value