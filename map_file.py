list_c =["flow_key", "Src_IP", "Src_port", "Dst_IP", "Dst_port", 
        "flowEndReason", "proto", "application_protocol", "category", "web_service"]
list_ls =["flow_key", "Src_IP", "Src_port", "Dst_IP", "Dst_port", "flowEndReason", "proto", "application_protocol", "web_service", 
            "category","numeric_ip", "flowStart", "flowEnd", "flowDuration", "pktTotalCount", "octetTotalCount", "max_ps", "min_ps", 
            "avg_ps", "std_dev_ps", "min_piat", "max_piat", "avg_piat", "std_dev_piat"]
list_stats =["flowDuration", "max_ps", "min_ps", "avg_ps", "std_dev_ps", "min_piat", "max_piat", "avg_piat", "std_dev_piat"
            "pktTotalCount", "octetTotalCount"]
list_type = ["flowStart", "flowEnd", "flowDuration", "pktTotalCount", "octetTotalCount", "max_ps", "min_ps", 
            "avg_ps", "std_dev_ps", "min_piat", "max_piat", "avg_piat", "std_dev_piat"]
list_update = ["flow_key", "Src_IP", "Dst_IP", "Src_port", "timestamp", "duration", "flowEndReason", "web_service", "category",
            "proto", "application_protocol", "numeric_ip", "flowStart", "flowEnd", "flowDuration", "pktTotalCount", "octetTotalCount",
            "max_ps", "min_ps", "avg_ps", "std_dev_ps", "min_piat", "max_piat", "avg_piat", "std_dev_piat"]

list_existing_table = ["Flow", "NumericIP", "Packet", "PacketInterarrivalTime", "PacketSize", "Protocol", "TrafficStation", "TrafficStats", "TrafficTime"]

attr_map = {
    "flow_key": "Flow",
    "Src_IP": "Flow",
    "Dst_IP": "Flow",
    "Src_port": "Flow",
    "Dst_port": "Flow",
    "timestamp": "Flow",
    "duration": "Flow",
    "flowEndReason": "Flow",
    
    "web_service": "Services",
    "category": "Services",
    
    "proto": "Protocol",
    "application_protocol": "Protocol",
    
    "numeric_ip": "NumericIP",

    "flowStart": "TrafficTime",
    "flowEnd": "TrafficTime",
    "flowDuration": "TrafficTime",
    
    "pktTotalCount": "Packet",
    "octetTotalCount": "Packet",

    "max_ps": "PacketSize",
    "min_ps": "PacketSize",
    "avg_ps": "PacketSize",
    "std_dev_ps": "PacketSize",

    "min_piat": "PacketInterarrivalTime",
    "max_piat": "PacketInterarrivalTime",
    "avg_piat": "PacketInterarrivalTime",
    "std_dev_piat": "PacketInterarrivalTime"
}

condition_map = {
    "-t": "timestamp",
    "-d": "duration",
    "-p": "proto",
    "-s": "web_service",
    "-c": "category",
    "-pc": "pktTotalCount",
    "-ps": "octetTotalCount",
    "-ap": "application_protocol",
    "-sp": "Src_port",
    "-dp": "Dst_port",
    "-fs": "flowStart",
    "-fe": "flowEnd",
    "-fd": "flowDuration",
    "-n": "numeric_ip"
    #-l: limit line
    #-w: write to file
    #-v: value for update
}


