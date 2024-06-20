import pymysql

def add_class(db, cursor, ID, name, point):
    sql = "INSERT INTO Classes (ClassID, Name, Point) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (ID, name, point)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    

def change_class(db, cursor, ID, num, newinf):
    if (num == 1):
        sql = "UPDATE Classes SET Name = %s WHERE ClassID = %s"
    if (num == 2):
        sql = "UPDATE Classes SET Point = %s WHERE ClassID = %s"
    try:
        cursor.execute(sql, (newinf, ID)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return    

def delete_class(db, cursor, ID):
    sql = "DELETE FROM Classes WHERE ClassID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    

def changeid_class(db, cursor, oldID, newID):
    sql = "CALL updateClassID(%s, %s)"
    try:
        cursor.execute(sql, (oldID, newID)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return