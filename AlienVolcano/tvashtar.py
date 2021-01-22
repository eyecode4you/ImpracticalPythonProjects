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
	"""Builds ejecta particles for volcano sim"""
	#Map colours, used for particle, path, name in legend
	gases_colours = {'SO2':LT_GRAY, 'CO2':GRAY, 'H2S':DK_GRAY, 'H2O':WHITE}
	
	VENT_LOCATION_XY = (320, 300) #Co-ords for mouth of volcano in image (Launch point for particles)
	IO_SURFACE_Y = 308 #Highest point on surface
	GRAVITY = 0.5 #Simulate acceleration of gravity. Px-per-frame; added to dy each game loop
	VELOCITY_SO2 = 8 #Px-per-frame
	
	#Scalars (SO2 atomic weight/particle atomic weight) used for velocity
	vel_scalar = {'SO2':1, 'CO2':1.45, 'H2S':1.9, 'H2O':3.6}
	
	def __init__(self, screen, background):
		super().__init__() #Call Sprite class initializer
		self.screen = screen
		self.background = background
		self.image = pg.Surface((4, 4)) #Pygame surface object (Square)
		self.rect = self.image.get_rect() #Get rectangle associated with surface object
		self.gas = random.choice(list(Particle.gases_colours.keys())) #Choose random gas
		
		#USING CLASS ATTRIBUTES RATHER THAN SELF!
		self.colour = Particle.gases_colours[self.gas] #Map colour
		self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
		self.x, self.y = Particle.VENT_LOCATION_XY #particle's origin X & Y (Mouth of volcano)
		
		self.vector() #Calculate particle's motion vector
		
	def vector(self):
		"""Calculate particle vector at launch"""
		orient = random.uniform(60, 120) #Launch Direction. 30 & 120 denotes 30 degrees either side of 90 degrees (Straight up)
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
	pg.display.set_caption("IO Volcano Simulator") #Name the window
	background = pg.image.load("tvashtar_plume.gif") #Setup window background
	
	#Setup colour-coded legend
	legend_font = pg.font.SysFont("None", 24) #Default font
	water_label = legend_font.render("--- H2O", True, WHITE, BLACK)
	h2s_label = legend_font.render("--- H2S", True, DK_GRAY, BLACK)
	co2_label = legend_font.render("--- CO2", True, GRAY, BLACK)
	so2_label = legend_font.render("--- SO2", True, LT_GRAY, BLACK)
	
	particles = pg.sprite.Group() #pygame uses sprite group container to manage sprites
	
	clock = pg.time.Clock() #Create Clock object to track & control frame rate
	
	while True: #Simulation loop
		clock.tick(60) #Set speed, max fps
		particles.add(Particle(screen, background)) #Instantiate particle and add to sprite group
		
		for event in pg.event.get(): #Event handler
			if event.type == pg.QUIT: #If window is closed
				pg.quit()
				sys.exit()
				
		#Render visual elements at co-ords of window (bg & legend)
		screen.blit(background, (0, 0))
		screen.blit(water_label, (40, 20))
		screen.blit(h2s_label, (40, 40))
		screen.blit(co2_label, (40, 60))
		screen.blit(so2_label, (40, 80))
		
		particles.update() #Runs particle object's own update() method
		particles.draw(screen) #Draw sprites on screen
		
		pg.display.flip() #Update game graphics
		
if __name__ == "__main__":
	main()
