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
added_date TIMESTAMPTZ DEFAULT NOW()
);


CREATE TABLE expense_participants(
uid BIGINT REFERENCES users(uid),
eid INT REFERENCES expenses(eid),
share NUMERIC(10,2),
PRIMARY KEY(eid, uid)
);



CREATE TABLE repayments(
rid SERIAL PRIMARY KEY,
sender BIGINT REFERENCES users(uid),
receiver BIGINT REFERENCES users(uid),
amount NUMERIC(10,2),
note VARCHAR(200),
added_date TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE cleared_date(
cleared_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""

# initialize cleared timesatmp
clear_timestamp_query = "INSERT INTO cleared_date DEFAULT VALUES;"


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
select Coalesce(part.participant, r.sender) as participant, Coalesce(part.payer,r.receiver) as payer, 
 COALESCE(part.total_share, 0) - COALESCE(r.total_repay, 0) AS debt 
from(
select p.uid as participant, e.payer, sum(share) as total_share
from expense_participants as p, expenses as e 
where p.eid = e.eid
and (p.uid=%s or e.payer =%s)
group by (participant, payer)) part

full join (
   select sender,receiver , sum(amount) as total_repay
   from repayments
   where sender = %s or receiver =%s
   group by (sender, receiver)
) r
on (part.participant= r.sender and part.payer = r.receiver); 
"""


def get_history_query(all: bool = True):
    return f"""
    Select 'expense' as type, 
        'e' || e.eid as id,
        e.payer, e.description, e.listed_by, e.amount, e.added_date,
        NULL::bigint as sender, NULL::bigint as receiver, NULL::text as note,
        json_agg(
            json_build_object(
                'uid',p.uid,
                'share',p.share)
        ) as participants
    From expenses as e
    Join expense_participants p
    On e.eid = p.eid

        {"" if all else "Where p.uid =%s  or e.payer = %s"}
    Group by e.eid

    Union All

    Select 'repayment' as type,
        'p' || r.rid as id,
        NULL::bigint as payer, NULL::text as description, NULL::bigint as listed_by, r.amount, r.added_date,
        r.sender, r.receiver, r.note, NULL
    From repayments as r
        {"" if all else "Where r.receiver =%s or r.sender=%s"}

    Order By added_date ASC;

    """


delete_participants_query = """
    DELETE From expense_participants 
    WHERE eid = %s;
  """
delete_expense_query = """
  DELETE FROM expenses
    where eid =%s;

"""

delete_repayment_entry_query = """
    DELETE From repayments
    Where rid=%s;
"""
