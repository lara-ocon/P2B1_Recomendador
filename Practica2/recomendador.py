
import pandas as pd
import re
import sys, signal


def handler_signal(signal, frame):
    # Esta función controla la salida del programa por una señal de
    # ctrl+C
    print("\n\n [!] Out .......\n")
    sys.exit(1)

signal.signal(signal.SIGINT, handler_signal)

def extract(archivo_csv):
    # lo de sepaador coma no hace falta, ya de por si lo hace
    df = pd.read_csv(archivo_csv, sep = ",")
    return df
    
def transform(df, cancion_actual):
    # En esta funcion transformamos los datos, para ello toma la cancion
    # que este sonando en ese momento y devuelve un dataframe con las 
    # canciones mas relacionadas con esta y cada una con un valor de cual es
    # la que mejor se adapta

    # primero busco en el df la cancion que esta sonando
    encontrado = False
    i = 0
    cancion = None
    while i < len(df) and not encontrado:
        if df.loc[i]['song'] == cancion_actual:
            encontrado = True
            cancion = df.iloc[i]
        i += 1
    # aqui puede no encontrar la cancion por lo que CONTROLAR ERROR
    if not encontrado:
        raise Exception("cancion no encontrada")

    # Ahora veamos las canciones similares a esta
    # para ello definimos la siguiente funcion de evaluacion:
    # si son del mismo genero 45%
    # si son del mismo artista 5%
    # si tienen tempos similares 10%
    # si tienen acousticness similares 5%
    # si tienen speechiness similares 5%
    # si tiene instrumentalness similares 5%
    # si tienen energy similares 10%
    # si tienen mismo key 5%
    # popularity +10% (nota del 1 al 100)

    canciones_puntuacion = {}
    top_10 = 0
    for i in range(len(df)):
        nota = 0
        if df.loc[i]['song'] != cancion_actual:
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
        
        if len(canciones_puntuacion) >= 10:
            if nota > top_10:
                top_10 = nota
                # sacamos la ultima y para meter la nueva
                canciones_puntuacion = eliminar_peor_elemento(canciones_puntuacion)
                canciones_puntuacion[df.loc[i]['song']] = nota
        else:
            if nota > top_10:
                top_10 = nota
            canciones_puntuacion[df.loc[i]['song']] = nota

        # ordenamos el diccionario
        canciones_puntuacion = dict(sorted(canciones_puntuacion.items()))

    return canciones_puntuacion


    # df.drop(columns = ["duration_ms"], inplace = True)
    # entrada = input("what genere wpul you like to hear?:\n")
    # create regex based on entrada that ignores case
    # regex = re.compile(entrada, re.IGNORECASE)
    # data = re.findall(regex, df)
    #return data

def eliminar_peor_elemento(dict):

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
    # separamos los generos que contiene la cancion
    generos1 = generos_cancion.split(", ")

    generos2 = generos_recomendada.split(", ")

    acertados = 0

    for genero in generos2:
        if re.search(genero, generos_cancion):
            acertados += 1

    # ahora aportamos una nota sobre 5 para todos los generos
    # que acierte del total de generos de la cancion_actual
    return acertados/len(generos1) * 4.5

def mismo_artista(artista1, artista2):
    if artista1 == artista2:
        return 0.5
    else:
        return 0

def tempos_energy_similares(tempo_actual, tempo_recomendada):
    var_tempo = abs(float(tempo_recomendada) - float(tempo_actual))
    # si son muy parecidos le quiero dar mas nota
    # como maximo dare 1 punto
    if var_tempo < 1:
        return 1
    else:
        return 1/var_tempo
    

def ac_and_inst_similares(ac_1, ac_2):

    var_ac = abs(float(ac_1) - float(ac_2))
    # si son muy parecidos le quiero dar mas nota
    # como maximo dare 1 punto

    if float(ac_1) > 0:
        if var_ac > 100:
                return 0 # no se parecen en nada las canciones
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
    var_key = abs(float(key1) - float(key2))
    if var_key == 0:
        return 0.5
    else:
        return 0.4 / var_key


def load(dict):
    # imprimo los resultados por pantalla
    print("También te puede gustar...\n")
    canciones = list(dict.keys())
    for cancion in canciones:
        print("\033[1;34m"+cancion+"\033[0;m\n")


if __name__ == "__main__":
    cancion_actual = input("Introduce el nombre de la canción que estés escuchando: ").strip()
    
    try:
        # extraemos los datos
        archivo_csv = 'songs_normalize.csv'
        df_canciones = extract(archivo_csv)

        # transformamos los datos
        mejores_canciones = transform(df_canciones, cancion_actual)

        # cargamos los datos en orden de relevancia
        load(mejores_canciones)

    except Exception as e:
        print(e)

    

    
