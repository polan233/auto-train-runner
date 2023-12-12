from flask import Flask, request, jsonify
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
# 创建表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS presets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        pre_code TEXT,
        interpreter_path TEXT,
        script_path TEXT,
        parameters TEXT,
        final_code TEXT,
        description TEXT
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

@app.route('/savePreset', methods=['POST'])
def save_preset():
    # 获取请求参数
    name = request.args.get('name')
    pre_codes = request.args.getlist('preCode')
    interpreter_path = request.args.get('interpreterPath')
    script_path = request.args.get('scriptPath')
    parameters = request.args.getlist('parameters')
    final_code = request.args.get('finalCode')
    description = request.args.get('description')

    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    # 将数据插入数据库表中
    cursor.execute('INSERT INTO presets (name, pre_code, interpreter_path, script_path, parameters,final_code,description) VALUES (?, ?, ?, ?, ?,?,?)',
                   (name, '\n'.join(pre_codes), interpreter_path, script_path, ' '.join(parameters), final_code,description))
    conn.commit()
    conn.close()

    return jsonify({'message': '预设保存成功'})

@app.route('/getPresets', methods=['GET'])
def get_presets():
    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 查询所有预设项目
    cursor.execute('SELECT * FROM presets')
    presets = cursor.fetchall()

    # 将查询结果转换为字典列表
    presets_list = []
    for preset in presets:
        preset_dict = {
            'id': preset[0],
            'name': preset[1],
            'pre_code': preset[2],
            'interpreter_path': preset[3],
            'script_path': preset[4],
            'parameters': preset[5],
            'final_code': preset[6],
            'description': preset[7]
        }
        presets_list.append(preset_dict)

    conn.close()

    return jsonify(presets_list)

if __name__ == '__main__':
    app.run(debug=True)
