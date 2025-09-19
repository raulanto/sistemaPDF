# Sistema de Facturas
**Juego de destruir bloques**

### Instalacion

1. Crear entorno virtual
```bash
python -m venv env
```

2. Activar entorno virtual
```bash
.\env\Scripts\activate
```

3. Instalar requisitos
```bash
pip install -r requirements.txt
```


4. Arbol
```
mi-app-empresa/
├── app/
│   ├── controllers/         # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── user_controller.py
│   │   └── data_controller.py
│   ├── services/           # Servicios y API calls
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── data_service.py
│   ├── models/             # Modelos de datos
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── message.py
│   ├── components/         # Widgets reutilizables
│   │   ├── __init__.py
│   │   ├── reactive_text.py
│   │   └── custom_widgets.py
│   ├── pages/              # Páginas de la aplicación
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   └── dashboard_page.py
│   ├── middleware/         # Middleware personalizado
│   │   ├── __init__.py
│   │   └── auth.py
│   └── routes.py           # Configuración de rutas
├── config/
│   └── settings.py         # Configuración de la aplicación
├── tests/
│   ├── unit/
│   └── integration/
├── docker-compose.yml      # Orquestación de contenedores
├── .env.example           # Variables de entorno
├── pyproject.toml
└── README.md
```