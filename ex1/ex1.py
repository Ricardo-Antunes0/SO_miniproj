import random
import sys

def timing():
    global next_event_type
    global time_next_event
    global sim_time
    global time_last_event

    min_time_next_event = 1e9
    next_event_type = ''
    time_last_event = sim_time

    for e in time_next_event:
        if time_next_event[e] < min_time_next_event:
            min_time_next_event = time_next_event[e]
            next_event_type = e

    if next_event_type == '':
        print('Event list is emplty at time', sim_time)
        sys.exit()

    sim_time = min_time_next_event


def update_costs():
    global handling_cost
    global shortage_cost
    global inventory_level

    if inventory_level < 0:
        shortage_cost += (-inventory_level) * (sim_time - time_last_event)
    elif inventory_level > 0:
        handling_cost += inventory_level * (sim_time - time_last_event)
    else: 
        return

def evaluate_inventory():
    global time_next_event
    global sim_time
    global inventory_level
    global handling_cost
    global shortage_cost
    global order_cost
    global z
    global express_orders
    global total_orders


    if inventory_level < s:
        total_orders += 1
        z = big_s - inventory_level  # Z itens
        # inventario < 0 significa que fazemos uma encomenda express e que o tempo de entrega sera uniformly distributed on [0.25, 0.50] month. 
        if inventory_level < 0:
            express_orders += 1
            order_cost += 48 + 4 * z
            time_next_event['arrive_order'] = sim_time + random.uniform(0.25, 0.5)
        # Calcular o custo total do pedido
        order_cost += setup_cost + incremental_cost * z
        # Adicionar o tempo de chegada do pedido ao evento
        time_next_event['arrive_order'] = sim_time + random.uniform(0.5, 1)

    time_next_event['evaluate_inventory'] = sim_time + 1  # Avalia novamente após 1 "mês"

def supplier_arrival():
    global time_next_event
    global sim_time
    global inventory_level
    global z
    global handling_cost
    global shortage_cost
    global inventory

    for _ in range(z):
        shelf_life = sim_time + random.uniform(1.5, 2.5)  # Tempo atual + validade do produto
        inventory.append(shelf_life)

    inventory_level += z  
    time_next_event["arrive_order"] = 1e9

def generate_demand():
    rand = random.random()
    if rand <= 1/6:
        return 1
    elif rand <= 1/2:
        return 2
    elif rand <= 5/6:
        return 3
    else:
        return 4

def customer_demand():
    global time_next_event
    global sim_time
    global inventory_level
    global inventory
    global spoiled

    # Gerar a procura do cliente
    time_next_event['demand_customer'] = sim_time + random.expovariate(1/0.1)

    # Gerar a procura do cliente
    demand = generate_demand()

    # Verificar a validade dos produtos no inventário
    while demand > 0 and inventory:
        item = inventory[0]     # Get the first item in the inventory
        if item >= sim_time:    # Check if the item is still valid
            demand -= 1   
            inventory.pop(0)    # Remove the item from the inventory
            inventory_level -= 1
        else:
            # Item expired, discard it
            spoiled += 1
            inventory.pop(0)
            inventory_level -= 1

    inventory_level -= demand


# main


print('Starting simulation')
print('-------------------')
print('Policy      Total cost    Ordering cost    Handling cost    Shortage cost')

# Define os nove pares de valores de s e S
inventory_policies = [(20, 40), (20, 60), (20, 80), (20, 100),
                      (40, 60), (40, 80), (40, 100),
                      (60, 80), (60, 100)]

for s, big_s in inventory_policies:

    # initialize

    # simulation clock
    sim_time = 0.0

    # Parâmetros do sistema de inventário
    setup_cost = 32 # setup cost
    incremental_cost = 3 # incremental cost
    end_of_simulation = 120
    inventory = []

    # state variables
    inventory_level = 60
    time_last_event = 0.0
    z = 0

    # statistics
    total_cost = 0
    order_cost = 0
    handling_cost = 0
    shortage_cost = 0
    spoiled = 0
    express_orders = 0
    total_orders = 0
        

    time_next_event = {}
    time_next_event['demand_customer'] = sim_time + random.expovariate(1/0.1)
    time_next_event['evaluate_inventory'] = 0
    time_next_event['end_simulation'] = end_of_simulation

    next_event_type = ''

    while next_event_type != 'end_simulation':
        timing()
        update_costs()
        if next_event_type == 'arrive_order':
            supplier_arrival()
        elif next_event_type == 'demand_customer':
            customer_demand()
        elif next_event_type == 'evaluate_inventory':
            evaluate_inventory()
        
    order_cost /= end_of_simulation
    handling_cost /= end_of_simulation
    shortage_cost /= end_of_simulation
    shortage_cost *= 5

    total_cost = order_cost + handling_cost + shortage_cost
    """
    print('For s =', s, 'and S =', big_s, 'the results are:')
    print('Total cost is', total_cost)
    print('Total ordering cost is', order_cost)
    print('Total handling cost is', handling_cost)
    print('Total shortage cost is', shortage_cost)
    print('End of simulation at', sim_time)
    print('Inventory level is', inventory_level)
    """
    print(f'({s},{big_s}):     {total_cost:<16.2f}{order_cost:<18.2f}{handling_cost:<16.2f}{shortage_cost:<15.2f}')


    print("Express orders %:", (express_orders/total_orders) * 100)

