--Exercice 1 :
CREATE TABLE Joueur (
    id_joueur INTEGER PRIMARY KEY,
    pseudo TEXT,
    niveau INTEGER,
    score INTEGER,
    statut TEXT
)
--Exercice 2:
INSERT INTO Joueur (id_joueur, pseudo, niveau, score, statut) VALUES
(1, 'Shadow', 12, 1500, 'actif'),
(2, 'Titan',8, 1900, 'actif'),
(3, 'Pixel', 4, 700, 'inactif'),
(4, 'Nova', 15, 5200, 'actif'),
(5, 'Ghost', 2, 200, 'suspendu');

--Exercice 3:
INSERT INTO Joueur (id, pseudo, niveau, score, statut) VALUES
(6, 'BlazeMi', 100, 5000, 'actif'),
(7, 'CyberRasta', 120, 4090, 'suspendu'),
(8, 'ZeroLimit', 90, 23400, 'désactivé');

--Exercice 4:
SELECT pseudo FROM Joueur;

SELECT pseudo FROM Joueur
WHERE statut = 'actif';

SELECT pseudo FROM Joueur
WHERE score > 2000;

SELECT pseudo FROM Joueur
ORDER BY score DESC;

--Exercice 5:
SELECT pseudo, score FROM Joueur
ORDER BY score DESC;

--Exercice 6:
UPDATE Joueur
SET score = score + 1000
WHERE id_joueur = 1;

UPDATE Joueur
SET niveau = niveau + 1
WHERE id_joueur = 3;

UPDATE Joueur
SET statut = 'actif'
WHERE id_joueur = 5;


UPDATE Joueur
SET score = score + 300
WHERE niveau < 5;

DELETE FROM Joueur
WHERE statut = 'suspendu';

DELETE FROM Joueur
WHERE score < 500;

SELECT pseudo, niveau FROM Joueur
ORDER BY niveau DESC;

SELECT pseudo, score FROM Joueur 
WHERE score >= 1000 and score <= 4000; 

SELECT pseudo, statut, niveau FROM Joueur 
WHERE statut = 'actif' and niveau > 10;

SELECT pseudo, statut FROM "Joueur"
WHERE statut = 'inactif' OR statut = 'suspendu';

SELECT * FROM "Joueur"

UPDATE "Joueur"
SET score = score + 500
WHERE niveau > 10,

UPDATE "Joueur"
SET statut = 'suspendu'
WHERE score < 300;

DELETE FROM Joueur
WHERE statut = 'inactif'

SELECT * FROM "Joueur"
ORDER BY score DESC
LIMIT 3;

ALTER TABLE Joueur 
ADD COLUMN date_inscription TEXT;