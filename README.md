# Vigilância Muro PoC 1

Primeira Poc de Sistema de Vigilância de Muro Automatizada

## 📋 Pré-requisitos

Rodando atualmente em **[Python 3.12.3](https://www.python.org/downloads/release/python-3123/)** com **[OpenCV](https://opencv.org/)** e **[NumPy](https://numpy.org/)**.

Utilize ``pip install -r requirements.txt`` para instalação do OpenCV e NumPy.

##  O que esta PoC prova?

Prova o conceito de que através das imagens de uma câmera, um sistema de 
detecção de pessoas e áreas de muro pré-configurados é possível verificar 
se uma pessoa está dentro ou fora da área configurada.

### Explicação do código

Existem várias classes iniciais para definição de linhas, retângulos e pontos 
que são utilizadas para a simução do muro, de uma pessoa e de pontos de 
referência para cálculos.

A classe ``Config`` é utlizada para configurar as cores utilizadas (fundo, 
linhas e pontos), o tamanho da imagem para simular a imagem de uma câmera, o
retângulo representando a pessoa e muro horizontal e vertical.

A classe ``Simulacao`` é onde a brincadeira acontece, onde temos:

* Método ``iniciar`` que inicia todo o processo;
* Método ``geraImagem`` que gera uma imagem de fundo para simular a imagem da 
câmera;
* Método ``desenhaPessoa`` que desenha o retângulo representando a pessoa.
* Métodos ``pontoInvasaoHorizontal`` e ``pontoInvasaoVertical`` que calcula de 
acordo com a posição atual da pessoa e dos muros se é uma invasão ou não;
* Método ``add_trackbar`` que adiciona as trackbar's para movimentar o muro e
a pessoa;
* E vários os métodos que implementam as movimentações através das trackbar's.

### Rodando a aplicação
Utilize ``python simula_muro.py`` ou ``python3 simula_muro.py`` para rodar 
dependendo do SO e instalação do Python na máquina.

Com a aplicação iniciada é possível ver a área escura de fundo, um retângulo 
com um ponto verde na parte superior esquerda, dois pontos amarelos, um ao 
lado do retângulo e outro abaixo e duas linha fechando uma área na parte 
inferior direita.

O retângulo na parte superior esquerda representa a pessoa e o ponto no centro 
representa o ponto de onde considero a invasão do muro.

Os pontos amarelos representam um referência das linhas do muro vertical e 
horizontal em uma reta com o ponto central da pessoa a partir de onde calculo 
se é uma invasão ou não (sim, mesmo fora da área do muro).

Utilize as trackbar's para mover a pessoa e o muro e observe que a partir do 
momento que o ponto central da pessoa está dentro da área do muro, o retângulo 
representando a pessoa fica vermelho (👽 Invasão detectada!).


Tudo isso usando apenas OpenCV e NumPy!!!
