db_name = "hisab_bot"
# create database
create_db = f"Create database {db_name}"


# create tables

create_all_tables = """

CREATE TABLE users (
uid BIGINT PRIMARY KEY,
name VARCHAR(100),
added_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE expenses (
eid SERIAL PRIMARY KEY,
payer BIGINT REFERENCES users(uid),
description VARCHAR(300),
listed_by BIGINT REFERENCES users(uid),
amount NUMERIC(10,2),
added_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE expense_participants(
uid BIGINT REFERENCES users(uid),
eid INT REFERENCES expenses(eid),
share NUMERIC(10,2),
PRIMARY KEY(eid, uid)
);



CREATE TABLE repayments(
sender BIGINT REFERENCES users(uid),
receiver BIGINT REFERENCES users(uid),
amount NUMERIC(10,2),
note VARCHAR(200),
added_date DATE DEFAULT CURRENT_DATE

);
"""


# delete entire database
delete_db = f"DROP DATABASE {db_name};"


# add vaues
add_expense_query = """
    INSERT INTO expenses(payer, description, listed_by, amount)
    VALUES (%s,%s,%s,%s)
    RETURNING eid;
"""
# the returning eid makes usre insert returns primary key (eid) which is needed to add particapnts


add_participant_query = """
    INSERT INTO expense_participants (uid,eid,share)
    VALUES (%s,%s,%s);
"""

add_user_query = """
    INSERT INTO users(uid,name)
    VALUES(%s,%s);
"""

add_repayment_query = """
    INSERT INTO repayments(sender, receiver,amount, note)
    VALUES(%s,%s,%s,%s) 
"""

# fetch users
get_users = """
    SELECT uid, name from users;
    
"""

get_balance_query = """
    Select uid as participiant, payer, sum(share) as total_debt
    from expense_participants as p, expenses as e
    where p.eid = e.eid 
    and (p.uid = %s or e.payer = %s)
    group by (participiant, payer);
"""
