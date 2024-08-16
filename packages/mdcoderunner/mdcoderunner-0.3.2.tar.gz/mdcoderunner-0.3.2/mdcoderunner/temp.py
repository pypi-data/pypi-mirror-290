import math

def calculate_circle_area(radius):
    return math.pi * radius * radius

radius = 5
area = calculate_circle_area(radius)
print(f"Area of circle with radius {radius} is {area}")