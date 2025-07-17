# avoDB
A small, end-to-end encrypted database as a service (DBaaS) with a focus on security.
- can create databases, tables, records
- integrated end-to-end encrypted messaging between users
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

## Project Deliverables

Please find here my [project deliverables document](https://github.com/WillGaston/avoDB/blob/main/avoDB_Project_Deliverables.pdf), featuring an outline of:
- the research I completed
- the tasks I accomplished
- my security mindset and considerations
- a reflection and analysis of what went well and what did not
- the challenges I encountered and how I overcame them.

## Short Report

Please find here my [short report document](https://github.com/WillGaston/avoDB/blob/main/avoDB_Short_Report.pdf), featuring a quick overview of
- what I achieved
- how I achieved it and the security concepts I explored
- the challenges I faced and how I overcame them

## 5 Pillars of Information Assurance

Below is a short exerpt from my Project Deliverables and Short Report which highlight the methods I used to adhere to the 5 pillars of information assurance. This is the primary security concept I explored, and my project is a real-world application of these principles.

1. Confidentiality
   All database records are encrypted client-side using AES-GCM (Advanced Encryption Algorithm with Galois/Counter Mode), ensuring end-to-end protection of database data. This guarantees the information input by the user has strong confidentiality both in transit and at rest on the server, preventing unauthorised access of the data even in the event the database is compromised.
- Client-Side Encryption: data is encrypted on client’s machine, thus plaintext is never exposed on the server
- AES-GCM: The algorithm provides authenticated confidentiality with a high number of bits of work to guarantee security.
2. Integrity
The integrity of the data used in my database is ensured through the authentication mechanism of AES-GCM which creates and verifies cryptographic authentication tags. 
- Tampering of the data and unauthorised modification (e.g. via changing bits) will cause the authentication tag check to fail.
3. Authentication
Data access is tied to cryptographic key ownership and identity verification.
- Password based encryption: data can only be correctly decrypted using the user’s password (used to encrypt/decrypt the private key stored in the database), ensuring only the authorized user can access
- GCM authentication tags: the algorithm provides authentication tags to ensure data originates from a legitimate source.
  . Availability
- Containerized database: dockerized Postgresql enhances portability and resilience.
- Data Persistence: volume mounting ensures database data is consistent across multiple instances.
5. Non-repudiation
To establish non-repudiation, I comployed digital signatures which link the user’s private key to their messages, verifiably linking actions to the users which perform them.
- Private key signing: receivers of data can validate signatures using the user’s public key, giving verifiable proof.

