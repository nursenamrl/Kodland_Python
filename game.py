# Oyunun adi Knight's Road'dir
# Bu oyunu Kodland is basvurusu icin yazdim. -Nur Sena MERAL
# Kodlarin daha kolay anlasilmasi icin yorum satirlari ekledim.

#Oyunun genisilik ve yukseklik degerleri
WIDTH = 960
HEIGHT = 540

# Oyundaki zemin cizgisinin dikey konumu.
# Karakter ve kale bu yukseklige gore yerlestirilir.
GROUND_Y = 475

# Oyuncunun kazanmak icin kat etmesi gereken toplam yol.
JOURNEY_DISTANCE = 3600 #Oyunu kazanmak icin gidilmesi gereken mesafe
# Kahraman bu noktaya kadar ekranda saga ilerler.
# Bu noktadan sonra yol hissi daha cok arka plan kaymasi ile verilir.
CAMERA_LOCK_X = 360
# Arka planin, asil yolculuga gore daha yavas kaymasini saglar.
BACKGROUND_SCROLL_FACTOR = 0.35 #Arka plan resminin kayma orani

# Ses seviyeleri 
BACKGROUND_MUSIC_VOLUME = 0.25
DEAD_SOUND_VOLUME = 1.0
KILL_SOUND_VOLUME = 1.0
WIN_SOUND_VOLUME = 1.0

# Kullanilan arka plan ve kale gorsellerinin adlari.
BACKGROUND_IMAGE_NAME = "background_scaled"
CASTLE_IMAGE_NAME = "castle_scaled"
# Kale cizilirken zemine biraz daha dogru otursun diye ek kaydirma.
CASTLE_BOTTOM_OFFSET = 18
# Kalenin ekrandaki hedef konumu.
CASTLE_SCREEN_X = WIDTH - 180
# Kahramanin kapinin biraz onunde degil, daha yakininda durmasi icin ofset.
CASTLE_DOOR_OFFSET_X = -88
KNIGHT_CASTLE_TARGET_X = (
    CASTLE_SCREEN_X + CASTLE_DOOR_OFFSET_X
)
# Kale hemen gorunmez.
# Oyuncu yeterince yaklastikca saga dogru ekrana girer.
CASTLE_APPROACH_DISTANCE = max(
    0,
    KNIGHT_CASTLE_TARGET_X - CAMERA_LOCK_X,
)

# Ana menu ayarlari 
# Oyunun o an hangi ekranda oldugunu tutar.
game_state = "main_menu"
# Tum sesler icin ana acma kapama durumu.
sound_enabled = True
# Muzik daha once basladi mi diye takip edilir.
background_music_playing = False

# Dusman uretme sayaci.
spawn_timer = 0
spawn_interval = 300 # Goblinlerin olusmasinin zaman araligi
maximum_active_goblins = 2 # Aynı anda maks 2 goblin ekranda olabilir

# Oyun boyunca ilerleme ve skor bilgileri burada tutulur.
journey_progress = 0
distance_remaining = JOURNEY_DISTANCE
goblins_defeated = 0

# Ana menu butonlarinin tiklanabilir alanlari.
start_button = Rect(330, 220, 300, 60)
sound_button = Rect(330, 300, 300, 60)
exit_button = Rect(330, 380, 300, 60)

# Kale görselini koyar ve konumunu belirler
castle_actor = Actor(
    CASTLE_IMAGE_NAME,
    midbottom=(
        CASTLE_SCREEN_X,
        GROUND_Y + CASTLE_BOTTOM_OFFSET,
    ),
)

# Arka plan muzigi ayarlari
def sync_background_music():
    # Ses aciksa muzik baslatilir.
    # Ses kapaliysa muzik durdurulur.
    global background_music_playing

    if sound_enabled:
        if not background_music_playing:
            sounds.backsound.set_volume(
                BACKGROUND_MUSIC_VOLUME
            )
            sounds.backsound.play(-1)
            background_music_playing = True
    elif background_music_playing:
        sounds.backsound.stop()
        background_music_playing = False


