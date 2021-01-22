#going_the_distance.py
"""Find which angle travels furthest"""
import sys, math, random
import pygame as pg

pg.init() #Initialize pygame

#COLOUR TABLE (RGB)
BLACK = (0,0,0)
WHITE = (255,255,255)
LT_GRAY = (180,180,180)
GRAY = (120,120,120)
DK_GRAY = (80,80,80)

class Particle(pg.sprite.Sprite): #Superclass is Sprite
	"""Builds ejecta particles"""
	#Map colours, used for particle, path, name in legend
	degree_colours = {'D':LT_GRAY}
	
	VENT_LOCATION_XY = (320, 300) #Co-ords for mouth of volcano in image (Launch point for particles)
	IO_SURFACE_Y = 308 #Highest point on surface
	GRAVITY = 0.5 #Simulate acceleration of gravity. Px-per-frame; added to dy each game loop
	VELOCITY_SO2 = 8 #Px-per-frame
	
	def __init__(self, screen, background):
		super().__init__() #Call Sprite class initializer
		self.screen = screen
		self.background = background
		self.image = pg.Surface((4, 4)) #Pygame surface object (Square)
		self.rect = self.image.get_rect() #Get rectangle associated with surface object
		self.gas = random.choice(list(Particle.degree_colours.keys())) #Choose random gas
		
		#USING CLASS ATTRIBUTES RATHER THAN SELF!
		self.colour = Particle.degree_colours[self.gas] #Map colour
		self.vel = Particle.VELOCITY_SO2
		self.x, self.y = Particle.VENT_LOCATION_XY #particle's origin X & Y (Mouth of volcano)
		
		self.vector() #Calculate particle's motion vector
		
	def vector(self):
		"""Calculate particle vector at launch"""
		orient = random.choice((5, 15, 25, 35, 45, 55, 65, 75, 85)) #Launch direction
		if orient == 45:
			self.colour = WHITE
		radians = math.radians(orient) #Math module uses radians, so convert orientation degree to radians
		#Vector components are calculated using trigonometry
		self.dx = self.vel * math.cos(radians)
		self.dy = -self.vel * math.sin(radians)
		
		
	def update(self): #Update particles as they move across screen
		"""Apply gravity, draw path, handle boundary conditions"""
		self.dy += Particle.GRAVITY #Apply gravity (only in y axis)
		#Draw path behind particle
		pg.draw.line(self.background, self.colour, (self.x, self.y), (self.x + self.dx, self.y + self.dy))
		#Update particle position
		self.x += self.dx
		self.y += self.dy
		
		#Prevent particles from escaping boundaries
		if self.x < 0 or self.x > self.screen.get_width():
			self.kill()
		if self.y < 0 or self.y > Particle.IO_SURFACE_Y:
			self.kill()
			
					
def main():
	"""Setup & run game screen & loop"""
	screen = pg.display.set_mode((639, 360)) #Pixel dimensions (Tuple)
	pg.display.set_caption("Which Angle Travels the Furthest?") #Name the window
	background = pg.image.load("tvashtar_plume.gif") #Setup window background
	
	#Setup colour-coded legend
	legend_font = pg.font.SysFont("None", 24) #Default font
	D85_label = legend_font.render("--- 85", True, LT_GRAY, BLACK)
	D75_label = legend_font.render("--- 75", True, LT_GRAY, BLACK)
	D65_label = legend_font.render("--- 65", True, LT_GRAY, BLACK)
	D55_label = legend_font.render("--- 55", True, LT_GRAY, BLACK)
	D45_label = legend_font.render("--- 45", True, WHITE, BLACK)
	D35_label = legend_font.render("--- 35", True, LT_GRAY, BLACK)
	D25_label = legend_font.render("--- 25", True, LT_GRAY, BLACK)
	D15_label = legend_font.render("--- 15", True, LT_GRAY, BLACK)
	D5_label = legend_font.render("--- 05", True, LT_GRAY, BLACK)
	
	particles = pg.sprite.Group() #pygame uses sprite group container to manage sprites
	
	clock = pg.time.Clock() #Create Clock object to track & control frame rate
	
	while True: #Simulation loop
		time_label = legend_font.render(str(pg.time.get_ticks() / 1000), True, LT_GRAY, BLACK)
		clock.tick(25) #Set speed, max fps
		particles.add(Particle(screen, background)) #Instantiate particle and add to sprite group
		
		for event in pg.event.get(): #Event handler
			if event.type == pg.QUIT: #If window is closed
				pg.quit()
				sys.exit()
				
		#Render visual elements at co-ords of window (bg & legend)
		screen.blit(background, (0, 0))
		screen.blit(legend_font.render("DEGREES:", True, WHITE, BLACK), (40, 20))
		screen.blit(D85_label, (40, 40))
		screen.blit(D75_label, (40, 60))
		screen.blit(D65_label, (40, 80))
		screen.blit(D55_label, (40, 100))
		screen.blit(D45_label, (40, 120))
		screen.blit(D35_label, (40, 140))
		screen.blit(D25_label, (40, 160))
		screen.blit(D15_label, (40,180))
		screen.blit(D5_label, (40, 200))
		screen.blit(time_label, (40, 300))
		
		particles.update() #Runs particle object's own update() method
		particles.draw(screen) #Draw sprites on screen
		
		pg.display.flip() #Update game graphics
		
		if (pg.time.get_ticks() / 1000) % 3 > 2.5: # A half-working reset button
			main()
		
if __name__ == "__main__":
	main()
