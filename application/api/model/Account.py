from application.api.access_control import Security


class Account:
    firstname = "Testuser"
    identifier = "1dCW2gcAdh5V2Cq19hul7"
    salt, password = Security.create_hash("password")


class Accounts:
    accounts = [Account()]
