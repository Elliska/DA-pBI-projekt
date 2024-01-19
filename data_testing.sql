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
	COUNT(YEAR(datum)) 
FROM factData fd 
WHERE stanice = 'L2PRIM01'
GROUP BY YEAR (datum);
;

DELETE FROM factData WHERE stanice = 'L2PRIM01';