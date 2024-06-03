This program simulates the operation of a restaurant with three tables (0, 1, 2), each with four seats, and a set of 40 customers coming in. It uses multithreading to model customers and waiters as separate threads. Each customer enters the restaurant, selects a table (either one of the main tables or a backup dish table if the main tables are full), places an order with a waiter, eats their food, pays the bill, and leaves the restaurant. The program also simulates various wait times, such as the time it takes for waiters to deliver orders, the time it takes for orders to be prepared in the kitchen, and the time customers spend eating. The restaurant's capacity and customer behavior are simulated in this program. 

40 customer threads

	python3 restaurants.py
