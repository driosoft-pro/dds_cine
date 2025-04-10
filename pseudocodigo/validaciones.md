FUNCIÓN validar_edad_pelicula(pelicula, usuario)
    edad = usuario.calcular_edad()
    SEGUN pelicula.clasificacion HACER
        CASO 'G': RETORNAR True
        CASO 'PG': RETORNAR edad >= 7
        CASO 'PG-13': RETORNAR edad >= 13
        CASO 'R': RETORNAR edad >= 17
        CASO 'C': RETORNAR edad >= 18
    FIN SEGUN
FIN FUNCIÓN