import pymysql

# 添加学生
def add_student(db, cursor, ID, name, Age, major, image=None):
    sql1 = "INSERT INTO Students (StudentID, Name, Age, Major, Photo) VALUES (%s, %s, %s, %s, %s)"
    sql2 = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(sql1, (ID, name, Age, major, image))
        cursor.execute(sql2, (ID, ID))
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    

# 对学生的属性进行修改
def change_student(db, cursor, ID, num, newinf):
    if (num == 1):
        sql = "UPDATE Students SET Name = %s WHERE StudentID = %s"
    if (num == 2):
        sql = "UPDATE Students SET Age = %s WHERE StudentID = %s"
    if (num == 3):
        sql = "UPDATE Students SET Major = %s WHERE StudentID = %s"
    if (num == 4):
        sql = "UPDATE Students SET Photo = %s WHERE StudentID = %s"
    try:
        cursor.execute(sql, (newinf, ID))
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return    

# 删除学生
def delete_student(db, cursor, ID):
    sql = "DELETE FROM Students WHERE StudentID = %s"
    sql2 = "DELETE FROM users WHERE username = %s"
    try:
        cursor.execute(sql, (ID, ))
        cursor.execute(sql2, (ID,))
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    

    
# 修改学号
def changeid_student(db, cursor, oldID, newID):
    sql = "CALL updateStudentID(%s, %s)"
    try:
        cursor.execute(sql, (oldID, newID)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

