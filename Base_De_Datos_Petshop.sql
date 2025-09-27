-- Crear la base de datos PETSHOP
CREATE DATABASE PETSHOP;
USE PETSHOP;

-- Tabla: NOMBRES_ADMINISTRADOR
CREATE TABLE NOMBRES_ADMINISTRADOR (
    id_nombre_admin INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50)
);

-- Tabla: ADMINISTRADOR
CREATE TABLE ADMINISTRADOR (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    id_nombre_admin INT NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(8) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    hora_ingreso TIME NOT NULL,
    hora_salida TIME NOT NULL,
    FOREIGN KEY (id_nombre_admin) REFERENCES NOMBRES_ADMINISTRADOR(id_nombre_admin)
);

-- Tabla: NOMBRES_CLIENTE
CREATE TABLE NOMBRES_CLIENTE (
    id_nombre_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50)
);

-- Tabla: CLIENTE
CREATE TABLE CLIENTE (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    id_nombre_cliente INT NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(8) NOT NULL,
    FOREIGN KEY (id_nombre_cliente) REFERENCES NOMBRES_CLIENTE(id_nombre_cliente)
);

-- Tabla: CATEGORIA_PRODUCTO
CREATE TABLE CATEGORIA_PRODUCTO (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla: PRODUCTO
CREATE TABLE PRODUCTO (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    descripcion TEXT,
    id_categoria INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES CATEGORIA_PRODUCTO(id_categoria)
);

-- Tabla: PEDIDO
CREATE TABLE PEDIDO (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_administrador INT,
    estado ENUM('pendiente', 'aceptado', 'rechazado') NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_administrador) REFERENCES ADMINISTRADOR(id_administrador)
);

-- Tabla: DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    id_detalle_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES PEDIDO(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

-- Tabla: VENTAS
CREATE TABLE VENTAS (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

-- Insertar categorías de productos
INSERT INTO CATEGORIA_PRODUCTO (nombre_categoria) VALUES 
('alimento'),
('farmacia'),
('accesorio');

-- Insertar nombres de administradores
INSERT INTO NOMBRES_ADMINISTRADOR (nombre, apellido_paterno, apellido_materno) VALUES
('Miguel', 'Perez', 'Gomez'),
('Ana', 'Lopez', 'Torres'),
('Carlos', 'Rodriguez', 'Fernandez');

-- Insertar administradores
INSERT INTO ADMINISTRADOR (id_nombre_admin, usuario, contrasena, fecha_ingreso, hora_ingreso, hora_salida) VALUES
(1, 'miguel.perez@petshop.com', 'admin123', '2025-04-24', '08:00:00', '17:00:00'),
(2, 'ana.lopez@petshop.com', 'admin456', '2025-04-24', '09:00:00', '18:00:00'),
(3, 'carlos.rodriguez@petshop.com', 'admin789', '2025-04-24', '10:00:00', '19:00:00');

-- Insertar nombres de clientes
INSERT INTO NOMBRES_CLIENTE (nombre, apellido_paterno, apellido_materno) VALUES
('Maria', 'Lopez', 'Torres'),
('Luis', 'Garcia', 'Martinez'),
('Paula', 'Sanchez', 'Diaz');

-- Insertar clientes
INSERT INTO CLIENTE (id_nombre_cliente, usuario, contrasena) VALUES
(1, 'maria.lopez@gmail.com', 'cliente1'),
(2, 'luis.garcia@gmail.com', 'cliente2'),
(3, 'paula.sanchez@gmail.com', 'cliente3');

-- Insertar productos y categorías
INSERT INTO PRODUCTO (nombre, precio, stock, descripcion, id_categoria) VALUES
('Hop Perro Adulto Raza Mediana y Grande 21kg', 450.00, 5, 'comida perro', 1),
('Lata Agility Perro Sabor Carne 340 gr', 95.10, 4, 'comida perro', 1),
('Excellent Gato Adulto Pollo y Arroz 3 kg', 255.00, 4, 'comida gato', 1),
('Lata Agility Gato Sabor Merluza 340 gr', 55.10, 3, 'comida gato', 1),
('Naturaliss Cobaya Adulta 1,81 Kg Cunipic', 39.00, 4, 'comida roedor', 1),
('Alimentación Súper Premium para Agapornis Cunipic', 39.00, 4, 'comida aves', 1),
('Vivanimals Escamas para peces de agua fría', 35.00, 5, 'comida peces', 1),
('Pipeta Perro Power Ultra de 11 a 20 kg', 35.00, 4, 'medicina perro', 2),
('Antiparasitario Basken Suspensión 15 ml', 38.50, 4, 'medicina gato', 2),
('Comedero Bebedero Con Tolva 15L/700g', 55.00, 3, 'bebedero', 3),
('Juguete para Gato Catnip', 75.00, 3, 'juguete', 3),
('Savic Bebedero para Conejos y roedores Biba', 55.00, 3, 'bebedero', 3),
('Arquivet Jaula Nueva Lugano', 410.20, 2, 'jaula', 3),
('Laguna Bomba Max Flo Sumergible 600/2200', 255.00, 2, 'bomba de agua', 3);

-- Insertar pedidos
INSERT INTO PEDIDO (id_cliente, id_administrador, estado, fecha) VALUES
(1, 1, 'pendiente', '2025-04-20'),
(2, 2, 'aceptado', '2025-04-21'),
(3, 3, 'rechazado', '2025-04-22'),
(1, 3, 'pendiente', '2025-04-23'),
(2, 1, 'aceptado', '2025-04-24');

-- Insertar ventas
INSERT INTO VENTAS (id_producto, cantidad, fecha, hora) VALUES
(1, 2, '2025-04-20', '10:30:00'),
(3, 1, '2025-04-21', '11:00:00'),
(8, 3, '2025-04-22', '12:45:00'),
(10, 4, '2025-04-23', '14:20:00'),
(13, 1, '2025-04-24', '15:10:00');

