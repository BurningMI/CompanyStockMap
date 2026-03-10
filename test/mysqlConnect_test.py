


import pymysql

try:
    # 建立连接
    conn = pymysql.connect(
        host="127.0.0.1",      # 本机数据库
        port=3306,             # MySQL端口
        user="root",           # 用户名
        password="123456",     # 密码
        database="mysql",      # 测试数据库（mysql默认有）
        charset="utf8mb4"
    )

    print("✅ MySQL 连接成功")

    # 创建游标
    cursor = conn.cursor()

    # 执行测试SQL
    #cursor.execute("SELECT VERSION();")
    cursor.execute("SELECT * FROM user;")

    # 获取结果
    #version = cursor.fetchone()
    users=cursor.fetchall()


    #print("MySQL版本:", version)
    print("用户列表:", users)

except Exception as e:
    print("❌ 连接失败")
    print("错误信息:", e)

finally:
    try:
        cursor.close()
        conn.close()
        print("数据库连接已关闭")
    except:
        pass