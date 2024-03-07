
create table admin (
    email varchar(320) not null,
    password varchar(50) not null,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    address varchar(100) not null,
    city varchar(100) not null,
    country varchar(100) not null,
    phone_num varchar(50) not null,

    constraint admin_primary_key primary key (email),
    constraint admin_phone_num_unique unique (phone_num),
    constraint admin_email_check check (email like '%@%')
);

create table user (
    email varchar(320) not null,
    password varchar(50) not null,
    first_name varchar(100) not null,
    last_name varchar(100) not null,

    constraint user_primary_key primary key (email),
    constraint user_email_check check (email like '%@%')
);

create table card (
    number varchar(19) not null,
    exp_date varchar(5) not null,  -- format 'MM/YY'
    cvc varchar(4) not null,  -- 3 or 4 digits long
    owner_email varchar(320),  -- null ako ne postoji korisnik koji je povezan sa karticom
    verified boolean not null,

    constraint card_primary_key primary key (number),
    constraint card_foreign_key foreign key (owner_email) references user(email) on update cascade,
    constraint card_exp_date_check check (exp_date like '__/__')
);

create table balance (
    card_num varchar(19) not null,
    currency varchar(10) not null,
    amount decimal(65, 2) not null,

    constraint balance_primary_key primary key (card_num, currency),
    constraint balance_foreign_key foreign key (card_num) references card(number),
    constraint balance_currency_check check (currency in ('rsd', 'eur', 'usd')),
    constraint balance_amount_check check (amount >= 0)
);

create table bank_check (
    code varchar(15) not null,
    currency varchar(10) not null,
    amount decimal(65,2) not null,

    constraint bank_check_primary_key primary key (code),
    constraint bank_check_currency_check check (currency in ('rsd', 'eur', 'usd')),
    constraint bank_check_amount_check check (amount >= 0)
);

create table transaction_id (
    value integer not null,

    constraint transaction_id_primary_key primary key (value),
    constraint transaction_id check (value > 0)
);

create table transaction (
    transaction_id integer not null,
    sender_card_num varchar(19) not null,
    receiver_card_num varchar(19) not null,
    currency varchar(10) not null,  -- currency mora da bude u ovoj tabeli zajedno sa brojevima kartica jer je to kljuc balance tabele, pa da mogu da koristim inner join
    sent_amount decimal(65, 2) not null,
    date_and_time datetime not null,
    executed boolean not null,

    constraint transaction_primary_key primary key (transaction_id),
    constraint transaction_foreign_key foreign key (transaction_id) references transaction_id(value) on delete cascade,
    constraint transaction_sent_amount_check check (sent_amount >= 0),
    constraint transaction_currency_check check (currency in ('rsd', 'eur', 'usd'))
    -- (sender_card_num + currency) i (receiver_card_num + currency) nisu foreign key zato sto transakcije treba da ostanu u bazi i kada korisnik izbrise karticu svog naloga
);



insert into admin values ('1dragangavric@gmail.com', '123', 'Dragan', 'Gavric', 'Gavrila Principa 12', 'Bijeljina', 'Bosnia & Hercegovina', '0038766231312');
insert into admin values ('arsenije.knezevic6@gmail.com', '123', 'Arsenije', 'Knezevic', 'Martinbrdska 16', 'Backa Palanka', 'Serbia', '00381649522432');
insert into admin values ('bojankuljic16@gmail.com', '123', 'Bojan', 'Kuljic', 'Hercegovacka 24', 'Biograd', 'Bosnia & Hercegovina', '00381642347584');
insert into admin values ('ispanovic.luka@gmail.com', '123', 'Luka', 'Ispanovic', 'Dositeja Obradovica 18', 'Subotica', 'Serbia', '0038766421321');

insert into user values ('1dragangavric@gmail.com', '123', 'Dragan', 'Gavric');
insert into user values ('arsenije.knezevic6@gmail.com', '123', 'Arsenije', 'Knezevic');
insert into user values ('bojankuljic16@gmail.com', '123', 'Bojan', 'Kuljic');
insert into user values ('ispanovic.luka@gmail.com', '123', 'Luka', 'Ispanovic');


insert into card values ('2468428723827492', '07/25', '232', '1dragangavric@gmail.com', 1);
insert into card values ('5324232424542353', '05/26', '443', '1dragangavric@gmail.com', 1);

insert into card values ('3545343245234234', '12/24', '112', 'arsenije.knezevic6@gmail.com', 1);
insert into card values ('3404203204230423', '10/24', '302', 'arsenije.knezevic6@gmail.com', 1);

