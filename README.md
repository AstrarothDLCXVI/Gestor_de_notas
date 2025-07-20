# 📝 Gestor de Notas con Flask

Un gestor de notas completo desarrollado con Flask, SQLite y Bootstrap. Incluye autenticación de usuarios, CRUD completo, sistema de categorías y una interfaz moderna y responsiva.

## ✨ Características

- **🔐 Autenticación completa**: Registro, login y logout seguro
- **📝 CRUD de notas**: Crear, leer, actualizar y eliminar notas
- **🏷️ Sistema de categorías**: Organiza tus notas con categorías personalizables
- **🎨 Interfaz moderna**: Diseño responsivo con Bootstrap 5
- **💾 Base de datos SQLite**: Almacenamiento local y ligero
- **👤 Multi-usuario**: Cada usuario ve solo sus propias notas
- **🔒 Seguridad**: Contraseñas hasheadas y sesiones seguras

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática

1. **Crear directorio del proyecto**:
```bash
mkdir gestor-notas
cd gestor-notas
```

2. **Crear y ejecutar el script de configuración**:
```bash
# Copiar el contenido de setup.py al archivo
python setup.py
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python app.py
```

### Opción 2: Instalación Manual

1. **Crear estructura de directorios**:
```bash
mkdir gestor-notas
cd gestor-notas
mkdir templates static
```

2. **Crear archivos necesarios**:
   - Copiar `app.py` (archivo principal)
   - Copiar todos los templates HTML a la carpeta `templates/`
   - Crear `requirements.txt`

3. **Instalar dependencias y ejecutar**:
```bash
pip install -r requirements.txt
python app.py
```

## 📁 Estructura del Proyecto

```
gestor-notas/
│
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── notes.db              # Base de datos SQLite (se crea automáticamente)
├── setup.py              # Script de configuración
│
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── login.html        # Página de login
│   ├── register.html     # Página de registro
│   ├── dashboard.html    # Dashboard principal
│   ├── note_form.html    # Formulario de notas
│   ├── categories.html   # Lista de categorías
│   └── category_form.html # Formulario de categorías
│
└── static/               # Archivos estáticos (vacío, usa CDN)
```

## 🔧 Configuración

### Variables Importantes

En `app.py`, asegúrate de cambiar:

```python
app.secret_key = 'tu_clave_secreta_aqui'  # ⚠️ Cambiar por una clave segura
```

### Base de Datos

La base de datos SQLite se crea automáticamente al ejecutar la aplicación por primera vez. Incluye las siguientes tablas:

- **users**: Información de usuarios
- **categories**: Categorías de notas
- **notes**: Notas de los usuarios

## 🎯 Uso de la Aplicación

### 1. Registro y Login
- Accede a `http://localhost:5000`
- Regístrate con usuario, email y contraseña
- Inicia sesión con tus credenciales

### 2. Gestión de Notas
- **Crear**: Click en "Nueva Nota" en el dashboard o sidebar
- **Editar**: Click en el menú de opciones (⋮) de cualquier nota
- **Eliminar**: Desde el menú de opciones con confirmación
- **Categorizar**: Asigna categorías durante la creación/edición

### 3. Gestión de Categorías
- Ve a la sección "Categorías" en el sidebar
- Crea categorías con nombres personalizados y colores
- Edita o elimina categorías existentes
- Las notas sin categoría quedan como "Sin categoría"

## 🛠️ Características Técnicas

### Backend (Flask)
- **Rutas protegidas**: Decorador `@login_required`
- **Seguridad**: Hashing de contraseñas con Werkzeug
- **Base de datos**: SQLite con conexiones contextuales
- **Sesiones**: Manejo seguro de sesiones de usuario

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **Font Awesome**: Iconos vectoriales
- **JavaScript**: Interacciones dinámicas
- **CSS personalizado**: Estilos adicionales para mejorar UX

### Base de Datos
- **SQLite**: Base de datos embebida
- **Relaciones**: Foreign keys entre tablas
- **Timestamps**: Fechas de creación y actualización automáticas

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con `generate_password_hash()`
- ✅ Protección de rutas con decorador de autenticación
- ✅ Validación de pertenencia de datos por usuario
- ✅ Escape automático de HTML en templates
- ✅ Sesiones seguras con secret_key

## 📱 Funcionalidades

### Dashboard
- Vista de tarjetas con todas las notas
- Indicadores visuales de categorías
- Acciones rápidas (editar/eliminar)
- Búsqueda visual por colores de categoría

### Gestión de Notas
- Editor de texto amplio
- Selección de categorías
- Timestamps automáticos
- Previsualización truncada en dashboard

### Sistema de Categorías
- Colores personalizables
- Gestión independiente
- Asignación opcional a notas
- Manejo de eliminación (notas quedan sin categoría)

## 🎨 Personalización

### Cambiar Colores del Tema
En `templates/base.html`, modifica el CSS:

```css
.sidebar {
    background: linear-gradient(135deg, #tu-color-1 0%, #tu-color-2 100%);
}
```

### Añadir Nuevos Campos
1. Modifica la base de datos añadiendo columnas
2. Actualiza los formularios HTML
3. Modifica las rutas Flask correspondientes

### Cambiar Estilos
Modifica los estilos CSS en la sección `<style>` de `base.html` o crea archivos CSS separados en `static/`.

## 🐛 Resolución de Problemas

### Error: "No such table"
- Ejecuta la aplicación una vez para que se cree la base de datos automáticamente

### Error: "Working outside of application context"
- Asegúrate de que todas las consultas a la base de datos estén dentro de las rutas Flask

### Error: "Template not found"
- Verifica que todos los archivos HTML estén en la carpeta `templates/`

### Error: "Secret key not set"
- Configura `app.secret_key` en `app.py`

## 📚 Dependencias

- **Flask 3.0.0**: Framework web
- **Werkzeug 3.0.1**: Utilidades WSGI y seguridad

## 🚀 Próximas Mejoras

- [ ] Búsqueda de notas por título/contenido
- [ ] Exportación de notas (PDF, TXT)
- [ ] Etiquetas adicionales además de categorías
- [ ] Editor de texto rico (WYSIWYG)
- [ ] Modo oscuro
- [ ] API REST
- [ ] Backup automático
- [ ] Compartir notas entre usuarios

## 📄 Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras bugs o tienes ideas para mejoras, no dudes en:

1. Reportar issues
2. Proponer mejoras
3. Enviar pull requests

---

**¡Disfruta organizando tus notas! 📝✨**
