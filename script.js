const formulario = document.getElementById("formProducto");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaProductos");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function(e){

    e.preventDefault();

    if(nombre.value.trim()==="" ||
       descripcion.value.trim()==="" ||
       categoria.value.trim()===""){

        mensaje.innerHTML =
        "<div class='alert alert-danger'>Todos los campos son obligatorios.</div>";

        return;
    }

    mensaje.innerHTML =
    "<div class='alert alert-success'>Producto agregado correctamente.</div>";

    const tarjeta = document.createElement("div");

    tarjeta.className = "card p-3 mt-3";

    tarjeta.innerHTML = `
        <h5>${nombre.value}</h5>

        <p>${descripcion.value}</p>

        <span class="badge bg-primary">${categoria.value}</span>

        <br><br>

        <button class="btn btn-danger eliminar">
            Eliminar
        </button>
    `;

    lista.appendChild(tarjeta);

    contador++;

    total.textContent = contador;

    tarjeta.querySelector(".eliminar").addEventListener("click", function(){

        tarjeta.remove();

        contador--;

        total.textContent = contador;

    });

    formulario.reset();

});