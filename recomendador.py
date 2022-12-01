# Practica 2 Bloque 1 - Adquisición de datos iMat
# Hecho por: Lara Ocón Madrid


# Importamos las librerias que vamos a usar
import pandas as pd
import re
import sys, signal
import random


def handler_signal(signal, frame):
    # Controlamos la salida del programa por control + C
    print("\n\n [!] Out .......\n")
    sys.exit(1)


def extract(archivo_csv):
    # extraemos el fichero donde guarda las canciones y la información
    # acerca de ellas
    df = pd.read_csv(archivo_csv, sep = ",")
    return df
    

def transform(df, cancion_actual):
    # En esta funcion transformamos los datos, para ello toma la cancion
    # que este sonando en ese momento y devuelve un dataframe con las 10
    # canciones mas relacionadas con esta y en orden de cual está mas 
    # relacionada a menos

    # En primer lugar, buscamos la canción que nos han introducido en el csv
    # en caso de no estar la canción en este, no tenemos información acerca 
    # de ella, por lo que devolemos una canción aleatoria del nuestro csv.

    canciones = list(df['song'])

    encontrado = False
    i = 0
    while i < len(canciones) and not encontrado:
        # queremos que busque la cancion en todas las canciones sin importar
        # mayusculas
        if re.search(cancion_actual, canciones[i], re.I):
            encontrado = True
            cancion = df.iloc[i]
        i += 1
    
    # En el caso de que la cancion insertada no esté en el csv, salimos de la 
    # función transformar
    if not encontrado:
        return {}

    # Ahora veamos las canciones similares a esta
    # para ello hemos definido una función de evaluación para cada carcaterística que comparten 
    # las canciones del csv con la canción que está escuchando el usuario, de forma que mediante
    # la suma de todas estas funciones de evaluación, cada canción recibe una nota, donde la canción
    # con mejor nota es la más recomendada

    canciones_puntuacion = {}
    top_5 = 0
    for i in range(len(df)):
        nota = 0
        if not re.search(cancion_actual, df.loc[i]['song'], re.I):
            # evitamos que nos devuelva otra vez la cancion actual
            nota += mismos_generos(cancion['genre'], df.loc[i]['genre'])
            nota += mismo_artista(cancion['artist'], df.loc[i]['artist'])
            nota += tempos_energy_similares(cancion['tempo'], df.loc[i]['tempo']) 
            nota += ac_and_inst_similares(cancion['acousticness'], df.loc[i]['acousticness'])
            nota += ac_and_inst_similares(cancion['instrumentalness'], df.loc[i]['instrumentalness'])
            nota += ac_and_inst_similares(cancion['speechiness'], df.loc[i]['speechiness'])
            nota += tempos_energy_similares(cancion['energy'], df.loc[i]['energy']) 
            nota += mismo_key(cancion['key'], df.loc[i]['key'])
            nota += int(df.loc[i]['popularity']) / 100 # le damos el peso de 1 / 10
        
        # metemos las canciones en el top_5
        if len(canciones_puntuacion) >= 5:
            if nota > top_5:
                top_5 = nota
                # sacamos la ultima y para meter la nueva
                canciones_puntuacion = eliminar_peor_elemento(canciones_puntuacion)
                canciones_puntuacion[df.loc[i]['song']] = nota
        else:
            if nota > top_5:
                top_5 = nota
            canciones_puntuacion[df.loc[i]['song']] = nota

        # ordenamos el diccionario
        canciones_puntuacion = dict(sorted(canciones_puntuacion.items()))

    return canciones_puntuacion


def eliminar_peor_elemento(dict):
    # Esta función la empleamos para a la hora de añadir una cancion a la lista del
    # top 5 recomendado, sacar a la canción con peor nota de recomendación.

    llaves = list(dict.keys())
    peor_v = dict[llaves[0]]
    peor_llave = llaves[0]

    for i in range(1, len(llaves)):
        if dict[llaves[i]] < peor_v:
            peor_v = dict[llaves[i]]
            peor_llave = llaves[i]
    
    del dict[peor_llave]
    return dict


