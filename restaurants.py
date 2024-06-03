import threading
import time
import random

NUM_TABLES = 3
TABLE_CAPACITY = 4
NUM_CUSTOMERS = 40
WAITER_WAIT_TIME = (200, 800)  # Wait time range for waiters in milliseconds
ORDER_WAIT_TIME = (300, 1000)  # Wait time range for orders to be prepared in milliseconds
EAT_TIME = (200, 1000)  # Time it takes for customers to eat in milliseconds

class Restaurant:
    def __init__(self):
        self.tables = [threading.Semaphore(value=TABLE_CAPACITY) for _ in range(NUM_TABLES)]  # 3 tables with 4 seats each
        self.kitchen_ready = threading.Semaphore(value=1)  # Only one waiter can use the kitchen at a time
        self.queue_ready = [threading.Semaphore(value=7) for _ in range(3)]  # Three queues for each table
        self.backup_dish_table = threading.Semaphore(value=4)  # Backup dish table with 4 seats
        self.waiter_ready = [threading.Semaphore(value=1) for _ in range(3)]  # One waiter per table
        self.customers_paid = 0  # Counter to keep track of customers who have paid

def waiter_func(table_id, customer_id, restaurant):
    print(f"Waiter {table_id} takes Customer {customer_id}'s order.")

    with restaurant.kitchen_ready:
        # Simulate time spent in the kitchen to deliver the order
        kitchen_prep_time = random.uniform(0.1, 0.5)
        time.sleep(kitchen_prep_time)
        print(f"Waiter {table_id} delivers order to the kitchen.")
        
        # Simulate time waiting for the order to be ready
        kitchen_wait_time = random.uniform(0.3, 1)
        time.sleep(kitchen_wait_time)
        print(f"Waiter {table_id} picks up order from kitchen.")
        
        # Simulate time spent in the kitchen getting the order
        kitchen_get_order_time = random.uniform(0.1, 0.5)
        time.sleep(kitchen_get_order_time)
        print(f"Waiter {table_id} delivers order to Customer {customer_id}.")

    print(f"Waiter {table_id} is waiting for the next customer.")
    time.sleep(random.uniform(0.1, 0.5))

def customer_func(customer_id, restaurant):
    print(f"Customer {customer_id} enters the restaurant.")
    
    # Choose a table
    table_id = random.randint(0, 2)
    backup_table_id = random.choice([i for i in range(3) if i != table_id])

    with restaurant.queue_ready[table_id]:
        if restaurant.queue_ready[table_id]._value > 0:
            print(f"Customer {customer_id} joins the main queue for Table-{table_id}.")
            restaurant.queue_ready[table_id].acquire()
        else:
            print(f"Customer {customer_id} joins the backup dish table queue.")
            restaurant.backup_dish_table.acquire()

    # Choose a table based on line length
    chosen_table_id = table_id if restaurant.queue_ready[table_id]._value > 0 else backup_table_id

    for _ in range(4):
        with restaurant.tables[chosen_table_id]:
            print(f"Customer {customer_id} sits at Table-{chosen_table_id}.")
            # Call the waiter
            with restaurant.waiter_ready[chosen_table_id]:
                waiter_thread = threading.Thread(target=waiter_func, args=(chosen_table_id, customer_id, restaurant))
                waiter_thread.start()
                waiter_thread.join()

    print(f"Customer {customer_id} leaves the table.")
    
    if restaurant.queue_ready[table_id]._value > 0:
        restaurant.queue_ready[table_id].release()  # Release the main table queue
    else:
        restaurant.backup_dish_table.release()  # Release the backup dish table seat

    # Customer eats the food
    eat_time = random.uniform(EAT_TIME[0] / 1000, EAT_TIME[1] / 1000)
    time.sleep(eat_time)
    
    print(f"Customer {customer_id} finishes eating and is ready to pay.")

    # Only one customer can pay at a time
    with restaurant.tables[chosen_table_id]:
        if restaurant.customers_paid < 49:
            restaurant.customers_paid += 1
            print(f"Customer {customer_id} pays the bill and leaves the restaurant.")

def main():
    restaurant = Restaurant()
    
    customer_threads = []
    for i in range(NUM_CUSTOMERS):
        customer_thread = threading.Thread(target=customer_func, args=(i, restaurant))
        customer_threads.append(customer_thread)
        customer_thread.start()

    for thread in customer_threads:
        thread.join()

    print("All customers have left. Waiter is cleaning the tables.")

if __name__ == "__main__":
    main()

