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
register       --username <*username*> --password <*password*>
login          --username <*username*> --password <*password*>
userList
logout

message commands:
initiateConvo  --userId <*userId*>
viewConvos
sendMsg        --message <*message*>
viewMsgs

database commands:
dbCreate       --name <*name*>
dbList
dbDelete       --dbId <*dbId*>

table commands:
tbCreate       --dbId <*dbId*> --name <*name*> --schema <*schema*>
tbList         --dbId <*dbId*>
tbSchema       --dbId <*dbId*> --tbId <*tbId*>
tbDelete       --dbId <*dbId*> --tbId <*tbId*> 

data/row commands
insert       --dbId <*dbId*> --tbId <*tbId*> --data <*data*>
select       --dbId <*dbId*> --tbId <*tbId*>
rwList       --dbId <*dbId*> --tbId <*tbId*>
rwDelete     --dbId <*dbId*> --tbId <*tbId*> --rwId <*rwId*>

```
