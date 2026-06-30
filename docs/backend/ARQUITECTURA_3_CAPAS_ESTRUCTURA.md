# Estructura Física de 3 Capas

La arquitectura ahora también se ve en carpetas, no solo en documentación conceptual.

```text
apps/
├── presentacion/
│   └── web/
│       ├── auth_views.py
│       ├── estudiante_views.py
│       ├── docente_views.py
│       └── admin_views.py
├── negocio/
│   └── servicios/
│       ├── usuarios.py
│       ├── informes.py
│       ├── observaciones.py
│       └── reglamento.py
├── datos/
│   └── repositorios/
│       ├── usuarios.py
│       ├── informes.py
│       ├── observaciones.py
│       └── reglamento.py
├── core/
│   ├── views.py
│   └── admin_views.py
├── usuarios/
├── informes/
├── observaciones/
└── reglamento/
```

## Criterio

- `presentacion`: recibe requests y responde con templates/redirecciones.
- `negocio`: concentra servicios y lógica de aplicación.
- `datos`: encapsula acceso ORM y consultas reutilizables.
- `apps` originales de Django siguen existiendo para mantener modelos, migraciones y compatibilidad.
