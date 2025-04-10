FUNCIÓN calcular_precio(ticket)
    precio_base = 18000  // General 2D
    
    SI ticket.sala.tipo == '3D' ENTONCES
        SI ticket.tipo_silla == 'preferencial' ENTONCES
            precio_base = 25000
        SINO
            precio_base = 18000
    FIN SI
    
    edad = ticket.cliente.calcular_edad()
    
    SI edad < 12 ENTONCES
        precio_base = 15000
    SINO SI edad > 60 ENTONCES
        precio_base = 16000
    FIN SI
    
    // Aplicar 2x1 en martes/jueves tarde para preferencial
    SI ticket.fecha_funcion.weekday() in [1, 3] Y ticket.hora_funcion.jornada == 'tarde' Y ticket.tipo_silla == 'preferencial' ENTONCES
        precio_base = precio_base / 2
    FIN SI
    
    RETORNAR precio_base
FIN FUNCIÓN