insert into card values ('8324023423402334', '01/27', '102', 'bojankuljic16@gmail.com', 1);
insert into card values ('2312423123124412', '02/24', '553', 'bojankuljic16@gmail.com', 1);

insert into card values ('1208472342302342', '09/25', '324', 'ispanovic.luka@gmail.com', 1);
insert into card values ('3242032402341289', '05/25', '431', 'ispanovic.luka@gmail.com', 1);

-- kartice sa kojima nijedan korisnik nije povezan
insert into card values ('1432435934598399', '02/26', '321', null, 0);
insert into card values ('5234234235234754', '04/24', '341', null, 0);
insert into card values ('5457623565635435', '03/25', '672', null, 0);
insert into card values ('9758657566345654', '12/26', '364', null, 0);
insert into card values ('5654756565436875', '02/27', '582', null, 0);
insert into card values ('0345035735407340', '09/26', '035', null, 0);


insert into balance values ('2468428723827492', 'rsd', 23432);
insert into balance values ('2468428723827492', 'eur', 4321.23);
insert into balance values ('5324232424542353', 'rsd', 213203);

insert into balance values ('3545343245234234', 'rsd', 27321);
insert into balance values ('3545343245234234', 'eur', 1024.32);
insert into balance values ('3404203204230423', 'rsd', 4423);

insert into balance values ('8324023423402334', 'rsd', 52344);
insert into balance values ('8324023423402334', 'eur', 54.2);
insert into balance values ('2312423123124412', 'rsd', 4423);

insert into balance values ('1208472342302342', 'rsd', 708);
insert into balance values ('1208472342302342', 'eur', 24000.42);
insert into balance values ('3242032402341289', 'rsd', 5600);

insert into balance values ('1432435934598399', 'usd', 2600);
insert into balance values ('5234234235234754', 'eur', 232);
insert into balance values ('5457623565635435', 'rsd', 34220);
insert into balance values ('9758657566345654', 'eur', 1120);
insert into balance values ('5654756565436875', 'rsd', 24120);
insert into balance values ('0345035735407340', 'rsd', 123520);


insert into bank_check values ('759370528521429', 'rsd', 20000);
insert into bank_check values ('830593861738835', 'rsd', 12500);
insert into bank_check values ('467543635836567', 'eur', 1000);
insert into bank_check values ('534654363567354', 'usd', 100);
insert into bank_check values ('857696680656434', 'usd', 500);
insert into bank_check values ('357643586456765', 'usd', 1200);
insert into bank_check values ('675767546564733', 'eur', 250);
insert into bank_check values ('349890879678654', 'rsd', 10000);
insert into bank_check values ('345654756543543', 'usd', 1250);
insert into bank_check values ('346978606123421', 'rsd', 50000);


insert into transaction_id values (1);
insert into transaction_id values (2);
insert into transaction_id values (3);
insert into transaction_id values (4);
insert into transaction_id values (5);
insert into transaction_id values (6);
insert into transaction_id values (7);
insert into transaction_id values (8);
insert into transaction_id values (9);
insert into transaction_id values (10);


insert into transaction values (1, '2468428723827492', '3545343245234234', 'rsd', 1000, '2022-01-08 22:05:32', 1);
insert into transaction values (2, '5324232424542353', '3242032402341289', 'rsd', 7000, '2023-07-18 14:42:00', 1);
insert into transaction values (3, '2468428723827492', '8324023423402334', 'eur', 37, '2023-10-23 07:15:32', 1);

insert into transaction values (4, '3545343245234234', '1208472342302342', 'rsd', 2000, '2021-02-03 00:00:00', 1);
insert into transaction values (5, '3545343245234234', '1208472342302342', 'eur', 2500, '2023-04-06 14:13:32', 1);

insert into transaction values (6, '8324023423402334', '1208472342302342', 'eur', 100, '2022-01-12 22:21:23', 1);
insert into transaction values (7, '2312423123124412', '3242032402341289', 'rsd', 320, '2023-05-18 04:02:09', 1);
insert into transaction values (8, '8324023423402334', '3545343245234234', 'eur', 50, '2019-04-30 15:44:35', 1);
insert into transaction values (9, '2312423123124412', '5324232424542353', 'rsd', 500, '2021-01-28 11:32:12', 1);

insert into transaction values (10, '1208472342302342', '3545343245234234', 'rsd', 5300, '2023-08-08 19:41:01', 1);


commit;