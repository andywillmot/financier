SELECT q.tyear, q.tmonth, q.tname,
	sum(q.tvalue) as total,
	sum(q.abstvalue) as abstotal,
	to_char(avg(q.tvalue),'FM99999999.00') as average,
	to_char(avg(q.abstvalue),'FM99999999.00') as absaverage
from 
(	SELECT t.date as tdate,
		date_part('month',t.date)as tmonth,
		date_part('year',t.date) as tyear,
		t.title as ttitle,
		t.value as tvalue,
		abs(t.value) as abstvalue,
		(CASE WHEN s.name is Null THEN 'Unknown'
 		ELSE s.name END) as tname
	FROM public.financier_transaction t
	LEFT OUTER JOIN	public.financier_subcategory s
	ON t.subcategory_id = s.id
) q
GROUP BY q.tyear, q.tmonth, q.tname
ORDER BY q.tyear desc, q.tmonth desc
