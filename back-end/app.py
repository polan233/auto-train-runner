from flask import Flask, request
import sqlite3
import datetime
import subprocess
from flask_cors import CORS


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
CORS(app, supports_credentials=True)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/execute', methods=['POST'])
def execute_code():
    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    code = request.args.get('code')
    print("接收到代码：", code)
    run_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = ''
    
    # 拆分多行代码为一个指令列表
    commands = code.strip().split('\n')
    
    # 逐行执行指令
    for command in commands:
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            result += f'\n{output}'
        except subprocess.CalledProcessError as e:
            result += f'\nError executing command: {command}\n{e.output}'
    
    # 将代码和日期时间插入到数据库中
    cursor.execute('INSERT INTO code_history (code, run_datetime, result) VALUES (?, ? ,?)', (code, run_datetime, result))
    conn.commit()
    conn.close()

    return result

if __name__ == '__main__':
    app.run(debug=True)