class Knight:
    def __init__(self):
        # Kahramanin ekrandaki gorsel nesnesi.
        self.actor = Actor(
            "knight/idle_right_1",
            (200, 435),
        )

        # Temel hareket degerleri.
        self.speed = 5
        self.direction = "right"
        # Bu karede alinan yol miktari.
        self.journey_step = 0

        # Karakterin o anki durumu.
        self.is_moving = False
        self.is_attacking = False
        self.is_dead = False
        self.death_finished = False
        # Bir saldirida birden fazla vurmayi engeller.
        self.attack_has_hit = False

        # Butun animasyonlar ayni sayac mantigi ile ilerler.
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = 6

        # Saga bakarken bekleme kareleri.
        self.idle_right_frames = [
            "knight/idle_right_1",
            "knight/idle_right_2",
            "knight/idle_right_3",
        ]

        # Sola bakarken bekleme kareleri.
        self.idle_left_frames = [
            "knight/idle_left_1",
            "knight/idle_left_2",
            "knight/idle_left_3",
        ]

        # Saga kosma kareleri.
        self.run_right_frames = [
            "knight/run_right_1",
            "knight/run_right_2",
            "knight/run_right_3",
            "knight/run_right_4",
            "knight/run_right_5",
        ]

        # Sola kosma kareleri.
        self.run_left_frames = [
            "knight/run_left_1",
            "knight/run_left_2",
            "knight/run_left_3",
            "knight/run_left_4",
            "knight/run_left_5",
        ]

        # Saga saldiri kareleri.
        self.attack_right_frames = [
            "knight/attack_right_1",
            "knight/attack_right_2",
            "knight/attack_right_3",
            "knight/attack_right_4",
            "knight/attack_right_5",
            "knight/attack_right_6",
        ]

        # Sola saldiri kareleri.
        self.attack_left_frames = [
            "knight/attack_left_1",
            "knight/attack_left_2",
            "knight/attack_left_3",
            "knight/attack_left_4",
            "knight/attack_left_5",
            "knight/attack_left_6",
        ]

        # Olme animasyonu kareleri.
        self.die_frames = [
            "knight/die_1",
            "knight/die_2",
            "knight/die_3",
            "knight/die_4",
        ]

    def reset(self):
        # Yeni oyun baslarken karakteri ilk haline getirir.
        self.actor.pos = (200, 435)
        self.actor.image = "knight/idle_right_1"

        self.direction = "right"
        self.journey_step = 0

        self.is_moving = False
        self.is_attacking = False
        self.is_dead = False
        self.death_finished = False
        self.attack_has_hit = False

        self.animation_frame = 0
        self.animation_timer = 0

    def move(self):
        # Hareket hem ekrandaki konumu hem de toplam ilerlemeyi etkiler.
        global journey_progress

        self.is_moving = False
        self.journey_step = 0

        # Karakter saldirirken veya oluyken hareket edemez.
        if self.is_attacking or self.is_dead:
            return

        # Ekranin solundan disari cikmasin diye sinir koyulur.
        left_limit = self.actor.width / 2

        if keyboard.left or keyboard.a:
            self.direction = "left"

            # Geri gitmek icin once biraz yol alinmis olmasi gerekir.
            if journey_progress > 0:
                self.is_moving = True
                self.journey_step = -min(
                    self.speed,
                    journey_progress,
                )

                # Sola giderken karakter gercekten sola kayar.
                self.actor.x -= self.speed

                if self.actor.x < left_limit:
                    self.actor.x = left_limit

        elif keyboard.right or keyboard.d:
            self.direction = "right"

            # Hedefe varilmadiysa saga ilerlenebilir.
            if journey_progress < JOURNEY_DISTANCE:
                self.is_moving = True

                # Kalan yola gore bu karede ne kadar ilerlenebilecegi hesaplanir.
                remaining_journey = (
                    JOURNEY_DISTANCE - journey_progress
                )

                self.journey_step = min(
                    self.speed,
                    remaining_journey,
                )

                # Kale yakininda karakter yeniden fiziksel olarak kaleye dogru yurur.
                if (
                    distance_remaining
                    <= CASTLE_APPROACH_DISTANCE
                ):
                    target_x = KNIGHT_CASTLE_TARGET_X

                    if self.actor.x < target_x:
                        self.actor.x += self.speed

                        if self.actor.x > target_x:
                            self.actor.x = target_x

                # Normal durumda karakter belli bir noktaya kadar saga gider.
                # Sonra ekran sanki ilerliyormus hissi verir.
                elif self.actor.x < CAMERA_LOCK_X:
                    self.actor.x += self.speed

                    if self.actor.x > CAMERA_LOCK_X:
                        self.actor.x = CAMERA_LOCK_X

    def start_attack(self):
        # Yeni saldiri sadece karakter uygunsa baslatilir.
        if self.is_attacking or self.is_dead:
            return

        self.is_attacking = True
        self.is_moving = False
        self.journey_step = 0
        self.attack_has_hit = False

        self.animation_frame = 0
        self.animation_timer = 0
        self.actor.image = self.get_attack_frames()[0]

    def start_death(self):
        # Olme durumu bir kere baslatilir.
        global sound_enabled

        if self.is_dead:
            return

        self.is_dead = True
        self.is_attacking = False
        self.is_moving = False
        self.journey_step = 0
        self.death_finished = False

        self.animation_frame = 0
        self.animation_timer = 0
        self.actor.image = self.die_frames[0]

        if sound_enabled:
            sounds.dead.set_volume(
                DEAD_SOUND_VOLUME
            )
            sounds.dead.play()

    def get_attack_frames(self):
        # Karakterin baktigi yone gore saldiri karelerini verir.
        if self.direction == "left":
            return self.attack_left_frames

        return self.attack_right_frames

    def get_normal_frames(self):
        # Hareket varsa kosma, yoksa bekleme kareleri secilir.
        if self.is_moving:
            if self.direction == "left":
                return self.run_left_frames

            return self.run_right_frames

        if self.direction == "left":
            return self.idle_left_frames

        return self.idle_right_frames

    def get_body_hitbox(self):
        # Carpisma alani gorselden biraz daha dar tutulur.
        return Rect(
            self.actor.x - 20,
            self.actor.y - 34,
            40,
            68,
        )

    def get_attack_area(self):
        # Kilicin vurabilecegi alan yonune gore hesaplanir.
        attack_width = 58
        attack_height = 65
        attack_y = self.actor.y - attack_height / 2

        if self.direction == "right":
            attack_x = self.actor.x + 18
        else:
            attack_x = (
                self.actor.x
                - attack_width
                - 18
            )

        return Rect(
            attack_x,
            attack_y,
            attack_width,
            attack_height,
        )

    def can_damage_enemy(self):
        # Hasar sadece saldirinin uygun aninda ve bir kez verilir.
        return (
            self.is_attacking
            and not self.attack_has_hit
            and 2 <= self.animation_frame <= 4
        )

    def update_attack_animation(self):
        # Saldiri animasyonu biterse karakter normal duruma doner.
        attack_frames = self.get_attack_frames()

        self.animation_timer += 1

        if self.animation_timer < self.animation_delay:
            return

        self.animation_timer = 0
        self.animation_frame += 1

        if self.animation_frame >= len(attack_frames):
            self.is_attacking = False
            self.attack_has_hit = False
            self.animation_frame = 0
            self.actor.image = self.get_normal_frames()[0]
            return

        self.actor.image = attack_frames[self.animation_frame]

    def update_normal_animation(self):
        # Kosma ve bekleme animasyonu dongu halinde oynar.
        current_frames = self.get_normal_frames()

        self.animation_timer += 1

        if self.animation_timer < self.animation_delay:
            return

        self.animation_timer = 0
        self.animation_frame += 1

        if self.animation_frame >= len(current_frames):
            self.animation_frame = 0

        self.actor.image = current_frames[self.animation_frame]

    def update_death_animation(self):
        # Olme animasyonu son karede kalir.
        self.animation_timer += 1

        if self.animation_timer < self.animation_delay:
            return

        self.animation_timer = 0
        self.animation_frame += 1

        if self.animation_frame >= len(self.die_frames):
            self.animation_frame = len(self.die_frames) - 1
            self.death_finished = True
            return

        self.actor.image = self.die_frames[self.animation_frame]

    def update_animation(self):
        # Duruma gore dogru animasyon guncellenir.
        if self.is_dead:
            self.update_death_animation()
        elif self.is_attacking:
            self.update_attack_animation()
        else:
            self.update_normal_animation()

    def update(self):
        # Her karede once hareket sonra animasyon guncellenir.
        self.move()
        self.update_animation()

    def draw(self):
        # Karakteri ekrana cizer.
        self.actor.draw()


