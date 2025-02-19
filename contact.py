from pygame.math import Vector2
from physics_objects import *

# Returns a new contact object of the correct subtype
# This function has been done for you.
def generate(a, b, **kwargs):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order, 
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"{a.contact_type}_{b.contact_type}"](a, b, **kwargs)
    

# Generic contact class, to be overridden by specific scenarios
class Contact():
    def __init__(self, a, b, resolve=False, **kwargs):
        self.a = a
        self.b = b
        self.overlap = 0
        self.kwargs = kwargs
        self.update() # the update() function is created in the derived classes
        if resolve:
            self.resolve(update=False)

    def resolve(self, update=True, **kwargs):
        if update:
            self.update()
        # # This pattern first checks keywords to resolve, then keywords given to contact.

        #relative_velocity_at_contact = relative_velocity + self.a.radius * self.a.avel * self.normal

        # # Keywords given here to resolve override the previous ones given to contact.
        restitution = kwargs.get("restitution", self.kwargs.get("restitution", 0)) # 0 is default
        friction_coefficient = kwargs.get("friction", self.kwargs.get("friction", 0))
        rebound_speed = kwargs.get("rebound_speed", self.kwargs.get("rebound_speed", 0))
        # # RESOLVE OVERLAP
        if self.overlap > 0:
            tangent = self.normal.rotate(90)
            m = 1 / (1 / self.a.mass + 1 / self.b.mass)
            
            self.a.set(pos = self.a.pos +((m/self.a.mass) * (self.overlap * self.normal)))
            self.b.set(pos = self.b.pos - ((m/self.b.mass) * self.overlap * self.normal))
                
            point = self.point()
            sa = point - self.a.pos
            sb = point - self.b.pos
            
            va = self.a.vel + math.radians(self.a.avel)*sa.rotate(90)
            vb = self.b.vel + math.radians(self.b.avel)*sb.rotate(90)
            
            v = va-vb
            vdotn = v.dot(self.normal)
                
            if vdotn < 0:
                #Calculate the impulses needed for collision resolution
                sa_cross_n = sa.cross(self.normal)
                sb_cross_n = sb.cross(self.normal)
                
                #Moment of inertia for each object
                ja = (sa_cross_n**2) / self.a.mom_i
                jb = (sb_cross_n**2) / self.b.mom_i
                
                m = 1 / (1 / self.a.mass + 1/self.b.mass + ja + jb)
                jn = -(1+restitution) * vdotn
                
                J = jn / (1 / self.a.mass + 1 / self.b.mass + ja + jb)
                
                impulse = J * self.normal
                self.a.impulse(impulse)
                self.b.impulse(-impulse)
                
                vdott = v.dot(tangent)
                Jt = -m * vdott
                
                if abs(Jt) < friction_coefficient * jn:
                    shift_vector = vdott / vdotn * self.overlap * tangent
                    self.a.pos += shift_vector * m / self.a.mass
                    self.b.pos -= shift_vector * m / self.b.mass
                else:
                    Jt = friction_coefficient * jn * math.copysign(1 , -vdott)

                
            if rebound_speed > 0 :
                relative_velocity = self.a.vel - self.b.vel
                relative_velocity_at_contact = relative_velocity.dot(self.normal) * self.normal
                
                reduced_mass = (self.a.mass * self.b.mass) / (self.a.mass + self.b.mass)
                
                impulse_magnitude = -(1 + restitution) * relative_velocity_at_contact * self.normal + m * rebound_speed
                
                collisionDamping = .1
                #print(impulse_magnitude * self.normal)
                #print(impulse_magnitude * self.normal * collisionDamping)
                

                    # Apply impulse to both bumper and the object it collided with
                self.a.impulse(impulse_magnitude * self.normal * collisionDamping)
                self.b.impulse(-impulse_magnitude * self.normal * collisionDamping)

# Contact class for two circles
class Circle_Circle(Contact):
    def update(self):  # compute the appropriate values
        self.contact_type = "CircleBumper"
        
        r = self.a.pos - self.b.pos
        
        distance = r.magnitude()
        
        if distance > 0:
            self.overlap = (self.a.radius + self.b.radius) - distance
            
            if self.overlap > 1e-5:
                self.normal = r.normalize() * .5 
                print(f"Overlap: {self.overlap}, Normal: {self.normal}")
            else: 
                self.normal = Vector2(0,0)
                self.overlap = 0
        else:
            self.normal = Vector2(0,0)
            self.overlap = 0
            
    def point(self):
        return self.a.pos - self.normal * self.a.radius

# Contact class for Circle and a Wall
# Circle is before Wall because it comes before it in the alphabet
class Circle_Wall(Contact):
    def update(self):  # compute the appropriate values
        self.a : Circle
        self.b : Wall
        
        self.overlap = 0
        self.contact_type = "Wall"
        
        #Vector from the wall point to circle center
        r = self.a.pos - self.b.point1
        
        distance = r.dot(self.b.normal)
        
        EPSILON = 1e-5
        
        #print("overlap",self.overlap)
        if distance < self.a.radius - EPSILON:
            self.overlap = self.a.radius - distance
            
            self.normal = self.b.normal.normalize()
        else:
            self.normal = Vector2(0,0)
    def point(self):
        return self.a.pos - self.normal * self.a.radius
        

