SELECT * FROM factData fd ;
SELECT * FROM dimStation ;
SELECT * FROM dimDate ;


SELECT 
	stanice,
	COUNT(*) AS pocet_zaznamu
FROM factData fd 
GROUP BY stanice
ORDER BY pocet_zaznamu desc;

SELECT 
	YEAR (datum) ,
	COUNT(YEAR(datum)) AS pocet_dni
FROM factData fd 
WHERE stanice = 'U2LIBC01'
GROUP BY YEAR (datum)
ORDER BY pocet_dni asc
;

SELECT *
FROM factData fd
WHERE stanice IS NULL;

DELETE FROM factData WHERE stanice = 'U2LIBC01';
DELETE FROM dimStation WHERE indikativ_stanice = 'U2LIBC01' AND id_note > 35;