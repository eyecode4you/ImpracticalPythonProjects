#Highlight APEX in white
import sys, math, random
import pygame as pg

pg.init() #Initialize pygame

#COLOUR TABLE (RGB)
BLACK = (0,0,0)
WHITE = (255,255,255)
DK_GRAY = (80,80,80)

class Particle(pg.sprite.Sprite):
	"""Builds ejecta particles for volcano sim"""
	
	VENT_LOCATION_XY = (320, 300) #Co-ords for mouth of volcano in image
	IO_SURFACE_Y = 308 #Highest point on surface
	GRAVITY = 0.25 
	VELOCITY_SO2 = 8 #Px-per-frame
	
	
	#Scalars (SO2 atomic weight/particle atomic weight) used for velocity
	vel_scalar = {'SO2':1}
	
	def __init__(self, screen, background):
		super().__init__()
		self.screen = screen
		self.background = background
		self.image = pg.Surface((4, 4))
		self.rect = self.image.get_rect()
		self.gas = 'SO2'
		
		#USING CLASS ATTRIBUTES RATHER THAN SELF!
		self.colour = DK_GRAY
		self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
		self.x, self.y = Particle.VENT_LOCATION_XY
		
		self.vector() #Calculate particle's motion vector
		
	def vector(self):
		"""Calculate particle vector at launch"""
		orient = random.uniform(60, 120) #Launch Direction. 30 & 120 denotes 30 degrees either side of 90 degrees (Straight up)
		radians = math.radians(orient) #Math module uses radians, so convert orientation degree to radians
		
		self.dx = self.vel * math.cos(radians)
		self.dy = -self.vel * math.sin(radians)
		
	def update(self):
		"""Apply gravity, draw path, handle boundary conditions"""
		self.dy += Particle.GRAVITY #Apply gravity (only in y axis)
		
		#map out apex region
		if self.dy >= -1.0 and self.dy <= 1.0:
			self.colour = WHITE
		else:
			self.colour = DK_GRAY
		
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
	screen = pg.display.set_mode((639, 360))
	pg.display.set_caption("IO Volcano Simulator")
	background = pg.image.load("tvashtar_plume.gif")
	
	#Setup colour-coded legend
	legend_font = pg.font.SysFont("None", 24)
	water_label = legend_font.render("--- APEX REGION", True, WHITE, BLACK)
	
	particles = pg.sprite.Group()
	
	clock = pg.time.Clock()
	
	while True:
		clock.tick(30)
		particles.add(Particle(screen, background))
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
				
		#Render visual elements at co-ords of window (bg & legend)
		screen.blit(background, (0, 0))
		screen.blit(water_label, (40, 176))
		
		particles.update()
		particles.draw(screen)
		
		pg.display.flip()
		
if __name__ == "__main__":
	main()
