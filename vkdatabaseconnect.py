import mysql.connector
from mysql.connector import Error
import config
import boto3

def addUser(name, passdata = {}):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO user_data (username, salt, nonce, tag, password, encryptkey) 
                                        VALUES (%s, %s, %s, %s, %s, %s) """

        record = (name, passdata.get('salt'), passdata.get('nonce'), passdata.get('tag'), passdata.get('cipher_text'),
                  passdata.get('key'))
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into vkdata")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def saveImg(filename, user):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor(buffered= True)
        cursor.execute("SELECT id from user_data where username = %s ;", (user,))
        id = cursor.fetchone()
        connection.commit()

        s3 = boto3.resource('s3')
        i = 1
        for f in filename:
            name = str(i) + '.jpg'
            data = open(f, 'rb')
            s3.Bucket('visual-key-image-bucket').put_object(Key= id[0] + '/' + name, Body=data)
            i += 1

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def resaveImg(user, images):
    s3 = boto3.resource('s3')
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """SELECT id from user_data where username = %s ;"""
        user = cursor.execute(mySql_insert_query, user)
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    response = s3.delete_object(Bucket='visual-key-image-bucket', Key= user + '/')
    if response['DeleteMarker'] == True:
        saveImg(images, user)
    else:
        print(response)

def resetpasswd(email, passdata = {}):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()

        mySql_insert_query = """UPDATE user_data SET `salt` = %s, `nonce` = %s, 
                                `tag` = %s, `password` = %s `encryptkey` = %s WHERE (`email` = %s)"""

        record = (passdata.get('salt'), passdata.get('nonce'), passdata.get('tag'), passdata.get('cipher_text'),
                  passdata.get('key'), email)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record updated successfully into vkdata")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def checkUser(username):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """SELECT * from user_data where username = %s ;"""
        cursor.execute(mySql_insert_query, (username,))
        record = cursor.fetchone()
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    if record:
        return True
    else:
        return False

def getImages(username);
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """SELECT id from user_data where username = %s ;"""
        cursor.execute(mySql_insert_query, (username,))
        id = cursor.fetchone()
        connection.commit()

        s3 = boto3.resource('s3')
        bucket = s3.Bucket('visual-key-image-bucket')
        images = []
        for obj in bucket.objects.filter(Prefix= id[0] + '/'):
            images.append(obj.key)
    except Error as e:
        print("Error while connecting to MySQL", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    
    return images

def getPassword(username):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """SELECT * from user_data where username = %s ;"""
        cursor.execute(mySql_insert_query, (username,))
        record = cursor.fetchone()
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return record
    
