select [Date],
group_concat(case when Zone = 'North' then cs_traffic end) as North_cs_traffic,
group_concat(case when Zone = 'Central' then cs_traffic end) as Central_cs_traffic,
group_concat(case when Zone = 'South' then cs_traffic end) as South_cs_traffic
from(
SELECT [Date], Zone, sum([CS Traffic WD (Erl)]) as cs_traffic
from DailyData
where [Date] > date('now','-31 day')
Group by [Date], Zone)
group by [Date]