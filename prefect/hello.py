from prefect import flow, task
import time

from prefect.blocks.system import String

string_block = String.load("future-nba-champs")

@task
def get_message(): 
    str = string_block.value
    return str

@flow
def sub_flow_message(x):
    return x + x

@flow
def hello_world(x):
    message = get_message()
    sub_flow_message_result = sub_flow_message(x)
    return message + " " + str(sub_flow_message_result)

if __name__ == "__main__":
    result = hello_world(2)
    print(result)