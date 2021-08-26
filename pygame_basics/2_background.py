import pygame

pygame.init()  # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480  # 가로크기
screen_height = 640  # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")  # 게임 이름

# 배경 이미지 불러오기
background = pygame.image.load(
    "/Users/pup-paw/Desktop/study/Python/python-gameProgramming/background.png")

# 이벤트 루프 (이벤트 루프가 있어야 창이 꺼지지 않음)
running = True  # 게임이 진행중인가?
while running:
    for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:  # 창을 닫히는 이벤트가 발생하였는가?
            running = False  # 게임이 진행중이 아님

    # screen.fill((225, 225, 255)) # rgb 값으로 배경 색 채우기
    screen.blit(background, (0, 0))  # 배경 그리기

    pygame.display.update()  # 게임화면을 다시 그리기 (계속 업데이트 필요)

# pygame 종료
pygame.quit()
