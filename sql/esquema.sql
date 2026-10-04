USE girls;

CREATE TABLE IF NOT EXISTS proveedores (

    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    empresa VARCHAR(100),

    email VARCHAR(100),

    telefono VARCHAR(20)

);

CREATE TABLE IF NOT EXISTS productos (

    id_producto INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT,

    precio DECIMAL(10,2) NOT NULL,

    stock INT NOT NULL,

    id_proveedor INT,

    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)

);

CREATE TABLE IF NOT EXISTS usuarios (

    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario VARCHAR(50) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL

);