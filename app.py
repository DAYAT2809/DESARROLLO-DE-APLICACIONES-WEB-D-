from flask import Flask, render_template, request, redirect, url_for, flash

import os

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion, obtener_cursor

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from models import Usuario


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-girls-2026"

# =========================
# CREAR TABLAS EN POSTGRESQL
# =========================

def crear_tablas_postgresql():

    if not os.getenv("DATABASE_URL"):
        return

    try:

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                empresa VARCHAR(100),
                email VARCHAR(100),
                telefono VARCHAR(20)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                precio DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL,
                id_proveedor INT,
                id_usuario INT,
                FOREIGN KEY (id_proveedor)
                    REFERENCES proveedores(id_proveedor),
                FOREIGN KEY (id_usuario)
                    REFERENCES usuarios(id)
            )
        """)

        conexion.commit()

        cursor.close()
        conexion.close()

        print("TABLAS DE POSTGRESQL VERIFICADAS CORRECTAMENTE")

    except Exception as e:

        print("ERROR AL CREAR TABLAS POSTGRESQL:", e)

# =========================
# CONFIGURACIÓN LOGIN
# =========================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None

# =========================
# REGISTRO DE USUARIOS
# =========================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            flash(
                "El nombre de usuario ya existe.",
                "danger"
            )

            cursor.close()
            conexion.close()

            return render_template(
                "registro.html",
                form=form
            )

        # Proteger la contraseña mediante hash
        password_hash = generate_password_hash(
            form.password.data
        )

        # Guardar usuario en MySQL
        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = obtener_cursor(conexion)

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["password"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(url_for("inicio"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# =========================
# CERRAR SESIÓN
# =========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))


# =========================
# INICIO
# =========================

@app.route("/")
def inicio():

    nombre_tienda = "GIRLS"

    return render_template(
        "index.html",
        nombre_tienda=nombre_tienda
    )


# =========================
# PRODUCTOS
# =========================

@app.route("/productos", methods=["GET", "POST"])
@login_required
def productos():

    form = ProductoForm()

    # =========================
    # OBTENER PROVEEDORES
    # =========================

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    cursor.execute("""
        SELECT id_proveedor, nombre, empresa
        FROM proveedores
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Crear opciones para el campo proveedor
    form.proveedor.choices = [
        (
            proveedor["id_proveedor"],
            f'{proveedor["nombre"]} - {proveedor["empresa"]}'
        )
        for proveedor in proveedores
    ]

    # =========================
    # AGREGAR PRODUCTO
    # =========================

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                stock,
                id_proveedor,
                id_usuario
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            form.proveedor.data,
            current_user.id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto agregado correctamente.",
            "success"
        )

        return redirect("/productos")

    # =========================
    # MOSTRAR PRODUCTOS
    # =========================

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.id_proveedor,
            p.id_usuario,
            pr.nombre AS proveedor,
            pr.empresa,
            u.usuario AS usuario
        FROM productos p

        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor

        LEFT JOIN usuarios u
            ON p.id_usuario = u.id
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )


# =========================
# EDITAR PRODUCTO
# =========================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    # =========================
    # OBTENER PROVEEDORES
    # =========================

    cursor.execute("""
        SELECT id_proveedor, nombre, empresa
        FROM proveedores
    """)

    proveedores = cursor.fetchall()

    # =========================
    # ACTUALIZAR PRODUCTO
    # =========================

    if request.method == "POST":

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        id_proveedor = request.form["id_proveedor"]

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            nombre,
            descripcion,
            precio,
            stock,
            id_proveedor,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect("/productos")

    # =========================
    # BUSCAR PRODUCTO
    # =========================

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            descripcion,
            precio,
            stock,
            id_proveedor,
            id_usuario
        FROM productos
        WHERE id_producto = %s
    """, (id,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_producto.html",
        producto=producto,
        proveedores=proveedores
    )


# =========================
# ELIMINAR PRODUCTO
# =========================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect("/productos")

# =========================
# USUARIOS
# =========================

@app.route("/usuarios", methods=["GET", "POST"])
@login_required
def usuarios():

    form = UsuarioForm()

    # =========================
    # AGREGAR USUARIO
    # =========================

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            flash(
                "El nombre de usuario ya existe.",
                "danger"
            )

            cursor.close()
            conexion.close()

            return redirect(url_for("usuarios"))

        # Proteger contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario agregado correctamente.",
            "success"
        )

        return redirect(url_for("usuarios"))

    # =========================
    # MOSTRAR USUARIOS
    # =========================

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    cursor.execute("""
        SELECT
            id,
            usuario
        FROM usuarios
        ORDER BY id
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        form=form
    )


