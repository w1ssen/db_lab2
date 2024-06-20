import pymysql

# 查询某个学生的基本信息
def select_student_baseinfo(db, cursor, ID):
    sql = "SELECT * FROM Students WHERE StudentID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
    
# 查询某个学生获得的奖项
def select_student_prizes(db, cursor, ID):
    sql = "SELECT * FROM Prizetime WHERE StudentID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
    
# 查询某个学生获得的惩罚
def select_student_punish(db, cursor, ID):
    sql = "SELECT * FROM Punishtime WHERE StudentID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
    
# 查询某个学生的全部成绩
def select_student_score(db, cursor, ID):
    sql = "SELECT c.ClassId, c.name, c.Point, s.Score FROM classes c JOIN scores s ON c.ClassId = s.ClassId WHERE s.StudentID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        Scores = cursor.fetchall()
        return Scores
    except Exception as e:
        print(f"发生错误：{e}")
        return


# 查询学生列表
def select_students_all(db, cursor):
    sql = "SELECT * FROM Students"
    try:
        cursor.execute(sql) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
    
# 查询课程列表
def select_classes_all(db, cursor):
    sql = "SELECT * FROM Classes"
    try:
        cursor.execute(sql) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return

# 查询奖项列表
def select_prize_all(db, cursor):
    sql = "SELECT * FROM Prizetime"
    try:
        cursor.execute(sql) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return

def select_score_all(db, cursor):
    sql = "SELECT * FROM scores"
    try:
        cursor.execute(sql)
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
    
# 查询惩罚列表
def select_punish_all(db, cursor):
    sql = "SELECT * FROM Punishtime"
    try:
        cursor.execute(sql) 
        student_info = cursor.fetchall()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return

    
# 按课程号查询课程
def select_class_ID(db, cursor, ID):
    sql = "SELECT * FROM Classes WHERE ClassID = %s"
    try:
        cursor.execute(sql, (ID, )) 
        student_info = cursor.fetchone()
        return student_info
    except Exception as e:
        print(f"发生错误：{e}")
        return
