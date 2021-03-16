import os, math, random as ran, time
import pygame as pg

#COLOR TABLE: WHITE, BLACK, RED, GREEN, LT_BLUE
COLOR = ((255,255,255), (0,0,0), (255,0,0), (0,255,0), (173,216,230))

class Satellite(pg.sprite.Sprite): #Obj from this will be sprites
	""" Satellite object that rotates to face planet """
	def __init__(self, bg):
		super().__init__() #Invoke __init__ of Sprite superclass
		
		self.background = bg
		
		#Load & Convert satellite images
		self.image_sat = \
		pg.image.load(r".\resource\satellite.png").convert()
		self.image_crash = \
		pg.image.load(r".\resource\satellite_crash_40x33.png").convert()
		
		self.image = self.image_sat
		
		#Pygame places sprites on rectangle surface objects, needs to
		#know dimensions and locations of rectangles as program runs
		self.rect = self.image.get_rect()
		self.image.set_colorkey(COLOR[1]) #Black - Transparent
		
		#Starting Location & Velocity
		self.x = ran.randrange(315, 425) #Sat starts near top of screen
		self.y = ran.randrange(70, 180)
		self.dx = ran.choice([-3, 3]) #rand -> or <- wise velocity
		self.dy = 0 #gravity() will take you
		
		self.heading = 0 #Sat dish orientation
		self.fuel = 500 #full tank
		#25% fuel threshold Used for warning label
		self.fuel_thresh = self.fuel * 0.25
		self.mass = 1
		self.distance = 0 #Between sat & planet
		self.thrust = pg.mixer.Sound(r".\resource\thrust_audio.ogg")
		self.thrust.set_volume(0.03) #Values 0-1
		
	def thruster(self, dx, dy):
		""" Execute thruster operation """
		self.dx += dx
		self.dy += dy
		self.fuel -= 2
		self.thrust.play()
		
	def chk_keys(self):
		""" Check if arrow keys pressed """
		if(self.y >= 270 and self.y <= 370 and self.x < 400):
			pass #Disable controls if sat in shadow
		else:
			keys = pg.key.get_pressed() #Tuple Bools of keyboard keystates
			#Fire thrusters
			if keys[pg.K_d]: #Right
				self.thruster(dx=0.05, dy=0)
			elif keys[pg.K_a]: #Left
				self.thruster(dx=-0.05, dy=0)
			elif keys[pg.K_w]: #Up
				self.thruster(dx=0, dy=-0.05)
			elif keys[pg.K_s]: #Down
				self.thruster(dx=0, dy=0.05)
				
	def locate(self, planet):
		""" Calc distance & heading to planet """
		px, py = planet.x, planet.y #Get planet's x & y coords
		dist_x, dist_y = self.x - px, self.y - py # - from sat coords
		
		#get direction of planet to point sat dish
		
		#calc arc tangent in radians (math module)
		planet_dir_radians = math.atan2(dist_x, dist_y)
		
		#Pygame uses degrees so conv to degrees
		self.heading = planet_dir_radians * 180 / math.pi
		
		#-90 degrees to keep sat dish pointed at planet
		#neg angles result in clockwise rotation in pygame
		self.heading -= 90 #Sprite travelling tail-first
		
		#Get Euclidian distance between sat and planet
		self.distance = math.hypot(dist_x, dist_y)
		
	def rotate(self):
		""" Rotate sat using degrees so dish faces planet """
		self.image = pg.transform.rotate(self.image_sat, self.heading)
		self.rect = self.image.get_rect()
		
	def path(self):
		""" Update sat position & draw orbital path """
		last_center = (self.x, self.y) #1st point in line
		self.x += self.dx
		self.y += self.dy
		pg.draw.line(self.background, COLOR[0], last_center, \
		(self.x, self.y)) #2nd point
		
	def update(self):
		""" Update sat object during game """
		self.chk_keys() #Check player interaction
		self.rotate() #Keep pointing toward planet
		self.path() #update pos & draw path
		self.rect.center = (self.x, self.y) #Keep track of sat sprite
		
		#Lose
		if self.dx == 0 and self.dy == 0:
			self.image = self.image_crash
			self.image.set_colorkey(COLOR[1])
			