# =========================
# EDITAR USUARIO
# =========================

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form.get("password")

        if password:

            password_hash = generate_password_hash(password)

            cursor.execute("""
                UPDATE usuarios
                SET
                    usuario = %s,
                    password = %s
                WHERE id = %s
            """, (
                usuario,
                password_hash,
                id
            ))

        else:

            cursor.execute("""
                UPDATE usuarios
                SET usuario = %s
                WHERE id = %s
            """, (
                usuario,
                id
            ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario actualizado correctamente.",
            "success"
        )

        return redirect(url_for("usuarios"))

    cursor.execute("""
        SELECT
            id,
            usuario
        FROM usuarios
        WHERE id = %s
    """, (id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


# =========================
# ELIMINAR USUARIO
# =========================

@app.route("/usuarios/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_usuario(id):

    # No permitir eliminar el usuario que está conectado
    if int(current_user.id) == id:

        flash(
            "No puedes eliminar el usuario con el que has iniciado sesión.",
            "danger"
        )

        return redirect(url_for("usuarios"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Usuario eliminado correctamente.",
        "success"
    )

    return redirect(url_for("usuarios"))

# =========================
# CLIENTES
# =========================

@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():

    form = ClienteForm()

    clientes = [
        {
            "id": "001",
            "nombre": "Camila Andrade",
            "correo": "camila.andrade@gmail.com",
            "telefono": "0987654321",
            "ciudad": "Quito"
        },
        {
            "id": "002",
            "nombre": "Valentina Torres",
            "correo": "valentina.torres@gmail.com",
            "telefono": "0998765432",
            "ciudad": "Guayaquil"
        },
        {
            "id": "003",
            "nombre": "Sofía Mendoza",
            "correo": "sofia.mendoza@gmail.com",
            "telefono": "0976543210",
            "ciudad": "Cuenca"
        },
        {
            "id": "004",
            "nombre": "Daniela Cárdenas",
            "correo": "daniela.cardenas@gmail.com",
            "telefono": "0965432109",
            "ciudad": "Ambato"
        }
    ]

    if form.validate_on_submit():

        nuevo_cliente = {
            "id": str(len(clientes) + 1).zfill(3),
            "nombre": form.nombre.data,
            "correo": form.email.data,
            "telefono": form.telefono.data,
            "ciudad": form.direccion.data
        }

        clientes.append(nuevo_cliente)

    return render_template(
        "clientes.html",
        clientes=clientes,
        form=form
    )


# =========================
# PROVEEDORES
# =========================

@app.route("/proveedores", methods=["GET", "POST"])
@login_required
def proveedores():

    form = ProveedorForm()

    # =========================
    # AGREGAR PROVEEDOR
    # =========================

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (
                nombre,
                empresa,
                email,
                telefono
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.empresa.data,
            form.email.data,
            form.telefono.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor agregado correctamente.",
            "success"
        )

        return redirect("/proveedores")

    # =========================
    # MOSTRAR PROVEEDORES
    # =========================

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            empresa,
            email,
            telefono
        FROM proveedores
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )

# =========================
# EDITAR PROVEEDOR
# =========================

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()
    cursor = obtener_cursor(conexion)

    # =========================
    # ACTUALIZAR PROVEEDOR
    # =========================

    if request.method == "POST":

        nombre = request.form["nombre"]
        empresa = request.form["empresa"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        cursor.execute("""
            UPDATE proveedores
            SET
                nombre = %s,
                empresa = %s,
                email = %s,
                telefono = %s
            WHERE id_proveedor = %s
        """, (
            nombre,
            empresa,
            email,
            telefono,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    # =========================
    # BUSCAR PROVEEDOR
    # =========================

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            empresa,
            email,
            telefono
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_proveedor.html",
        proveedor=proveedor
    )


# =========================
# ELIMINAR PROVEEDOR
# =========================

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))

# =========================
# FACTURACIÓN
# =========================

@app.route("/facturacion", methods=["GET", "POST"])
@login_required
def facturacion():

    form = FacturacionForm()

    facturas = [
        {
            "numero": "F001-001",
            "cliente": "Camila Andrade",
            "fecha": "15/08/2026",
            "total": 35.00,
            "estado": "Pagada"
        },
        {
            "numero": "F001-002",
            "cliente": "Valentina Torres",
            "fecha": "15/08/2026",
            "total": 25.00,
            "estado": "Pagada"
        },
        {
            "numero": "F001-003",
            "cliente": "Sofía Mendoza",
            "fecha": "14/08/2026",
            "total": 53.00,
            "estado": "Pendiente"
        },
        {
            "numero": "F001-004",
            "cliente": "Daniela Cárdenas",
            "fecha": "13/08/2026",
            "total": 28.00,
            "estado": "Pagada"
        }
    ]

    if form.validate_on_submit():

        total = form.cantidad.data * form.precio.data

        nueva_factura = {
            "numero": f"F001-{len(facturas) + 1:03d}",
            "cliente": form.cliente.data,
            "fecha": "29/08/2026",
            "total": total,
            "estado": "Pendiente"
        }

        facturas.append(nueva_factura)

    return render_template(
        "facturacion.html",
        facturas=facturas,
        form=form
    )


# =========================
# EJECUTAR APLICACIÓN
# =========================

crear_tablas_postgresql()

if __name__ == "__main__":

    crear_tablas_postgresql()

    try:

        conexion = obtener_conexion()

        if os.getenv("DATABASE_URL"):
            print("CONEXIÓN EXITOSA CON POSTGRESQL")
        else:
            print("CONEXIÓN EXITOSA CON MYSQL LOCAL")

        conexion.close()

    except Exception as e:

        print("ERROR DE CONEXIÓN:", e)

    app.run(debug=True)