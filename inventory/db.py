from mongoengine import connect

connect(
    db="inventory_db",
    host="localhost",
    port=27017
)