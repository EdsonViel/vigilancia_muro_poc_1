from enum import Enum

import cv2
import numpy as np


class Lado(Enum):
    esquerdo = 1
    direito = 2


class StatusPessoa(Enum):
    dentro = 1
    fora = 2
    invasor = 3


class Fonte:
    def __init__(self) -> None:
        self.fonte = cv2.FONT_HERSHEY_SIMPLEX
        self.tamanho_fonte = 0.35
        self.espessura_fonte = 1
        self.posicao = (10, 20)


class Localizacao:
    def __init__(self, pontoX: int, pontoY: int) -> None:
        self.pontoX = pontoX
        self.pontoY = pontoY
    
    def to_tuple(self):
        return (self.pontoX, self.pontoY)


class Linha:
    def __init__(self, pontoA: Localizacao, pontoB: Localizacao) -> None:
        self.pontoA = pontoA
        self.pontoB = pontoB


class TamanhoRetangulo:
    def __init__(self, largura: int, altura: int) -> None:
        self.largura = largura
        self.altura = altura


class Retangulo:
    def __init__(self, localizacao: Localizacao, area: TamanhoRetangulo) -> None:
        self.pontoInical = localizacao
        self.area = area
        
    def centro(self):
        return Localizacao(self.pontoInical.pontoX + (self.area.largura//2), self.pontoInical.pontoY + (self.area.altura//2))

    def posicaoInical(self):
        return self.pontoInical.to_tuple()
    
    def posicaoFinal(self):
        return (self.pontoInical.pontoX + self.area.largura, self.pontoInical.pontoY + self.area.altura)
    

class Config:
    def __init__(self) -> None:
        # cores
        self.fundo_imagem = (50, 50, 50)
        self.azul = (255, 0, 0)
        self.verde = (0, 255, 0)
        self.vermelho = (50, 50, 255)
        self.amarelo = (0, 255, 255)
        self.laranja = (0, 91, 247)

        self.tamanhoImagem = Localizacao(640, 480)
        self.interior_condominio = Lado.direito
        self.fonte_imagem = Fonte()
        self.posicao_pessoa = Retangulo(Localizacao(0, 0), TamanhoRetangulo(50, 100))
        self.muro_horizontal = Linha(Localizacao(0, self.tamanhoImagem.pontoY//2), Localizacao(self.tamanhoImagem.pontoX, self.tamanhoImagem.pontoY//2))  # ([pontoA], [pontoB])
        self.muro_vertical = Linha(Localizacao(self.tamanhoImagem.pontoX//2, 0), Localizacao(self.tamanhoImagem.pontoX//2, self.tamanhoImagem.pontoY))  # ([pontoA], [pontoB])


config = Config()

class Simulacao:
    def __init__(self) -> None:
        self.nome_simulacao = 'Simulacao Muro 2.0'
        self.muroHorizontal = config.muro_horizontal
        self.muroVertical = config.muro_vertical
        self.posicaoPessoa = config.posicao_pessoa
        self.video = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, config.tamanhoImagem.to_tuple()) # type: ignore

    def iniciar(self):
        self.geraImagem()
        self.add_trackbar()
        cv2.waitKey(0)
        self.video.release()
        return self

    def geraImagem(self) -> cv2.Mat:
        imagem: cv2.Mat = config.fundo_imagem[0] * np.ones((config.tamanhoImagem.pontoY, config.tamanhoImagem.pontoX, 3), dtype=np.uint8)  # type: ignore
        return imagem

    def add_trackbar(self):
        cv2.namedWindow(self.nome_simulacao)

        cv2.createTrackbar('Muro vertical A', self.nome_simulacao, config.muro_vertical.pontoA.pontoX, config.tamanhoImagem.pontoX, self.on_trackbar_muro_vertical_topo) # type: ignore
        cv2.createTrackbar('Muro vertical B', self.nome_simulacao, config.muro_vertical.pontoB.pontoX, config.tamanhoImagem.pontoX, self.on_trackbar_muro_vertical_base) # type: ignore

        cv2.createTrackbar('Muro horizontal A', self.nome_simulacao, self.muroHorizontal.pontoA.pontoY, config.tamanhoImagem.pontoY, self.on_trackbar_muro_horizontal_esquerdo) # type: ignore
        cv2.createTrackbar('Muro horizontal B', self.nome_simulacao, self.muroHorizontal.pontoB.pontoY, config.tamanhoImagem.pontoY, self.on_trackbar_muro_horizontal_direito) # type: ignore
        
        if config.interior_condominio == Lado.esquerdo:
            cv2.createTrackbar('Muro horizontal X', self.nome_simulacao, 0, config.tamanhoImagem.pontoX//2, self.on_trackbar_muro_horizontal_x) # type: ignore
        else:
            cv2.createTrackbar('Muro horizontal X', self.nome_simulacao, config.tamanhoImagem.pontoX, config.tamanhoImagem.pontoX, self.on_trackbar_muro_horizontal_x) # type: ignore
            cv2.setTrackbarMin('Muro horizontal X', self.nome_simulacao, config.tamanhoImagem.pontoX//2)
        
        cv2.createTrackbar('Pessoa horizontal', self.nome_simulacao, self.posicaoPessoa.pontoInical.pontoX, config.tamanhoImagem.pontoX, self.on_trackbar_pessoa_horizontal) # type: ignore
        cv2.createTrackbar('Pessoa vertical', self.nome_simulacao, self.posicaoPessoa.pontoInical.pontoY, config.tamanhoImagem.pontoY, self.on_trackbar_pessoa_vertical) # type: ignore
    
    def on_trackbar_muro_vertical_topo(self, val: int):
        imagem = self.geraImagem()

        if config.interior_condominio == Lado.esquerdo:
            pontoA_validacao = Localizacao(val, self.muroHorizontal.pontoB.pontoY)
        else:
            pontoA_validacao = Localizacao(val, self.muroHorizontal.pontoA.pontoY)
        
        if pontoA_validacao != self.muroVertical.pontoA:
            cv2.line(imagem, pontoA_validacao.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)
            cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)

            if config.interior_condominio == Lado.esquerdo:
                if pontoA_validacao.pontoX != self.muroHorizontal.pontoB.pontoX:
                    self.muroHorizontal.pontoB.pontoX = pontoA_validacao.pontoX 
            else:
                if pontoA_validacao.pontoX != self.muroHorizontal.pontoA.pontoX:
                    self.muroHorizontal.pontoA.pontoX = pontoA_validacao.pontoX

            self.muroVertical.pontoA = pontoA_validacao
            cv2.setTrackbarPos('Muro horizontal X', self.nome_simulacao, self.muroVertical.pontoA.pontoX)
      
            self.desenhaPessoa(imagem)
    
    def on_trackbar_muro_vertical_base(self, val: int):
        imagem = self.geraImagem()

        pontoB_validacao = Localizacao(val, self.muroVertical.pontoB.pontoY)

        cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), pontoB_validacao.to_tuple(), config.azul)
        cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)

        if pontoB_validacao != self.muroVertical.pontoB:
            self.muroVertical.pontoB = pontoB_validacao

        self.desenhaPessoa(imagem)

    def on_trackbar_muro_horizontal_esquerdo(self, val: int):
        imagem = self.geraImagem()

        if config.interior_condominio == Lado.esquerdo:
            if self.muroHorizontal.pontoA.pontoX != 0:
                if val <= config.tamanhoImagem.pontoY//2:
                    cv2.setTrackbarPos('Muro horizontal A', self.nome_simulacao, 0)
                    return
                else:
                    cv2.setTrackbarPos('Muro horizontal A', self.nome_simulacao, config.tamanhoImagem.pontoY)
                    return
            pontoA_validacao = Localizacao(self.muroHorizontal.pontoA.pontoX, val)

        else:
            pontoA_validacao = Localizacao(self.muroVertical.pontoA.pontoX, val)

        if pontoA_validacao != self.muroHorizontal.pontoA:
            cv2.line(imagem, pontoA_validacao.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)
            cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)

            if config.interior_condominio == Lado.direito:
                if pontoA_validacao.pontoY != self.muroVertical.pontoA.pontoY:
                    self.muroVertical.pontoA.pontoY = pontoA_validacao.pontoY
            
            self.muroHorizontal.pontoA = pontoA_validacao
        
        self.desenhaPessoa(imagem)

    def on_trackbar_muro_horizontal_direito(self, val: int):
        imagem = self.geraImagem()

        if (config.interior_condominio == Lado.direito and 
              self.muroHorizontal.pontoB.pontoX != config.tamanhoImagem.pontoX):
            if val <= config.tamanhoImagem.pontoX//2:
                cv2.setTrackbarPos('Muro horizontal B', self.nome_simulacao, 0)
            else:
                cv2.setTrackbarPos('Muro horizontal B', self.nome_simulacao, config.tamanhoImagem.pontoX)
            return

        if config.interior_condominio == Lado.esquerdo:
            pontoB_validacao = Localizacao(self.muroVertical.pontoA.pontoX, val)
        else:
            pontoB_validacao = Localizacao(config.tamanhoImagem.pontoX, val)
        
        if pontoB_validacao != self.muroHorizontal.pontoB:
            cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), pontoB_validacao.to_tuple(), config.azul)
            cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)
        
            if config.interior_condominio == Lado.esquerdo:
                if pontoB_validacao.pontoY != self.muroVertical.pontoA.pontoY:
                    self.muroVertical.pontoA.pontoY = pontoB_validacao.pontoY

            self.muroHorizontal.pontoB = pontoB_validacao

            self.desenhaPessoa(imagem)

    def on_trackbar_muro_horizontal_x(self, val: int):
        imagem = self.geraImagem()

        if config.interior_condominio == Lado.esquerdo:
            if self.muroHorizontal.pontoA.pontoY != 0 and self.muroHorizontal.pontoA.pontoY != config.tamanhoImagem.pontoY:
                cv2.setTrackbarPos('Muro horizontal X', self.nome_simulacao, 0)
                return
        else:
            if self.muroHorizontal.pontoB.pontoY != 0 and self.muroHorizontal.pontoB.pontoY != config.tamanhoImagem.pontoY:
                cv2.setTrackbarPos('Muro horizontal X', self.nome_simulacao, config.tamanhoImagem.pontoX)
                return

        if config.interior_condominio == Lado.esquerdo:
            self.muroHorizontal.pontoA.pontoX = val
        else:
            self.muroHorizontal.pontoB.pontoX = val

        cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)
        cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)

        self.desenhaPessoa(imagem)
    
    def on_trackbar_pessoa_horizontal(self, val: int):
        imagem = self.geraImagem()

        self.posicaoPessoa.pontoInical.pontoX = val

        cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)
        cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)

        self.desenhaPessoa(imagem)
    
    def on_trackbar_pessoa_vertical(self, val: int):
        imagem = self.geraImagem()

        self.posicaoPessoa.pontoInical.pontoY = val

        cv2.line(imagem, self.muroHorizontal.pontoA.to_tuple(), self.muroHorizontal.pontoB.to_tuple(), config.azul)
        cv2.line(imagem, self.muroVertical.pontoA.to_tuple(), self.muroVertical.pontoB.to_tuple(), config.azul)

        self.desenhaPessoa(imagem)

    def desenhaPessoa(self, imagem: cv2.Mat):
        invasaoHorizontal = self.pontoInvasaoHorizontal(imagem)
        invasaoVertical = self.pontoInvasaoVertical(imagem)

        if invasaoHorizontal and invasaoVertical:
            cor = config.vermelho
        else:
            cor = config.verde

        cv2.rectangle(imagem, self.posicaoPessoa.posicaoInical(), self.posicaoPessoa.posicaoFinal(), cor, 2)
        cv2.circle(imagem, self.posicaoPessoa.centro().to_tuple(), 2, cor, -1, 8)

        self.video.write(imagem)
        cv2.imshow(self.nome_simulacao, imagem)

    def pontoInvasaoHorizontal(self, imagem: cv2.Mat):
        # calcula invasao horizontal
        alturaMuroHorizontal = self.muroHorizontal.pontoB.pontoY - self.muroHorizontal.pontoA.pontoY
        larguraMuroHorizontal = self.muroHorizontal.pontoB.pontoX - self.muroHorizontal.pontoA.pontoX
        
        diferencaTopoHorizontal = self.muroHorizontal.pontoA.pontoY
        diferencaEsquerdaHorizontal = self.muroHorizontal.pontoA.pontoX

        # fração que vai aumentar ou diminuir a cada pixel que andar a direita
        if larguraMuroHorizontal > 0:
            fracaoPixelColunaLargura = 1.0 / larguraMuroHorizontal
        else:
            fracaoPixelColunaLargura = 1.0
        
        # altura x fração largura = base para calcular qual é o pixel
        # de altura do muro de acordo com a posição horizontal
        baseCalculoLargura = alturaMuroHorizontal * fracaoPixelColunaLargura

        # base * posição horizontal = calcula a altura do muro
        # na posição da pessoa
        pontoReferenciaLargura = round((baseCalculoLargura * (self.posicaoPessoa.centro().pontoX - diferencaEsquerdaHorizontal)) + diferencaTopoHorizontal)

        cv2.circle(imagem, ((self.posicaoPessoa.centro().pontoX),pontoReferenciaLargura), 2, config.amarelo, -1,8)
        if self.posicaoPessoa.centro().pontoY >= pontoReferenciaLargura:
            return True
            
        return False

    def pontoInvasaoVertical(self, imagem: cv2.Mat):
        alturaMuroVertical = self.muroVertical.pontoB.pontoY - self.muroVertical.pontoA.pontoY
        larguraMuroVertical = self.muroVertical.pontoB.pontoX - self.muroVertical.pontoA.pontoX
        
        diferencaTopoVertical = self.muroVertical.pontoA.pontoY
        diferencaEsquerdaVertical = self.muroVertical.pontoA.pontoX

        # calcula invasao vertical
        if alturaMuroVertical > 0:
            fracaoPixelColunaAltura = 1.0 / alturaMuroVertical
        else:
            fracaoPixelColunaAltura = 1.0
        
        # largura x fração altura = base para calcular qual é o pixel
        # de largura do muro de acordo com a posição vertical
        baseCalculoAltura = larguraMuroVertical * fracaoPixelColunaAltura
        
        # base * posição vertical = calcula a largura do muro
        # na posição da pessoa
        pontoReferenciaAltura = round((baseCalculoAltura * (self.posicaoPessoa.centro().pontoY - diferencaTopoVertical)) + diferencaEsquerdaVertical)
    
        cv2.circle(imagem, (pontoReferenciaAltura,(self.posicaoPessoa.centro().pontoY)), 2, config.amarelo, -1, 8)
        if config.interior_condominio == Lado.esquerdo:
            if self.posicaoPessoa.centro().pontoX <= pontoReferenciaAltura:
                return True
            else:
                return False
        else:
            if self.posicaoPessoa.centro().pontoX >= pontoReferenciaAltura:
                return True
            else:
                return False

        
simulacao = Simulacao()
simulacao.iniciar()

cv2.destroyAllWindows()
