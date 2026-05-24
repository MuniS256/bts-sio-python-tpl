--Exercice 1

CREATE TABLE Joueur (
    id_joueur INT PRIMARY KEY,
    pseudo TEXT,
    niveau INTEGER,
    score INTEGER
);

--Exercice 2

CREATE TABLE Arme (
    id_arme INT PRIMARY KEY,
    nom TEXT,
    degats INTEGER
    rarete TEXT
)

--Exercice 3
INSERT INTO Joueur (pseudo, niveau, score) VALUES 
('DragonMordu', 10, 1500),
('NoobAndSpirit', 1, 50),
('ShadowGunners', 25, 4500),
('PandaRoux', 12, 2100),
('LynxRapide', 8, 1250);

--Exercice 4
CREATE TABLE armes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    rarete TEXT
);

INSERT INTO armes (nom, rarete) VALUES 
('Épée en bois', 'commun'),
('Arc long', 'rare'),
('Hache de guerre', 'épique'),
('Bâton magique', 'rare'),
('Dague empoisonnée', 'épique');

--Exercice 5
SELECT * FROM joueur;

--Exercice 6
SELECT pseudo, score FROM joueur;

--Exercice 7
SELECT * FROM joueur
WHERE niveau > 5;

--Exercice 8
SELECT * FROM joueur 
ORDER BY score DESC;

--Exercice 9

DROP TABLE joueurs;

CREATE TABLE joueurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT,
    niveau INTEGER,
    score INTEGER
);

INSERT INTO joueurs (pseudo, niveau, score) VALUES 
('DragonMordu', 10, 1500),    -- Sera l'ID 1
('NoobAndSpirit', 1, 50),     -- Sera l'ID 2
('ShadowGunners', 25, 4500),  -- Sera l'ID 3
('PandaRoux', 12, 2100),      -- Sera l'ID 4
('LynxRapide', 8, 1250);      -- Sera l'ID 5
UPDATE joueurs
SET score = score + 500 
WHERE id = 3;

--Exercice 10
UPDATE joueurs 
SET niveau = niveau + 1;

--Il applique directement par défaut, il est possible alors de le faire en 1 ligne

--Exercice 11
DELETE FROM joueurs 
WHERE score < 100;

--C'est dangereux car on ne peut pas retourner en arrière, il est préférable de faire une sauvegarde avant de faire ce genre d'opération.

--Exercice 12
SELECT * FROM joueurs 
ORDER BY score DESC 
LIMIT 3;

--Exercice 13
SELECT * FROM joueurs 
WHERE score > 1000 
AND niveau > 3;

--Exercice 14
SELECT * FROM armes 
WHERE rarete = 'rare' 
OR rarete = 'épique';

--Il met les armes de la table "joueur" et de la table "joueurs"

--Exercice 15
ALTER TABLE armes ADD COLUMN degats INTEGER;

UPDATE armes SET degats = 80 WHERE nom = 'Hache de guerre';
UPDATE armes SET degats = 45 WHERE nom = 'Arc long';
UPDATE armes SET degats = 15 WHERE nom = 'Épée en bois';
UPDATE armes SET degats = 60 WHERE nom = 'Bâton magique';
UPDATE armes SET degats = 55 WHERE nom = 'Dague empoisonnée';
SELECT * FROM armes 
ORDER BY degats DESC 
LIMIT 1;

--Bonus 1
INSERT INTO joueurs (pseudo, niveau, score) 
VALUES ('AdminBossProf', 99, 99999);

--Bonus 2
DELETE FROM joueurs 
WHERE niveau = 1;

--Bonus 3
SELECT * FROM joueurs 
ORDER BY niveau DESC, score DESC;

--Bonus 4
INSERT INTO armes (nom, rarete, degats) 
VALUES ('Lame de la mort qui tue', 'légendaire', 150);

--Réponse Réflexion

-- 1- INSERT sert à rajouter une valeur à une variable.
-- 2- UPDATE sert à modifier une valeur d'une variable / DELETE sert à supprimer une valeur d'une variable.
-- 3- WHERE est important car il permet de cibler une ligne précise, sans lui on pourrait faire des modifications sur toutes les lignes d'une table.
-- 4- SQL est utile en développement en général, il permet de stocker des données de manière structurée et facilement accessible, ce qui est essentiel pour la plupart des applications modernes.