# avoDB
A small, end-to-end encrypted database as a service (DBaaS) with a focus on security.
```
                     ____   ____  
  __ _ __   __ ___  |  _ \ | __ ) 
 / _` |\ \ / // _ \ | | | ||  _ \ 
| (_| | \ V /| (_) || |_| || |_) |
 \__,_|  \_/  \___/ |____/ |____/ 

---------------------------------------------------------
| avoDB: an end-to-end encrypted database as a service. |
---------------------------------------------------------

user commands:
register       --username <*username*>
login          --username <*username*>
logout  

database commands:
dbCreate       --databaseName <*dbName*>
dbList
dbDelete       --dbId <*dbId*>

table commands:
tbCreate       --dbId <*dbId*> --tbname <*name*> --schema <*schema*>
tbList         --dbId <*dbId*>
tbDelete       --dbId <*dbId*> --tbId <*tbId*> 
tbSchema       --dbId <*dbId*> --tbId <*tbId*> 

data/row commands
insert       --dbId <*dbId*> --tbId <*tbId*> --data <*data*>
select       --dbId <*dbId*> --tbId <*tbId*>
rwDelete     --dbId <*dbId*> --tbId <*tbId*> --rwId <*rwId*>

```
