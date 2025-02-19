import math
from pygame.math import Vector2, Vector3
import pygame

class Particle:
    def __init__(self, pos=(0,0), vel=(0,0), mass = 1, angle = 0, avel = 0,torque = 0, mom_i = math.inf, static = False):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.mass = mass
        self.angle = angle
        self.avel = avel
        self.mom_i = mom_i
        self.torque = torque
        self.static = static
        self.contact_type = "NoContact"
        self.contact_point = Vector2(0,0)
        self.force = Vector2(0,0)

    def clear_force(self):
        self.force *=0

    def add_force(self, force):
        if not self.static:
            self.force += force
        
    def impulse(self,impulse):
        if not self.static:
            self.vel += impulse/self.mass
            
            Sa = self.contact_point - self.pos
            
            angular_impulse = Sa.cross(impulse) / self.mom_i
            
            self.avel += angular_impulse

    def update(self, dt):
        if not self.static:
            self.avel += self.torque / self.mom_i * dt
            
            # update velocity using the current force
            self.vel += self.force/self.mass * dt
            # update position using the newly updated velocity
            self.pos += self.vel * dt
            
            self.angle += self.avel * dt
    def set(self, pos=None, angle=None):
        if pos is not None:
            self.pos = Vector2(pos)
        if angle is not None:
            self.angle = angle

class Circle(Particle):
    def __init__(self, radius = 100, color= (255,255,255), width = 0, fixed = False, highlighted = False, **kwargs):
        self.color = Vector3(color)
        self.radius = radius
        self.width = width
        self.fixed = fixed
        self.overlap = 0
        self.highlighted = highlighted
        super().__init__(**kwargs)
        self.contact_type = "Circle"

    def draw(self, window):
        if self.highlighted:
            pygame.draw.circle(window,(255,255,255), self.pos, self.radius + 10, self.width)
        pygame.draw.circle(window,self.color, self.pos, self.radius, self.width)
    
    def contains_point(self,point):
        diff_point = Vector2(point)
        distance = (self.pos - diff_point).length_squared()
        return distance <= self.radius ** 2

class Polygon(Particle):
    def __init__(self, local_points,bumper = False, color = (255,255,255), width = 0, normals_length = 0, **kwargs):
        super().__init__(**kwargs)
        self.local_points = [Vector2(x) for x in local_points]
        self.local_normals = [(self.local_points[i] - self.local_points[i-1]).normalize().rotate(90) for i in range(len(self.local_points))]
        self.color = color
        self.width = width
        self.normals_length = normals_length
        self.points = []
        self.normals = []
        self.update_polygon()
        self.contact_type = "Polygon"
        self.bumper = bumper
        
    def update(self,dt):
        super().update(dt)
        self.update_polygon()
        
    def update_polygon(self):
        self.points = [x.rotate(self.angle) + self.pos for x in self.local_points]
        self.normals = [x.rotate(self.angle) for x in self.local_normals]
        
    def draw(self,window):
        pygame.draw.polygon(window, self.color, self.points, self.width)
        if self.normals.__len__() > 0:
            for point,normal in zip(self.points, self.normals):
                pygame.draw.line(window, (0,0,0), point, point + self.normals_length * normal)
    def set(self, pos=None, angle=None):
        super().set(pos=pos, angle=angle)
        self.update_polygon()
        
class Wall(Particle):
    def __init__(self, point1=(0,0), point2=(0,0), color = (255,255,255), width = 1):
        self.color = Vector3(color)
        self.width = width
        self.point1 = Vector2(point1)
        self.point2 = Vector2(point2)
        self.overlap = 0
        self.normal = (self.point2 - self.point1).normalize().rotate(90)
        super().__init__(pos=(self.point1 + self.point2)/2, mass = math.inf)
        self.contact_type = "Wall"
        
    def draw(self,window):
        pygame.draw.line(window, self.color, self.point1, self.point2, self.width)
        
    def contains(self, point):
        """Check if the point is near or intersecting the wall."""
        # Vector from point1 to the point
        v1 = point - self.point1
        # Vector from point1 to point2 (the direction of the wall)
        v2 = self.point2 - self.point1
        # Project v1 onto v2 to get the closest point on the wall
        projection = v1.dot(v2.normalize())  # Scalar projection of v1 onto v2
        
        # Check if the projection is between 0 and the length of the wall (v2 length)
        if 0 <= projection <= v2.length():
            # Distance from the point to the wall (perpendicular distance)
            closest_point = self.point1 + v2.normalize() * projection
            distance_to_wall = (point - closest_point).length()

            # Check if the point is close enough to the wall (within some threshold)
            return distance_to_wall < self.width / 2  # You can adjust the threshold based on wall width or tolerance
        return False
        
class UniformCircle(Circle):
    def __init__(self, density=1, pos = [0,0], radius = 0, **kwargs):
        # calculate mass and moment of inertia
        mass = density * math.pi * radius**2
        mom_i = .5 * mass * radius **2
        density = mass/(math.pi * radius**2)

        super().__init__(mass=mass, radius = radius, pos = pos, mom_i=mom_i, **kwargs)


class UniformPolygon(Polygon):
    def __init__(self, density=None, local_points=[], pos=[0,0], angle=0, shift=True, mass=None, **kwargs):
        if mass is not None and density is not None:
            raise("Cannot specify both mass and density.")
        if mass is None and density is None:
            mass = 1 # if nothing specified, default to mass = 1
        # Calculate mass, moment of inertia, and center of mass
        total_mass = 0
        total_momi = 0
        cenmass_numerator = Vector2(0,0)
        # by looping over all "triangles" of the polygon
        for i in range(len(local_points)):
            ri = Vector2(*local_points[i])
            ri2 = Vector2(*local_points[i-1])
            # triangle area
            tri_area = .5 * (ri.x * ri2.y - ri2.x * ri.y)
            # triangle mass
            tri_mass = density * tri_area
            # triangle moment of inertia
            tri_mom_i = 1/6 * (ri.magnitude_squared() + ri2.magnitude_squared() + (ri.dot(ri2)))
            # triangle center of mass
            tri_cenmass = (ri + ri2)/3

            # add to total mass
            total_mass += tri_mass
            # add to total moment of inertia
            total_momi += tri_mom_i
            # add to center of mass numerator
            cenmass_numerator += tri_mass * tri_cenmass
        total_com = cenmass_numerator / total_mass
        
        # calculate total center of mass by dividing numerator by denominator (total mass)

        # if mass is specified, then scale mass and momi
        if mass is not None:
            total_momi *= mass/total_mass
            total_mass = mass
        # Usually we shift local_points origin to center of mass
        if shift:
            # Shift local_points by com
            local_points = [(point[0] - total_com.x ,point[1] - total_com.y) for point in local_points]
            # shift pos
            pos  = Vector2(pos) + total_com#+= total_momi.rotate(self.angle)
            # Use parallel axis theorem to correct the moment of inertia
            shifted_momi = total_momi + total_mass * (total_com.magnitude_squared())
        else:
            shifted_momi = total_momi          

        # Then call super().__init__() with those correct values
        super().__init__(mass=total_mass, mom_i=shifted_momi, local_points=local_points, pos=pos, angle=angle, **kwargs) 
