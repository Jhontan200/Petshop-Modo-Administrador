# 💻 PETSHOP: ADMINISTRACIÓN DE DATOS (Python/Flask)
## ⭐ Objetivo y Descripción del Proyecto
Este proyecto es una aplicación web diseñada para simular un Modo Administrador (Admin) de una tienda de mascotas. Su objetivo principal es permitir la gestión completa de los datos y el inventario de la tienda a través de una interfaz conectada a una base de datos MySQL.

## 🛠️ Tecnologías y Librerías
Esta aplicación fue desarrollada en Python y utiliza el siguiente stack de tecnologías:
| Tecnología | Rol |
|-----------|-----|
| Python y JavaScript | Lenguajes principales para la lógica del servidor y la interactividad del frontend. |
| MySQL | Base de datos relacional utilizada para el almacenamiento de todos los datos (administradores, clientes, pedidos, categorías, productos). |
| Flask | Micro-framework de Python esencial para el desarrollo de la aplicación web y el routing.|
| pandas | Utilizado para la manipulación y procesamiento de datos. |
| mysql.connector | Librería oficial de Python para la conexión y comunicación con la base de datos MySQL. |
| fpdf | Utilizado para la generación de reportes y documentos en formato PDF. |

### Librerías Auxiliares Importantes

| Tecnología | Rol |
|-----------|-----|
| matplotlib.pyplot | Herramienta de visualización de datos para crear gráficos estáticos. |
| io | Módulo para trabajar con flujos de datos en memoria (buffers) para archivos temporales. |
| zipfile | Módulo para comprimir y archivar múltiples archivos (reporte Excel y gráfico). |
| os | Módulo de interacción con el sistema operativo (usado para eliminar archivos temporales). |

## 🚀 Instalación y Configuración Local
### 📌 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- 🐍 **Python 3** (versión más reciente recomendada)  
- 🛢️ **MySQL Workbench** (para alojar la base de datos local)  
- 🧑‍💻 **VS Code** u otro entorno de desarrollo compatible con Python

---

### 🧭 Pasos de Instalación

#### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/Jhontan200/Petshop-Modo-Administrador.git
cd Petshop-Modo-Administrador
```
2️⃣ Instalar Dependencias de Python

Ejecuta el siguiente comando para instalar las librerías necesarias:
```bash
pip install Flask pandas mysql-connector-python fpdf
```
3️⃣ Configurar la Base de Datos (⚠ Paso Crítico)

En el archivo principal (app.py o el de configuración), busca la sección de conexión a la base de datos y reemplaza las credenciales por las tuyas:
```bash
# Ejemplo de configuración a modificar
mydb = mysql.connector.connect(
    host="localhost",
    user="[TU_USUARIO_MYSQL]",
    password="[TU_CONTRASEÑA]",
    database="[NOMBRE_DE_TU_BD]"
)
```
Asegúrate de haber:

* 📌 Creado la base de datos [NOMBRE_DE_TU_BD] en MySQL

* 📥 Importado los esquemas/tablas necesarias antes de iniciar la app

## 💡 Uso del Proyecto
### ▶ 1️⃣ Ejecutar la Aplicación

Inicia el servidor Flask desde la terminal:
```bash
python app.py
```
## 🌐 2️⃣ Acceso Web e Interacción

**URL local:** http://127.0.0.1:5000

**Interfaz Admin:** Desde esta interfaz podrás:

* ✍️ Agregar, editar o eliminar datos

* 📈 Generar reportes en PDF y excel

* 📊 Consultar datos en tiempo real desde la base de datos

* 🧑‍💼 Simular operaciones administrativas de la tienda
## 👨‍💻 Autor y Contacto

Desarrollado por: **Jhontan200**

[🔗 Perfil de GitHub](https://github.com/Jhontan200)

## 📄 Licencia
Distribuido bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
[![GitHub license](https://img.shields.io/github/license/Jhontan200/Petshop-Modo-Administrador)](./LICENSE) 