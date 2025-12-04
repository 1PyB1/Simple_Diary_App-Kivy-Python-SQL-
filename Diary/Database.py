import mysql.connector 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  #Enter Your Own Sql Information
    database="database" #Enter Your Own Sql Information
)
mycursor = db.cursor()
#mycursor.execute("CREATE TABLE User_Information (id INT PRIMARY KEY AUTO_INCREMENT, Username varchar(20), Password varchar(50), created datetime)")

def add_user(username, password):
    sql = "INSERT INTO user_information (Username, Password) VALUES (%s, %s)"
    mycursor.execute(sql, (username, password))
    db.commit()
def get_user(username):
    sql = "SELECT * FROM user_information WHERE Username = %s"
    mycursor.execute(sql, (username,))
    return mycursor.fetchone()

def add_data(user_id, text, date):
    sql = "INSERT INTO Diary_Data (user_id, Text, Date) VALUES (%s, %s, %s)"
    mycursor.execute(sql, (user_id, text, date))
    db.commit()
def get_user_diary(user_id):
    sql = "SELECT Date, Text FROM Diary_Data WHERE user_id = %s"
    mycursor.execute(sql, (user_id,))
    return mycursor.fetchall()
###
    mycursor.execute("DROP TABLE IF EXISTS Diary_Data")

    mycursor.execute("""
    CREATE TABLE Diary_Data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        Text VARCHAR(3000),
        Date VARCHAR(100),
        FOREIGN KEY (user_id) REFERENCES user_information(id)
    )
    """)
###
def get_pages(user_id):
    sql = "SELECT Date, Text FROM diary_data WHERE user_id = %s ORDER BY id"
    mycursor.execute(sql, (user_id,))
    return mycursor.fetchall()
def update_page(user_id ,page_number, content, date):
    sql = """
    UPDATE diary_data
    SET Text = %s, Date = %s
    WHERE user_id = %s AND id = %s
    """
    mycursor.execute(sql, (content, date, user_id, page_number))
    db.commit()
def page_exists(user_id, page_number):
    sql = "SELECT id FROM diary_data WHERE user_id=%s AND id=%s"
    mycursor.execute(sql, (user_id, page_number))
    return mycursor.fetchone()







