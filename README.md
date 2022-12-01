# Practica2_bloque1
Recomendador de canciones de Spotify - Adquisición de Datos - IMat

Hecho por Lara Ocón Madrid - 202115710

Para esta práctica hemos hecho un recomendador de canciones de Spotify en base a la canción introducida por el usuario. Para ello, es necesario tener instaldas las librerías indicadas en el fichero requirements.txt para después lanzar correctamente el programa recomendador.py.

A la hora de lanzar el programa, es necesario introducir una canción por argumento separada por comillas (como por ejemplo: python3 recomendador.py "The Real Slim Shady"), en caso de no hacerlo, el programa imprimirá un mensaje informando al usuario de que debe introducir una canción y terminará la ejecución. En caso de que sí se introduzca una canción por argumento, lanzaremos una ETL para devolver la recomendación propuesta.

La ETL estará formada por las siguientes fases:

1) Extracción de datos: Extraemos los datos del fichero 'songs_normalize.csv', que contiene la información relativa a canciones de Spotify, y lo cargamos en un pandas dataframe.

2) Transformación de datos: Buscaremos dentro del dataframe la canción que nos han pasado por argumento (sin tener en cuenta las mayúsculas), para así poder acceder a toda su información. En caso de no encontrar la canción informamos al usuario de que no tenemos información acerca de esa canción y le decimos que pruebe a escuchar una canción aleatoria que sí que está en el csv. En caso de que si que encontrasemos la canción en el csv, ya tendremos todo lo suficiente para comenzar la recomendación. 

En la recomendación, iremos recorriendo todas las canciones del csv y evaluaremos empleando distintas funciones de evaluación los parecidos entre estas canciones y la canción introducida por el usuario, dando distinto peso a cada característica. Por ejemplo, le cedemos más importancia a que las canciones compartan los mismos géneros, a que tengan el mismo artista, o a que tengan la misma instrumentalidad...

Una vez recorrido todo el dataframe, nos quedaremos con las 5 canciones con mejor nota en base a nuestra recomendación, y las devolveremos en un diccionario.

3) Carga de datos: Esta función recibirá la recomendación propuesta y la imprimirá por pantalla, imprimiendo las canciones en negrita y en azul y separadas por espacios.


