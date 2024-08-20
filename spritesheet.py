import pygame

class ParticleStar:
    def __init__(self, profile):
        self.profile = pygame.image.load(profile)
        self.confetti_list = []
        self.max_confetti = 12
        self.confetti_speed = 1
        self.effect_active = False
        self.effect_start_time = 0
        self.effect_duration = 2000  # 2 saniye, milisaniye cinsinden

    def add_confetti(self, x, y):
        if len(self.confetti_list) >= self.max_confetti:
            self.confetti_list.pop(0)
        confetti_rect = self.profile.get_rect(center=(x, y))
        self.confetti_list.append(confetti_rect)

    def move_confetti(self):
        for rect in self.confetti_list:
            rect.y -= self.confetti_speed
            if rect.bottom < 0:
                self.confetti_list.remove(rect)

    def draw_confetti(self, screen):
        for rect in self.confetti_list:
            screen.blit(self.profile, rect)

    def trigger_confetti_effect(self):
        self.effect_active = True
        self.effect_start_time = pygame.time.get_ticks()  # Efekti başlatma zamanını kaydet

    def update(self):
        # Efektin süresini kontrol et
        if self.effect_active and (pygame.time.get_ticks() - self.effect_start_time) > self.effect_duration:
            self.effect_active = False
            self.confetti_list.clear()  # Listeyi temizle
