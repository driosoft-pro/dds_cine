INICIO
    IMPORTAR pyfiglet, rich, datetime, json, os
    
    // Definición de clases principales
    CLASE Persona
        ATRIBUTOS PRIVADOS:
            identificacion: str
            nombre: str
            correo: str
            fecha_nacimiento: date
            estado: bool
        
        MÉTODOS:
            Constructor(identificacion, nombre, correo, fecha_nacimiento)
            Getters y Setters para todos los atributos
            calcular_edad() -> int
            mostrar_info() -> str
    
    CLASE Usuario HEREDA DE Persona
        ATRIBUTOS PRIVADOS:
            tipo: str  // 'cliente' o 'administrador'
            historial_compras: list
            historial_reservas: list
        
        MÉTODOS:
            Constructor(identificacion, nombre, correo, fecha_nacimiento, tipo)
            mostrar_info() SOBREESCRITO
            agregar_compra(compra)
            agregar_reserva(reserva)
    
    CLASE Pelicula
        ATRIBUTOS PRIVADOS:
            titulo: str
            lanzamiento: date
            director: str
            genero: str
            sinopsis: str
            duracion: int  // en minutos
            clasificacion: str  // G, PG, PG-13, R, C
            idioma: str
            origen: str
            sala: str  // '2D' o '3D'
            fechas: list[date]
            horas: list[str]
            jornadas: list[str]  // 'mañana', 'tarde', 'noche'
            estado: bool
        
        MÉTODOS:
            Constructor(titulo, lanzamiento, director, genero, sinopsis, duracion, clasificacion, idioma, origen, sala)
            agregar_funcion(fecha, hora, jornada)
            mostrar_info() -> str
            verificar_clasificacion(edad) -> bool
    
    CLASE Sala
        ATRIBUTOS PRIVADOS:
            tipo: str  // '2D' o '3D'
            capacidad: int
            sillas_disponibles: dict  // {'general': [], 'preferencial': []}
            sillas_ocupadas: dict
        
        MÉTODOS:
            Constructor(tipo)
            inicializar_sillas()
            mostrar_disponibilidad(fecha, hora) -> dict
            reservar_silla(tipo_silla, posicion, cliente)
            liberar_silla(tipo_silla, posicion)
    
    CLASE Ticket
        ATRIBUTOS PRIVADOS:
            id: str
            pelicula: Pelicula
            sala: Sala
            fecha_funcion: date
            hora_funcion: str
            cliente: Usuario
            tipo_silla: str  // 'general' o 'preferencial'
            posicion_silla: str
            precio: float
            estado: str  // 'reservado', 'pagado', 'cancelado'
            fecha_compra: datetime
            menu_comida: list
        
        MÉTODOS:
            Constructor(pelicula, sala, fecha_funcion, hora_funcion, cliente, tipo_silla, posicion_silla)
            calcular_precio() -> float
            aplicar_descuentos()
            agregar_comida(menu_item)
            mostrar_info() -> str
    
    CLASE MenuComida
        ATRIBUTOS PRIVADOS:
            items: list
        
        MÉTODOS:
            Constructor()
            agregar_item(codigo, categoria, producto, tamaño, valor)
            buscar_por_categoria(categoria) -> list
            buscar_por_nombre(nombre) -> list
            mostrar_menu() -> str
    
    CLASE SistemaCinema
        ATRIBUTOS PRIVADOS:
            usuarios: list[Usuario]
            peliculas: list[Pelicula]
            salas: list[Sala]
            menu_comida: MenuComida
            ventas: list[Ticket]
            reservas: list[Ticket]
        
        MÉTODOS:
            Constructor()
            cargar_datos_iniciales()
            guardar_datos()
            login(correo, contraseña) -> Usuario
            registrar_usuario(datos) -> bool
            buscar_pelicula(criterio, valor) -> list[Pelicula]
            mostrar_cartelera() -> str
            comprar_ticket(datos_compra) -> Ticket
            reservar_ticket(datos_reserva) -> Ticket
            cancelar_reserva(id_ticket) -> bool
            mostrar_asientos_disponibles(pelicula, fecha, hora) -> str
            generar_reporte_ventas() -> str
            validar_edad_pelicula(pelicula, usuario) -> bool
    
    // Controladores
    CLASE UserController
        MÉTODOS:
            crear_usuario(datos)
            actualizar_usuario(id, datos)
            listar_usuarios()
            buscar_usuario(criterio, valor)
    
    CLASE MovieController
        MÉTODOS:
            crear_pelicula(datos)
            actualizar_pelicula(titulo, datos)
            listar_peliculas()
            buscar_pelicula(criterio, valor)
    
    // Vistas
    CLASE LoginView
        MÉTODOS:
            mostrar_login() -> dict
            mostrar_mensaje(mensaje)
    
    CLASE MenuView
        MÉTODOS:
            mostrar_menu_principal(usuario) -> str
            mostrar_menu_cliente() -> str
            mostrar_menu_admin() -> str
    
    // Main
    FUNCIÓN main()
        sistema = SistemaCinema()
        sistema.cargar_datos_iniciales()
        
        MIENTRAS True HACER
            opcion = LoginView.mostrar_login()
            
            SI opcion['tipo'] == 'login' ENTONCES
                usuario = sistema.login(opcion['correo'], opcion['contraseña'])
                SI usuario NO ES None ENTONCES
                    MIENTRAS True HACER
                        opcion = MenuView.mostrar_menu_principal(usuario)
                        
                        SEGUN opcion HACER
                            CASO 'ver_cartelera':
                                cartelera = sistema.mostrar_cartelera()
                                MOSTRAR cartelera
                            
                            CASO 'comprar_entrada':
                                datos_compra = TicketView.mostrar_formulario_compra()
                                SI sistema.validar_edad_pelicula(datos_compra['pelicula'], usuario) ENTONCES
                                    ticket = sistema.comprar_ticket(datos_compra)
                                    MOSTRAR "Compra exitosa"
                                SINO
                                    MOSTRAR "No cumple con la clasificación de edad"
                            
                            CASO 'salir':
                                SALIR
                        FIN SEGUN
                SINO
                    MOSTRAR "Credenciales incorrectas"
            SINO SI opcion['tipo'] == 'registro' ENTONCES
                sistema.registrar_usuario(opcion['datos'])
            FIN SI
        FIN MIENTRAS
    
    EJECUTAR main()
FIN