# Empty class for Wall - Wall collisions
# The intersection of two infinite walls is not interesting, so skip them
class Wall_Wall(Contact):
    def update(self):
        pass
    pass
class Polygon_Polygon(Contact):
    def update(self):
        #pass
        self.a: Polygon
        self.b: Polygon
        self.index = -1
        self.overlap = math.inf   # Set initial overlap to infinity
        self.point_polygon = self.a   # Treat 'a' as the polygon and 'b' as a list of walls
        for pos, normal in zip(self.b.points, self.b.normals):
            max_overlap = -math.inf
            max_normal = Vector2(0,0)
            strange_index = 0
            # Calculate the overlap between 'a' and each "wall" of 'b'
            for i, point in enumerate((self.a.points)):
                r = point - pos
                overlap = (-r).dot(normal)
                if  overlap > max_overlap:
                    strange_index = i
                    max_overlap = overlap
                    max_normal = normal
                    
            if max_overlap < self.overlap :
                self.overlap = max_overlap
                self.normal = max_normal
                self.index = strange_index
                self.point_polygon = self.a
        #------------------------------------
        for pos, normal in zip(self.a.points, self.a.normals):
            max_overlap = -math.inf
            max_normal = Vector2(0,0)
            strange_index = 0
            # Calculate the overlap between 'a' and each "wall" of 'b'
            for i, point in enumerate((self.b.points)):
                r = point - pos
                overlap = (-r).dot(normal)
                if  overlap > max_overlap:
                    strange_index = i
                    max_overlap = overlap
                    max_normal = normal
                    
            if max_overlap < self.overlap :
                self.overlap = max_overlap
                self.normal = -1 * max_normal
                self.index = strange_index
                self.point_polygon = self.b
        #-----------------------------------
    
    def point(self):
        self.a.contact_point = self.point_polygon.points[self.index]
        self.b.contact_point = self.point_polygon.points[self.index]

        return self.point_polygon.points[self.index]


class Polygon_Wall(Contact):
    def update(self):
        self.a: Polygon
        self.b: Wall
        self.index = 0
        # self.overlap needs to be the minimum overlap
        # First set it to infinity and then keep searching for lower
        self.overlap = math.inf
        self.max_overlap = 0
        self.max_index = 0
        self.normal = Vector2(0, 0)
        self.contact_type = "Wall"
        
        # Implement polygon-wall collision detection logic
        for i, point in enumerate(self.a.points):
            r = (point - self.b.pos)
            n = self.b.normal
            overlap = -r.dot(n)
            #print(overlap)
            if  self.overlap > overlap > self.max_overlap:
                self.max_overlap = overlap
                self.max_index = i
                
        self.index = self.max_index
        self.overlap = self.max_overlap
        self.normal = n
        
    def point(self):
        self.a.contact_point = self.a.points[self.index]
        # Return the contact point based on the collision detection logic
        return self.a.points[self.index]

class Circle_Polygon(Contact):
    def update(self):
        self.a : Circle
        self.b : Polygon
        self.index = 0
        # self.overlap needs to be the minimum overlap
        #First set it to infinity and then keep searching for lower
        self.overlap = math.inf
        self.normal = Vector2(0,0)
        self.contact_type = "Polygon"
        
        
        for i, (point, normal) in enumerate(zip(self.b.points, self.b.normals)):
            overlap = self.a.radius - (self.a.pos - point).dot(normal)
            if overlap < self.overlap:
                self.index = i
                self.overlap = overlap
                self.normal = normal
                
        if 0 < self.overlap < self.a.radius:
            point1 = self.b.points[self.index]
            point2 = self.b.points[(self.index + 1) % len(self.b.points)]  # Wrap around to the first point

            # Calculate the contact point
            r = self.a.pos - point1
            self.contact_point = point1 + r.project(self.normal)

            # Check for circle-corner collision
            circle_center = self.a.pos 
            endpoint1 = point1
            endpoint2 = point2

            # Calculate the vectors from circle center to endpoints
            vector_to_endpoint1 = endpoint1 - circle_center
            vector_to_endpoint2 = endpoint2 - circle_center

            # Check if the circle center lies beyond one of the endpoints
            if vector_to_endpoint1.dot(self.normal) > 0:
                circle_b = Circle(pos=endpoint1, radius=0)
                c = Circle_Circle(self.a, circle_b)
                c.update()
                if c.overlap > 0:
                    self.overlap = c.overlap
                    self.normal = c.normal

            if vector_to_endpoint2.dot(self.normal) > 0:
                circle_b = Circle(pos=endpoint2, radius=0)
                c = Circle_Circle(self.a, circle_b)
                c.update()
                if c.overlap > 0 and c.overlap < self.overlap:
                    self.overlap = c.overlap
                    self.normal = c.normal
    
    def point(self):
        self.b.contact_point = self.a.pos + self.a.radius * (-self.normal)
        self.a.contact_point = self.a.pos + self.a.radius * (-self.normal)

        return self.a.pos + self.a.radius * (-self.normal)