class Goblin:
    def __init__(self, x_position):
        # Dusman her zaman ekranin saginda dogar.
        self.actor = Actor(
            "goblin/run_1",
            (x_position, 440),
        )

        # Goblinin ilerleme hizi.
        self.speed = 2

        # Yasayip yasamadigi ve animasyonun bitip bitmedigi tutulur.
        self.is_dead = False
        self.death_finished = False

        # Goblin animasyon sayaclari.
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = 6

        # Goblin kosma kareleri.
        self.run_frames = [
            "goblin/run_1",
            "goblin/run_2",
            "goblin/run_3",
            "goblin/run_4",
            "goblin/run_5",
            "goblin/run_6",
            "goblin/run_7",
        ]

        # Goblin olme kareleri.
        self.die_frames = [
            "goblin/die_1",
            "goblin/die_2",
            "goblin/die_3",
            "goblin/die_4",
            "goblin/die_5",
            "goblin/die_6",
        ]

    def start_death(self):
        # Goblin oldugunde olme animasyonu ve ses baslar.
        if self.is_dead:
            return

        self.is_dead = True
        self.animation_frame = 0
        self.animation_timer = 0
        self.actor.image = self.die_frames[0]

        if sound_enabled:
            sounds.kill.set_volume(
                KILL_SOUND_VOLUME
            )
            sounds.kill.play()

    def move(self):
        # Canli goblinler surekli sola yurur.
        if not self.is_dead:
            self.actor.x -= self.speed

    def get_body_hitbox(self):
        # Carpisma alani gorselden biraz daha kucuktur.
        return Rect(
            self.actor.x - 16,
            self.actor.y - 28,
            32,
            56,
        )

    def update_run_animation(self):
        # Kosma kareleri sirayla oynatilir.
        self.animation_timer += 1

        if self.animation_timer < self.animation_delay:
            return

        self.animation_timer = 0
        self.animation_frame += 1

        if self.animation_frame >= len(self.run_frames):
            self.animation_frame = 0

        self.actor.image = self.run_frames[self.animation_frame]

    def update_death_animation(self):
        # Olme animasyonu bitince goblin silinmeye hazir olur.
        self.animation_timer += 1

        if self.animation_timer < self.animation_delay:
            return

        self.animation_timer = 0
        self.animation_frame += 1

        if self.animation_frame >= len(self.die_frames):
            self.death_finished = True
            return

        self.actor.image = self.die_frames[self.animation_frame]

    def is_outside_screen(self):
        # Ekranin solundan tamamen cikti mi diye bakar.
        return self.actor.right < 0

    def update(self):
        # Goblinin hareketi ve animasyonu birlikte guncellenir.
        self.move()

        if self.is_dead:
            self.update_death_animation()
        else:
            self.update_run_animation()

    def draw(self):
            # Goblini ekrana cizer.
        self.actor.draw()


        # Oyunda tek bir kahraman ve bir goblin listesi kullanilir.
