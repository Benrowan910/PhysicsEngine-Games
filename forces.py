import pygame
from pygame.math import Vector2
import itertools
import math

from physics_objects import Wall

class SingleForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        for obj in self.objects_list:
            force = self.force(obj)  # force function implemented in every subclass
            obj.add_force(force)


class PairForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        # Loop over all pairs of objects and apply the calculated force
        # to each object, respecting Newton's 3rd Law.  
        # Use either two nested for loops (taking care to do each pair once)
        # or use the itertools library (specifically, the function combinations).

                
        for a,b in itertools.combinations(self.objects_list, 2):
            force = self.force(a,b)
            a.add_force(force)
            b.add_force(-force)
            
class CohesionForce(PairForce):
    def __init__(self, objects_list = [], strength = 1.0, radius= 50):
        self.strength = strength
        self.radius = radius
        super().__init__(objects_list)
        
    def force(self, a, b):
        r = a.pos - b.pos
        
        if r.length() < self.radius and r.length() > 0:
            cohesion_force_magnitude = -self.strength * (r.length() - self.radius)
            cohesion_force = r.normalize() * cohesion_force_magnitude
            return cohesion_force
        else:
            return Vector2(0,0)

class Viscosity(SingleForce):
    def __init__(self, objects_list=[], viscosity_coefficient=0.1, **kwargs):
        self.viscosity_coefficient = viscosity_coefficient
        super().__init__(objects_list)
        
    def force(self,obj):
        drag_force = -self.viscosity_coefficient * obj.vel
        return drag_force
    
class PressureForce(PairForce):
    def __init__(self, objects_list=[], pressure_strength=1.0):
        self.pressure_strength = pressure_strength
        super().__init__(objects_list)
        
    def force(self, a, b):
        r = a.pos - b.pos
        distance = r.length()
        
        if distance > 0:
        
            # Calculate the density around particles and apply pressure if overlap occurs
            overlap = a.radius + b.radius - distance
            if overlap > 0:
                pressure_force_magnitude = self.pressure_strength * overlap
                pressure_force = r.normalize() * pressure_force_magnitude
                return pressure_force
        return Vector2(0, 0)
    
class WallInteraction(SingleForce):
    def __init__(self, objects_list=[], walls=[], restitution=0.5, **kwargs):
        self.walls = walls
        super().__init__(objects_list)
        self.restitution = restitution
    
    def force(self, obj):
        total_force = Vector2(0,0)
        for wall in self.walls:
            # If the particle intersects with the wall, apply a restitution force
            if wall.contains(obj.pos):
                wall_normal = (wall.point2 - wall.point1).normalize()
                velocity_normal = obj.vel.dot(wall_normal)
                restitution_force = -self.restitution * velocity_normal * wall_normal
                total_force += restitution_force
        return total_force

class BondForce:
    def __init__(self, pairs_list=[]):
        # pairs_list has the format 
        # [[obj1, obj2], [obj3, obj4], ... ] 
        # ^ each pair representing a bond
        self.pairs_list = pairs_list

    def apply(self):
        # Loop over all *pairs* from the pairs list.
        # Calculate force between that pair  
        for a, b in self.pairs_list:
            force = self.force(a, b)
        # Apply the force to each member of the pair respecting Newton's 3rd Law.
        # Object A receives the force
            a.add_force(force)
        # Object B receives negative force (i.e., same magnitude with opposite direction)
            b.add_force(-force)


# Add Gravity, SpringForce, SpringRepulsion, AirDrag
class Gravity(SingleForce):
    def __init__(self, acc=(0,0), **kwargs):
        self.acc = Vector2(acc)
        super().__init__(**kwargs)

    def force(self, obj):
        return obj.mass*self.acc
        # Note: this will throw an error if the object has infinite mass.
        # Think about how to handle those.
        
class SpringForce(BondForce):
    def __init__(self, stiffness = 0, damping = 0, natural_length = 0, **kwargs):
        self.stiffness = stiffness
        self.damping = damping
        self.natural_length = natural_length
        self.start_pos = Vector2(0,0)
        self.end_pos = Vector2(0,0)
        self.normal = (0,0)
        self.pos = Vector2(0,0)
        self.wall = None
        super().__init__(**kwargs)
        #print(self)
        
    def force(self, a, b):
        r = a.pos - b.pos
        v = a.vel - b.vel
        
        fSpring = (-self.stiffness* (r.length() - self.natural_length) - self.damping*v * r.normalize()) * r.normalize()
        
        return fSpring
    
    def remove_bonds(self, circle_to_remove):
        bond_to_remove = []
        
        for bond in self.pairs_list:
            if circle_to_remove in bond:
                bond_to_remove.append(bond)
        
        for bond in bond_to_remove:
            self.pairs_list.remove(bond)
    def draw(self, window):
        for a, b in self.pairs_list:
            pygame.draw.line(window, color = (255,255,255), start_pos = a.pos, end_pos = b.pos, width = 1)
            self.wall = Wall(point1=a.pos, point2=b.pos, color=(255,255,255))
            self.normal = (b.pos - a.pos).normalize().rotate(90)
            #print(self.normal)
            self.start_pos = Vector2(a.pos)
            self.end_pos = Vector2(b.pos)
            self.pos = Vector2((self.start_pos.x + self.end_pos.x)/2, (self.start_pos.y + self.end_pos.y) / 2)
            
class Drag(SingleForce):
    def __init__(self, objects_list=[], drag_coefficient=0.1, cross_sectional_area=1.0, air_density=1.0,wind_velocity = Vector2(0,0), **kwargs):
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area
        self.air_density = air_density
        self.wind_velocity = wind_velocity
        super().__init__(objects_list)

    def force(self, obj):
        # Calculate the velocity magnitude
        v_magnitude = obj.vel - self.wind_velocity

        # Calculate the drag force magnitude using the air drag formula
        drag_force_magnitude = -0.5 * self.drag_coefficient * self.air_density * (math.pi * obj.radius * obj.radius) * obj.vel.length() * obj.vel + self.wind_velocity

        # Calculate the total drag force
        drag_force = v_magnitude * drag_force_magnitude
        
        #debug check
        print(f"drag force: {drag_force}")
        
        return drag_force_magnitude
    
class SpringRepulsion(PairForce):
    def __init__(self, objects_list=[], spring_constant=100000):
        self.spring_constant = spring_constant
        super().__init__(objects_list)

    def force(self, a, b):
        # r vector a to b
        r = a.pos - b.pos

        if r.length() > 0:
            # sum of radius
            sum_of_radii = a.radius + b.radius

            # Calculate the overlap distance
            overlap = sum_of_radii - abs(r.length())

            # Check if there is overlap between the circles
            if overlap > 0:
                # Calculate the repulsive force magnitude
                repulsion_force_magnitude = self.spring_constant * overlap

                # Calculate the direction of the repulsive force (opposite to r)
                repulsion_direction = r.normalize()

                # Calculate the total repulsive force vector
                repulsion_force = repulsion_direction * repulsion_force_magnitude

                return repulsion_force
        return Vector2(0, 0)
class FrictionForce(SingleForce):
    def __init__(self, mu = .3, g = 9.81):
        self.mu = mu
        self.g = g
        #super().__init__(objects_list)
            
    def apply(self,obj):
        if obj.vel.length() > 0:
            friction_force = -self.mu * obj.mass * self.g * obj.vel.normalize()
            obj.add_force(friction_force)
        else: 
            obj.vel =  Vector2(0,0)