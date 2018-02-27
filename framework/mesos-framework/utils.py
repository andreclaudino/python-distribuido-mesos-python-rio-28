from addict import Dict
import getpass
import socket

def new_executor(memory, cpus, command='print("Hello World")'):
    executor = Dict()
    executor.executor_id.value = 'Example Executor'
    executor.name = executor.executor_id.value
    executor.command.value = f'python3 -c "{command}"'
    executor.resources = [
        dict(name='mem', type='SCALAR', scalar={'value': memory}),
        dict(name='cpus', type='SCALAR', scalar={'value': cpus}),
    ]

    return executor

def build_framework():
    framework = Dict()
    framework.user = getpass.getuser()
    framework.name = "Example Framework"
    framework.hostname = socket.gethostname()

    return framework