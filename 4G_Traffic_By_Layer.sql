SELECT [Start Time],
GROUP_CONCAT(case when Tech = 'L2100' then sum_traffic end) as 'L2100',
GROUP_CONCAT(case when Tech = 'L900' then sum_traffic end) as 'L900'
from(
select [Start Time], Tech, sum([LTE Traffic Daily (MB)]) as sum_traffic
from dailydata
WHERE [Start Time] > date('now','-31 day')
group by [Start Time], Tech)
group by [Start Time]