# Sistema CRM Web Simplificado (MVP)
---
Este sistema es un CRM (Customer Relationship Management) simplificado diseñado para microempresas de menos de cinco empleados que necesitan centralizar la gestión de clientes, ventas e inventario en una sola plataforma sencilla y accesible.

## Descripcion 
Este proyecto es un Producto Mínimo Viable (MVP) enfocado en resolver un problema común en micronegocios: el uso de múltiples herramientas informales (Excel, libretas, notas) para gestionar operaciones.

El sistema permite organizar la información comercial y mejorar el control operativo sin necesidad de software complejo o costoso.

## Enfoque del proyecto
- Simplicidad de uso
- Centralización de información
- Control operativo básico
- Escalabilidad futura a producto comercial

## Funcionalidades Principales
### Control de acceso por roles: 
Control de acceso basado en 5 roles: 
- Dueño (control total).
- Administrador (operación diaria).
- Vendedor (fuerza comercial).
- Consultor (análisis de datos sin edición financiera).
- Superusuario (análisis de datos con edición financiera).

### Pipeline de Oportunidades:
Tablero tipo Kanban con etapas:
- Prospecto
- Calificación
- Propuesta
- Negociación
- Cierre - Ganado

### Gestión Operativa: 
- Clientes
- Inventario
- Proveedores
- Servicios
- Empleados
- Ventas
- Cotizaciones

### Importación de clientes
Carga masiva de clientes mediante archivos Excel (.xlsx)

### Personalización
Capacidad de subir un logotipo propio del micronegocio para identidad visual.
### Corte de Caja
Visualización de ingresos diarios y filtrado por fechas.
### Eliminación lógica
Los registros no se eliminan físicamente, permitiendo mantener historial.

## Tecnologías utilizadas
### Backend 
- Django (Python)
### Frontend
- Bootstrap
- JavaScript
- HTML
- CSS
### Base de datos
- MySQL

>Este sistema fue desarrollado bajo un enfoque de **Database-First**, donde la base de datos fue diseñada previamente y posteriormente integrada al sistema.

## Documentación técnica
El proyecto cuenta con documentación en la carpeta '/docs':
- Análisis de Requerimientos: Metodología MoSCoW y especificación de requerimientos.
- Diagramas de casos de uso
- Modelo Entidad-Relación (E-R)

## Instalación y Configuración Local
1. Clonar el repositorio  
git clone https://github.com/GloriaEsther/Sistema-CRM-web-simplificado.git  
cd Sistema-CRM-web-simplificado

2. Configurar el Entorno Virtual:
- Crear el entorno: python -m venv venv
- Activar el entorno:
  - En Windows: venv\Scripts\activate
  - Linux/macOS:source venv/bin/activate
    
3. Instalar Dependencias  
Con el entorno activo, instala las librerías necesarias listadas en el archivo requirements.txt:  
pip install -r requirements.txt

4. Configurar de la Base de Datos  
- Crear esquema en MySQL
- Importar archivo SQL ubicado en /docs/sql
- Configurar credenciales en crm/settings.py
- python manage.py migrate

5. Ejecutar Servidor
- python manage.py runserver
- Abrir en navegador: http://127.0.0.1:8000

## Capturas del sistema
>Los datos que se ven en las imagenes son un ejemplo
### Login
![image alt](https://github.com/GloriaEsther/Sistema-CRM-web-simplificado/blob/c78726a17c7fe1967f3a4060679720b271c11a72/crm/static/img/Login.png)
### Pipeline de Oportunidades
![image alt](https://github.com/GloriaEsther/Sistema-CRM-web-simplificado/blob/9982c74e32abdb368272cc767216f8562de67546/crm/static/img/Pipeline%20de%20Oportunidades.png)
### Opciones
![image alt](https://github.com/GloriaEsther/Sistema-CRM-web-simplificado/blob/c78726a17c7fe1967f3a4060679720b271c11a72/crm/static/img/Opciones.png)
### Gestión de Clientes
![image alt](https://github.com/GloriaEsther/Sistema-CRM-web-simplificado/blob/c78726a17c7fe1967f3a4060679720b271c11a72/crm/static/img/Clientes.png)
### Importar clientes desde Excel
![image alt](https://github.com/GloriaEsther/Sistema-CRM-web-simplificado/blob/c78726a17c7fe1967f3a4060679720b271c11a72/crm/static/img/Importar%20clientes%20desde%20Excel.png)

## ⚠️Uso del código
Este repositorio es público únicamente con fines de portafolio.
No está permitido el uso, copia o distribución del código sin autorización del autor.

## Estado del proyecto
MVP funcional desarrollado como parte de Residencia Profesional.
Actualmente en evaluación para evolución a producto comercial.

## Autor
Gloria Esther Martínez Martínez

