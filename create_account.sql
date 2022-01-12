create table Clients (
    client_id        char(36),
    username        varchar(35) not null UNIQUE,
    password        char(10),
    priv            decimal(1,0),

    primary key (client_id)
);