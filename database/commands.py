db_name = "hisab_bot"
# create database
create_db = f"Create database {db_name}"


# create tables

create_all_tables = """

CREATE TABLE User (
uid INT PRIMARY KEY,
name VARCHAR(100),
added_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Expense (
eid SERIAL PRIMARY KEY,
payer INT REFERENCES User(id),
description VARCHAR(300),
listed_by INT REFERENCES User(id),
amount INT,
added_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE Participant(
participant INT REFERENCES User(id),
amount INT
);



CREATE TABLE Repayment(
sender INT REFERENCES User(id),
receiver INT REFERENCES User(id),
amount INT,
note VARCHAR(200),
added_date DATE DEFAULT CURRENT_DATE

);
"""


add_expense = """
    INSERT INTO Expense(payer, description, listed_by, amount)
    VALUES (%s,%s,%s,%s);
"""

add_participant = """
    INSERT INTO Participant (participant,amount)
    VALUES (%s,%s);
"""

add_user = """
    INSERT INTO User(uid,name)
    VALUES(%s,%s);
"""

add_repayment = """
    INSERT INTO Repayment(sender, receiver,amount, note)
    VALUES(%s,%s,%s,%s) 
"""



