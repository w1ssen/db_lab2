import pymysql

def add_prizetime(db, cursor, sID, name, date):
    sql = "INSERT INTO Prizetime (StudentID, PrizeName, Date) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (sID, name, date)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return


def delete_prizetime(db, cursor, sID, name):
    sql = "DELETE FROM Prizetime WHERE StudentID = %s AND PrizeName = %s"
    try:
        cursor.execute(sql, (sID, name)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return