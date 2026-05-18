-- =========================
-- CREATION BASE DRIVE
-- =========================

CREATE DATABASE IF NOT EXISTS drive;
USE drive;

-- =========================
-- TABLE CATEGORIES
-- =========================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    descriptif TEXT
);

-- =========================
-- TABLE PRODUITS
-- =========================

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    date_peremption DATE,
    photo VARCHAR(255),
    marque VARCHAR(100),
    prix DECIMAL(10,2) NOT NULL,
    categorie_id INT NOT NULL,

    FOREIGN KEY (categorie_id)
    REFERENCES categories(id)
    ON DELETE CASCADE
);

-- =========================
-- TABLE CLIENTS
-- =========================

CREATE TABLE clients (
    numero_client INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_inscription DATE NOT NULL,
    adresse TEXT NOT NULL
);

-- =========================
-- TABLE COMMANDES
-- =========================

CREATE TABLE commandes (
    numero_commande INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id)
    REFERENCES clients(numero_client)
    ON DELETE CASCADE
);

-- =========================
-- TABLE LIGNES COMMANDE
-- =========================

CREATE TABLE lignes_commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL,

    FOREIGN KEY (commande_id)
    REFERENCES commandes(numero_commande)
    ON DELETE CASCADE,

    FOREIGN KEY (produit_id)
    REFERENCES produits(id)
    ON DELETE CASCADE
);

-- =========================
-- INSERTION CATEGORIES
-- =========================

INSERT INTO categories (nom, descriptif) VALUES
('Boissons', 'Boissons fraiches'),
('Fruits', 'Fruits frais'),
('Snacks', 'Produits aperitif');

-- =========================
-- INSERTION PRODUITS
-- =========================

INSERT INTO produits
(nom, date_peremption, photo, marque, prix, categorie_id)
VALUES
('Coca Cola 1L', '2026-12-31', 'coca.jpg', 'Coca Cola', 2.50, 1),
('Jus Orange', '2026-10-15', 'jus.jpg', 'Tropicana', 3.20, 1),
('Pommes Golden', '2026-06-15', 'pommes.jpg', 'Vergers France', 1.99, 2),
('Chips Nature', '2026-09-01', 'chips.jpg', 'Lays', 2.10, 3);

-- =========================
-- INSERTION CLIENTS
-- =========================

INSERT INTO clients
(nom, prenom, date_inscription, adresse)
VALUES
('Dupont', 'Jean', '2026-01-10', '12 rue des Fleurs Mulhouse'),
('Martin', 'Claire', '2026-02-15', '5 avenue de Colmar Mulhouse'),
('Bernard', 'Lucas', '2026-03-20', '8 rue des Vosges Colmar');

-- =========================
-- INSERTION COMMANDES
-- =========================

INSERT INTO commandes (client_id)
VALUES
(1),
(2);

-- =========================
-- INSERTION LIGNES COMMANDE
-- =========================

INSERT INTO lignes_commande
(commande_id, produit_id, quantite)
VALUES
(1, 1, 2),
(1, 3, 5),
(2, 2, 1),
(2, 4, 3);

-- =========================
-- AFFICHAGE FICHE COMMANDE
-- =========================

SELECT
    c.numero_commande,
    cl.nom,
    cl.prenom,
    p.nom AS produit,
    p.prix,
    lc.quantite,
    (p.prix * lc.quantite) AS total_ligne
FROM lignes_commande lc
JOIN commandes c
ON lc.commande_id = c.numero_commande

JOIN clients cl
ON c.client_id = cl.numero_client

JOIN produits p
ON lc.produit_id = p.id

WHERE c.numero_commande = 1;


-- ╔════════════════════════════════════════════════════════════════════════════╗
-- ║                         CRUD COMPLETS SQL                                  ║
-- ╚════════════════════════════════════════════════════════════════════════════╝


-- ════════════════════════════════════════════════════════════════════════════
-- 🧩 CRUD — CATÉGORIES
-- ════════════════════════════════════════════════════════════════════════════

-- ➕ CREATE CATEGORIE
-- INSERT INTO categories (nom, descriptif)
-- VALUES ('Boissons', 'Sodas et boissons fraîches');

-- 📖 READ ALL CATEGORIES
-- SELECT * FROM categories;

-- 📖 READ BY ID
-- SELECT * FROM categories WHERE id = 1;

-- ✏️ UPDATE CATEGORIE
-- UPDATE categories
-- SET nom = 'Boissons froides',
--     descriptif = 'Sodas, jus, eaux'
-- WHERE id = 1;

-- ❌ DELETE CATEGORIE
-- DELETE FROM categories
-- WHERE id = 1;


-- ════════════════════════════════════════════════════════════════════════════
-- 📦 CRUD — PRODUITS
-- ════════════════════════════════════════════════════════════════════════════

-- ➕ CREATE PRODUIT
-- INSERT INTO produits (nom, date_peremption, photo, marque, prix, categorie_id)
-- VALUES ('Coca 1L', '2026-12-31', 'coca.jpg', 'Coca Cola', 2.50, 1);

