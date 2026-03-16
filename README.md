# Sistema CRM Web Simplificado (MVP)
Este sistema es un CRM (Customer Relationship Management) en su version Producto Mínimo Viable (MVP) diseñado para microempresas de menos de cinco empleados. Su objetivo es centralizar y organizar la gestión de clientes, ventas y procesos operativos básicos que suelen manejarse de forma dispersa en herramientas informales.
El proyecto fue desarrollado como proyecto de Residencias Profesionales para la carrera de Ingeniería en Sistemas Computacionales cuyo objetivo es aplicar principios de ingeniería de software y gestión de bases de datos.

---
## Descripcion 
El sistema permite administrar información clave de clientes, productos y ventas dentro de un mismo entorno. Está pensado para micronegocios que requieren llevar un control básico de su actividad comercial sin utilizar herramientas complejas o costosas.

## Funcionalidades Principales
- Control de acceso por roles: Control de acceso basado en 5 roles: Dueño (control total), Administrador (operación diaria), Vendedor (fuerza comercial), Consultor (análisis de datos sin edición financiera) y Superusuario (análisis de datos con edición financiera).Cada rol tiene acceso únicamente a las funciones correspondientes dentro del sistema.
- Pipeline de Oportunidades: Tablero Kanban con etapas: Prospecto, Calificación, Propuesta, Negociación y Cierre-Ganado.
- Control Operativo: Gestión de clientes, inventarios, proveedores, servicios, empleados, ventas y generación de cotizaciones.
- Importación Masiva: Carga de clientes desde archivos Excel (.xlsx).
- Personalización: Capacidad de subir un logotipo propio del micronegocio para identidad visual.
- Corte de Caja: Visualización de ingresos diarios y filtrado por fechas.
- Seguridad de Datos: Implementación de eliminación lógica de registros para prevenir pérdida accidental de información.

## Documentación de Ingeniería
El proyecto cuenta con una base de análisis y diseño, clos cuales se encuentran en la carpeta /docs:

- Análisis de Requerimientos: Metodología MoSCoW para la priorización de funcionalidades del MVP y especificación de requerimientos funcionales y no funcionales.

- Diseño de Procesos: Diagramas de Casos de Uso detallando las interacciones por roles críticos.

- Arquitectura de Datos: Diagrama Entidad-Relación que detalla la estructura normalizada de la base de datos.

## Tecnologías utilizadas
### Backend 
- Django (Python)
### Frontend
- Bootstrap
- JavaScript
- HTML / CSS
### Base de datos
- MySQL
 - Enfoque Database-First: La base de datos fue diseñada y normalizada previamente para asegurar la integridad empresarial, integrándose posteriormente al sistema mediante el mapeo de modelos de Django.
### Otras herramientas
- Git
- Github
---
## Instalación y Configuración Local
Sigue estos pasos para ejecutar el proyecto en tu entorno local.
Nota: Este proyecto utiliza un enfoque Database-First. Asegúrate de tener instalado MySQL y de contar con el esquema de la base de datos antes de iniciar.

1. Clonar el repositorio
   git clone https://github.com/GloriaEsther/Sistema-CRM-web-simplificado.git

   cd Sistema-CRM-web-simplificado

2. Configurar el Entorno Virtual
   Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto:
   - Crear el entorno: python -m venv venv
   - Activar el entorno:
      - En Windows: venv\Scripts\activate
      - Linux/macOS:source venv/bin/activate
    
3. Instalar Dependencias
   Con el entorno activo, instala las librerías necesarias listadas en el archivo requirements.txt : pip install -r requirements.txt

4. Configuración de la Base de Datos
   Crea un esquema en tu gestor de MySQL.
   Importa el archivo Base de datos_CRM.sql (el cual esta en /docs/sql ) o asegúrate de que las tablas coincidan con el diseño E-R proporcionado en la carpeta /docs/diagramas.
   Actualiza tus credenciales locales (Usuario, Contraseña, Host) en el archivo crm/settings.py.
   Ejecuta el siguiente comando para sincronizar el estado del framework con la base de datos importada: python manage.py migrate
  ##### Esto registrará las tablas existentes en el historial de Django y asegurará el correcto funcionamiento del sistema de autenticación.

5. Inicialización del Sistema
   Por ultimo, queda inicializar el servidor de desarrollo: python manage.py runserver
   Accede a: http://127.0.0.1:8000
