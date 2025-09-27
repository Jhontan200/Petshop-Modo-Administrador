from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import mysql.connector
from fpdf import FPDF
import os
from flask import jsonify

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Isaias20@04@',
    'database': 'PETSHOP'
}

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirige al formulario de inicio de sesión

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            # Obtener datos del formulario
            usuario = request.form["usuario"]
            contrasena = request.form["contrasena"]

            print(f"Intentando iniciar sesión con usuario: {usuario}")  # Depuración

            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Verificar credenciales en la tabla ADMINISTRADOR
            query_admin = """
            SELECT usuario FROM ADMINISTRADOR
            WHERE usuario = %s AND contrasena = %s;
            """
            cursor.execute(query_admin, (usuario, contrasena))
            admin_result = cursor.fetchone()
            conn.close()

            # Redirigir si las credenciales son correctas
            if admin_result:
                print(f"Inicio de sesión exitoso: {usuario}")  # Depuración
                return redirect(url_for("lista_administradores"))  # Redirige a la lista de administradores
            else:
                # Mostrar error si las credenciales no son válidas
                return render_template("login.html", error="Usuario o contraseña incorrectos.")

        return render_template("login.html")
    except Exception as e:
        print(f"Error en inicio de sesión: {e}")
        return "Hubo un error en el sistema.", 500