knight = Knight()
goblins = []


def reset_game():
            # Oyun yeniden baslatilirken her sey ilk haline cekilir.
    global spawn_timer
    global journey_progress
    global distance_remaining
    global goblins_defeated
    global goblins

    knight.reset()

    spawn_timer = 0
    journey_progress = 0
    distance_remaining = JOURNEY_DISTANCE
    goblins_defeated = 0

    goblins = [
        Goblin(WIDTH + 70),
    ]


def get_alive_goblin_count():
    # Sadece hayatta olan goblinlerin sayisini bulur.
    alive_count = 0

    for goblin in goblins:
        if not goblin.is_dead:
            alive_count += 1

    return alive_count


def spawn_goblins():
    # Uygun zaman gelince yeni goblin ekler.
    global spawn_timer

    # Ekranda yeterince goblin varsa yenisi gelmez.
    if get_alive_goblin_count() >= maximum_active_goblins:
        return

    spawn_timer += 1

    if spawn_timer < spawn_interval:
        return

    goblins.append(Goblin(WIDTH + 70))
    spawn_timer = 0


def update_journey():
    # Karakterin aldigi adim, toplam yolculuga eklenir.
    global journey_progress
    global distance_remaining
    global game_state

    # Karakter olduysa artik ilerleme degismez.
    if knight.is_dead:
        return

    journey_progress += knight.journey_step

    if journey_progress < 0:
        journey_progress = 0

    if journey_progress > JOURNEY_DISTANCE:
        journey_progress = JOURNEY_DISTANCE

    distance_remaining = (
        JOURNEY_DISTANCE - journey_progress
    )

    # Yol tamamlandiysa oyun kazanilir.
    if journey_progress >= JOURNEY_DISTANCE:
        journey_progress = JOURNEY_DISTANCE
        distance_remaining = 0

        if sound_enabled:
            sounds.win.set_volume(
                WIN_SOUND_VOLUME
            )
            sounds.win.play()

        game_state = "victory"