def mismos_generos(generos_cancion, generos_recomendada):
    # Función de evaluación que asigna una puntuación en base 
    # al género de la cancion.

    # separamos los generos que contiene la cancion
    generos1 = generos_cancion.split(", ")

    generos2 = generos_recomendada.split(", ")

    acertados = 0

    # sumamos 1 punto por cada genero que compartan ambas canciones
    for genero in generos2:
        if re.search(genero, generos_cancion):
            acertados += 1

    # ahora aportamos una nota sobre 5 para todos los generos
    # que acierte del total de generos de la cancion_actual
    return acertados/len(generos1) * 4.5


def mismo_artista(artista1, artista2):
    # función evaluacion que asigna una puntuación
    # de 0.5 si comparten el mismo artista
    if artista1 == artista2:
        return 0.5
    else:
        return 0


def tempos_energy_similares(tempo_actual, tempo_recomendada):
    # función de evaluación que asigna una puntuación en base a si los tempos 
    # son similares

    var_tempo = abs(float(tempo_recomendada) - float(tempo_actual))
    if var_tempo < 1:
        return 1
    else:
        return 1/var_tempo
    

def ac_and_inst_similares(ac_1, ac_2):
    # función de evaluación que asigna una puntuación en base a si la instrumentalidad 
    # y la acústica en ambas canciones es similar

    var_ac = abs(float(ac_1) - float(ac_2))

    if float(ac_1) > 0:
        if var_ac > 100:
                return 0
        else:
            return 0.5
    else:
        # solo nos queda que ac_1 sea menor que 0, en ese caso la otra tambien
        # debe tener muuy poca acustica
        if var_ac > 0:
            return 0
        else:
            return 0.5


def mismo_key(key1, key2):
    # función de evaluación que asigna una puntuación de 0.5 si las canciones 
    # comparten la misma key
    var_key = abs(float(key1) - float(key2))
    if var_key == 0:
        return 0.5
    else:
        return 0.4 / var_key


def load(dict):
    # Función de carga de datos, esta función 
    if dict == {}:
        # si el diccionario está vacío es porque no se ha encontrado
        # la cancion introducida en el csv, por lo que recomendamos una
        # al azar
        # Esto es que no ha encontrado la cancion en el csv, asi que recomendamos una aleatoria
        print(f"\nVaya! No sabemos cual es esa canción...   :( ")
        cancion = df_canciones.iloc[random.randint(0, len(df_canciones)-1)]
        print(f'\nPero prueba a escuchar  "{cancion.song}" de {cancion.artist} !!!\n')
    else:
        # En el caso que si haya encontrado la canción habrá diccionario, por lo que 
        # imprimos las 5 canciones recomendadas
        print("\nTambién te puede gustar...\n")
        canciones = list(dict.keys())
        for cancion in canciones:
            print("\033[1;34m"+cancion+"\033[0;m\n")


if __name__ == "__main__":

    # Controlamos la salida por la señal ctrl+C
    signal.signal(signal.SIGINT, handler_signal)
    
    try:
        # Obtenemos la canción sobre la cual nos vamos a basar en nuestra 
        # recomendación, en caso de que el usuario no introduzca canción, 
        # atraparemos el error con el except e indicaremos al usuario
        # de que introduzca la cancion
        cancion_actual = sys.argv[1]

        # EXTRACCIÓN DE DATOS:
        archivo_csv = 'songs_normalize.csv'
        df_canciones = extract(archivo_csv)

        # TRANSFORMAMOS LOS DATOS: en función de la cancion que nos introduzcan
        # buscamos las 5 mejores canciones relacionadas con esta
        mejores_canciones = transform(df_canciones, cancion_actual)

        # CARGA DE DATOS: imprimimos la recomendación por pantalla
        load(mejores_canciones)

    except:
        print("\nDebes pasar una canción por argumento para que podamos recomendarte que escuchar! :) \n")
        print('\nSi ya nos has pasado una canción, prueba a ponerla entre comillas! (Por ejemplo: "The Real Slim Shady"\n')
        

    

    