# Ruta para mostrar la tabla de administradores
@app.route('/administradores')
def lista_administradores():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
        SELECT 
            a.id_administrador,
            CONCAT(n.nombre, ' ', n.apellido_paterno, ' ', n.apellido_materno) AS nombre_completo,
            a.usuario,
            a.contrasena,
            a.fecha_ingreso,
            a.hora_ingreso,
            a.hora_salida
        FROM 
            ADMINISTRADOR a
        JOIN 
            NOMBRES_ADMINISTRADOR n 
        ON 
            a.id_nombre_admin = n.id_nombre_admin
    """
    cursor.execute(query)
    administradores = cursor.fetchall()
    conn.close()
    return render_template('administradores.html', administradores=administradores)


# Ruta para añadir administrador
@app.route('/añadir_administrador', methods=['GET', 'POST'])
def añadir_administrador():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido_paterno = request.form['apellido_paterno'].strip()
        apellido_materno = request.form['apellido_materno'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena']
        fecha_ingreso = request.form['fecha_ingreso']
        hora_ingreso = request.form['hora_ingreso']
        hora_salida = request.form['hora_salida']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar en NOMBRES_ADMINISTRADOR y obtener el ID generado
        query_nombres = """
            INSERT INTO NOMBRES_ADMINISTRADOR (nombre, apellido_paterno, apellido_materno)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_nombres, (nombre, apellido_paterno, apellido_materno))
        id_nombre_admin = cursor.lastrowid

        # Insertar en ADMINISTRADOR
        query_administrador = """
            INSERT INTO ADMINISTRADOR (id_nombre_admin, usuario, contrasena, fecha_ingreso, hora_ingreso, hora_salida)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_administrador, (id_nombre_admin, usuario, contrasena, fecha_ingreso, hora_ingreso, hora_salida))

        conn.commit()
        conn.close()
        # Eliminado flash("Administrador añadido correctamente.")
        return redirect(url_for('lista_administradores'))
    return render_template('añadir_administrador.html')

# Ruta para editar un administrador
@app.route('/editar_administrador/<int:id>', methods=['GET', 'POST'])
def editar_administrador(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre'].strip()
        apellido_paterno = request.form['apellido_paterno'].strip()
        apellido_materno = request.form['apellido_materno'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena']
        fecha_ingreso = request.form['fecha_ingreso']
        hora_ingreso = request.form['hora_ingreso']
        hora_salida = request.form['hora_salida']

        # Actualizar los datos en NOMBRES_ADMINISTRADOR
        query_nombres = """
            UPDATE NOMBRES_ADMINISTRADOR
            SET nombre = %s, apellido_paterno = %s, apellido_materno = %s
            WHERE id_nombre_admin = (
                SELECT id_nombre_admin 
                FROM ADMINISTRADOR 
                WHERE id_administrador = %s
            )
        """
        cursor.execute(query_nombres, (nombre, apellido_paterno, apellido_materno, id))

        # Actualizar los datos en ADMINISTRADOR
        query_administrador = """
            UPDATE ADMINISTRADOR
            SET usuario = %s, contrasena = %s, fecha_ingreso = %s, hora_ingreso = %s, hora_salida = %s
            WHERE id_administrador = %s
        """
        cursor.execute(query_administrador, (usuario, contrasena, fecha_ingreso, hora_ingreso, hora_salida, id))

        conn.commit()
        conn.close()
        # Eliminado flash("Administrador actualizado correctamente.")
        return redirect(url_for('lista_administradores'))

    # Si es una solicitud GET, obtener los datos del administrador existente
    query = """
        SELECT 
            a.id_administrador,
            n.nombre,
            n.apellido_paterno,
            n.apellido_materno,
            a.usuario,
            a.contrasena,
            a.fecha_ingreso,
            a.hora_ingreso,
            a.hora_salida
        FROM 
            ADMINISTRADOR a
        JOIN 
            NOMBRES_ADMINISTRADOR n 
        ON 
            a.id_nombre_admin = n.id_nombre_admin
        WHERE 
            a.id_administrador = %s
    """
    cursor.execute(query, (id,))
    administrador = cursor.fetchone()
    conn.close()

    return render_template('editar_administrador.html', administrador={
        'id_administrador': administrador[0],
        'nombre': administrador[1],
        'apellido_paterno': administrador[2],
        'apellido_materno': administrador[3],
        'usuario': administrador[4],
        'contrasena': administrador[5],
        'fecha_ingreso': administrador[6],
        'hora_ingreso': administrador[7],
        'hora_salida': administrador[8],
    })

# Ruta para eliminar un administrador
@app.route('/eliminar_administrador/<int:id>', methods=['POST'])
def eliminar_administrador(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Eliminar de ADMINISTRADOR
    query_administrador = "DELETE FROM ADMINISTRADOR WHERE id_administrador = %s"
    cursor.execute(query_administrador, (id,))

    conn.commit()
    conn.close()
    return redirect(url_for('lista_administradores'))

@app.route('/clientes')
def lista_clientes():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """
        SELECT 
            c.id_cliente,
            CONCAT(n.nombre, ' ', n.apellido_paterno, ' ', n.apellido_materno) AS nombre_completo,
            c.usuario,
            c.contrasena
        FROM 
            CLIENTE c
        JOIN 
            NOMBRES_CLIENTE n 
        ON 
            c.id_nombre_cliente = n.id_nombre_cliente
    """
    cursor.execute(query)
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/añadir_cliente', methods=['GET', 'POST'])
def añadir_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre'].strip()
        apellido_paterno = request.form['apellido_paterno'].strip()
        apellido_materno = request.form['apellido_materno'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar en NOMBRES_CLIENTE y obtener el ID generado
        query_nombres = """
            INSERT INTO NOMBRES_CLIENTE (nombre, apellido_paterno, apellido_materno)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_nombres, (nombre, apellido_paterno, apellido_materno))
        id_nombre_cliente = cursor.lastrowid

        # Insertar en CLIENTE
        query_cliente = """
            INSERT INTO CLIENTE (id_nombre_cliente, usuario, contrasena)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_cliente, (id_nombre_cliente, usuario, contrasena))

        conn.commit()
        conn.close()

        # Redirigir a la lista de clientes
        return redirect(url_for('lista_clientes'))

    return render_template('añadir_cliente.html')

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre'].strip()
        apellido_paterno = request.form['apellido_paterno'].strip()
        apellido_materno = request.form['apellido_materno'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena']

        # Actualizar los datos en NOMBRES_CLIENTE
        query_nombres = """
            UPDATE NOMBRES_CLIENTE
            SET nombre = %s, apellido_paterno = %s, apellido_materno = %s
            WHERE id_nombre_cliente = (
                SELECT id_nombre_cliente 
                FROM CLIENTE 
                WHERE id_cliente = %s
            )
        """
        cursor.execute(query_nombres, (nombre, apellido_paterno, apellido_materno, id))

        # Actualizar los datos en CLIENTE
        query_cliente = """
            UPDATE CLIENTE
            SET usuario = %s, contrasena = %s
            WHERE id_cliente = %s
        """
        cursor.execute(query_cliente, (usuario, contrasena, id))

        conn.commit()
        conn.close()

        # Redirigir a la lista de clientes
        return redirect(url_for('lista_clientes'))

    # Si es una solicitud GET, obtener los datos del cliente existente
    query = """
        SELECT 
            c.id_cliente,
            n.nombre,
            n.apellido_paterno,
            n.apellido_materno,
            c.usuario,
            c.contrasena
        FROM 
            CLIENTE c
        JOIN 
            NOMBRES_CLIENTE n 
        ON 
            c.id_nombre_cliente = n.id_nombre_cliente
        WHERE 
            c.id_cliente = %s
    """
    cursor.execute(query, (id,))
    cliente = cursor.fetchone()
    conn.close()

    return render_template('editar_cliente.html', cliente={
        'id_cliente': cliente[0],
        'nombre': cliente[1],
        'apellido_paterno': cliente[2],
        'apellido_materno': cliente[3],
        'usuario': cliente[4],
        'contrasena': cliente[5]
    })

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Eliminar de CLIENTE
    query_cliente = "DELETE FROM CLIENTE WHERE id_cliente = %s"
    cursor.execute(query_cliente, (id,))

    conn.commit()
    conn.close()

    # Redirigir a la lista de clientes
    return redirect(url_for('lista_clientes'))

@app.route('/verificar_cliente/<int:id_cliente>')
def verificar_cliente(id_cliente):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM CLIENTE WHERE id_cliente = %s"
    cursor.execute(query, (id_cliente,))
    resultado = cursor.fetchone()
    conn.close()

    return {'existe': resultado[0] > 0}

@app.route('/verificar_administrador/<int:id_administrador>')
def verificar_administrador(id_administrador):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM ADMINISTRADOR WHERE id_administrador = %s"
    cursor.execute(query, (id_administrador,))
    resultado = cursor.fetchone()
    conn.close()

    return {'existe': resultado[0] > 0}

@app.route('/verificar_producto/<int:id_producto>')
def verificar_producto(id_producto):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nombre, stock FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    conn.close()

    if producto:
        return {
            'existe': True,
            'stock': producto['stock'],
            'nombre': producto['nombre']
        }
    else:
        return { 'existe': False }



@app.route('/pedidos')
def lista_pedidos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Obtener todos los pedidos con nombres de cliente y administrador, ordenados por ID
    query_pedidos = """
        SELECT 
            p.id_pedido,
            CONCAT(nc.nombre, ' ', nc.apellido_paterno, ' ', nc.apellido_materno) AS nombre_cliente,
            CONCAT(na.nombre, ' ', na.apellido_paterno, ' ', na.apellido_materno) AS nombre_administrador,
            p.estado,
            p.fecha
        FROM PEDIDO p
        JOIN CLIENTE c ON p.id_cliente = c.id_cliente
        JOIN NOMBRES_CLIENTE nc ON c.id_nombre_cliente = nc.id_nombre_cliente
        JOIN ADMINISTRADOR a ON p.id_administrador = a.id_administrador
        JOIN NOMBRES_ADMINISTRADOR na ON a.id_nombre_admin = na.id_nombre_admin
        ORDER BY p.id_pedido ASC
    """
    cursor.execute(query_pedidos)
    pedidos = cursor.fetchall()

    pedidos_con_detalles = []
    for pedido in pedidos:
        query_detalles = """
            SELECT 
                dp.id_detalle_pedido,
                pr.nombre AS nombre_producto,
                dp.cantidad
            FROM DETALLE_PEDIDO dp
            JOIN PRODUCTO pr ON dp.id_producto = pr.id_producto
            WHERE dp.id_pedido = %s
        """
        cursor.execute(query_detalles, (pedido[0],))
        detalles = cursor.fetchall()

        pedidos_con_detalles.append({
            'id_pedido': pedido[0],
            'nombre_cliente': pedido[1],
            'nombre_administrador': pedido[2],
            'estado': pedido[3],
            'fecha': pedido[4],
            'detalles': [{'id_detalle_pedido': d[0], 'nombre_producto': d[1], 'cantidad': d[2]} for d in detalles]
        })

    conn.close()
    return render_template('pedidos.html', pedidos=pedidos_con_detalles)




@app.route('/añadir_pedido', methods=['GET', 'POST'])
def añadir_pedido():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente'].strip()
        id_administrador = request.form['id_administrador'].strip()
        estado = request.form['estado'].strip()
        fecha = request.form['fecha'].strip()
        id_productos = request.form.getlist('id_producto[]')
        cantidades = request.form.getlist('cantidad[]')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Validar cliente
        cursor.execute("SELECT COUNT(*) FROM CLIENTE WHERE id_cliente = %s", (id_cliente,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return render_template('añadir_pedido.html', error="El ID del cliente no existe.")

        # Validar administrador
        cursor.execute("SELECT COUNT(*) FROM ADMINISTRADOR WHERE id_administrador = %s", (id_administrador,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return render_template('añadir_pedido.html', error="El ID del administrador no existe.")

        # Validar productos
        for id_producto in id_productos:
            cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
            if cursor.fetchone()[0] == 0:
                conn.close()
                return render_template('añadir_pedido.html', error=f"El producto {id_producto} no existe.")

        # Insertar pedido
        cursor.execute("""
            INSERT INTO PEDIDO (id_cliente, id_administrador, estado, fecha)
            VALUES (%s, %s, %s, %s)
        """, (id_cliente, id_administrador, estado, fecha))
        id_pedido = cursor.lastrowid

        # Insertar detalles
        for id_producto, cantidad in zip(id_productos, cantidades):
            if id_producto and cantidad:
                cursor.execute("""
                    INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad)
                    VALUES (%s, %s, %s)
                """, (id_pedido, id_producto, cantidad))

        conn.commit()
        conn.close()
        return redirect(url_for('lista_pedidos'))

    # GET: cargar nombres
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id_cliente, CONCAT(nc.nombre, ' ', nc.apellido_paterno, ' ', nc.apellido_materno) AS nombre_cliente
        FROM CLIENTE c
        JOIN NOMBRES_CLIENTE nc ON c.id_nombre_cliente = nc.id_nombre_cliente
    """)
    clientes = cursor.fetchall()

    cursor.execute("""
        SELECT a.id_administrador, CONCAT(na.nombre, ' ', na.apellido_paterno, ' ', na.apellido_materno) AS nombre_admin
        FROM ADMINISTRADOR a
        JOIN NOMBRES_ADMINISTRADOR na ON a.id_nombre_admin = na.id_nombre_admin
    """)
    administradores = cursor.fetchall()

    cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
    productos = cursor.fetchall()

    conn.close()
    return render_template('añadir_pedido.html', clientes=clientes, administradores=administradores, productos=productos)


