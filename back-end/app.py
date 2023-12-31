from flask import Flask, request, jsonify
import sqlite3
import datetime
import subprocess
from flask_cors import CORS
import json


# 连接数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# 创建表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        run_datetime TEXT,
        result TEXT,
        status varchar(20),
        name varchar(50),
        description TEXT
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
        description TEXT,
        p_names TEXT,
        p_values TEXT
    )
''')
conn.commit()
conn.close()

app = Flask(__name__)
CORS(app, origins='http://localhost:8080', supports_credentials=True)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/execute', methods=['POST'])
def execute_code():
    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    code = request.args.get('code')
    exe_time = request.args.get('time')
    name=request.args.get('name')
    description=request.args.get('description')
    print("接收到代码：", code)
    

    # 拆分多行代码为一个指令列表
    commands = code.strip().split('\n')

    for _ in range(int(exe_time)):

        for index, cmd in enumerate(commands):
                    # 逐行执行指令
            run_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result_str = ''
            # 将代码和日期时间插入到数据库中
            cursor.execute('INSERT INTO runs (code, run_datetime, result, status ,name,description) VALUES (?, ?, ?, ?,?,?)', (cmd, run_datetime, result_str, "running",name,description))
            run_id = cursor.lastrowid  # 获取插入数据的id
            conn.commit()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            status = "success"
            # 命令执行的根目录为项目文件夹根目录
            result_str = f'\n------------------第{_+1}次运行第{index+1}条指令-----------------------\n{result.stdout}'
            if result.returncode != 0:
                result_str = f'\n!!!!!!!!!!!!!!!!!!!!!!!!!运行报错!!!!!!!!!!!!!!!!!!!!!!!\n{result.stderr}'
                status = "error"
                break
            cursor.execute('UPDATE runs SET result = ?, status = ? WHERE id = ?', (result_str, status, run_id))
            conn.commit()
            print("结果",result_str)
    conn.close()

    return "运行完毕"

@app.route('/savePreset', methods=['POST'])
def save_preset():
    # 获取请求参数
    name = request.args.get('name')
    pre_codes = json.loads(request.args.get('preCodeList'))
    interpreter_path = request.args.get('interpreterPath')
    script_path = request.args.get('scriptPath')
    parameters = json.loads(request.args.get('parametersList'))
    final_code = request.args.get('finalCode')
    description = request.args.get('description')
    print("接收到参数", name, pre_codes, interpreter_path, script_path, parameters, final_code, description)
    
     # 将参数列表中的 name 和 value 分别用空格分隔
    p_names = ' '.join([param['name'] for param in parameters])
    p_values = ' '.join([param['value'] for param in parameters])
    # 将参数列表中的 name 和 value 分别用空格分隔，并拼接为字符串
    parameters_str = ' '.join([f"{param['name']} {param['value']}" for param in parameters])

    
    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    # 将数据插入数据库表中
    cursor.execute('INSERT INTO presets (name, pre_code, interpreter_path, script_path, parameters,final_code,description,p_names,p_values) \
                    VALUES (?, ?, ?, ?, ?,?,?,?,?)',
                   (name, '\n'.join(pre_codes), interpreter_path, script_path, parameters_str, final_code,description,p_names,p_values))
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
    conn.close()

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
            'description': preset[7],
            'p_names': preset[8],
            'p_values': preset[9]
        }
        presets_list.append(preset_dict)

    

    return jsonify(presets_list)

@app.route('/getRuns', methods=['GET'])
def get_runs():
    conn = sqlite3.connect('database.db')  # 替换为你的数据库文件路径
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM runs")
    rows = cursor.fetchall()
    conn.close()

    runs = []
    for row in rows:
        run = {
            'id': row[0],
            'code': row[1],
            'run_datetime': row[2],
            'result': row[3],
            'status': row[4],
            'name':row[5],
            'description':row[6]
        }
        runs.append(run)

    return jsonify(runs)

@app.route('/deleteRun', methods=['POST'])
def delete_run():
    run_id = request.args.get('id')

    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 删除对应id的运行记录
    cursor.execute('DELETE FROM runs WHERE id = ?', (run_id,))
    conn.commit()
    conn.close()

    return '删除成功'

@app.route('/deletePreset', methods=['POST'])
def delete_preset():
    # 获取请求中的参数 id
    id = request.args.get('id')

    # 连接数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 删除对应的行
    cursor.execute('DELETE FROM presets WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return '删除成功'

if __name__ == '__main__':
    app.run(debug=True)
