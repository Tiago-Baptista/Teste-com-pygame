import pygame
import os
pygame.font.init()
pygame.mixer.init()

LARGURA, ALTURA = 1000, 500
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Primeiro Jogo!')

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

BORDAS = pygame.Rect(LARGURA // 2 - 5, 0, 10, ALTURA)

BALA_HIT_SOM = pygame.mixer.Sound('Assets/hit_laser.wav')
TIRO_SOM = pygame.mixer.Sound('Assets/tiro_laser.wav')
SOM_VENCEDOR = pygame.mixer.Sound('Assets/game_over.wav')

VIDA_FONTE = pygame.font.SysFont('comicsans', 35)
VENCEDOR_FONTE = pygame.font.SysFont('comics', 100)

FPS = 60
VEL = 6
BALAS_VEL = 8
MAX_BALAS = 3

NAVE_LARGURA, NAVE_ALTURA = 60, 60

HIT_AMARELO = pygame.USEREVENT + 1
HIT_VERMELHO = pygame.USEREVENT + 2

IMAGEM_NAVE_AMARELA = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
NAVE_AMARELA = pygame.transform.rotate(pygame.transform.scale(IMAGEM_NAVE_AMARELA, (NAVE_LARGURA, NAVE_ALTURA)), 90)
IMAGEM_NAVE_VERMELHA = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
NAVE_VERMELHA = pygame.transform.rotate(pygame.transform.scale(IMAGEM_NAVE_VERMELHA, (NAVE_LARGURA, NAVE_ALTURA)), 270)
ESPAÇO = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (LARGURA, ALTURA))


def janela(vermelha, amarela, balas_amarelo, balas_vermelho, vida_vermelo, vida_amarelo):
    WIN.blit(ESPAÇO, (0, 0))
    pygame.draw.rect(WIN, PRETO, BORDAS)
    vida_vermelo_texto = VIDA_FONTE.render('VIDA: ' + str(vida_vermelo), 1, BRANCO)
    vida_amarelo_texto = VIDA_FONTE.render('VIDA: ' + str(vida_amarelo), 1, BRANCO)
    WIN.blit(vida_vermelo_texto, (LARGURA - vida_vermelo_texto.get_width() - 10, 10))
    WIN.blit(vida_amarelo_texto, (10, 10))
    WIN.blit(NAVE_AMARELA, (amarela.x, amarela.y))
    WIN.blit(NAVE_VERMELHA, (vermelha.x, vermelha.y))
    for bala in balas_vermelho:
        pygame.draw.rect(WIN, AMARELO, bala)
    for bala in balas_amarelo:
        pygame.draw.rect(WIN, VERMELHO, bala)
    pygame.display.update()


def movimento_amarela(tecla, amarela):
    if tecla[pygame.K_w] and amarela.y - VEL > 0:  # cima
        amarela.y -= VEL
    if tecla[pygame.K_s] and amarela.y + VEL < 440:  # baixo
        amarela.y += VEL


def movimento_vermelha(tecla, vermelha):
    if tecla[pygame.K_UP] and vermelha.y - VEL > 0:
        vermelha.y -= VEL
    if tecla[pygame.K_DOWN] and vermelha.y - VEL < 430:
        vermelha.y += VEL


def tiro(balas_amarelo, balas_vermelho, amarela, vermelha):
    for bala in balas_amarelo:
        bala.x += BALAS_VEL
        if vermelha.colliderect(bala):
            pygame.event.post(pygame.event.Event(HIT_VERMELHO))
            balas_amarelo.remove(bala)
        elif bala.x > LARGURA:
            balas_amarelo.remove(bala)

    for bala in balas_vermelho:
        bala.x -= BALAS_VEL
        if amarela.colliderect(bala):
            pygame.event.post(pygame.event.Event(HIT_AMARELO))
            balas_vermelho.remove(bala)
        elif bala.x < 0:
            balas_vermelho.remove(bala)


def vencedor(texto):
    winner = VENCEDOR_FONTE.render(texto, 1, BRANCO)
    WIN.blit(winner, (LARGURA/2 - winner.get_width()/2, ALTURA/2 - winner.get_height()/2))
    pygame.display.update()
    SOM_VENCEDOR.play()
    pygame.time.delay(10000)


def main():
    vermelha = pygame.Rect(830, 250, NAVE_ALTURA, NAVE_LARGURA)
    amarela = pygame.Rect(100, 250, NAVE_ALTURA, NAVE_LARGURA)
    balas_vermelho = []
    balas_amarelo = []
    vida_vermelho = 10
    vida_amarelo = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(balas_amarelo) < MAX_BALAS:
                    bala = pygame.Rect(amarela.x + amarela.width, amarela.y + amarela.height // 2 - 2, 10, 5)
                    balas_amarelo.append(bala)
                    TIRO_SOM.play()
                if event.key == pygame.K_DELETE and len(balas_vermelho) < MAX_BALAS:
                    bala = pygame.Rect(vermelha.x, vermelha.y + vermelha.height//2 - 2, 10, 5)
                    balas_vermelho.append(bala)
                    TIRO_SOM.play()
            if event.type == HIT_VERMELHO:
                vida_vermelho -= 1
                BALA_HIT_SOM.play()
            if event.type == HIT_AMARELO:
                vida_amarelo -= 1
                BALA_HIT_SOM.play()
        texto_win = ''
        if vida_vermelho <= 0:
            texto_win = 'AMARELO WIN!!!'
        if vida_amarelo <= 0:
            texto_win = 'VERMELHO WIN!!!'
        if texto_win != '':
            vencedor(texto_win)
            break

        tecla = pygame.key.get_pressed()
        movimento_vermelha(tecla, vermelha)
        movimento_amarela(tecla, amarela)
        tiro(balas_amarelo, balas_vermelho, amarela, vermelha)
        janela(vermelha, amarela, balas_vermelho, balas_amarelo, vida_vermelho, vida_amarelo)

    main()


if __name__ == '__main__':
    main()
