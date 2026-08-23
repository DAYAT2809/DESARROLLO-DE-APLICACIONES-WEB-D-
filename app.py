from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    nombre_tienda = "GIRLS"

    return render_template(
        "index.html",
        nombre_tienda=nombre_tienda
    )


@app.route("/productos")
def productos():

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

    return render_template(
        "productos.html",
        productos=productos
    )


@app.route("/clientes")
def clientes():

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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/proveedores")
def proveedores():

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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )

@app.route("/facturacion")
def facturacion():

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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


if __name__ == "__main__":
    app.run(debug=True)