def check_sword_hits():
    # Kilic alanina giren ilk canli goblin vurulur.
    global goblins_defeated

    if not knight.can_damage_enemy():
        return

    attack_area = knight.get_attack_area()

    for goblin in goblins:
        if goblin.is_dead:
            continue

        if attack_area.colliderect(
            goblin.get_body_hitbox()
        ):
            goblin.start_death()
            knight.attack_has_hit = True
            goblins_defeated += 1
            return


def check_knight_collision():
    # Goblin oyuncuya dokunursa kaybetme sureci baslar.
    global game_state

    knight_hitbox = knight.get_body_hitbox()

    for goblin in goblins:
        if goblin.is_dead:
            continue

        if knight_hitbox.colliderect(
            goblin.get_body_hitbox()
        ):
            knight.start_death()
            game_state = "knight_dead"
            return


def remove_finished_goblins():
    # Olme animasyonu biten veya disari cikan goblinler silinir.
    for goblin in goblins[:]:
        if (
            goblin.death_finished
            or goblin.is_outside_screen()
        ):
            goblins.remove(goblin)


def draw():
    # O anki oyun durumuna gore hangi ekranin cizilecegi secilir.
    screen.clear()

    if game_state == "main_menu":
        draw_main_menu()

    elif game_state in ("playing", "knight_dead"):
        draw_game()

    elif game_state == "game_over":
        draw_game_over()

    elif game_state == "victory":
        draw_victory()


