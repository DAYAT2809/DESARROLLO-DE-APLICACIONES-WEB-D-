from flask import Flask, render_template

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-girls-2026"


@app.route("/")
def inicio():
    nombre_tienda = "GIRLS"

    return render_template(
        "index.html",
        nombre_tienda=nombre_tienda
    )


@app.route("/productos", methods=["GET", "POST"])
def productos():
    form = ProductoForm()

    productos = [
        {
            "nombre": "Blusa Rosada",
            "precio": 25.00,
            "stock": 8,
            "categoria": "Ropa"
        },
        {
            "nombre": "Vestido Celeste",
            "precio": 35.00,
            "stock": 4,
            "categoria": "Ropa"
        },
        {
            "nombre": "Labial Nude",
            "precio": 12.50,
            "stock": 0,
            "categoria": "Maquillaje"
        },
        {
            "nombre": "Gloss Rosado",
            "precio": 10.00,
            "stock": 6,
            "categoria": "Maquillaje"
        }
    ]

    if form.validate_on_submit():
        nuevo_producto = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "precio": form.precio.data,
            "stock": form.stock.data,
            "categoria": "Sin categoría"
    }

        productos.append(nuevo_producto)

    return render_template(
        "productos.html",
        productos=productos,
        form=form
    )


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


@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    form = ProveedorForm()

    proveedores = [
        {
            "id": "001",
            "nombre": "Moda Trend S.A.",
            "producto": "Ropa",
            "contacto": "0981234567",
            "ciudad": "Quito"
        },
        {
            "id": "002",
            "nombre": "Bella Cosmetics",
            "producto": "Maquillaje",
            "contacto": "0992345678",
            "ciudad": "Guayaquil"
        },
        {
            "id": "003",
            "nombre": "Style Accessories",
            "producto": "Accesorios",
            "contacto": "0973456789",
            "ciudad": "Cuenca"
        }
    ]

    if form.validate_on_submit():

        nuevo_proveedor = {
            "id": str(len(proveedores) + 1).zfill(3),
            "nombre": form.nombre.data,
            "producto": form.empresa.data,
            "contacto": form.telefono.data,
            "ciudad": form.email.data
        }

        proveedores.append(nuevo_proveedor)

    return render_template(
        "proveedores.html",
        proveedores=proveedores,
        form=form
    )

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

if __name__ == "__main__":
    app.run(debug=True)