-- dump of database schema

create table if not exists UsersMeta (
  user_id               UUID primary key,
  username              text not null unique,
  kek_salt              text not null,
  pk_iv                 text not null,
  hashed_password       text not null,
  encrypted_private_key text not null,
  public_key            text not null,
  created_at            timestamp not null default current_timestamp
);

create table if not exists Databases (
  db_id                 UUID primary key,
  owner_id              UUID not null references UsersMeta(user_id) on delete cascade,
  iv                    text not null,
  encrypted_db_name     text not null,
  encrypted_master_key  text not null
);

create table if not exists Tables (
  table_id              UUID primary key,
  db_id                 UUID not null references Databases(db_id) on delete cascade,
  encrypted_table_name  text not null,
  encrypted_schema      text not null
);

create table if not exists Rows (
  row_id                UUID not null primary key,
  table_id              UUID not null references Tables(table_id) on delete cascade,
  encrypted_data        text not null,
  iv                    text not null,
  created_at            timestamp not null default current_timestamp
); 