def draw_main_menu():
    # Ana menude arka plan, baslik ve butonlar cizilir.
    screen.blit(BACKGROUND_IMAGE_NAME, (0, 0))

    screen.draw.text(
        "KNIGHT'S ROAD",
        center=(WIDTH // 2, 120),
        fontsize=65,
        color="white",
    )

    screen.draw.filled_rect(
        start_button,
        "darkgreen",
    )
    screen.draw.rect(
        start_button,
        "white",
    )
    screen.draw.text(
        "START GAME",
        center=start_button.center,
        fontsize=35,
        color="white",
    )

    screen.draw.filled_rect(
        sound_button,
        "darkblue",
    )
    screen.draw.rect(
        sound_button,
        "white",
    )

    if sound_enabled:
        sound_text = "SOUND: ON"
    else:
        sound_text = "SOUND: OFF"

    screen.draw.text(
        sound_text,
        center=sound_button.center,
        fontsize=35,
        color="white",
    )

    screen.draw.filled_rect(
        exit_button,
        "darkred",
    )
    screen.draw.rect(
        exit_button,
        "white",
    )
    screen.draw.text(
        "EXIT",
        center=exit_button.center,
        fontsize=35,
        color="white",
    )


def draw_journey_progress():
    # Yolculuk yuzdesi hem cubuk hem yazi olarak gosterilir.
    progress_bar_x = 20
    progress_bar_y = 58
    progress_bar_width = 300
    progress_bar_height = 20

    progress_ratio = (
        journey_progress / JOURNEY_DISTANCE
    )

    completed_width = int(
        progress_bar_width * progress_ratio
    )

    progress_background = Rect(
        progress_bar_x,
        progress_bar_y,
        progress_bar_width,
        progress_bar_height,
    )

    progress_fill = Rect(
        progress_bar_x,
        progress_bar_y,
        completed_width,
        progress_bar_height,
    )

    screen.draw.filled_rect(
        progress_background,
        "darkgray",
    )

    if completed_width > 0:
        screen.draw.filled_rect(
            progress_fill,
            "green",
        )

    screen.draw.rect(
        progress_background,
        "white",
    )

    progress_percentage = int(
        progress_ratio * 100
    )

    screen.draw.text(
        f"CASTLE PROGRESS: {progress_percentage}%",
        topleft=(20, 84),
        fontsize=22,
        color="white",
    )


def draw_scrolling_background():
    # Arka plan iki kez cizilerek kesintisiz kayma etkisi verilir.
    background_width = images.background_scaled.get_width()
    scroll_offset = int(
        journey_progress * BACKGROUND_SCROLL_FACTOR
    ) % background_width

    screen.blit(
        BACKGROUND_IMAGE_NAME,
        (-scroll_offset, 0),
    )
    screen.blit(
        BACKGROUND_IMAGE_NAME,
        (background_width - scroll_offset, 0),
    )


def draw_castle():
    # Kale oyuncu yaklastikca gorunur hale gelir.
    castle_width = castle_actor.width

    if CASTLE_APPROACH_DISTANCE > 0:
        hidden_castle_x = (
            WIDTH + castle_width / 2
        )
        # Kalenin ne kadar ortaya cikacagi hesaplanir.
        visible_progress = 1 - min(
            distance_remaining,
            CASTLE_APPROACH_DISTANCE,
        ) / CASTLE_APPROACH_DISTANCE
        castle_screen_x = (
            hidden_castle_x
            + (CASTLE_SCREEN_X - hidden_castle_x)
            * visible_progress
        )
    else:
        castle_screen_x = CASTLE_SCREEN_X

    castle_actor.midbottom = (
        castle_screen_x,
        GROUND_Y + CASTLE_BOTTOM_OFFSET,
    )

    castle_actor.draw()


def draw_game():
    # Oyun ekrani burada parca parca cizilir.
    draw_scrolling_background()

    draw_castle()

    # Once kahraman sonra dusmanlar cizilir.
    knight.draw()

    for goblin in goblins:
        goblin.draw()

    screen.draw.text(
        f"DISTANCE TO CASTLE: {distance_remaining}",
        topleft=(20, 20),
        fontsize=26,
        color="white",
    )

    draw_journey_progress()

    screen.draw.text(
        f"GOBLINS DEFEATED: {goblins_defeated}",
        topright=(WIDTH - 20, 20),
        fontsize=24,
        color="white",
    )


def draw_game_over():
    # Kaybetme ekrani oyuncuya ne yapacagini soyler.
    screen.blit(BACKGROUND_IMAGE_NAME, (0, 0))

    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, 190),
        fontsize=75,
        color="red",
    )

    screen.draw.text(
        "PRESS ENTER TO RESTART",
        center=(WIDTH // 2, 290),
        fontsize=35,
        color="white",
    )

    screen.draw.text(
        "PRESS ESC TO RETURN TO MENU",
        center=(WIDTH // 2, 345),
        fontsize=27,
        color="white",
    )


def draw_victory():
    # Kazanma ekrani sonuc bilgisini gosterir.
    screen.blit(BACKGROUND_IMAGE_NAME, (0, 0))

    screen.draw.text(
        "VICTORY",
        center=(WIDTH // 2, 170),
        fontsize=75,
        color="gold",
    )

    screen.draw.text(
        "YOU REACHED THE CASTLE",
        center=(WIDTH // 2, 255),
        fontsize=35,
        color="white",
    )

    screen.draw.text(
        f"GOBLINS DEFEATED: {goblins_defeated}",
        center=(WIDTH // 2, 305),
        fontsize=27,
        color="white",
    )

    screen.draw.text(
        "PRESS ENTER TO PLAY AGAIN",
        center=(WIDTH // 2, 360),
        fontsize=28,
        color="white",
    )

    screen.draw.text(
        "PRESS ESC TO RETURN TO MENU",
        center=(WIDTH // 2, 405),
        fontsize=24,
        color="white",
    )


def update():
    # Oyunun ana mantik dongusu.
    # Her karede bu fonksiyon tekrar cagrilir.
    global game_state

    if game_state == "playing":
        # Once kahraman hareket eder ve animasyonu ilerler.
        knight.update()
        update_journey()

        # Oyun durumu degistiyse bu kare erken biter.
        if game_state != "playing":
            return

        # Sonra goblinler guncellenir.
        for goblin in goblins:
            goblin.update()

        # Hasar ve temas kontrolleri burada yapilir.
        check_sword_hits()
        check_knight_collision()

        if game_state != "playing":
            return

        # En sonda temizlik ve yeni goblin ekleme yapilir.
        remove_finished_goblins()
        spawn_goblins()

    elif game_state == "knight_dead":
        # Kahraman olduyse sadece olme animasyonu tamamlanir.
        knight.update_animation()

        if knight.death_finished:
            game_state = "game_over"


def on_key_down(key):
    # Klavye tuslari oyunun bulundugu ekrana gore farkli islenir.
    global game_state

    if game_state == "playing":
        # Bosluk tusu saldiri baslatir.
        if key == keys.SPACE:
            knight.start_attack()

        # ESC oyunu ana menuye dondurur.
        elif key == keys.ESCAPE:
            game_state = "main_menu"

    elif game_state in ("game_over", "victory"):
        # Oyun sonu ekranlarinda Enter yeniden baslatir.
        if key == keys.RETURN:
            reset_game()
            game_state = "playing"

        # ESC ana menuye geri goturur.
        elif key == keys.ESCAPE:
            game_state = "main_menu"


def on_mouse_down(pos):
    # Fare tiklari sadece ana menude kullanilir.
    global game_state
    global sound_enabled

    if game_state != "main_menu":
        return

    # Baslat butonu yeni oyun acilir.
    if start_button.collidepoint(pos):
        reset_game()
        game_state = "playing"

    # Ses butonu tum sesleri acip kapatir.
    elif sound_button.collidepoint(pos):
        sound_enabled = not sound_enabled
        sync_background_music()

    # Cikis butonu oyunu kapatir.
    elif exit_button.collidepoint(pos):
        quit()


# Dosya acildiginda muzik durumu hemen ayarlanir.
sync_background_music()