-- dump of database schema

create table if not exists UsersMeta (
  user_id               text primary key,
  hashed_username       text not null,
  kek_salt              text not null,
  hashed_password       text not null,
  encrypted_master_key   text not null
);

create table if not exists Databases (
  db_id                 text primary key,
  owner_id              text not null references UsersMeta(user_id) on delete cascade,
  encrypted_db_name     text not null
);

create table if not exists Tables (
  table_id              text primary key,
  db_id                 text not null references Databases(db_id) on delete cascade,
  encrypted_table_name  text not null,
  encrypted_schema      text not null
);

create table if not exists Rows (
  row_id                text not null primary key,
  table_id              text not null references Tables(table_id) on delete cascade,
  encrypted_data        text not null,
  iv                    text not null,
  created_at            timestamp not null default current_timestamp
); 