class Planet(pg.sprite.Sprite):
	""" Planet obj that rotates & projects gravity field """
	def __init__(self):
		super().__init__()
		self.image_mars = \
		pg.image.load(r".\resource\mars.png").convert()
		
		self.image_water = \
		pg.image.load(r".\resource\mars_water.png").convert()
		
		#copy of original img - no permanent modifications
		self.image_copy = \
		pg.transform.scale(self.image_mars, (100, 100)) #scale 100x100px
		
		self.image_copy.set_colorkey(COLOR[1])
		self.rect = self.image_copy.get_rect()
		self.image = self.image_copy
		
		self.mass = 2000 #Planet G
		self.x = 400
		self.y = 320
		self.rect.center = (self.x, self.y)
		self.angle = math.degrees(0)
		self.rotate_by = math.degrees(0.01) #degrees to rotate planet by
		
	def rotate(self):
		""" Rotate planet with each game loop 
			As the image rotates, the bounding rectangle obj rect
			remains stationary and must expand for new config - can 
			affect center point of rect, so assign last_center point to
			current center point """
		last_center = self.rect.center
		self.image = pg.transform.rotate(self.image_copy, self.angle)
		self.rect = self.image.get_rect() #reset rect obj
		self.rect.center = last_center #re-center
		self.angle += self.rotate_by # += 0.01 degrees
		
	def gravity(self, sat):
		""" Calc impact of G on Satellite """
		G = 1.0 # Grav constant for game
		dist_x = self.x - sat.x #Get distance between sat and planet
		dist_y = self.y - sat.y
		
		#Euclidian Distance (r in Gravity Equation)
		distance = math.hypot(dist_x, dist_y)
		
		#Noramize to unit vector, needed to preserve direction
		dist_x /= distance
		dist_y /= distance
		
		#Apply G (dx & dy = px/frame), Law of Universal G
		force = G * (sat.mass * self.mass) / (math.pow(distance, 2))
		sat.dx += (dist_x * force) #Calc accel change in V each step
		sat.dy += (dist_y * force)
		
	def update(self):
		""" Call rotate() """
		self.rotate()
		
def calc_eccentricity(dist_list):
	""" Calc & return eccentricity from list of radii """
	apoapsis = max(dist_list)
	periapsis = min(dist_list)
	eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)
	return eccentricity
	
def instruct_label(screen, text, color, x, y):
	""" Render list of strings to screen """
	instruct_font = pg.font.SysFont(None, 25) #Force Pygame default font
	line_spacing = 22
	for i, line in enumerate(text): #Index list of texts for locations
		label = instruct_font.render(line, True, color, COLOR[1])
		screen.blit(label, (x, y + i * line_spacing))
		
def box_label(screen, text, dimensions, color):
	""" Make fixed size labels """
	readout_font = pg.font.SysFont(None, 27)
	base = pg.Rect(dimensions) #Create fixed-size rect to hold dyna text
	pg.draw.rect(screen, color, base, 0) #Draw base
	label = readout_font.render(text, True, COLOR[1])
	label_rect = label.get_rect(center=base.center) #In center of base
	screen.blit(label, label_rect)
	
def mapping_on(planet):
	""" Show Soil Moisture image of planet """
	last_center = planet.rect.center #Keep at center of screen
	planet.image_copy = \
	pg.transform.scale(planet.image_water, (100, 100))
	planet.image_copy.set_colorkey(COLOR[1])
	planet.rect = planet.image_copy.get_rect()
	planet.rect.center = last_center
	
def mapping_off(planet):
	""" Restore normal planet image """
	planet.image_copy = \
	pg.transform.scale(planet.image_mars, (100, 100))
	planet.image_copy.set_colorkey(COLOR[1])
	
def cast_shadow(screen):
	""" Add shadow behind planet """
	shadow = pg.Surface((400, 100), flags=pg.SRCALPHA) #tuple is w, h px
	shadow.fill((0,0,0,220)) #RGB + Transparency
	screen.blit(shadow, (0, 270)) #Top left coords
	
def shadow_lock_controls(screen, sat):
	""" Display control lock text if within shadow of planet """
	if(sat.y >= 270 and sat.y <= 370 and sat.x < 400): #Shadow dimension
		instruct_label(screen, "Controls Locked", COLOR[2], 145, 100)
	
