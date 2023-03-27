import mysql.connector
from mysql.connector import Error
import config
import boto3
from PIL import Image
import numpy as np

def addUser(name, email):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO user_data (username, email) VALUES (%s, %s) """
        record = (name, email)
        cursor.execute(mySql_insert_query, record)

        # Get the UUID generated id value
        get_id_query = "SELECT id FROM user_data WHERE username = %s AND email = %s"
        cursor.execute(get_id_query, record)
        result = cursor.fetchone()
        uid = result[0]

        connection.commit()
        print("Record addUser() inserted successfully into vkdata")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return uid

def addPass(uid, passdata = {} ):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO notthepass (uid, salt, nonce, tag, password, encrkey)
                                        VALUES (%s, %s, %s, %s, %s, %s) """
        record = (uid, passdata.get('salt'), passdata.get('nonce'), passdata.get('tag'), passdata.get('cipher_text'),
                  passdata.get('key'))
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into vkdata notthepass")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def saveImg(filename, uid):
    try:
        s3 = boto3.resource('s3')
        i = 1
        for f in filename:
            name = str(i) + '.jpg'
            data = open(f, 'rb')
            s3.Bucket('visual-key-image-bucket').put_object(Key= uid + '/' + name, Body=data)
            i += 1
        print('Images added')

        bucket = s3.Bucket('visual-key-image-bucket')
        imgnames = []
        for obj in bucket.objects.filter(Prefix=uid + '/'):
            imgnames.append(obj.key)

        images = []

        for key in imgnames:
            object = bucket.Object(key)
            response = object.get()
            file_stream = response['Body']
            im = Image.open(file_stream)
            images.append(np.array(im))
        return images
    except Error as e:
        print("Error adding images on S3: ", e)

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

def getImages(username):
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
        imgnames = []
        for obj in bucket.objects.filter(Prefix= id[0] + '/'):
            imgnames.append(obj.key)

        images = []

        for key in imgnames:
            object = bucket.Object(key)
            response = object.get()
            file_stream = response['Body']
            im = Image.open(file_stream)
            images.append(np.array(im))
        return images

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
        mySql_insert_query = """SELECT password from user_data where username = %s ;"""

        getpassquery = ('''SELECT s.password FROM user_data f JOIN notthepass s ON f.id = s.uid 
                            WHERE f.username = %s;''')

        cursor.execute(getpassquery, (username,))
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

def getPasswordData(username):
    try:
        connection = mysql.connector.connect(host= config.host,
                                             database= config.db_name,
                                             user= config.user,
                                             password= config.passwd)
        cursor = connection.cursor()
        mySql_insert_query = """SELECT s.salt, s.password, s.nonce, s.tag, s.encrkey 
                                FROM user_data f JOIN notthepass s ON f.id = s.uid WHERE f.username = %s;"""
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

def getUserfromMail(email):
    try:
            connection = mysql.connector.connect(host= config.host,
                                                database= config.db_name,
                                                user= config.user,
                                                password= config.passwd)
            cursor = connection.cursor()
            mySql_insert_query = """SELECT username from user_data where email = %s ;"""
            cursor.execute(mySql_insert_query, (email,))
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