-- 📖 READ ALL PRODUITS
-- SELECT * FROM produits;

-- 📖 READ ALL PRODUITS AVEC CATEGORIE
-- SELECT p.*, c.nom AS categorie
-- FROM produits p
-- JOIN categories c ON p.categorie_id = c.id;

-- 📖 READ PRODUIT BY ID
-- SELECT * FROM produits WHERE id = 1;

-- ✏️ UPDATE PRODUIT
-- UPDATE produits
-- SET nom = 'Coca Zero',
--     prix = 2.70
-- WHERE id = 1;

-- ❌ DELETE PRODUIT
-- DELETE FROM produits
-- WHERE id = 1;


-- ════════════════════════════════════════════════════════════════════════════
-- 👤 CRUD — CLIENTS
-- ════════════════════════════════════════════════════════════════════════════

-- ➕ CREATE CLIENT
-- INSERT INTO clients (nom, prenom, date_inscription, adresse)
-- VALUES ('Dupont', 'Jean', '2026-01-10', '12 rue des Fleurs');

-- 📖 READ ALL CLIENTS
-- SELECT * FROM clients;

-- 📖 READ CLIENT BY ID
-- SELECT * FROM clients WHERE numero_client = 1;

-- ✏️ UPDATE CLIENT
-- UPDATE clients
-- SET adresse = '5 avenue de Colmar'
-- WHERE numero_client = 1;

-- ❌ DELETE CLIENT
-- DELETE FROM clients
-- WHERE numero_client = 1;


-- ════════════════════════════════════════════════════════════════════════════
-- 🧾 CRUD — COMMANDES
-- ════════════════════════════════════════════════════════════════════════════

-- ➕ CREATE COMMANDE
-- INSERT INTO commandes (client_id)
-- VALUES (1);

-- 📖 READ ALL COMMANDES
-- SELECT * FROM commandes;

-- 📖 READ COMMANDES AVEC CLIENT
-- SELECT c.numero_commande, cl.nom, cl.prenom, c.date_commande
-- FROM commandes c
-- JOIN clients cl ON c.client_id = cl.numero_client;

-- 📖 READ COMMANDE BY ID
-- SELECT * FROM commandes WHERE numero_commande = 1;

-- ✏️ UPDATE COMMANDE
-- UPDATE commandes
-- SET client_id = 2
-- WHERE numero_commande = 1;

-- ❌ DELETE COMMANDE
-- DELETE FROM commandes
-- WHERE numero_commande = 1;


-- ════════════════════════════════════════════════════════════════════════════
-- 🧮 CRUD — LIGNES DE COMMANDE
-- ════════════════════════════════════════════════════════════════════════════

-- ➕ CREATE LIGNE COMMANDE
-- INSERT INTO lignes_commande (commande_id, produit_id, quantite)
-- VALUES (1, 2, 3);

-- 📖 READ ALL LIGNES COMMANDE
-- SELECT * FROM lignes_commande;

-- 📖 READ DETAIL COMMANDE
-- SELECT lc.*, p.nom, p.prix
-- FROM lignes_commande lc
-- JOIN produits p ON lc.produit_id = p.id;

-- 📖 READ LIGNES BY COMMANDE ID
-- SELECT lc.*, p.nom, p.prix
-- FROM lignes_commande lc
-- JOIN produits p ON lc.produit_id = p.id
-- WHERE lc.commande_id = 1;

-- ✏️ UPDATE LIGNE COMMANDE
-- UPDATE lignes_commande
-- SET quantite = 5
-- WHERE id = 1;

-- ❌ DELETE LIGNE COMMANDE
-- DELETE FROM lignes_commande
-- WHERE id = 1;


-- ════════════════════════════════════════════════════════════════════════════
-- 📊 QUERIES AVANCÉES
-- ════════════════════════════════════════════════════════════════════════════

-- 💰 Montant total par commande
-- SELECT 
--     c.numero_commande,
--     cl.nom,
--     cl.prenom,
--     SUM(p.prix * lc.quantite) AS montant_total
-- FROM lignes_commande lc
-- JOIN commandes c ON lc.commande_id = c.numero_commande
-- JOIN clients cl ON c.client_id = cl.numero_client
-- JOIN produits p ON lc.produit_id = p.id
-- GROUP BY c.numero_commande, cl.nom, cl.prenom;

-- 🏆 Produit le plus commandé
-- SELECT 
--     p.nom,
--     SUM(lc.quantite) AS total_vendu
-- FROM lignes_commande lc
-- JOIN produits p ON lc.produit_id = p.id
-- GROUP BY p.nom
-- ORDER BY total_vendu DESC;

-- 👨‍💼 Clients avec nombre de commandes
-- SELECT 
--     cl.numero_client,
--     cl.nom,
--     cl.prenom,
--     COUNT(c.numero_commande) AS nombre_commandes
-- FROM clients cl
-- LEFT JOIN commandes c ON cl.numero_client = c.client_id
-- GROUP BY cl.numero_client, cl.nom, cl.prenom;
