# digital_hunter_2
# Part 2 of the final test
# Yoseph Rechdiner
# 213507742

---

# Porpuse
The main porpuse of the part is to make the database accessible for the user.
I used fastapi and uvicorn for running the server and also mysql.connector as the db communicator.


To run the program open your terminal make sure you are in the root directory and copy and run this:
```bash
docker compose up --build
```

---

# Stucture
Ingestion-service is not used in production only for local test uses.
I copied dump.sql to the root directory for db initialization and created new docker-compose file.

Api-service is the main application.
app directory contain all the code of the app.
    db_connection.py contains mysql manager which responsible for mysql connection.
    db_dal.py contains MysqlDal class which responsible for all dal operations.
    routes.py contains all app endpoints.
    main.py contains app initialization.

Dockerfile for docker containerztion
requirements.txt for app dependencies