import pygame
import numpy as np

pygame.init()

# Configurações da tela
largurat = 900
alturat = 700
tela = pygame.display.set_mode((largurat, alturat))
pygame.display.set_caption("Sistemas de Massas e Molas")
pre = (0, 0, 0)
bra = (255, 255, 255)

# Fonte para textos
font = pygame.font.Font(None, 36)
modo = "input"

# Listas para armazenar múltiplas massas
massas = []
constantes_molas = []
posicoes = []
velocidades = []
frequencias = []  # Lista para armazenar as frequências dos modos normais

# Controle de input
reinput = False
inputx = ""
current_input = "massa"  # Alterna entre massa e constante da mola, sem isso 
finalizando_input = False  # Indica se o usuário quer finalizar a entrada de massas

# Controle de simulação
massa_atual = 0  # Índice da massa atualmente exibida
dt = 0.01  # Intervalo de tempo

g = 9.81  # Gravidade
tampend = 0.5  # Tamanho do pêndulo
escala = 300
mx1 = largurat // 2
mx2 = largurat // 6
mx3 = largurat // 1.2
y = alturat // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if modo == "input":
                if event.key == pygame.K_SPACE and not reinput:
                    reinput = True
                    inputx = ""
                    finalizando_input = False
                elif reinput:
                    if event.key == pygame.K_RETURN:
                        try:
                            if inputx == "" and len(massas) > 0:  # Se não há input, inicia a simulação
                                modo = "simulacao"
                            else:
                                if current_input == "massa":
                                    massas.append(float(inputx))
                                    current_input = "constante"
                                elif current_input == "constante":
                                    constantes_molas.append(float(inputx))
                                    posicoes.append(0.8)
                                    velocidades.append(0.0)
                                    frequencias.append(np.sqrt(constantes_molas[-1] / massas[-1]))  # Cálculo da frequência
                                    current_input = "massa"
                                    print(f"Massa {len(massas)} adicionada com constante {constantes_molas[-1]} e frequência {frequencias[-1]:.2f} rad/s")
                        except ValueError:
                            print("Erro: Insira um número válido.")
                        inputx = ""
                    elif event.key == pygame.K_BACKSPACE:
                        inputx = inputx[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == ".":
                            inputx += event.unicode

            elif modo == "simulacao" and pygame.K_1 <= event.key <= pygame.K_9:
                indice = event.key - pygame.K_1
                if 0 <= indice < len(massas):
                    massa_atual = indice
                    print(f"Mudando para Massa {massa_atual + 1}")

    tela.fill(pre)

    if modo == "simulacao" and len(massas) > 0:
        massa = massas[massa_atual]
        constante_mola = constantes_molas[massa_atual]
        posin = posicoes[massa_atual]
        velin = velocidades[massa_atual]
        freq = frequencias[massa_atual]

        aceleracao = -(constante_mola / massa) * (posin - 0.42)
        velin += aceleracao * dt
        posin += velin * dt
        posicoes[massa_atual] = posin
        velocidades[massa_atual] = velin

        angpend = (posin - 0.42) / tampend
        pendulo_x = mx2 + (tampend * np.sin(angpend) * escala)
        pendulo_y = y + (tampend * np.cos(angpend) * escala)
        molac = mx1 + int((posin - 0.42) * escala)
        molad = y + int((posin - 0.42) * escala * 0.5)

        pygame.draw.line(tela, (255, 0, 0), (300, 550), (300, 0), 5)
        pygame.draw.line(tela, (255, 0, 0), (900, 100), (0, 100), 5)
        pygame.draw.line(tela, (255, 0, 0), (900, 550), (0, 550), 5)
        pygame.draw.line(tela, (255, 0, 0), (600, 550), (600, 0), 5)

        tela.blit(font.render("Frontal", True, bra), (mx2 - 50, y - 300))
        tela.blit(font.render("Superfície", True, bra), (mx1 - 50, y - 300))
        tela.blit(font.render("Lateral", True, bra), (mx3 - 50, y - 300))

        tela.blit(font.render(f"Massa {massa_atual + 1}: {massa} kg", True, bra), (20, alturat - 125))
        tela.blit(font.render(f"Velocidade: {velin:.2f} m/s", True, bra), (20, alturat - 100))
        tela.blit(font.render(f"Frequência: {freq:.2f} rad/s", True, bra), (20, alturat - 75))
        tela.blit(font.render("Pressione 'ESC' para sair", True, (250, 0, 0)), (20, alturat - 50))

        pygame.draw.line(tela, (255, 255, 255), (mx1, y), (molac, y), 2)
        pygame.draw.circle(tela, (255, 0, 0), (molac, y), 15)
        pygame.draw.line(tela, (255, 255, 255), (mx2, y), (pendulo_x, pendulo_y), 2)
        pygame.draw.circle(tela, (0, 255, 0), (pendulo_x, pendulo_y), 15)
        pygame.draw.line(tela, (255, 255, 255), (mx3, y), (mx3, molad), 2)
        pygame.draw.circle(tela, (0, 0, 255), (mx3, molad), 15)

    if modo == "input":
        if reinput:
            prompt = f"Digite a {current_input}: " + inputx
        else:
            prompt = "Pressione 'ESPAÇO' para inserir massa"
        tela.blit(font.render(prompt, True, bra), (20, 180))

    pygame.display.flip()

pygame.quit()