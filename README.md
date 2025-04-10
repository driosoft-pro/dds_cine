# Sistema de Venta de Entradas para un Cinema

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
sistema_venta_entrada_cinema/
│
├── app/                            # 📂 Código fuente principal
│   ├── __init__.py
│   ├── main.py                     # Punto de entrada de la aplicación
│
│   ├── models/                     # 📂 Modelos del negocio
│   │   ├── __init__.py
│   │   ├── cinema.py               # Modelo de Salas y Entradas
│   │   ├── reservation.py          # Modelo de Reservas
│   │   ├── user.py                 # Modelo de Usuarios
│   │   ├── movie.py                # 🎬 Modelo de Películas
│   │   ├── ticket.py               # 🎟️ Modelo de Boletas
│   │   ├── food_menu.py            # 🍿 Modelo de Menú de Comidas
│   │   └── payment.py              # 💳 Modelo de pagos y métodos
│
│   ├── controllers/                # 📂 Lógica entre modelos y vistas
│   │   ├── __init__.py
│   │   ├── cinema_controller.py
│   │   ├── reservation_controller.py
│   │   ├── user_controller.py
│   │   ├── movie_controller.py
│   │   ├── food_menu_controller.py
│   │   ├── ticket_controller.py
│   │   └── payment_controller.py
│
│   ├── views/                      # 📂 Interfaz en consola con Rich y Pyfiglet
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── login_view.py
│   │   ├── user_view.py
│   │   ├── movie_view.py
│   │   ├── reservation_view.py
│   │   ├── ticket_view.py
│   │   ├── food_menu_view.py
│   │   └── availability_view.py
│
│   ├── services/                   # 📂 Servicios de negocio o utilidades
│   │   ├── __init__.py
│   │   ├── auth_service.py           # Servicio para login y permisos 
│   │   ├── date_utils.py             # Utilidades de fechas (validaciones, etc.)
│
│   ├── data/                       # 📂 Almacenamiento de datos
│   │   ├── __init__.py
│   │   ├── database.py             # Manejo de persistencia
│   │   └── data.json               # 📄 Archivo con la información persistida
│
├── doc/                            # 📂 Documentación del proyecto
│   ├── caracteristicas.txt
│   ├── requerimientos.txt
│   ├── requerimientos.txt          # 🎨 Diagrama opcional de arquitectura o clases
│   └── diseño_base.png             # 🎨 Diagrama opcional de arquitectura o clases
│
├── requirements.txt                # 📜 Dependencias
├── .gitignore                      # 🚫 Archivos a ignorar
└── README.md                       # 📖 Documentación principal
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