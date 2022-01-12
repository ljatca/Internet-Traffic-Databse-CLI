WITH flow_hour9_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour9 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 9 AND month(from_unixtime(timeStamp)) = 4),
freq_hour9 as
(SELECT COUNT(*) AS freq9, web_service FROM flow_hour9_table natural join Services GROUP BY web_service order by freq9),
flow_hour10_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour10 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 10 AND month(from_unixtime(timeStamp)) = 4),
freq_hour10 as
(SELECT COUNT(*) AS freq10, web_service FROM flow_hour10_table natural join Services GROUP BY web_service order by freq10),
flow_hour11_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour11 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 11 AND month(from_unixtime(timeStamp)) = 4),
freq_hour11 as
(SELECT COUNT(*) AS freq11, web_service FROM flow_hour11_table natural join Services GROUP BY web_service order by freq11),
flow_hour12_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour12 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 12 AND month(from_unixtime(timeStamp)) = 4),
freq_hour12 as
(SELECT COUNT(*) AS freq12, web_service FROM flow_hour12_table natural join Services GROUP BY web_service order by freq12),
flow_hour13_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour13 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 13 AND month(from_unixtime(timeStamp)) = 4),
freq_hour13 as
(SELECT COUNT(*) AS freq13, web_service FROM flow_hour13_table natural join Services GROUP BY web_service order by freq13),
flow_hour14_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour14 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 14 AND month(from_unixtime(timeStamp)) = 4),
freq_hour14 as
(SELECT COUNT(*) AS freq14, web_service FROM flow_hour14_table natural join Services GROUP BY web_service order by freq14),
flow_hour15_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour15 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 15 AND month(from_unixtime(timeStamp)) = 4),
freq_hour15 as
(SELECT COUNT(*) AS freq15, web_service FROM flow_hour15_table natural join Services GROUP BY web_service order by freq15),
flow_hour16_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour16 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 16 AND month(from_unixtime(timeStamp)) = 4),
freq_hour16 as
(SELECT COUNT(*) AS freq16, web_service FROM flow_hour16_table natural join Services GROUP BY web_service order by freq16),
flow_hour17_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour17 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 17 AND month(from_unixtime(timeStamp)) = 4),
freq_hour17 as
(SELECT COUNT(*) AS freq17, web_service FROM flow_hour17_table natural join Services GROUP BY web_service order by freq17),
flow_hour18_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour18 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 18 AND month(from_unixtime(timeStamp)) = 4),
freq_hour18 as
(SELECT COUNT(*) AS freq18, web_service FROM flow_hour18_table natural join Services GROUP BY web_service order by freq18),
flow_hour19_table as
(SELECT timeStamp, hour(from_unixtime(timeStamp)) as flow_hour19 FROM Flow WHERE hour(from_unixtime(timeStamp)) = 19 AND month(from_unixtime(timeStamp)) = 4),
freq_hour19 as
(SELECT COUNT(*) AS freq19, web_service FROM flow_hour19_table natural join Services GROUP BY web_service order by freq19)

select * from freq_hour9 
natural join freq_hour10
natural join freq_hour11 
natural join freq_hour12 
natural join freq_hour13 
natural join freq_hour14 
natural join freq_hour15 
natural join freq_hour16
natural join freq_hour17 
natural join freq_hour18 
natural join freq_hour19;