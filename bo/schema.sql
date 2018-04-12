-- Insert code to create Database Schema
-- This will create your .db database file for use
drop table if exists customers;

create table customers (
	customer_id integer primary key,
	first_name text not null, 
	last_name text not null,
	company text not null,
	email text not null,
	phone_number text not null
);

create table address (
	address_id integer primary key,
	street_address text not null,
	city text not null,
	state text not null,
	country text not null,
	zipcode integer not null,
	customer_id integer not null,
	foreign key (customer_id) references customers(customer_id)
);

create table orders (
	order_id integer primary key,
	name_of_part text not null,
	manufacturer_of_part text not null,
	customer_id integer not null,
	foreign key (customer_id) references customers(customer_id)
);

create table order_detail (
	order_detail_id integer primary key,
	customer_id integer not null,
	order_id integer not null,
	foreign key (order_id) references orders (order_id),
	foreign key (customer_id) references customers(customer_id)
);