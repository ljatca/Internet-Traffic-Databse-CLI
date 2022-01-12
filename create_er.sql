tee create_er-outfile.txt;

drop table if exists PacketInterarrivalTime;
drop table if exists PacketSize;
drop table if exists Packet;
drop table if exists TrafficTime;
drop table if exists TrafficStats;
drop table if exists NumericIP;
drop table if exists Protocol;
drop table if exists Services;
drop table if exists Flow;
drop table if exists TrafficStation;

select '---------------------------------------------------------------------------------------' as '';
select 'Create TrafficStation' as '';

create table TrafficStation (
    IP varchar(15),
    port int,

    primary key(IP, port)
);

insert ignore into TrafficStation(IP, port) 
    select src_ip, src_port 
    from Internet_Traffic;

insert ignore into TrafficStation(IP, port) 
    select dst_ip, dst_port
    from Internet_Traffic;

select '---------------------------------------------------------------------------------------' as '';
select 'Create Flow' as '';

create table Flow (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    Src_IP varchar(15),
    Src_port int,
    Dst_IP varchar(15),
    Dst_port int,
    flowEndReason int,

    primary key(flow_key, timeStamp, duration),
    foreign key (Src_IP,Src_port) references TrafficStation(IP, port) on update cascade,
    foreign key (Dst_IP,Dst_port) references TrafficStation(IP, port) on update cascade
);

insert ignore into Flow (flow_key, timeStamp, duration, Src_IP, Src_port, Dst_IP, Dst_port, flowEndReason) 
    select flow_key, t_flowStart, t_flowDuration, src_ip, src_port, dst_ip, dst_port, flowEndReason 
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create Protocol' as '';

create table Protocol (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    proto int,
    application_protocol varchar(25),

    primary key(flow_key, timeStamp, duration),
    foreign key (flow_key,timeStamp, duration) references Flow(flow_key,timeStamp, duration) on update cascade
);

insert ignore into Protocol (flow_key, timeStamp, duration, proto, application_protocol) 
    select flow_key, t_flowStart, t_flowDuration, proto, application_protocol
    from Internet_Traffic;
    

select '---------------------------------------------------------------------------------------' as '';
select 'Create Services' as '';

create table 
 (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    category varchar(35),
    web_service varchar(25),

    primary key (flow_key, timeStamp, duration),
    foreign key (flow_key,timeStamp, duration) references Flow(flow_key,timeStamp, duration) on update cascade
);

insert ignore into Services(flow_key, timeStamp, duration, category, web_service) 
    select flow_key, t_flowStart, t_flowDuration, category, web_service 
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create NumericIP' as '';

create table NumericIP (
    IP varchar(15),
    numeric_ip decimal(10),
    
    primary key (IP),
    foreign key (IP) references TrafficStation(IP) on update cascade
);

insert ignore into NumericIP(IP, numeric_ip) 
    select src_ip, src_ip_numeric
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create TrafficStats' as '';

create table TrafficStats (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    type enum('forward', 'backward', 'total'),

    primary key(flow_key, timeStamp, duration, type),
    foreign key (flow_key,timeStamp, duration) references Flow (flow_key,timeStamp, duration) on update cascade

);

insert ignore into TrafficStats(flow_key, timeStamp, duration, type) 
    select flow_key, t_flowStart, t_flowDuration,'total'
    from Internet_Traffic;

insert ignore into TrafficStats(flow_key, timeStamp, duration, type) 
    select flow_key, t_flowStart, t_flowDuration,'forward'
    from Internet_Traffic;

insert ignore into TrafficStats(flow_key, timeStamp, duration, type) 
    select flow_key, t_flowStart, t_flowDuration, 'backward'
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create TrafficTime' as '';

create table TrafficTime (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    type enum('forward', 'backward', 'total'),
    flowStart double precision, 
    flowEnd double precision,
    flowDuration double precision,

    primary key(flow_key, timeStamp, duration, type),
    foreign key (flow_key,timeStamp, duration, type) references TrafficStats (flow_key,timeStamp, duration, type) on update cascade
);

insert ignore into TrafficTime(flow_key, timeStamp, duration, type, flowStart, flowEnd, flowDuration) 
    select flow_key, t_flowStart, t_flowDuration, 'total', t_flowStart, t_flowEnd, t_flowDuration
    from Internet_Traffic;

