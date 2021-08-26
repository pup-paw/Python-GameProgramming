import os
import pygame

# --------- 필수 환경 설정
#초기화 (필수)
pygame.init()

# 화면 크기 설정 (필수)
screen_width = 640  # 가로
screen_height = 480  # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 (필수)
pygame.display.set_caption("PANGPANG Game by DINGDONG")  # 게임이름

#FPS (필수)
clock = pygame.time.Clock()

# --------- 사용자 설정
# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 높이위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_heigh = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_heigh - stage_height

# 좌표이동 (키보드 이동 연결)
character_to_x = 0
character_speed = 7

# 무기만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_with = weapon_size[0]  # 무기가 날아가는 위치와 길이를 파악하기 위해

# 무기는 여러발 동시에 가능함
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 최초 속도 설정
# ball_images 의 index 0,1,2,3 에 해당함 / 마이너스로 해야 위로 줄어드는 속도로 반영되므로
ball_speed_y = [-18, -15, -12, -9]

# 공 정보
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x": 50,  # 공의 x 좌표
    "pos_y": 50,  # 공의 y 좌표
    "img_idx": 0,  # 공의 이미지 인덱스
    "to_x": 3,  # 공의 x축 이동 방향 (-3이면 왼쪽, 3이면 오른쪽)
    "to_y": -6,  # 공의 y축 이동 방향 (-6이면 위, 6이면 아래)
    "init_spd_y": ball_speed_y[0]  # y 최초의 속도
})

# 사라질 무기, 공정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_tick = pygame.time.get_ticks()  # 시직 시간 정의

# 게임 종료 메시지 : 성공, 시간종료, 게임오버
#"Time Out"
#"Mission Complete"
game_result = "Game Over"

# 총 시간
# 시직 시간정보
# 이벤트 루프
running = True  # 게임 진행에 대한 불리언, 종료되지 않도록 기본 설정 되어 있음 (필수)
while running:
    dt = clock.tick(30)  # 게임화면의 초당 프레임수를 설정
    # ------------ 실제 이벤트 영역 설정
    for event in pygame.event.get():  # 이벤트 발생여부 체크)
        if event.type == pygame.QUIT:  # 종료 x 버튼을 누르면 끝나도록 되어 있음
            running = False  # 게임 진행중이 아님을 확인

    # 키보드 동작 반영
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 왼쪽으로 이동
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  # 오른쪽으로 이동
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기발사
                weapon_x_pos = character_x_pos + character_width/2 - \
                    weapon_with/2  # 캐릭터 위치에서 무기 반만큼 이동시켜서 캐릭터 가운데에서 발사되도록
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 프레임 내에 위치 설정
    character_x_pos += character_to_x

    # 캐릭터 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width

    # 무기 위치를 위로 조정
    weapons = [[w[0], w[1]-weapon_speed] for w in weapons]  # 위로 올라가는것 처럼 보이기

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]]
               for w in weapons if w[1] > 0]  # 천정에 안 닿은거만 남겨둠, y좌표가 0보다 큰 경우

    # 공 위치 정의 (enumerate로 인덱스값을 정의해서, 딕셔너리안에서 값을 찾아옴)
    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공이 가로벽에 부딪히면 반대로 튕기도록 함
        if ball_x_pos < 0 or ball_x_pos > screen_width-ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 공이 가로벽에 부딪히면 반대로 튕기도록 함
        # 스테이지에 튕겨서 올라가는 처리
        if ball_y_pos >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        # 속도의 감속 (시작값이 마이너스 였기 때문에 증가가 크게 증가하진 않음)
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 충돌 처리 collision
    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_x_pos
        ball_rect.top = ball_y_pos

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            # 무기와 공과 충돌 처리 (공도 무기도 사라짐)
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx  # 해당 무기를 없애기 위한 값 설정
                ball_to_remove = ball_idx  # 해당 공 없애기 위한 값 설정

                # 볼 사이즈별로 분리 (큰 공이 아니면 다음 단계 공으로 나눠주기)
                if ball_img_idx < 3:

                    # 현재 볼 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보 (다음공이라 인덱스에 +1)
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[0]

                    # 왼쪽으로 튕겨나가는 1단계 작은공
                    balls.append({
                        # 공의 x 좌표
                        "pos_x": ball_x_pos + ball_width/2 - (small_ball_width/2),
                        # 공의 y 좌표
                        "pos_y": ball_y_pos + ball_height/2 - (small_ball_height/2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -3,  # 공의 x축 이동 방향 (-3이면 왼쪽, 3이면 오른쪽)
                        "to_y": -6,  # 공의 y축 이동 방향 (-6이면 위, 6이면 아래)
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초의 속도
                    })
                    # 오른쪽으로 튕겨나가는 1단게 작은공
                    balls.append({
                        # 공의 x 좌표
                        "pos_x": ball_x_pos + ball_width/2 - (small_ball_width/2),
                        # 공의 y 좌표
                        "pos_y": ball_y_pos + ball_height/2 - (small_ball_height/2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 3,  # 공의 x축 이동 방향 (-3이면 왼쪽, 3이면 오른쪽)
                        "to_y": -6,  # 공의 y축 이동 방향 (-6이면 위, 6이면 아래)
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초의 속도
                    })

                break
        else:  # 게임을 진행하되 내부에서 break 가 걸리면 else 조건이 실행됨
            continue
        break  # 안쪽 for 문에서 break 조건일때 실행

    # 충돌 된 공 혹은 무기 없애기 (닿은 공에 인덱스 값을 주고, 해당 인덱스 값에 해당 하는 리스트가 없어짐)
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앴을 경우 게임종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 화면 배경을 매번 업데이트 되어야함 (필수, 순서대로 노출)
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_x_pos = val["pos_x"]
        ball_y_pos = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_x_pos, ball_y_pos))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_tick)/1000  # ms에 대해 s로 전환
    timer = game_font.render("Time : {}".format(
        int(total_time-elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간이 초과되었을 경우,
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# 게임오버 메세지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 잠시 대기 (2초)
pygame.time.delay(2000)

# 이벤트 루프 종료/게임 종료 (필수)
pygame.quit()