def main():
	""" Setup labels & instructions, create objs & run game loop """
	pg.init() #Initialize Game
	
	#Setup display
	os.environ['SDL_VIDEO_WINDOW_POS'] = '700, 100' #game window origin
	#Set display window resolution
	screen = pg.display.set_mode((800, 645))
	pg.display.set_caption("Satellite Orbiter Game")
	background = pg.Surface(screen.get_size()) #bg same size as screen
	pg.mixer.init() #For sound effects
	
	#Create and show title screen
	title_image = pg.image.load(r".\resource\title.jpg").convert()
	screen.blit(title_image, (0,0))
	pg.display.flip()
	time.sleep(3)
	
	intro_txt = [
	' The Mars Orbiter experienced an error during Orbit insertion.',
	' Use thrusters to correct to a circular mapping orbit without',
	' running out of propellant or burning up in the atmosphere.']
	
	instruct_text1 = [
	'Orbital altitude must be within 69-120 miles',
	'Orbital Eccentricity must be < 0.05',
	'Avoid top of atmosphere at 68 miles']
 
	instruct_text2 = [
	'A = Decrease Dx',
	'D = Increase Dx',
	'W = Decrease Dy',
	'S = Increase Dy',
	'Space Bar = Clear Path',
	'Escape = Quit Game']
	
	#Instantiate planet & satellite objects
	planet = Planet()
	planet_sprite = pg.sprite.Group(planet)
	sat = Satellite(background) #bg for drawing path
	sat_sprite = pg.sprite.Group(sat)
	
	#Circular Orbit Verification
	dist_list = [] #Hold distance values for each loop
	eccentricity = 1 #Non-circular starting orbit
	eccentricity_calc_interval = 5
	
	#Time keeping
	clock = pg.time.Clock()
	fps = 60
	tick_count = 0 #clearing text and calling calc_eccentricity()
	
	#Soil Moisture mapping functionality
	mapping_enabled = False #Winning condition = True
	
	running = True #Program run flag
	fail = False #Lose condition - If fuel 0 or distance <= 69
	while running: #Game loop
		if fail == True:
			time.sleep(2)
			quit(0)
		clock.tick(fps) #Set game speed
		tick_count += 1
		dist_list.append(sat.distance)
		
		#Get keyboard input
		for event in pg.event.get(): #get pygame event buffer
			if event.type == pg.QUIT: #if closed window
				running = False
			elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				quit(0) #Quit Game
			elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
				background.fill(COLOR[1]) #Clear sat drawn path
			elif event.type == pg.KEYUP:
				sat.thrust.stop() #Stop sound
				mapping_off(planet) #Turn off moisture map view
			elif mapping_enabled:
				if event.type == pg.KEYDOWN and event.key == pg.K_m:
					mapping_on(planet)
					
		#Get heading & distance to planet & apply gravity
		sat.locate(planet) #Sat's heading * distance to planet
		planet.gravity(sat) #Apply planet's G on Sat
		
		#Calc orbital eccentricity every 300frames (5 seconds)
		if tick_count % (eccentricity_calc_interval * fps) == 0:
			eccentricity = calc_eccentricity(dist_list)
			dist_list = []
			
		#Re-blit bg for drawing cmd - prevents clearing path
		screen.blit(background, (0,0))
		
		#Fuel/Altitude fail conditions
		if sat.fuel <= 0:
			instruct_label \
			(screen, ['Fuel Depleted!'], COLOR[2], 340, 195)
			sat.thrust.stop()
			fail = True #Lose flag
		elif sat.distance <= 68: #dist from center, rather than surface
			instruct_label \
			(screen, ['Atmospheric Entry!'], COLOR[2], 320, 195)
			sat.dx, sat.dy = 0, 0 #Sat locked to planet, turns red
			fail = True
			
		#Enable mapping functionality (Win conditions)
		if eccentricity < 0.05 and sat.distance >= 69 \
		and sat.distance <= 120:
			map_instruct = ['Press & hold M to map soil moisture']
			instruct_label(screen, map_instruct, COLOR[4], 250, 175)
			mapping_enabled = True
		else:
			mapping_enabled = False
			
		#Update & draw planet & Sat sprites on screen
		planet_sprite.update()
		planet_sprite.draw(screen)
		sat_sprite.update()
		sat_sprite.draw(screen)
		
		#Display intro text for 15 secs
		if pg.time.get_ticks() <= 15000: #ms
			instruct_label(screen, intro_txt, COLOR[3], 145, 100)
			
		#Display Telemetry & Instructions
		box_label(screen, 'Dx', (70, 20, 75, 20), COLOR[0])
		box_label(screen, 'Dy', (150, 20, 80, 20), COLOR[0])
		box_label(screen, 'Altitude', (240, 20, 160, 20), COLOR[0])
		box_label(screen, 'Fuel', (410, 20, 160, 20), COLOR[0])
		box_label(screen, 'Eccentricity', (580, 20, 150, 20), COLOR[0])
		
		#Dx, Dy, Alt, Fuel, Eccen.
		box_label(screen, '{:.1f}'.format(sat.dx), (70, 50, 75, 20),\
		COLOR[0])
		box_label(screen, '{:.1f}'.format(sat.dy), (150, 50, 80, 20),\
		COLOR[0])
		
		#Alt value Red if above 120 miles
		if(sat.distance > 120):
			box_label \
			(screen, '{:.1f}'.format(sat.distance), (240, 50, 160, 20),\
			COLOR[2])
		else:
			box_label \
			(screen, '{:.1f}'.format(sat.distance), (240, 50, 160, 20),\
			COLOR[0])
		
		#If fuel remaining < 10% label Red
		if(sat.fuel < sat.fuel_thresh):
			box_label(screen, f'{sat.fuel}', (410, 50, 160, 20),\
			COLOR[2])
		else:
			box_label(screen, f'{sat.fuel}', (410, 50, 160, 20),\
			COLOR[0])
		
		#Ecc value label Red if >0.05
		if(eccentricity > 0.05 or sat.distance > 120):
			box_label \
			(screen, '{:.8f}'.format(eccentricity), (580, 50, 150, 20),\
			COLOR[2])
		else:
			box_label \
			(screen, '{:.8f}'.format(eccentricity), (580, 50, 150, 20),\
			COLOR[0])
		
		instruct_label(screen, instruct_text1, COLOR[3], 10, 575)
		instruct_label(screen, instruct_text2, COLOR[3], 575, 510)
		
		#Add terminator & border
		cast_shadow(screen)
		pg.draw.rect(screen, COLOR[0], (1, 1, 798, 643), 1)
		shadow_lock_controls(screen, sat)
		
		pg.display.flip() #blit to display
		
if __name__ == "__main__":
	main()
