import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import sys

pygame.init()

window_width, window_height = 1000, 800

pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)

glOrtho(0, window_width, 0, window_height, -1, 1)
glClearColor(0.15, 0.15, 0.15, 1)

menu_font = pygame.font.Font(None, 36)
game_over_sfx = pygame.mixer.Sound("game_over.mp3")
bite_sfx = pygame.mixer.Sound("bite.mp3")
ouch_sfx = pygame.mixer.Sound("ouch.mp3")

gold = (255, 215, 0, 255)
blue = (36, 128, 219, 255)

def reset_values():
  global snake_position, snake_segments, snake_direction, \
    food_position, food_spawned, food_segment, pause, point_counter, \
    game_over
  pause  = False
  game_over = False
  point_counter = 0
  snake_direction = random.sample([1,2,4], 1)[0]
  snake_position = [random.randint(40, window_width - 40)//20*20, random.randint(40, window_height - 80)//20*20]

  snake_segments = [[snake_position[0] - n * 10, snake_position[1]] for n in range(10)]
  food_segment = [False for _ in range(len(snake_segments))]
  food_position = [window_width / 2, window_height / 2]
  food_spawned = False


def draw_square(position, size = 10):
  glBegin(GL_QUADS)
  glVertex2f(position[0] - size, position[1] + size)
  glVertex2f(position[0] + size, position[1] + size)
  glVertex2f(position[0] + size, position[1] - size)
  glVertex2f(position[0] - size, position[1] - size)
  glEnd()


def draw_snake(snake_segments):
  global food_segment
  for i, segment in enumerate(snake_segments):
    glColor3f(128/255, 219/255, 36/255)
    if not food_segment[i]:
      draw_square(segment)
    else:
      draw_square(segment, 12)


def draw_food(food_position):
  glColor3f(219/255, 36/255, 128/255)
  draw_square(food_position)


def draw_border():
  border_thickness = 10
  glColor3f(36/255, 128/255, 219/255)
  glBegin(GL_QUADS)

  glVertex2f(0, 0)
  glVertex2f(window_width, 0)
  glVertex2f(window_width, border_thickness)
  glVertex2f(0, border_thickness)

  glVertex2f(0, 0)
  glVertex2f(border_thickness, 0)
  glVertex2f(border_thickness, window_height)
  glVertex2f(0, window_height)

  glVertex2f(0, window_height - border_thickness)
  glVertex2f(window_width, window_height - border_thickness)
  glVertex2f(window_width, window_height)
  glVertex2f(0, window_height)

  glVertex2f(window_width - border_thickness, 0)
  glVertex2f(window_width, 0)
  glVertex2f(window_width, window_height)
  glVertex2f(window_width - border_thickness, window_height)

  glEnd()


def draw_text(text, position, color = (128, 218, 36, 255), y = window_width / 2 - 85):
  textSurface = menu_font.render(text, True, (0.75, 0.75, 0.75, 255), color)
  textData = pygame.image.tostring(textSurface, "RGBA", True)
  glWindowPos2d(y, position)
  glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def start_menu():
  while True:
    global point_counter, gold

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    draw_text("Snake Game", 700)
    draw_text("Select Difficulty:", 500)
    draw_text("1. Easy", 400)
    draw_text("2. Medium", 350)
    draw_text("3. Hard", 300)
    draw_text("4. Expert", 250)
    draw_text("5. Master", 200)
    draw_text("ESC. QUIT", 100)

    if game_over:
      draw_text("Game over!", 650, (255, 0, 0, 255))

    if point_counter != 0:
      draw_text(f"Your store: {point_counter} ", 600, gold)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          return 10
        elif event.key == pygame.K_2:
          return 20
        elif event.key == pygame.K_3:
          return 30
        elif event.key == pygame.K_4:
          return 40
        elif event.key == pygame.K_5:
          return 60
        elif event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()

    pygame.display.flip()
    pygame.time.Clock().tick(10)

def check_food_collision(position, segments):
  for segment in segments:
    if (
      segment[0] + 10 >= position[0] 
      and segment[0] - 15 <= position[0]
      and segment[1] + 15 >= position[1] 
      and segment[1] - 15 <= position[1]
      ):
      return True
  return False

def check_collision(position, segments):
  for segment in segments:
    if (
      segment[0] + 10 > position[0] 
      and segment[0] - 10 < position[0]
      and segment[1] + 10 > position[1] 
      and segment[1] - 10 < position[1]
      ):
      return True
  return False

def generate_food_position(segments):
  while True:
    new_food_position = [random.randint(40, window_width - 40)//20*20, random.randint(40, window_height - 80)//20*20]
    if not check_food_collision(new_food_position, segments):
      return new_food_position

def game():
  global snake_speed, snake_position, snake_segments, snake_direction, \
    food_position, food_spawned, food_segment, pause, point_counter, \
    game_over, gold, blue

  reset_values()

  snake_speed = start_menu()

  while True:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          pause = False
        elif event.key == pygame.K_ESCAPE:
          game_over = True
    
    while not pause and not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP and not snake_direction == 4:
            snake_direction = 2
          elif event.key == pygame.K_DOWN and not snake_direction == 2:
            snake_direction = 4
          elif event.key == pygame.K_LEFT and not snake_direction == 1:
            snake_direction = 3
          elif event.key == pygame.K_RIGHT and not snake_direction == 3:
            snake_direction = 1
          elif event.key == pygame.K_SPACE:
            pause = True
          elif event.key == pygame.K_ESCAPE:
            game_over = True

      if snake_direction == 1:
        snake_position[0] += 10
      elif snake_direction == 2:
        snake_position[1] += 10
      elif snake_direction == 3:
        snake_position[0] -= 10
      elif snake_direction == 4:
        snake_position[1] -= 10

      if check_food_collision(food_position, [snake_position]):
        point_counter += snake_speed
        food_spawned = False
        food_segment.insert(0, True)
        bite_sfx.play()
      else:
        snake_segments.pop()
        food_segment.pop()

      food_segment.insert(0, False)
      snake_segments.insert(0, list(snake_position))

      if not food_spawned:
        food_position = generate_food_position(snake_segments)
        food_spawned = True

      if check_collision(snake_position, snake_segments[1:]):
        game_over = True
        bite_sfx.play()
        ouch_sfx.play()

      if (
        snake_position[0] <= 20
        or snake_position[0] >= window_width - 20
        or snake_position[1] <= 20
        or snake_position[1] >= window_height - 20
      ):
        game_over = True
        game_over_sfx.play()

      glClear(GL_COLOR_BUFFER_BIT)
      draw_border()
      draw_snake(snake_segments)
      draw_food(food_position)
      draw_text(f'Your score: {point_counter} ', 750, gold, 700)
      pygame.display.flip()
      pygame.time.Clock().tick(snake_speed)
    
    draw_border()
    draw_snake(snake_segments)
    draw_food(food_position)
    draw_text(f'Your score: {point_counter} ', 750, gold, 700)
    if pause:
      draw_text(' ***Pause*** ', 500, blue)

    pygame.display.flip()
    pygame.time.Clock().tick(10)
    
    if game_over:
      snake_speed = start_menu()
      reset_values()

game()