insert ignore into TrafficTime(flow_key, timeStamp, duration, type, flowStart, flowEnd, flowDuration) 
    select flow_key, t_flowStart, t_flowDuration, 'forward', f_flowStart, f_flowEnd, f_flowDuration
    from Internet_Traffic;

insert ignore into TrafficTime(flow_key, timeStamp, duration, type, flowStart, flowEnd, flowDuration) 
    select flow_key, t_flowStart, t_flowDuration, 'backward', b_flowStart, b_flowEnd, b_flowDuration
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create Packet' as '';

create table Packet (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    type enum('total', 'forward', 'backward'),
    pktTotalCount int,
    octetTotalCount bigint,
    
    primary key (flow_key, timeStamp, duration, type),
    foreign key (flow_key,timeStamp, duration, type) references TrafficStats (flow_key,timeStamp, duration, type) on update cascade
);

insert ignore into Packet(flow_key, timeStamp, duration, type, pktTotalCount, octetTotalCount) 
    select flow_key, t_flowStart, t_flowDuration, 'total', t_pktTotalCount, t_octetTotalCount
    from Internet_Traffic;

insert ignore into Packet(flow_key, timeStamp, duration, type, pktTotalCount, octetTotalCount) 
    select flow_key, t_flowStart, t_flowDuration, 'forward', f_pktTotalCount, f_octetTotalCount
    from Internet_Traffic;

insert ignore into Packet(flow_key, timeStamp, duration, type, pktTotalCount, octetTotalCount) 
    select flow_key, t_flowStart, t_flowDuration, 'backward', b_pktTotalCount, b_octetTotalCount
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create PacketSize' as '';

create table PacketSize (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    type enum('forward', 'backward', 'total'),
    min_ps int,
    max_ps int,
    avg_ps double precision,
    std_dev_ps double precision,

    primary key (flow_key, timeStamp, duration, type),
    foreign key (flow_key,timeStamp, duration, type) references TrafficStats (flow_key,timeStamp, duration, type) on update cascade
);

insert ignore into PacketSize(flow_key, timeStamp, duration, type, min_ps, max_ps, avg_ps, std_dev_ps) 
    select flow_key, t_flowStart, t_flowDuration, 'total', t_min_ps, t_max_ps, t_avg_ps, t_std_dev_ps
    from Internet_Traffic;

insert ignore into PacketSize(flow_key, timeStamp, duration, type, min_ps, max_ps, avg_ps, std_dev_ps) 
    select flow_key, t_flowStart, t_flowDuration, 'forward', f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps
    from Internet_Traffic;

insert ignore into PacketSize(flow_key, timeStamp, duration, type, min_ps, max_ps, avg_ps, std_dev_ps) 
    select flow_key, t_flowStart, t_flowDuration, 'backward', b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps
    from Internet_Traffic;


select '---------------------------------------------------------------------------------------' as '';
select 'Create PacketInterarrivalTime' as '';

create table PacketInterarrivalTime (
    flow_key char(32),
    timeStamp double precision,
    duration double precision,
    type enum('forward', 'backward', 'total'),
    min_piat double precision,
    max_piat double precision,
    avg_piat double precision,
    std_dev_piat double precision,
    
    primary key (flow_key, timeStamp, duration, type),
    foreign key (flow_key,timeStamp, duration, type) references TrafficStats (flow_key,timeStamp, duration, type) on update cascade
);

insert ignore into PacketInterarrivalTime (flow_key, timeStamp, duration, type, min_piat, max_piat, avg_piat, std_dev_piat) 
    select flow_key, t_flowStart, t_flowDuration, 'total', t_min_piat, t_max_piat, t_avg_piat, t_std_dev_piat
    from Internet_Traffic;

insert ignore into PacketInterarrivalTime (flow_key, timeStamp, duration, type, min_piat, max_piat, avg_piat, std_dev_piat) 
    select flow_key, t_flowStart, t_flowDuration, 'forward', f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat
    from Internet_Traffic;

insert ignore into PacketInterarrivalTime (flow_key, timeStamp, duration, type, min_piat, max_piat, avg_piat, std_dev_piat) 
    select flow_key, t_flowStart, t_flowDuration, 'backward', b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat
    from Internet_Traffic;