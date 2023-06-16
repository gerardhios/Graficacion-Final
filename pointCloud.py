from chainCodes import af8
import imageio
import matplotlib.pyplot as plt
from skimage import feature, measure
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage, misc
import itertools

def convertir_a_letras(numeros):
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    resultado = []
    for numero in numeros:
        if numero >= 0 and numero < len(letras):
            resultado.append(letras[numero])
        else:
            resultado.append(str(numero))  # Si el número no tiene una letra correspondiente, se agrega como cadena de texto
    return resultado

def obtenerPuntosQuiebre(lista_letras):
    resultado = []
    i = 0

    while i < len(lista_letras):
        if lista_letras[i] == 'h' and i < len(lista_letras) - 1 and lista_letras[i+1] == 'b':
            resultado.append('h')
            resultado.append('b')
            i += 2
        elif lista_letras[i] == 'b' and i < len(lista_letras) - 1 and lista_letras[i+1] == 'h':
            resultado.append('b')
            resultado.append('h')
            i += 2
        elif lista_letras[i] == 'a':
            resultado.append('a')
            i += 1
        else:
            resultado.append('x')
            i += 1

    return resultado

def reducirCadena(lista):
    resultado = ""
    contador = 0

    for letra in lista:
        if letra == "a":
            contador += 1
        else:
            if contador > 0:
                resultado += "a^" + str(contador) + " "
                contador = 0
            resultado += letra

    if contador > 0:
        resultado += "a^" + str(contador) + " "

    return resultado

def obtener_borde_imagen(ruta_imagen, lista_letras):
    ## Leer la imagen en escala de grises
    imagen = imageio.imread(ruta_imagen, as_gray=True)

    # Aplicar el detector de bordes Canny
    borde = feature.canny(imagen, sigma=1.0)

    # Mostrar el borde
    for i in range(borde.shape[0]):
        for j in range(borde.shape[1]):
            if borde[i, j] != 0:
                if lista_letras[i] == 'x':
                    plt.scatter(i, j, color='red', s=10)
                else:
                    plt.scatter(i, j, color='blue', s=2)

    plt.axis("off")
    plt.show()

def printBreakPoints(imagen_path, lista):
    imagen = imageio.imread(imagen_path, as_gray=True)

    
    # Binarizar la imagen (convertir a blanco y negro)
    umbral = 0.5  # Umbral para la binarización
    imagen_binaria = imagen > umbral

    # Encontrar los contornos utilizando find_contours
    contornos = measure.find_contours(imagen_binaria, 0.5)
    
    # Crear una figura y ejes para mostrar la imagen y los contornos
    fig, ax = plt.subplots()
    
    
    
    # Dibujar los contornos
    for i, contorno in enumerate(contornos):
        coordenadas_x = contorno[:, 1]
        coordenadas_y = contorno[:, 0]
        
        # Distribuir la serie de datos en la lista mayor
        lista = list(itertools.islice(itertools.cycle(lista), len(contorno)))
        for j in range(len(contorno)):
            x = coordenadas_x[j]
            y = coordenadas_y[j]

            try:
                if (lista[j] == 'x'):
                    ax.scatter(x, y, s=50, color='red')
            except:
                continue
        
        ax.plot(contorno[:, 1], contorno[:, 0], linewidth=2, color='blue')
        print(i)

    # Configurar los ejes
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()


def freeContextGrammar(imageData:list):
    # Border coords son las coordenas del contorno como se siguio
    code, border_coords = af8(imageData, ret=True, coords=True)

    code = convertir_a_letras(code)

    grammar_complete = obtenerPuntosQuiebre(code)

    grammar_reduced = reducirCadena(grammar_complete)
    print(grammar_reduced)


    #sacar el borde para graficar con plt
    try:
        contorno = printBreakPoints(imageData[1], grammar_complete)
        #borde_imagen = printBreakPoints(imageData[1], grammar_complete)   
    except Exception as e:
        print("Ocurrió un error:", e)
        input("Presiona Enter para continuar...")



    #grammar_complete obtener las coordenadas de las x 

    #graficar todo :)
