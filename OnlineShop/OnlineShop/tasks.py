# tasks.py 
from celery import Celery 
from redis import StrictRedis 
import time 
 
app = Celery('tasks', broker='redis://redis:6379/0') 
redis_client = StrictRedis(host='redis', port=6379, db=0) 
 
def get_free_server_port(): 
    taken_ports = redis_client.smembers('taken_ports') 
    all_ports = set(range(8001, 8003)) 
 
    free_ports = all_ports - taken_ports 
 
    if free_ports: 
        port = free_ports.pop() 
        return port 
    else: 
        raise Exception("Both ports are busy.") 
 
def set_server_busy(server_port): 
    redis_client.sadd('taken_ports', server_port) 
 
def set_server_idle(server_port): 
    redis_client.srem('taken_ports', server_port) 
 
def is_server_busy(server_port): 
    return bool(int(redis_client.sismember('taken_ports', server_port))) 
 
@app.task 
def process_image(image_path): 
    for port in range(8001, 8003): 
        if not is_server_busy(port): 
            try: 
                set_server_busy(port) 
                print(f"Processing image on server {port}: {image_path}") 
                time.sleep(40) 
                #print(f"Image processed on server {port}: {image_path}") 
                return f"Image processed on server {port}: {image_path}" 
 
            finally: 
                set_server_idle(port) 
                process_queue() 
            #return f"Image processed on server {port}" 
 
    # If both servers are busy, add to the queue 
    # print(f"Both servers are busy. Adding task to the queue: {image_path}") 
    redis_client.rpush('image_queue', image_path) 
    return f"Both servers are busy. Task added to the queue for processing: {image_path}" 
 
def process_queue(): 
    queue_length = redis_client.llen('image_queue') 
    if queue_length > 0: 
        image_path = redis_client.lpop('image_queue').decode('utf-8') 
        process_image.delay(image_path)