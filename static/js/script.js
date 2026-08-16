// ===============================
// ELEMENTOS DEL DOM
// ===============================

const formulario = document.getElementById("formProducto");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");
const spinner = document.getElementById("spinner");

// ===============================
// MODAL PRODUCTO REGISTRADO
// ===============================

const elementoModal = document.getElementById("modalRegistro");

let modal = null;

if (elementoModal) {
    modal = new bootstrap.Modal(elementoModal);
}

// ===============================
// ARREGLO DE PRODUCTOS
// ===============================

let productos = [
    {
        nombre: "Vestidos de Moda",
        descripcion: "Diseños modernos inspirados en las últimas tendencias.",
        categoria: "Ropa"
    },
    {
        nombre: "Maquillaje",
        descripcion: "Productos ideales para uso diario y ocasiones especiales.",
        categoria: "Maquillaje"
    },
    {
        nombre: "Accesorios",
        descripcion: "Complementos para destacar tu estilo personal.",
        categoria: "Accesorios"
    }
];

// ===============================
// MOSTRAR PRODUCTOS DINÁMICAMENTE
// ===============================

function mostrarProductos() {

    const contenedor = document.getElementById("contenedorProductos");

    // Comprobar que el contenedor existe
    if (!contenedor) {
        return;
    }

    contenedor.innerHTML = "";

    if (productos.length === 0) {

        contenedor.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning">
                    No existen productos registrados.
                </div>
            </div>
        `;

        if (total) {
            total.textContent = "0";
        }

        return;
    }

    productos.forEach(producto => {

        contenedor.innerHTML += `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 shadow">

                    <div class="card-body">

                        <h5 class="card-title">
                            ${producto.nombre}
                        </h5>

                        <p class="card-text">
                            ${producto.descripcion}
                        </p>

                        <span class="badge bg-primary">
                            ${producto.categoria}
                        </span>

                    </div>

                </div>
            </div>
        `;

    });

    if (total) {
        total.textContent = productos.length;
    }
}

// ===============================
// MOSTRAR PRODUCTOS AL CARGAR
// ===============================

mostrarProductos();

// ===============================
// REGISTRAR PRODUCTO
// ===============================

if (formulario) {

    formulario.addEventListener("submit", function(e) {

        e.preventDefault();

        // Ocultar mensaje anterior
        if (mensaje) {
            mensaje.classList.add("d-none");
        }

        // VALIDACIÓN

        if (
            nombre.value.trim() === "" ||
            descripcion.value.trim() === "" ||
            categoria.value === ""
        ) {

            if (mensaje) {

                mensaje.className = "alert alert-danger mt-3";

                mensaje.textContent =
                    "Todos los campos son obligatorios.";

                mensaje.classList.remove("d-none");
            }

            return;
        }

        // Mostrar spinner

        if (spinner) {
            spinner.classList.remove("d-none");
        }

        // Simulación de carga

        setTimeout(function() {

            if (spinner) {
                spinner.classList.add("d-none");
            }

            // Crear producto nuevo

            let nuevoProducto = {
                nombre: nombre.value.trim(),
                descripcion: descripcion.value.trim(),
                categoria: categoria.value
            };

            // Agregar producto

            productos.push(nuevoProducto);

            // Actualizar tarjetas

            mostrarProductos();

            // Mostrar mensaje

            if (mensaje) {

                mensaje.className =
                    "alert alert-success mt-3";

                mensaje.textContent =
                    "Producto agregado correctamente.";

                mensaje.classList.remove("d-none");
            }

            // Mostrar modal

            if (modal) {
                modal.show();
            }

            // Limpiar formulario

            formulario.reset();

            // Ocultar alerta después de 3 segundos

            setTimeout(function() {

                if (mensaje) {
                    mensaje.classList.add("d-none");
                }

            }, 3000);

        }, 2000);

    });

}