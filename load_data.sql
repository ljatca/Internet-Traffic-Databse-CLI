tee project-data-outfile.txt;

drop table if exists Internet_Traffic;

select '---------------------------------------------------------------------------------------' as '';

select 'Create Internet_Traffic' as '';

create table Internet_Traffic (flow_key char(32),
       	     	                src_ip_numeric decimal(10),
                                src_ip varchar(15),
                                src_port int,
                                dst_ip varchar(15),
                                dst_port int,
                                proto int,
                                t_pktTotalCount int,
                                t_octetTotalCount bigint,
                                t_min_ps int,
                                t_max_ps int,
                                t_avg_ps double precision,
                                t_std_dev_ps double precision,
                                t_flowStart double precision,
                                t_flowEnd double precision, 
                                t_flowDuration double precision,
                                t_min_piat double precision,
                                t_max_piat double precision,
                                t_avg_piat double precision,
                                t_std_dev_piat double precision,
                                f_pktTotalCount int,
                                f_octetTotalCount bigint,
                                f_min_ps int,
                                f_max_ps int,
                                f_avg_ps double precision,
                                f_std_dev_ps double precision,
                                f_flowStart double precision,
                                f_flowEnd double precision,
                                f_flowDuration double precision,
                                f_min_piat double precision,
                                f_max_piat double precision,
                                f_avg_piat double precision,
                                f_std_dev_piat double precision,
                                b_pktTotalCount int,
                                b_octetTotalCount bigint,
                                b_min_ps int,
                                b_max_ps int,
                                b_avg_ps double precision,
                                b_std_dev_ps double precision,
                                b_flowStart double precision,
                                b_flowEnd double precision,
                                b_flowDuration double precision,
                                b_min_piat double precision,
                                b_max_piat double precision,
                                b_avg_piat double precision,
                                b_std_dev_piat double precision,
                                flowEndReason int,
                                category varchar(35),
                                application_protocol varchar(25),
                                web_service varchar(25)
                            );

load data infile '/var/lib/mysql-files/21-Network-Traffic/Unicauca-dataset-April-June-2019-Network-flows.csv' ignore into table Internet_Traffic
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines;

show warnings limit 100;