@app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_cliente = request.form['id_cliente'].strip()
        id_administrador = request.form['id_administrador'].strip()
        estado = request.form['estado'].strip()
        fecha = request.form['fecha'].strip()
        id_productos = request.form.getlist('id_producto[]')
        cantidades = request.form.getlist('cantidad[]')

        # Validar cliente
        cursor.execute("SELECT COUNT(*) FROM CLIENTE WHERE id_cliente = %s", (id_cliente,))
        if cursor.fetchone()['COUNT(*)'] == 0:
            conn.close()
            return render_template('editar_pedido.html', error="El cliente no existe.")

        # Validar administrador
        cursor.execute("SELECT COUNT(*) FROM ADMINISTRADOR WHERE id_administrador = %s", (id_administrador,))
        if cursor.fetchone()['COUNT(*)'] == 0:
            conn.close()
            return render_template('editar_pedido.html', error="El administrador no existe.")

        # Validar productos
        for id_producto in id_productos:
            cursor.execute("SELECT COUNT(*) FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
            if cursor.fetchone()['COUNT(*)'] == 0:
                conn.close()
                return render_template('editar_pedido.html', error=f"El producto {id_producto} no existe.")

        # Actualizar pedido
        cursor.execute("""
            UPDATE PEDIDO
            SET id_cliente = %s, id_administrador = %s, estado = %s, fecha = %s
            WHERE id_pedido = %s
        """, (id_cliente, id_administrador, estado, fecha, id))

        # Eliminar detalles anteriores
        cursor.execute("DELETE FROM DETALLE_PEDIDO WHERE id_pedido = %s", (id,))

        # Insertar nuevos detalles
        for id_producto, cantidad in zip(id_productos, cantidades):
            if id_producto and cantidad:
                cursor.execute("""
                    INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad)
                    VALUES (%s, %s, %s)
                """, (id, id_producto, cantidad))

        conn.commit()
        conn.close()
        return redirect(url_for('lista_pedidos'))

    # GET: cargar datos del pedido
    cursor.execute("""
        SELECT id_pedido, id_cliente, id_administrador, estado, fecha
        FROM PEDIDO
        WHERE id_pedido = %s
    """, (id,))
    pedido = cursor.fetchone()

    cursor.execute("""
        SELECT id_detalle_pedido, id_producto, cantidad
        FROM DETALLE_PEDIDO
        WHERE id_pedido = %s
    """, (id,))
    detalles = cursor.fetchall()

    # Cargar clientes con nombres
    cursor.execute("""
        SELECT c.id_cliente, CONCAT(nc.nombre, ' ', nc.apellido_paterno, ' ', nc.apellido_materno) AS nombre_cliente
        FROM CLIENTE c
        JOIN NOMBRES_CLIENTE nc ON c.id_nombre_cliente = nc.id_nombre_cliente
    """)
    clientes = cursor.fetchall()

    # Cargar administradores con nombres
    cursor.execute("""
        SELECT a.id_administrador, CONCAT(na.nombre, ' ', na.apellido_paterno, ' ', na.apellido_materno) AS nombre_admin
        FROM ADMINISTRADOR a
        JOIN NOMBRES_ADMINISTRADOR na ON a.id_nombre_admin = na.id_nombre_admin
    """)
    administradores = cursor.fetchall()

    # Cargar productos
    cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
    productos = cursor.fetchall()

    conn.close()

    return render_template('editar_pedido.html',
        pedido={
            'id_pedido': pedido['id_pedido'],
            'id_cliente': pedido['id_cliente'],
            'id_administrador': pedido['id_administrador'],
            'estado': pedido['estado'],
            'fecha': pedido['fecha'],
            'detalles': detalles
        },
        clientes=clientes,
        administradores=administradores,
        productos=productos
    )


@app.route('/eliminar_pedido/<int:id_pedido>', methods=['POST'])
def eliminar_pedido(id_pedido):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Eliminar los detalles del pedido primero (por clave foránea)
        query_detalle = "DELETE FROM DETALLE_PEDIDO WHERE id_pedido = %s"
        cursor.execute(query_detalle, (id_pedido,))
        
        # Eliminar el pedido principal
        query_pedido = "DELETE FROM PEDIDO WHERE id_pedido = %s"
        cursor.execute(query_pedido, (id_pedido,))

        # Confirmar los cambios
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()  # En caso de error, revertir los cambios
        print(f"Error al eliminar el pedido: {err}")
        return {"error": "Hubo un problema al eliminar el pedido. Intenta nuevamente."}, 500
    finally:
        conn.close()

    return {"message": "Pedido eliminado correctamente."}, 200

@app.route('/verificar_categoria/<int:id_categoria>')
def verificar_categoria(id_categoria):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Verificar si la categoría existe
    query = "SELECT COUNT(*) FROM CATEGORIA_PRODUCTO WHERE id_categoria = %s"
    cursor.execute(query, (id_categoria,))
    resultado = cursor.fetchone()

    conn.close()

    # Devolver un resultado como JSON
    return {'existe': resultado[0] > 0}


@app.route('/productos')
def lista_productos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Consultar productos junto con el nombre de su categoría
    query = """
        SELECT 
            p.id_producto,
            p.nombre,
            p.precio,
            p.stock,
            p.descripcion,
            cp.nombre_categoria
        FROM PRODUCTO p
        JOIN CATEGORIA_PRODUCTO cp ON p.id_categoria = cp.id_categoria
        ORDER BY p.id_producto ASC
    """
    cursor.execute(query)
    productos = cursor.fetchall()

    conn.close()

    # Renderizar el template HTML con los datos de los productos
    return render_template('productos.html', productos=[
        {
            'id_producto': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'stock': producto[3],
            'descripcion': producto[4],
            'categoria': producto[5]
        } for producto in productos
    ])


@app.route('/añadir_producto', methods=['GET', 'POST'])
def añadir_producto():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion'].strip()
        id_categoria = request.form['id_categoria'].strip()

        # Validar si la categoría existe
        query_categoria = "SELECT COUNT(*) FROM CATEGORIA_PRODUCTO WHERE id_categoria = %s"
        cursor.execute(query_categoria, (id_categoria,))
        if cursor.fetchone()['COUNT(*)'] == 0:
            # Recargar categorías para mostrar el datalist en caso de error
            cursor.execute("SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO")
            categorias = cursor.fetchall()
            conn.close()
            return render_template('añadir_producto.html', error="El ID de la categoría no existe.", categorias=categorias)

        # Insertar el nuevo producto
        query_producto = """
            INSERT INTO PRODUCTO (nombre, precio, stock, descripcion, id_categoria)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_producto, (nombre, precio, stock, descripcion, id_categoria))
        conn.commit()
        conn.close()

        return redirect(url_for('lista_productos'))

    # GET: cargar categorías para el datalist
    cursor.execute("SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO")
    categorias = cursor.fetchall()
    conn.close()

    return render_template('añadir_producto.html', categorias=categorias)


@app.route('/editar_producto/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion'].strip()
        id_categoria = request.form['id_categoria'].strip()

        # Validar si la categoría existe
        cursor.execute("SELECT COUNT(*) FROM CATEGORIA_PRODUCTO WHERE id_categoria = %s", (id_categoria,))
        if cursor.fetchone()['COUNT(*)'] == 0:
            # Recargar categorías para el datalist
            cursor.execute("SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO")
            categorias = cursor.fetchall()
            conn.close()
            return render_template('editar_producto.html',
                error="El ID de la categoría no existe.",
                producto={
                    'id_producto': id_producto,
                    'nombre': nombre,
                    'precio': precio,
                    'stock': stock,
                    'descripcion': descripcion,
                    'id_categoria': id_categoria
                },
                categorias=categorias
            )

        # Actualizar el producto
        cursor.execute("""
            UPDATE PRODUCTO
            SET nombre = %s, precio = %s, stock = %s, descripcion = %s, id_categoria = %s
            WHERE id_producto = %s
        """, (nombre, precio, stock, descripcion, id_categoria, id_producto))

        conn.commit()
        conn.close()
        return redirect(url_for('lista_productos'))

    # GET: cargar datos del producto
    cursor.execute("""
        SELECT id_producto, nombre, precio, stock, descripcion, id_categoria
        FROM PRODUCTO
        WHERE id_producto = %s
    """, (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        conn.close()
        return "Producto no encontrado", 404

    # Cargar categorías para el datalist
    cursor.execute("SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO")
    categorias = cursor.fetchall()

    conn.close()

    return render_template('editar_producto.html',
        producto=producto,
        categorias=categorias
    )

@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Verificar si el producto existe
    cursor.execute("SELECT nombre FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    # Verificar si el producto está vinculado a algún pedido
    cursor.execute("SELECT COUNT(*) FROM DETALLE_PEDIDO WHERE id_producto = %s", (id_producto,))
    vinculaciones = cursor.fetchone()['COUNT(*)']

    if vinculaciones > 0:
        conn.close()
        return jsonify({
            "error": f"No se puede eliminar el producto '{producto['nombre']}' porque está vinculado a {vinculaciones} pedido(s)."
        }), 409

    # Eliminar el producto
    cursor.execute("DELETE FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": f"Producto '{producto['nombre']}' eliminado correctamente."}), 200



@app.route('/verificar_nombre_categoria/<string:nombre_categoria>')
def verificar_nombre_categoria(nombre_categoria):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Validar si el nombre ya existe en la base de datos
    query = "SELECT COUNT(*) FROM CATEGORIA_PRODUCTO WHERE nombre_categoria = %s"
    cursor.execute(query, (nombre_categoria,))
    resultado = cursor.fetchone()

    conn.close()

    # Devolver el resultado como JSON
    return {'existe': resultado[0] > 0}


@app.route('/categorias')
def lista_categorias():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Consultar los datos y ordenarlos por id_categoria en orden ascendente
    query = "SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO ORDER BY id_categoria ASC"
    cursor.execute(query)
    categorias = cursor.fetchall()
    
    conn.close()
    
    # Renderizar el template HTML con los datos de las categorías
    return render_template('categorias.html', categorias=[
        {
            'id_categoria': categoria[0],
            'nombre_categoria': categoria[1]
        } for categoria in categorias
    ])

@app.route('/añadir_categoria', methods=['GET', 'POST'])
def añadir_categoria():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_categoria = request.form['nombre_categoria'].strip()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Validar si el nombre ya existe
        query_verificar = "SELECT COUNT(*) FROM CATEGORIA_PRODUCTO WHERE nombre_categoria = %s"
        cursor.execute(query_verificar, (nombre_categoria,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return render_template('añadir_categoria.html', error="El nombre de la categoría ya existe.")

        # Insertar la nueva categoría
        query_insertar = "INSERT INTO CATEGORIA_PRODUCTO (nombre_categoria) VALUES (%s)"
        cursor.execute(query_insertar, (nombre_categoria,))

        conn.commit()
        conn.close()

        # Redirigir a la lista de categorías
        return redirect(url_for('lista_categorias'))

    # Si es una solicitud GET, renderizar el formulario vacío
    return render_template('añadir_categoria.html')

@app.route('/editar_categoria/<int:id_categoria>', methods=['GET', 'POST'])
def editar_categoria(id_categoria):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_categoria = request.form['nombre_categoria'].strip()

        # Validar si el nombre ya existe y no es el mismo
        query_verificar = """
            SELECT COUNT(*)
            FROM CATEGORIA_PRODUCTO
            WHERE nombre_categoria = %s AND id_categoria != %s
        """
        cursor.execute(query_verificar, (nombre_categoria, id_categoria))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return render_template('editar_categoria.html', error="El nombre de la categoría ya existe.",
                                   categoria={'id_categoria': id_categoria, 'nombre_categoria': nombre_categoria})

        # Actualizar la categoría en la base de datos
        query_actualizar = "UPDATE CATEGORIA_PRODUCTO SET nombre_categoria = %s WHERE id_categoria = %s"
        cursor.execute(query_actualizar, (nombre_categoria, id_categoria))

        conn.commit()
        conn.close()

        # Redirigir a la lista de categorías
        return redirect(url_for('lista_categorias'))

    # Si es GET, cargar los datos de la categoría existente
    query = "SELECT id_categoria, nombre_categoria FROM CATEGORIA_PRODUCTO WHERE id_categoria = %s"
    cursor.execute(query, (id_categoria,))
    categoria = cursor.fetchone()
    conn.close()

    if not categoria:
        return "Categoría no encontrada", 404

    # Renderizar el formulario con los datos actuales
    return render_template('editar_categoria.html', categoria={
        'id_categoria': categoria[0],
        'nombre_categoria': categoria[1]
    })

@app.route('/eliminar_categoria/<int:id_categoria>', methods=['POST'])
def eliminar_categoria(id_categoria):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Eliminar la categoría de la base de datos
        query = "DELETE FROM CATEGORIA_PRODUCTO WHERE id_categoria = %s"
        cursor.execute(query, (id_categoria,))
        
        conn.commit()
        conn.close()

        # Retornar éxito
        return {'mensaje': 'Categoría eliminada correctamente'}, 200
    except Exception as e:
        conn.rollback()
        conn.close()

        # Manejar errores
        return {'mensaje': 'Error al eliminar la categoría: ' + str(e)}, 500

@app.route('/ventas')
def lista_ventas():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Consultar los datos de la tabla VENTAS junto con el nombre del producto
    query = """
        SELECT v.id_venta, p.nombre, v.cantidad, v.fecha, v.hora
        FROM VENTAS v
        JOIN PRODUCTO p ON v.id_producto = p.id_producto
        ORDER BY v.id_venta ASC
    """
    cursor.execute(query)
    ventas = cursor.fetchall()
    conn.close()

    # Renderizar el template sin incluir id_producto
    return render_template('ventas.html', ventas=[
        {
            'id_venta': venta[0],
            'nombre_producto': venta[1],
            'cantidad': venta[2],
            'fecha': venta[3],
            'hora': venta[4]
        } for venta in ventas
    ])

@app.route('/añadir_venta', methods=['GET', 'POST'])
def añadir_venta():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_producto = request.form['id_producto'].strip()
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']
        hora = request.form['hora']

        # Verificar que el producto existe y obtener su stock
        cursor.execute("SELECT nombre, stock FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
            productos = cursor.fetchall()
            conn.close()
            return render_template('añadir_venta.html',
                                   error="El producto ingresado no existe.",
                                   productos=productos,
                                   datos={'id_producto': id_producto, 'cantidad': cantidad, 'fecha': fecha, 'hora': hora})

        stock_actual = producto['stock']
        nombre_producto = producto['nombre']

        # Validar stock suficiente
        if cantidad > stock_actual:
            cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
            productos = cursor.fetchall()
            conn.close()
            return render_template('añadir_venta.html',
                                   error=f"Stock insuficiente para '{nombre_producto}'. Solo hay {stock_actual} unidades disponibles.",
                                   productos=productos,
                                   datos={'id_producto': id_producto, 'cantidad': cantidad, 'fecha': fecha, 'hora': hora})

        # Insertar la venta
        cursor.execute("""
            INSERT INTO VENTAS (id_producto, cantidad, fecha, hora)
            VALUES (%s, %s, %s, %s)
        """, (id_producto, cantidad, fecha, hora))

        # Reducir el stock del producto
        cursor.execute("""
            UPDATE PRODUCTO
            SET stock = stock - %s
            WHERE id_producto = %s
        """, (cantidad, id_producto))

        conn.commit()
        conn.close()
        return redirect(url_for('lista_ventas'))

    # GET: cargar productos para el datalist
    cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
    productos = cursor.fetchall()
    conn.close()

    return render_template('añadir_venta.html', productos=productos)


@app.route('/editar_venta/<int:id_venta>', methods=['GET', 'POST'])
def editar_venta(id_venta):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_producto = request.form['id_producto'].strip()
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']
        hora = request.form['hora']

        # Verificar que el producto existe y obtener su stock
        cursor.execute("SELECT nombre, stock FROM PRODUCTO WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
            productos = cursor.fetchall()
            conn.close()
            return render_template('editar_venta.html',
                                   error="El producto ingresado no existe.",
                                   productos=productos,
                                   venta={'id_venta': id_venta, 'id_producto': id_producto, 'cantidad': cantidad, 'fecha': fecha, 'hora': hora})

        stock_actual = producto['stock']
        nombre_producto = producto['nombre']

        # Validar stock suficiente
        if cantidad > stock_actual:
            cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
            productos = cursor.fetchall()
            conn.close()
            return render_template('editar_venta.html',
                                   error=f"Stock insuficiente para '{nombre_producto}'. Solo hay {stock_actual} unidades disponibles.",
                                   productos=productos,
                                   venta={'id_venta': id_venta, 'id_producto': id_producto, 'cantidad': cantidad, 'fecha': fecha, 'hora': hora})

        # Actualizar la venta
        cursor.execute("""
            UPDATE VENTAS
            SET id_producto = %s, cantidad = %s, fecha = %s, hora = %s
            WHERE id_venta = %s
        """, (id_producto, cantidad, fecha, hora, id_venta))

        conn.commit()
        conn.close()
        return redirect(url_for('lista_ventas'))

    # GET: cargar datos de la venta y productos
    cursor.execute("SELECT id_venta, id_producto, cantidad, fecha, hora FROM VENTAS WHERE id_venta = %s", (id_venta,))
    venta = cursor.fetchone()

    if not venta:
        conn.close()
        return "Venta no encontrada", 404

    cursor.execute("SELECT id_producto, nombre FROM PRODUCTO")
    productos = cursor.fetchall()
    conn.close()

    return render_template('editar_venta.html',
                           venta={
                               'id_venta': venta['id_venta'],
                               'id_producto': venta['id_producto'],
                               'cantidad': venta['cantidad'],
                               'fecha': venta['fecha'],
                               'hora': venta['hora']
                           },
                           productos=productos)



@app.route('/eliminar_venta/<int:id_venta>', methods=['POST'])
def eliminar_venta(id_venta):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Eliminar la venta de la base de datos
        query = "DELETE FROM VENTAS WHERE id_venta = %s"
        cursor.execute(query, (id_venta,))
        
        conn.commit()
        conn.close()

        # Retornar éxito
        return {'mensaje': 'Venta eliminada correctamente'}, 200
    except Exception as e:
        conn.rollback()
        conn.close()

        # Manejar errores
        return {'mensaje': 'Error al eliminar la venta: ' + str(e)}, 500

@app.route("/reporte", methods=["GET"])
def reporte_formulario():
    return render_template("reporte.html")

@app.route("/ver_grafico", methods=["GET"])
def ver_grafico():
    from flask import request, Response
    import matplotlib.pyplot as plt
    import pandas as pd
    import mysql.connector
    import io

    try:
        # Recibir los parámetros desde el frontend
        tipo = request.args.get("tipo")  # Tipo de gráfico
        fecha_inicio = request.args.get("fecha_inicio", None)  # Fecha inicial (solo para Ventas)
        fecha_fin = request.args.get("fecha_fin", None)  # Fecha final (solo para Ventas)

        print(f"Recibido tipo: {tipo}, Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}")  # Depuración

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        print("Conexión exitosa")  # Depuración de conexión

        # Generar el gráfico según el tipo de reporte
        if tipo == "productos_mas_vendidos":
            # Consulta para productos más vendidos
            query = """
            SELECT P.nombre AS producto, SUM(V.cantidad) AS total_vendidos
            FROM VENTAS V
            JOIN PRODUCTO P ON V.id_producto = P.id_producto
            GROUP BY P.nombre
            ORDER BY total_vendidos DESC
            LIMIT 10;
            """
            print("Ejecutando consulta para productos más vendidos")  # Depuración
            df = pd.read_sql(query, conn)

            if df.empty:  # Si no hay datos
                print("No hay datos disponibles para productos más vendidos.")
                conn.close()
                return "No hay datos disponibles para mostrar el gráfico", 404

            # Crear el gráfico
            plt.figure(figsize=(8, 5))
            df.plot(kind="bar", x="producto", y="total_vendidos", legend=False, color="blue")
            plt.title("Top 10 Productos Más Vendidos")
            plt.xlabel("Producto")
            plt.ylabel("Cantidad Vendida")

        elif tipo == "ventas":
            # Validación de fechas
            if not fecha_inicio or not fecha_fin:
                conn.close()
                return "Por favor, proporcione el rango de fechas.", 400

            # Consulta para ventas por fecha
            query = f"""
            SELECT V.fecha AS fecha_venta, P.nombre AS producto, SUM(V.cantidad) AS cantidad_vendida
            FROM VENTAS V
            JOIN PRODUCTO P ON V.id_producto = P.id_producto
            WHERE V.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            GROUP BY V.fecha, P.nombre
            ORDER BY V.fecha ASC;
            """
            print(f"Ejecutando consulta para ventas entre {fecha_inicio} y {fecha_fin}")  # Depuración
            df = pd.read_sql(query, conn)

            if df.empty:  # Si no hay datos
                print(f"No hay datos disponibles para ventas entre {fecha_inicio} y {fecha_fin}.")
                conn.close()
                return "No hay datos disponibles para mostrar el gráfico", 404

            # Crear el gráfico
            plt.figure(figsize=(8, 5))
            df.groupby("fecha_venta")["cantidad_vendida"].sum().plot(kind="line", legend=False, color="green")
            plt.title(f"Ventas desde {fecha_inicio} hasta {fecha_fin}")
            plt.xlabel("Fecha de Venta")
            plt.ylabel("Cantidad Vendida")

        else:
            conn.close()
            return "Tipo de gráfico no válido.", 400

        # Ajustar diseño y guardar el gráfico en memoria
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        conn.close()

        # Enviar el gráfico como respuesta
        return Response(buf.getvalue(), mimetype="image/png")

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
        return f"Hubo un error al generar el gráfico: {e}", 500


@app.route("/reporte", methods=["POST"])
def reporte():
    from flask import send_file
    import matplotlib.pyplot as plt
    import os
    from fpdf import FPDF
    import pandas as pd
    import io
    import zipfile
    import mysql.connector

    try:
        # Recibir parámetros del formulario
        tipo = request.form["tipo"]  # Tipo de reporte: productos_mas_vendidos o ventas
        fecha_inicio = request.form.get("fecha_inicio", None)  # Fecha inicial
        fecha_fin = request.form.get("fecha_fin", None)  # Fecha final
        formato = request.form["formato"]  # Formato de salida (PDF o Excel)

        print(f"Recibido tipo: {tipo}, Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}, Formato: {formato}")  # Depuración

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        print("Conexión exitosa")  # Depuración

        if tipo == "productos_mas_vendidos":
            # Consulta para productos más vendidos
            query = """
            SELECT P.nombre AS producto, SUM(V.cantidad) AS total_vendidos
            FROM VENTAS V
            JOIN PRODUCTO P ON V.id_producto = P.id_producto
            GROUP BY P.nombre
            ORDER BY total_vendidos DESC
            LIMIT 10;
            """
            df = pd.read_sql(query, conn)

        elif tipo == "ventas":
            # Validación de fechas
            if not fecha_inicio or not fecha_fin:
                conn.close()
                return "Por favor, proporcione el rango de fechas.", 400

            # Consulta para ventas por fecha
            query = f"""
            SELECT V.fecha AS fecha_venta, P.nombre AS producto, SUM(V.cantidad) AS cantidad_vendida
            FROM VENTAS V
            JOIN PRODUCTO P ON V.id_producto = P.id_producto
            WHERE V.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            GROUP BY V.fecha, P.nombre
            ORDER BY V.fecha ASC;
            """
            df = pd.read_sql(query, conn)

        else:
            conn.close()
            return "Tipo de reporte no válido.", 400

        if df.empty:
            print("No hay datos disponibles para generar el reporte.")
            conn.close()
            return "No hay datos disponibles para mostrar el reporte.", 404

        # Generar gráfico
        plt.figure(figsize=(8, 5))
        if tipo == "productos_mas_vendidos":
            df.plot(kind="bar", x="producto", y="total_vendidos", legend=False, color="blue")
            plt.title("Top 10 Productos Más Vendidos")
            plt.xlabel("Producto")
            plt.ylabel("Cantidad Vendida")
        elif tipo == "ventas":
            df.groupby("fecha_venta")["cantidad_vendida"].sum().plot(kind="line", legend=False, color="green")
            plt.title(f"Ventas desde {fecha_inicio} hasta {fecha_fin}")
            plt.xlabel("Fecha de Venta")
            plt.ylabel("Cantidad Vendida")
        plt.tight_layout()

        # Guardar gráfico en archivo temporal
        grafico_path = "grafico_temp.png"
        plt.savefig(grafico_path)

        if formato == "pdf":
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            
            # Primera página: Gráfico
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Reporte de Ventas - Gráfico", ln=True, align="C")
            pdf.image(grafico_path, x=10, y=30, w=180)

            # Segunda página: Datos Tabulares en tabla horizontal
            pdf.add_page(orientation="L")  # Cambiar a orientación horizontal
            pdf.set_font("Arial", size=10)
            pdf.cell(275, 10, txt="Reporte de Ventas - Datos Tabulares", ln=True, align="C")
            pdf.ln(10)  # Salto de línea

            # Encabezados de la tabla
            pdf.set_font("Arial", style='B', size=10)
            col_width = 90  # Ancho de columna ajustado
            for header in df.columns:
                pdf.cell(col_width, 10, txt=header, border=1, align="C")
            pdf.ln(10)  # Salto de línea

            # Filas de la tabla
            pdf.set_font("Arial", size=10)
            for _, row in df.iterrows():
                for value in row:
                    pdf.cell(col_width, 10, txt=str(value), border=1, align="C")
                pdf.ln(10)  # Salto de línea

            pdf_path = "reporte.pdf"
            pdf.output(pdf_path)

            # Limpiar archivo temporal del gráfico
            os.remove(grafico_path)
            conn.close()
            return send_file(pdf_path, as_attachment=True)

        elif formato == "excel":
            buffer_excel = io.BytesIO()
            df.to_excel(buffer_excel, index=False, sheet_name="Reporte")
            buffer_excel.seek(0)

            buffer_grafico = io.BytesIO()
            plt.savefig(buffer_grafico, format="png")
            buffer_grafico.seek(0)

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                zf.writestr("reporte.xlsx", buffer_excel.getvalue())
                zf.writestr("grafico.png", buffer_grafico.getvalue())
            zip_buffer.seek(0)

            os.remove(grafico_path)
            conn.close()
            return send_file(zip_buffer, download_name="reporte_con_grafico.zip", as_attachment=True)

    except Exception as e:
        print(f"Error al generar el reporte: {e}")
        return f"Hubo un error al generar el reporte: {e}", 500



if __name__ == '__main__':
    app.run(debug=True)
