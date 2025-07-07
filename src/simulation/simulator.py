from datetime import timedelta
from simulation.train_manager import process_train_movement
from simulation.logger import clear_logs
from simulation.logger import log_event



def simulate_trains(trains, graph, simulation_duration, pheromones, start_time):
    edge_queues = {edge: [] for edge in graph.edges}
    track_queues = {edge: [] for edge in graph.edges}
    current_time = start_time
    clear_logs()      
    total_delay = {"value": 0}  # Store total delay in a dictionary
    total_punctuality = {"value": 0}
    
    while simulation_duration > 0:
        departed_edges = []
        for train in trains:
            process_train_movement(train, graph, current_time, departed_edges, edge_queues, pheromones, track_queues, trains, total_delay, total_punctuality)

        current_time += timedelta(minutes=1)  # Increment simulation time
        simulation_duration -= 1
        
    log_event("total_delay", str(total_delay["value"]))
    log_event("total_punct", str(total_punctuality["value"])+"/14")