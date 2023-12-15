import subprocess

commands = [
    'E:',
    'dir'
]

for cmd in commands:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("命令输出：", result.stdout)
    print("返回码：", result.returncode)