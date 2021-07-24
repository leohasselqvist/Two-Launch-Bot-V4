import sqlite3
import datetime

debug = False


def dprint(text):
    if debug:
        print(text)


tekdb = sqlite3.connect("1tek2.sqlite3")  # Get Database, if it does not exist, create it.
dprint("Database connected")


def setup():  # Make sure that the user "template" is in place, otherwise create it
    _ = sqlite3.connect("1tek2.sqlite3")  # Get Database, if it does not exist, create it.
    tekdb.execute("""CREATE TABLE IF NOT EXISTS USER
        (ID            INT     PRIMARY KEY,
        KB            INT     NOT NULL,
        NICK           TEXT    NOT NULL);""")
    tekdb.execute("""CREATE TABLE IF NOT EXISTS HISTORY
        (USER        INT    NOT NULL,
        DAY         TEXT    NOT NULL,
        AMOUNT      INT     NOT NULL,
        SENDER       TEXT    NOT NULL,
        RECEIVER     TEXT    NOT NULL,
        REASON       TEXT    NOT NULL
        )""")


def createuser(userid, nick):  # Create a user, choosing ID and Nickname.
    tekdb.execute(f"INSERT INTO USER (ID, KB, NICK) \
          VALUES ({userid}, 500, '{nick}');")
    tekdb.commit()


def deleteuser(userid=None, nick=None):
    statement = f"DELETE FROM USER WHERE "
    if nick:
        statement += f"NICK = '{nick}'"
    if userid:
        statement += f"ID = {userid}"
    tekdb.execute(statement)
    tekdb.commit()


def fetchuser(userid, nick=None):  # Fetch a user via ID. If nick arg is given a value it will be used instead of ID.
    try:
        if not nick:
            user = tekdb.execute(f"SELECT * FROM USER WHERE ID = {userid};")
        else:
            user = tekdb.execute(f"SELECT * FROM USER WHERE NICK = '{nick}';")
        return user.fetchall()[0]
    except IndexError:  # If no user is found, return nothing
        return None


# Insert ID, Column, and the New Value to edit entries. Column is not an index, it is the name, Ex: NICK or KB.
def edituser(userid, column, newvalue, nick=None):
    command = f"UPDATE USER set {column} = "  # Set basic info for the command
    # Correctly format if the new value is a string
    if type(newvalue) is str:
        command += f"'{newvalue}' "
    else:
        command += f"{newvalue} "

    # If nick arg is given a value, it will be used to fetch rather than ID. If no value is specified ID will be used.
    if nick:
        command += f"where NICK = {nick};"
    else:
        command += f"where ID = {userid};"

    tekdb.execute(command)
    tekdb.commit()


def editall(column, newvalue):
    command = f"UPDATE USER set {column} = "  # Set basic info for the command
    # Correctly format if the new value is a string
    if type(newvalue) is str:
        command += f"'{newvalue}' "
    else:
        command += f"{newvalue} "

    command += f"where {column} IS NOT NULL"

    tekdb.execute(command)
    tekdb.commit()


def fetchall():
    try:
        users = tekdb.execute(f"SELECT * FROM USER")
        return users.fetchall()
    except IndexError:  # If no user is found, return nothing
        return None


def createhistoryentry(user, sender, receiver, date, amount, reason):  # All user arguments must be ID's
    # Fetch all user's full info
    user = fetchuser(user)
    sender = fetchuser(sender)
    receiver = fetchuser(receiver)
    # Create the entry with all the information.
    tekdb.execute(f"INSERT INTO HISTORY(USER, DAY, AMOUNT, SENDER, RECEIVER, REASON) \
        VALUES ({user[0]}, '{date}', {amount}, '{sender[2]}', '{receiver[2]}', '{reason}');")
    tekdb.commit()  # Update the database


def fetchhistory(userid):
    try:
        history = tekdb.execute(f"SELECT * FROM HISTORY WHERE USER = {userid};")
        return history.fetchall()
    except IndexError:
        return None


class KB:
    @staticmethod
    def send(sender, receiver, amount, reason):  # Sender and receiver are user ID's.
        # Fetch both user's full info.
        sender = fetchuser(sender)
        receiver = fetchuser(receiver)
        if sender[1] >= amount > 0:
            # Remove money from sender and add to receiver
            edituser(sender[0], "KB", sender[1]-amount)
            edituser(receiver[0], "KB", receiver[1]+amount)
            # Add reasons
            createhistoryentry(sender[0], sender[0], receiver[0], datetime.datetime.now().date(), amount, reason)
            createhistoryentry(receiver[0], sender[0], receiver[0], datetime.datetime.now().date(), amount, reason)
        else:
            raise IndexError("Sender is missing credits")

    @staticmethod
    def nologsend(sender, receiver, amount):
        # Fetch both user's full info.
        sender = fetchuser(sender)
        receiver = fetchuser(receiver)
        if sender[1] >= amount:
            # Remove money from sender and add to receiver
            edituser(sender[0], "KB", sender[1] - amount)
            edituser(receiver[0], "KB", receiver[1] + amount)
        else:
            raise ValueError("Sender requires additional KB")

    @staticmethod
    def transfer(receiver, amount):  # Directly transfer KB to a user out of thin air, only to be used by admins!
        receiver = fetchuser(receiver)  # Fetch the receiver's full info
        edituser(receiver[0], "KB", receiver[1]+amount)  # Add the KB

    @staticmethod
    def remove(receiver, amount):  # Directly transfer KB to a user out of thin air, only to be used by admins!
        receiver = fetchuser(receiver)  # Fetch the receiver's full info
        edituser(receiver[0], "KB", receiver[1]-amount)  # Add the KB

    @staticmethod
    def transferall(amount):
        for user in fetchall():
            edituser(user[0], "KB", user[1]+amount)

    @staticmethod
    def removeall(amount):
        for user in fetchall():
            edituser(user[0], "KB", user[1]-amount)
