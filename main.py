import numpy as np
import pygame, sys
from numpy import dtype

pygame.init()

# Các thông số màn hình và đối tượng
WIDTH, HEIGHT = 432, 768
CLOUD_RADIUS = 24
TRAN_RADIUS = 24
DIST_C_T = (HEIGHT - 24) // 2
CLOUD_POS = np.array([WIDTH / 2 - CLOUD_RADIUS, HEIGHT - 672], dtype = np.float64)
CLOUD_VEL = [0,0]
TRAN_POS = np.array([WIDTH / 2 - TRAN_RADIUS, HEIGHT - 48], dtype = np.float64)
CENTER = np.array([WIDTH // 2 - TRAN_RADIUS, HEIGHT // 2 - CLOUD_RADIUS], dtype = np.float64)
# Hệ số ma sát
FRICTION = 0.8
GRAVITY_CLOUD = 0.2
GRAVITY_TRAN = 0.2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
BLACK = (0, 0, 0)
tran_movement = 0

# Load hình ảnh
tran_surface = pygame.image.load("assests/car.png").convert_alpha()
tran_surface = pygame.transform.scale(tran_surface, (48,48))  # specify new size
trans_rect = tran_surface.get_rect(center = (216 - 24, 768 - 48))
cloudy_surface = pygame.image.load("assests/cloudy.png").convert_alpha()
cloudy_surface = pygame.transform.scale(cloudy_surface, (48,48))  # specify new size

# Hàm vẽ đám mây
def draw_cloud():
    screen.blit(cloudy_surface, (CLOUD_POS[0], CLOUD_POS[1]))

# Hàm vẽ xe
def draw_tran(tran):
    new_tran = pygame.transform.rotozoom(tran, -tran_movement * 3, 1)
    return new_tran

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tran_movement  = -7  # Tăng vận tốc đi về bên trái
            elif event.key == pygame.K_RIGHT:
                tran_movement = 7  # Tăng vận tốc đi về bên phải

    # Cập nhật chuyển động của xe
    rotated_tran = draw_tran(tran_surface)
    trans_rect.x += tran_movement

    # Giảm dần vận tốc khi không có phím nào được nhấn
    tran_movement *= 0.9  # Hệ số giảm tốc có thể điều chỉnh
    # Giới hạn vị trí của xe trong khung
    # ... (giới hạn vị trí của xe như ban đầu)

    # Cập nhật chuyển động của đám mây
    CLOUD_VEL[1] += GRAVITY_CLOUD
    CLOUD_POS += CLOUD_VEL

    # Kiểm tra va chạm với khung và áp dụng ma sát
    if CLOUD_POS[0] < 0:
        CLOUD_POS[0] = 0
        CLOUD_VEL[0] *= -FRICTION
    elif CLOUD_POS[0] + CLOUD_RADIUS > WIDTH:
        CLOUD_POS[0] = WIDTH - CLOUD_RADIUS
        CLOUD_VEL[0] *= -FRICTION
    if CLOUD_POS[1] < 0:
        CLOUD_POS[1] = 0
        CLOUD_VEL[1] *= -FRICTION
    elif CLOUD_POS[1] + CLOUD_RADIUS > HEIGHT:
        CLOUD_POS[1] = HEIGHT - CLOUD_RADIUS
        CLOUD_VEL[1] *= -FRICTION

    # Kiểm tra va chạm với xe và xử lý va chạm
    if trans_rect.colliderect(cloudy_surface.get_rect(topleft=(CLOUD_POS[0], CLOUD_POS[1]))):
        # Collision detected, handle cloud deviation
        collision_vector = CENTER - CLOUD_POS
        collision_unit_vector = collision_vector / np.linalg.norm(collision_vector)

        # Áp dụng lực đẩy để làm lệch hướng đám mây
        DEFLECTION_FORCE = 2  # Điều chỉnh lực đẩy để thay đổi mức độ lệch hướng
        cloud_deflection = DEFLECTION_FORCE * collision_unit_vector
        CLOUD_VEL += cloud_deflection

    # Vẽ màn hình
    screen.fill(BLACK)
    draw_cloud()
    screen.blit(rotated_tran, trans_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()