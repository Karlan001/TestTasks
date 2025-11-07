-- Получение информации о сумме товаров заказанных под каждого клиента
select c."name" , sum(n.price) "sum orders", count(n.id) "count orders"
from orders o 
left join clients c on o.client_id = c.id 
left join numenclature n on o.numenclature_id = n.id
group by c."name" 

--Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.
select nc.title, count(nc2.id)
from numenclature_catalog nc 
left join numenclature_catalog nc2 on nc.id = nc2.perant_categoty 
where nc.perant_categoty is null
group by nc.title