import pygame, sys
from math import *
pygame.init()

screen = pygame.display.set_mode([800,600])
screen.fill([0, 0, 0])
ground  = 540   #Definição do pouso
y = 540
start = 90      
clock = pygame.time.Clock()
ship_mass = 5000.0
fuel = 5000.0 #Define a quantidade total de combustível da nave
fps = 30 #Define como 30 os frames por segundo que serão exibidos
delta_v = 0 #Define a variação de velocidade inicial, no caso 0


x_loc = 20
y_loc = 40  

x_offset = 40    
y_offset = -108  

x_speed = 2000.0   
y_speed = -800.0


x_velocity = x_speed / (10.0 * fps)  # Deslocamento da nave em m/s
y_velocity = y_speed / (10.0 * fps)

gravity = 1.5
thrust = 0

scale = 10   
throttle_down = False
left_down = False
right_down = False
#held_down = False
count = 0
x_pos = 0
y_pos = 0

#Classe que define as propriedades da nave, como seu Sprite, sua posição, seu eixo e centro de equilibrio.
class ShipClass(pygame.sprite.Sprite):
  def __init__(self, image_file, position): 

      pygame.sprite.Sprite.__init__(self)
      self.imageMaster = pygame.image.load(image_file)
      self.image = self.imageMaster
      self.rect = self.image.get_rect()
      self.position = position
      self.rect.centerx, self.rect.centery = self.position
      self.angle = 0

#Classe de define as atualizações de referentes a posicionamento
  def update(self):
      self.rect.centerx, self.rect.centery = self.position
      oldCenter = self.rect.center
      self.image = pygame.transform.rotate(self.imageMaster, self.angle)
      self.rect = self.image.get_rect()
      self.rect.center = oldCenter

#Calculo da posição, movimentação, aceleração e combustível
def calculate_velocity():
  global ship, thrust, fuel, x_velocity, y_velocity, x_loc, y_loc
  global tot_velocity, scale, x_pos, y_pos, x_speed, y_speed

  delta_t = 1/fps

  #Cálculo do empuxo gerado de acordo com o pressionar da barra de espaço
  if throttle_down:
      thrust = thrust + 100
      if thrust > 1000:
          thrust = 1000
  else:
      if thrust > 0:
          thrust = thrust - 200
          if thrust < 0:
              thrust = 0
  fuel -= thrust /(10 * fps)  # Cálculo do uso do combustível
  if fuel < 0:
    fuel = 0.0
  if fuel < 0.1:
    thrust = 0.0
  ythrust = thrust * cos(ship.angle*(pi/180)) #Deslocamento
  xthrust = thrust * sin(ship.angle*(pi/180))
  y_delta_v = delta_t * (-gravity + 50 * ythrust / (ship_mass + fuel)) #Variação de velocidade no eixo Y
  y_velocity = y_velocity + y_delta_v
  x_delta_v = delta_t * (-50 * xthrust/(ship_mass + fuel)) #Variação de velocidade no eixo X
  x_velocity = x_velocity + x_delta_v
  x_speed = x_velocity * 10.0/fps   #Velocidade em pixels por frame, em física seria m/s
  y_speed = y_velocity * 10.0/fps
  y_loc = y_loc + y_velocity/fps  
  x_loc = x_loc - x_velocity/fps
  tot_velocity = sqrt(x_velocity**2 + y_velocity**2) #Calc da velocidade total de acordo com os eixos x e y
  ship.position[0] = x_pos = screen.get_width()/2 - (scale * x_loc) + x_offset
  ship.position[1] = y_pos = screen.get_height() - (scale * y_loc) + y_offset

  if right_down:
      ship.angle = ship.angle - 2
  if left_down:
      ship.angle = ship.angle + 2
  ship.update()


ship = ShipClass('lunarlander.png', [500, 230]) #Nave

# Inicio do game loop

while True:
  clock.tick(30)
  fps = clock.get_fps()
  if fps < 1:
       fps = 30
  count += 1
  if y_loc > 0.01:
      calculate_velocity()
      screen.fill([0, 0, 0])
      screen.blit(ship.image, ship.rect)
      pygame.display.flip()


#Eventos do teclado
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          sys.exit()
      elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
              throttle_down = True
          if event.key == pygame.K_RIGHT:
              right_down = True
          if event.key == pygame.K_LEFT:
              left_down = True
      elif event.type == pygame.KEYUP:
          if event.key == pygame.K_SPACE:
              throttle_down = False
          if event.key == pygame.K_RIGHT:
              right_down = False
          if event.key == pygame.K_LEFT:
              left_down = False
