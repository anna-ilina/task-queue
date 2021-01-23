import time
import os
import sys
import random
import redis



# Simple task to add to queue
def simple_addition_fn(x, y, silent=True):
    result = int(x) + int(y)
    if not int(silent):
        print('simple_addition_fn args', x, y, 'result:', result)
    return result


# NOTE: If my tasks IDs are incrementing integers, and I always consume tasks
#       in a first-added, first-consumed order, and I only have one consumer,
#       it doesn't really make sense for me to have a list of tasks_ids;
#       instead I could keep track of next task to consume using a counter,
#       e.g. next_task_to_consume counter.

#       However if my task IDs were non-integer values (e.g. uuids), I would
#       want to use a list to keep track of which tasks need to be consumed.

#       Or I didn't need to guarantee the first-added, first-consumed order,
#       I could use a set to contain the IDs of tasks to be consumed

#       What if I used IDs, but had multiple consumers?? I think then a counter
#       for next task to consume would be sufficient...

def consume_tasks(r):
    while True:
        task_id = r.lpop('tasks_list')

        # NOTE: If executing the task fails (throws exception),
        # with this implementation it is not retried.
        # TODO: ALLOW OPTION TO SET # OF RETRIES ON A TASK IF IT FAILS

        if task_id is not None:

            print('CONSUMING TASK', task_id)

            # Parse fn call encoded by task
            task_hash_name = 'task:' + task_id
            fn_name = r.hget(task_hash_name, 'fn_name')
            num_args = int(r.hget(task_hash_name, 'num_args'))
            args = [
                r.hget(task_hash_name, 'arg:'+str(x))
                for x in range(num_args)
            ]
            num_kwargs = int(r.hget(task_hash_name, 'num_kwargs'))
            kwargs = dict([
                (
                    r.hget(task_hash_name, 'kwarg_name:'+str(x)),
                    r.hget(task_hash_name, 'kwarg_val:'+str(x))
                )
                for x in range(num_kwargs)
            ])

            try:
                # Execute fn call encoded by  task
                globals()[fn_name](*args, **kwargs)
            except Exception as e:
                print('ERROR RAISED WHILE CONSUMING TASK', task_id)
                print(e)

            r.delete(task_hash_name)

        time.sleep(3)


# Choose an id for new task, create an hmset entry for task details,
# and append task id to tasks_list
def add_task(r):
    # Add task details to hash of name task:<task_id>, values are:
    # fn_name <fn name>
    # num_args <num args>
    # num_kwargs <num kwargs>
    # arg:0 <0th arg>
    # arg:1 <1st arg>
    # kwarg_name:0 <0th kwarg name>
    # kwarg_val:0 <0th kwarg value>
    # kwarg_name:0 <0th kwarg name>
    # kwarg_val:0 <0th kwarg value>

    # TODO: FOR KWARGS, since order doesn't matter, consider using form
    # kwarg:<kwarg_name> <kwarg_value>
    # kwarg:<another_kwarg_name> <another_kwarg_value>
    
    task_id = r.get('next_task_id')

    print("ADDING TASK", task_id)

    # Encode fn call: `simple_addition_fn(1, 2, silent=False)`
    r.hset(
        'task:'+task_id,
        mapping={
            'fn_name': 'simple_addition_fn',
            'num_args': 2,
            'arg:0': random.randint(0,99),
            'arg:1': random.randint(0,99),
            'num_kwargs': 1,
            'kwarg_name:0': 'silent',
            'kwarg_val:0': 0,
        }
    )

    # Append task id to tasks_list
    r.rpush('tasks_list', task_id)

    # Increment next_task_id for next task
    r.incr('next_task_id')

    return task_id

# Tasks will be consumed in a first-added, first-consumed order
def main():

    print("Connecting to db")

    # r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)

    if not r.exists('next_task_id'):
        r.set('next_task_id', 0)

    # Each task will have an ID. When a new task is created, I increment the ID counter,
    # push its ID onto tasks list, and create an hset record to store the task details
    # (func name, args)

    if sys.argv[1] == "create":
        while True:
            add_task(r)
            time.sleep(2)

    elif sys.argv[1] == "consume":
        while True:
            consume_tasks(r)
            time.sleep(2)

    else:
        print("Please provide argument 'create' or 'consume'")


if __name__ == '__main__':
    main()