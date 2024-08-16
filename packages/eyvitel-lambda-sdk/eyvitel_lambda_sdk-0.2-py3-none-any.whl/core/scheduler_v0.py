'''
File: scheduler_v0.py

This is a task scheduler at the heart of the AI workflow system. It needs to schedule and run tasks. 
Tasks are typically executable programs that have some input, configuration and that performs some sort of data processing and generates an output. 
Outputs may have to be saved in different formats etc.

What are the fundamental problems with most data pipeline schedulers ? Like airflow for instance ?
The jobs are sort of fixed, the scheduler doesn't have intrinsic support for tasks that are created at runtime.
But AI agents are more like humans, they have to keep working or looking for work 24/7.
So is a scheduler a good start for an AI agent ?

Functional Requirements:
------------------------

[x] Use a priority queue and maintain a list of tasks to be scheduled in memory, ordered by the next execution time for the task.
[ ] Ability to support tasks being added dynamically at runtime.
[ ] Ability to support tasks being removed dynamically at runtime.
[ ] Ability to support changes in the Task schedule at runtime.
[x] Use Redis as a queue and add a message to the queue when the task is ready to be started.
[ ] Support running multiple schedulers (each task can only be assigned to a single scheduler).
[ ] Log all events (task start, task addition, task removal, task modification, scheduler status history).
[ ] Health check.

Quality Attributes:
-------------------

[ ] Availability (Uptime)
[ ] Performance  (Max allowed task delay time -> 5ms)
[ ] Performance  (Average task delay time -> 3ms)

'''
import asyncio
import heapq
import time
import uuid
from croniter import croniter
from datetime import datetime, timedelta
from multiprocessing import Pool
import redis
from rq import Queue
from rq import Worker as BaseClass

PRIORITY_QUEUE = []
MAX_WINDOW_SIZE = 1000
MAX_PROCESSES = 5

# When a new task instance is created
def add_task(task):
    if task.is_running:
        heapq.heappush(PRIORITY_QUEUE, (task.next_schedule_runtime, task.id, task))

# When a task instance is deleted
def remove_task(task):
    for index, (scheduled_runtime, taskid, task) in enumerate(PRIORITY_QUEUE):
        if taskid == task.id:
            del PRIORITY_QUEUE[index]
            break
    heapq.heapify(PRIORITY_QUEUE)

# When a task schedule is modified
# When a task.is_running is modified
def update_task(task):
    remove_task(task)
    if task.is_running:
        task.update_next_schedule_runtime()
        add_task(task)

# 1. When a new task instance is created, we need to call add_task.
# 2. When a task instance is deleted, we need to call remove_task.
# 3. When a task.schedule or task.is_running is modified, we need to call update_task.
# 4. When we call add_task, we need to check if task.is_running is set to True, only then will it be added to the priority queue.
# 5. When we call update_task, if is_running is set to True, we need to add the task to the queue and remove any previous instances of the task in the queue.
# 6. When there is no schedule, if i call add_task, we need to add it to the queue as an immediately starting task.
class Task:
    def __init__(self, schedule=None, schedule_description=None):
        self.id = uuid.uuid4()
        self.schedule = schedule # cron expression
        self.is_running = True
        self.schedule_description = schedule_description
        if not self.is_schedule_empty():
            self.parsed_schedule = croniter(self.schedule, datetime.now())
        self.update_next_schedule_runtime()

    def is_schedule_empty(self):
        return self.schedule is None or self.schedule == ''

    def update_next_schedule_runtime(self):
        if self.is_schedule_empty():
            self.next_schedule_runtime = datetime.now()
        else:
            self.next_schedule_runtime = self.parsed_schedule.get_next(datetime)

    def pause_task(self):
        self.is_running = False

def load_tasks(tasks):
    global PRIORITY_QUEUE
    for task in tasks:
        print('Loading Task( id=', task.id, ')', task.next_schedule_runtime, task.schedule_description, task.schedule)
        heapq.heappush(PRIORITY_QUEUE, (task.next_schedule_runtime, task.id, task))

def calculate_metrics(task, sliding_window, window_size, task_scheduled_runtime, total_delay, max_delay):
    global MAX_WINDOW_SIZE
    removed_delay = timedelta(0)
    if window_size >= MAX_WINDOW_SIZE:
        removed_delay = sliding_window.pop(0)
        window_size -= 1

    now = datetime.now()
    delay = now - task_scheduled_runtime
    sliding_window.append(delay)
    window_size += 1

    total_delay = (total_delay + delay) - removed_delay
    avg_delay = total_delay / window_size

    if delay > max_delay:
        max_delay = delay

    # message = "Task( id=" + str(task.id)
    # message += ") triggered at " + str(now) 
    # message += ", delay = " + str(delay)
    # message += ", max delay = " + str(max_delay)
    # message += ", avg delay = " + str(avg_delay) + ", "
    # message += str(task.schedule_description)
    # print(message, flush=True)    

    return (sliding_window, window_size, delay, total_delay, avg_delay, max_delay)

def start_worker(task):
    print('worker started for task (id=', str(task.id), ')')

def post_message_to_queue(task):
    print('start task (id=', str(task.id), ')')

    # Redis queue post
    queue = get_redis_queue()
    queue.enqueue(start_worker, task)

    # Log it to the tracking database.
    # Scheduler triggering the task.

def get_redis_connection(host='127.0.0.1', port=6379, db='0'):
    connection = redis.Redis(host=host, port=port, db=db)
    return connection

def get_redis_queue(host='127.0.0.1', port=6379, db='0'):
    connection = get_redis_connection(host, port, db)
    queue = Queue('task_queue', connection=connection)
    return queue

def main_loop():
    running = True
    avg_delay = max_delay = total_delay = timedelta(0)
    window_size = 0
    sliding_window = []
    global PRIORITY_QUEUE
    task_executor = Pool(MAX_PROCESSES)
    while running:
        if len(PRIORITY_QUEUE) > 0:
            # Check the heapq for tasks that are ready to run
            now = datetime.now()
            scheduled_runtime, taskid, task = PRIORITY_QUEUE[0]

            task_scheduled_runtime = task.next_schedule_runtime
            if (now >= task_scheduled_runtime):
                scheduled_runtime, taskid, task = heapq.heappop(PRIORITY_QUEUE)
                task.update_next_schedule_runtime()
                heapq.heappush(PRIORITY_QUEUE, (task.next_schedule_runtime, task.id, task))

                # Calculate Metrics
                sliding_window, window_size, delay, total_delay, avg_delay, max_delay = calculate_metrics(
                    task,
                    sliding_window, 
                    window_size, 
                    task_scheduled_runtime, 
                    total_delay, 
                    max_delay
                )
                # Trigger a push to the queue, immediately, network -> it has its own time
                # Logging
                task_executor.apply_async(post_message_to_queue, args=(task,))
