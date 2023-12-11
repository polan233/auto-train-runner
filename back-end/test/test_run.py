import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    command = input('请输入要执行的命令：')
    result = execute_command(command)
    print(result)