from flask import Flask, render_template, request, redirect

from conexion.conexion import obtener_conexion

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-girls-2026"


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
def productos():

    form = ProductoForm()

    # =========================
    # OBTENER PROVEEDORES
    # =========================

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            form.proveedor.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/productos")

    # =========================
    # MOSTRAR PRODUCTOS
    # =========================

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor,
            pr.empresa
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
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
def editar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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
            id_proveedor
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

    return redirect("/productos")


# =========================
# CLIENTES
# =========================

@app.route("/clientes", methods=["GET", "POST"])
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

        return redirect("/proveedores")

    # =========================
    # MOSTRAR PROVEEDORES
    # =========================

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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
# FACTURACIÓN
# =========================

@app.route("/facturacion", methods=["GET", "POST"])
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

if __name__ == "__main__":

    try:

        conexion = obtener_conexion()

        print("CONEXIÓN EXITOSA CON MYSQL")

        conexion.close()

    except Exception as e:

        print("ERROR DE CONEXIÓN:", e)

    app.run(debug=True)