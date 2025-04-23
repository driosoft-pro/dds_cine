# Sistema de Venta de Entradas para un Cinema DDS_CINE

## 🎟️ Descripción del Proyecto
Este sistema es una aplicación de consola que permite la gestión completa de ventas y reservas de entradas para un cinema, incluyendo:

- Dos salas (2D y 3D), con diferentes tipos de sillas y precios.
- Gestión de usuarios (clientes y administradores).
- Gestión de películas, disponibilidad, reservas y compras.
- Menú de alimentos y bebidas.
- Aplicación desarrollada con Programación Orientada a Objetos (POO).
- Persistencia de datos con archivo JSON.

## 🌐 Tecnologías Utilizadas
- Python 3.10+
- [Rich](https://github.com/Textualize/rich) - Para la interfaz en consola.
- [Pyfiglet](https://github.com/pwaller/pyfiglet) - Para títulos artísticos.
- JSON - Para persistencia de datos.
- POO con herencia, polimorfismo y encapsulamiento.

## 🌟 Características Destacadas
- Diferentes tarifas por edad, categoría y horario.
- Promoción 2x1 para sillas preferenciales los martes y jueves por la tarde.
- Sistema de autenticación (login).
- Validaciones de edad para clasificación de películas.
- Compra y reserva de boletas con opciones de menú de comida.
- Pagos en efectivo, tarjeta o transferencia.

## 🌐 Estructura del Proyecto
```bash
dds_cine/
├── app/
│   ├── __init__.py                     # Archivo de inicialización del paquete principal.
│   ├── main.py                         # Punto de entrada de la aplicación.
│   ├── config.py                       # Configuración global (rutas, constantes, etc.).
│
│   ├── models/                         # Contiene las clases principales del dominio del sistema.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de modelos.
│   │   ├── user.py                     # Define las clases Usuario y Admin.
│   │   ├── movie.py                    # Define la clase Película.
│   │   ├── showtime.py                 # Define la clase para horarios de películas.
│   │   ├── ticket.py                   # Define la clase Entrada.
│   │   ├── reservation.py              # Define la clase Reserva.
│   │   ├── payment.py                  # Define la clase Pago.
│   │   ├── food.py                     # Define la clase Menú de comida.
│   │   └── cinema.py                   # Define la clase Cinema/Sala.
│
│   ├── controllers/                    # Contiene la lógica de control para manejar las operaciones del sistema.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de controladores.
│   │   ├── user_controller.py          # Controlador para operaciones relacionadas con usuarios.
│   │   ├── movie_controller.py         # Controlador para operaciones relacionadas con películas.
│   │   ├── showtime_controller.py      # Controlador para operaciones relacionadas con horarios.
│   │   ├── ticket_controller.py        # Controlador para operaciones relacionadas con entradas.
│   │   ├── reservation_controller.py   # Controlador para operaciones relacionadas con reservas.
│   │   ├── payment_controller.py       # Controlador para operaciones relacionadas con pagos.
│   │   ├── food_controller.py          # Controlador para operaciones relacionadas con el menú de comida.
│   │   └── cinema_controller.py        # Controlador para operaciones relacionadas con las salas de cine y sillas.
│
│   ├── handlers/                       # Contiene funciones que manejan la lógica de interacción por flujo (handlers).
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de handlers.
│   │   ├── handle_auth.py              # Maneja el inicio de sesión, registro y autenticación de usuarios.
│   │   ├── handle_availability.py      # Muestra la disponibilidad de asientos por película y horario.
│   │   ├── handle_food_management.py   # Maneja la administración del menú de comida (CRUD para admins).
│   │   ├── handle_food_menu.py         # Muestra el menú de comida para clientes y permite búsquedas.
│   │   ├── handle_main_menu.py         # Muestra y gestiona el menú principal, redirigiendo a los demás handlers.
│   │   ├── handle_movie_listing.py     # Muestra la cartelera disponible para los clientes y permite buscar/ver detalles.
│   │   ├── handle_movie_management.py  # Maneja la gestión de películas para administradores (listar, agregar, actualizar, eliminar).
│   │   ├── handle_reports.py           # Genera reportes estadísticos por ventas, película o usuario.
│   │   ├── handle_ticket_purchase.py   # Maneja la compra de tickets por parte del cliente.
│   │   ├── handle_user_management.py   # Permite al administrador gestionar usuarios (CRUD).
│   │   ├── handle_reservation.py       # Permite hacer, listar, cancelar o convertir reservas en tickets.
│   │   └── handle_user_tickets.py      # Muestra al usuario sus tickets y reservas activas.
│
│   ├── services/                       # Contiene la lógica de negocio y servicios auxiliares.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de servicios.
│   │   ├── auth_service.py             # Servicio para autenticación (registro, login, sesión).
│   │   ├── validation_service.py       # Servicio para validaciones de entradas.
│   │   ├── ticket_service.py           # Lógica de precios y promociones de entradas.
│   │   ├── seat_service.py             # Lógica para la disponibilidad de sillas.
│   │   ├── date_utils.py               # Utilidades para manejo de fechas.
│   │   ├── report_service.py           # Servicio para generación de reportes.
│   │   └── discount_service.py         # Servicio para manejo de promociones (2x1, descuentos, etc.).
│
│   ├── core/                           # Contiene la lógica central del sistema.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete core.
│   │   ├── database.py                 # Capa de acceso a datos (manejo de JSON y archivos).
│   │   └── initial_data.py             # Datos precargados como películas y usuarios.
│
│   ├── data/                           # Contiene los datos persistentes del sistema.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de datos.
│   │   └── data.json                   # Base de datos simulada en formato JSON.
│
│   ├── views/                          # Contiene las vistas para la interacción con el usuario.
│   │   ├── __init__.py                 # Archivo de inicialización del paquete de vistas.
│   │   ├── menu_view.py                # Menú principal e interfaz de usuario.
│   │   ├── login_view.py               # Vista para el login de usuarios.
│   │   ├── user_view.py                # Vista para operaciones relacionadas con usuarios.
│   │   ├── movie_view.py               # Vista para operaciones relacionadas con películas.
│   │   ├── ticket_view.py              # Vista para operaciones relacionadas con entradas.
│   │   ├── reservation_view.py         # Vista para operaciones relacionadas con reservas.
│   │   ├── payment_view.py             # Vista para operaciones relacionadas con pagos.
│   │   ├── food_menu_view.py           # Vista para operaciones relacionadas con el menú de comida.
│   │   └── availability_view.py        # Vista para consultar disponibilidad de sillas.
│
├── doc/                                # Documentación del proyecto.
│   ├── diagramClaseSDDS.png
│   ├── diagramFlujoDDS.png
|   ├── requerimientos.txt              # Requisitos funcionales y técnicos.
│   └── requerimientosDetallados.txt    # Pruebas para los servicios.
|
├── requirements.txt                    # Dependencias
├── .gitignore                          # Archivos a ignorar
└── README.md                           # Documentación principal
```
## 📅 Reglas del Negocio
- Sala 2D: Solo sillas generales (100 sillas).
- Sala 3D: 80 sillas generales, 20 preferenciales.
- Tarifas:
  - Estándar: $18.000
  - Preferencial: $25.000
  - Niño (<12): $15.000
  - Adulto Mayor (>60): $16.000
  - Martes y jueves tarde (preferencial 2x1)
- Tipos de usuarios:
  - Cliente: Puede registrarse, comprar, reservar, cancelar.
  - Administrador: Puede crear, actualizar, listar y consultar usuarios, películas, ventas, reservas, menú, etc.
- Reservas: Óptimo entre 2 y 7 días antes.
- Cancelación: Máximo 2 días antes.
- Películas pre-cargadas (20 películas) con clasificación: G, PG, PG-13, R, C.

## 🍿 Menú de Comida
- **Combos**
  - Pequeño: $15.000
  - Mediano: $22.000
  - Grande: $28.000
  - Familiar: $35.000
- **Snacks**
  - Crispetas: $8.000 - $20.000
  - Nachos: $18.000
  - Perro: $12.000
  - Hamburguesa: $15.000
- **Bebidas**
  - Gaseosas: $6.000 - $10.000
  - Agua: $5.000
  - Jugo: $7.000
- **Dulces**
  - Chocolatina: $4.000
  - Dulces: $6.000

## 🔍 Funcionalidades
- [x] Registro/Login de usuario
- [x] Listado y consulta de películas
- [x] Compra y reserva de entradas
- [x] Cancelación de reservas
- [x] Vista de disponibilidad de sillas
- [x] Registro y consulta de ventas
- [x] Menú de comida en la compra
- [x] Pagos con manejo de vuelto

## ⚖️ Persistencia de Datos
- Se utiliza **archivo JSON** mediante un **controlador Python** personalizado en `data/database.py`.
- Permite guardar: usuarios, reservas, compras, menú, películas y trazabilidad.

## 💼 Recomendaciones
- Ejecuta el proyecto dentro de un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
o venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## ✅ Buenas Prácticas
- Cumple con la guía [PEP8](https://peps.python.org/pep-0008/) para estilo de código.
- Comentarios claros y funciones documentadas.
- Uso de clases, herencia, encapsulamiento y polimorfismo (sobrecarga y sobreescritura).

## ⚙️ Ejecutar el Proyecto
```bash
cd app
python main.py
```

## 🚀 Contribución
Si deseas colaborar, puedes abrir issues o enviar pull requests.

---

© Proyecto de Sistema de Venta de Entradas para Cinema. Todos los derechos reservados.

---  

✍️ **Desarrollado por:** **Deyton Riasco Ortiz**  
📅 **Fecha:** 2025  
📧 **Contacto:** [deyton007@gmail.com](mailto:deyton007@gmail.com)