from flask import Flask, request
import sqlite3
import datetime
import subprocess


# 连接数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# 创建表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        run_datetime TEXT,
        result TEXT
    )
''')
conn.commit()
conn.close()

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/execute', methods=['POST'])
def execute_code():
    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    code = request.form.get('code')
    run_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = 'success'
    
    # 执行命令行代码
    try:
        result = subprocess.check_output(code, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        result = str(e.output)
        return str(e.output)
    
    # 将代码和日期时间插入到数据库中
    cursor.execute('INSERT INTO code_history (code, run_datetime, result) VALUES (?, ? ,?)', (code, run_datetime, result))
    conn.commit()
    conn.close()

    return result

if __name__ == '__main__':
    app.run(debug=True)
