import networkx as nx
from datetime import datetime, timedelta
from simulation.logger import log_event
import math
import random

def process_train_movement(train, graph, current_time, departed_edges, edge_queues, pheromones, track_queues, trains, total_delay, total_punctuality):
    status_message = f"[{current_time.strftime('%H:%M')}] Train {train.id}: "
    if current_time.time() >= datetime.strptime(train.orginal_schedule[0], "%H:%M").time():
        
        # Completed train journey
        if train.completed:
            #print(status_message + "has completed its journey.")
            return
                            
                                
        # Handle traveling between stations
        if train.current_edge:
            
            edge_start, edge_end = train.current_edge
            
            if train.id not in track_queues[train.current_edge]:  
                track_queues[train.current_edge].append(train.id)
            
            station = graph.nodes[edge_end]["station"]
            
            
                
            if train.remaining_travel_time < station.dwell_time and train.id not in edge_queues[train.current_edge]:
                edge_queues[train.current_edge].append(train.id)
                msg = (f"Train {train.id} added to queue on edge {train.current_edge}")
                print(msg)
                log_event("Train_Q", msg)
                
            
                
            if train.remaining_travel_time > 0:
                
                    

                print(status_message + f"traveling between {edge_start} and {edge_end} ({train.remaining_travel_time} minutes remaining)")

                # Check edge direction from the graph and assign to the train
                edge_data = graph.get_edge_data(edge_start, edge_end)
                train.direction = edge_data["direction"] if edge_data else "unknown"
                
                #print(f"[{current_time.strftime('%H:%M')}] Train {train.id} is moving in the {train.direction} direction.")
                train.remaining_travel_time -= 1
                
                return

            elif train.remaining_travel_time <= 0:
                
                if track_queues[train.current_edge][0] != train.id:
                    print(f"[{current_time.strftime('%H:%M')}]Train {train.id} must wait behind Train {track_queues[train.current_edge][0]} on track {train.current_edge}")
                    return
                
                track_queues[train.current_edge].pop(0)
                # Travel complete
                
                 
                
                station = graph.nodes[edge_end]["station"]
                if not try_enter_station(train, station, current_time, edge_queues, pheromones,trains):
                    return  # Train is blocked, wait until platform is free
                else:
                    print(train.schedule)
                    edge_queues[train.current_edge].remove(train.id)

                    current_station = train.route[0]
                    if current_station in train.original_route:
                        log_event("train_arrivals" ,f"Train {train.id} arrived {current_station} at {current_time.strftime('%H:%M')}.")       
                    train.Arrived = True
                                                
                train.current_edge = None 
                
            #return

        # Handle dwell time at station
        if  len(train.route) == 1:
            train.original_route.pop(0)
            if len(train.original_route) <= 1:
                
                calculate_delay(train, current_time,train.orginal_schedule[-1])
                completion_message = f"Train {train.id} has completed its journey at {current_time.strftime('%H:%M')} (Delayed by {train.delay} minutes)"

                print(completion_message)
                log_event("completion_times", completion_message)

                if train.delay > 0:
                    log_event("train_delays", completion_message)
                    total_delay["value"] += train.delay
                    if train.TrainDis == "LongDistance":
                        if train.delay <= 10:
                            total_punctuality["value"] += 1
                    else:
                        if train.delay <= 5:
                            total_punctuality["value"] += 1
                else:
                    total_punctuality["value"] += 1
                log_event("train_arrivals", completion_message)     
                
                train.completed = True
                return
            else:      
                
                current_station = train.original_route[0]
                next_station = train.original_route[1]
                #calculate delay
                calculate_delay(train, current_time, train.schedule[0])
                if train.delay > 0:
                    message = f"Train {train.id} arrived {current_station} {train.delay} minutes delayed at {current_time.strftime('%H:%M')}."
                    log_event("train_delays", message)
                
                
                #calculate next path
                shortest_path = nx.shortest_path(graph, current_station, next_station, weight="weight")
                train.route = [current_station] + shortest_path[1:]
                print(f"[{current_time.strftime('%H:%M')}] Calculated shortest path: {train.route}")
                for _ in range(len(shortest_path) - 2):
                    train.schedule.insert(1, "00:00")
        
        if train.dwell_time > 0:
            if train.Arrived == False:
                current_station = train.route[0]
                expected_time_str = train.schedule[0]
                expected_time = datetime.strptime(expected_time_str, "%H:%M").time()


                                        
                train.Arrived = True
                    
                
                        
            print(status_message + f"waiting at {train.route[0]} (Dwell time remaining: {train.dwell_time} minutes)")
            train.reduce_dwell()
                
            return
            
        elif train.dwell_time <= 0:
            if train.Arrived == True:
                if len(train.route) > 1:
                    edge = (train.route[0], train.route[1])
                else:
                    edge = (train.route[0], train.route[0])
                
                if can_depart(train, edge, departed_edges, pheromones):
                    expected_time_str = train.schedule[0]
                    expected_time = datetime.strptime(expected_time_str, "%H:%M").time()
                    if current_time.time() < expected_time:
                        
                        print(f"[{current_time.strftime('%H:%M')}] Train {train.id} waiting for schedule at {expected_time}")
                        return
                        
                    station = graph.nodes[train.route[0]]["station"]
                    release_station_platform(train, station)
                    print(f"[{current_time.strftime('%H:%M')}] Train {train.id} left station at {current_time.strftime('%H:%M')}")
                    train.Arrived = False
                    
                    #new_station = train.route[1]
                    # if train.remaining_travel_time < new_station.dwell_time + 1 and train.id not in edge_queues[train.current_edge]:
                    #     edge_queues[train.current_edge].append(train.id)
                    #     msg = (f"Train {train.id} added to queue on edge {train.current_edge}")
                    #     print(msg)
                    #     log_event("Train_Q", msg)
                    
                else:
                    return
                
            #if train.schedule:            
            #    if train.current_edge == None and current_time.time() == datetime.strptime(train.schedule[0], "%H:%M").time():
            #        print(f"[{current_time.strftime('%H:%M')}] Train {train.id} left station at {current_time.strftime('%H:%M')}")
            #        train.Arrived = False
        
        
        current_station = train.route[0]
        next_station = train.route[1] if len(train.route) > 1 else None     
        expected_time_str = train.schedule[0]
        expected_time = datetime.strptime(expected_time_str, "%H:%M").time()

        if next_station:
            
            if not graph.has_edge(current_station, next_station):
                shortest_path = nx.shortest_path(graph, current_station, next_station, weight="weight")
                train.route = [current_station] + shortest_path[1:]
                print(f"[{current_time.strftime('%H:%M')}] Calculated shortest path: {train.route}")
                # Assign placeholder schedule times for intermediate stations
                for _ in range(len(shortest_path) - 1):
                    train.schedule.insert(1, "00:00")
                
                train.schedule = train.schedule[1:]
            #else:
            #    train.route = [current_station, train.route[1]]
            
        
        if current_time.time() >= expected_time:
            
            # Remove current station from route and schedule
            train.route.pop(0)
            train.schedule.pop(0)       
            if train.route:
                next_station = train.route[0]
                dwell_time = graph.nodes[next_station]["station"].dwell_time if next_station in train.original_route else 0
                train.set_dwell_time(dwell_time)

                distance = graph[current_station][next_station]["weight"]
                travel_time = int(math.ceil((distance / train.speed) * 60)) - 1
                train.current_edge = (current_station, next_station)
                train.remaining_travel_time = travel_time

                

    

def release_station_platform(train, station):
    # Release platform based on train direction
    if train.direction == "up":
        station.platforms_up += 1
    elif train.direction == "down":
        station.platforms_down += 1
    else:
        station.platforms_general += 1
        
    
        

        
def try_enter_station(train, station, current_time, edge_queues, pheromones, trains):
    """Handles train entry into stations, applying rescheduling before ACO selection."""
    status_message = f"[{current_time.strftime('%H:%M')}] Train {train.id} attempting to enter {station.name}: "

  
    train_queue = edge_queues[train.current_edge]
    
    # Apply rescheduling to prevent cascading delays
    train_dict = {train.id: train for train in trains}  # Convert train list to dictionary
    print(train.delay)
    train_queue = reschedule_trains(train_queue, train_dict)


    # Now apply ACO to pick the best train
    best_train = ant_colony_select_best_train(train_queue, pheromones, train.current_edge, trains)

    if best_train != train.id:
        print(f"Train {train.id} waiting in queue to enter station {station.name} (ACO prioritized Train {best_train})")
        return False

    # Check platform availability based on direction and dwell delay
    if train.direction == "up" and station.platforms_up > 0:
        station.platforms_up -= 1
        return True
    elif train.direction == "down" and station.platforms_down > 0:
        station.platforms_down -= 1
        
        print(status_message + f"Entered using a 'down' platform (Dwell Time: {train.dwell_time} min)")
        return True
    elif station.platforms_general > 0:
        station.platforms_general -= 1
        
        print(status_message + f"Entered using a general platform (Dwell Time: {train.dwell_time} min)")
        return True
    else:
        print(status_message + "Blocked! No available platforms. Train must wait.")
        return False

    
def can_depart(train, edge, departed_edges, pheromones):

    
    #print("CAN DEPART*************")
    if edge in departed_edges:
        print(f"Train {train.id} must wait before departing onto {edge}. Another train has already departed this minute.")
        #print(departed_edges)
        return False

    # Register departure for this edge
    departed_edges.append(edge)
    
    update_pheromones(train.id, edge, pheromones)
    
    return True

def calculate_delay(train, current_time, schedule_time_str):
    schedule_time = datetime.strptime(schedule_time_str, "%H:%M")
    train.delay = max(0, int((current_time-schedule_time).total_seconds()) // 60)
    print(train.delay)
    


def ant_colony_select_best_train(train_queue, pheromones, edge, train_objects):
    """ACO selection with rescheduling adjustments."""
    
    print(f"Train Queue: {train_queue}")

    alpha = 1  # Pheromone influence
    beta = 2   # Heuristic influence
    gamma = 1.5  # Train type influence

    train_dict = {train.id: train for train in train_objects}

    if not train_queue:
        return random.choice(train_queue)  

    probabilities = []
    total_pheromone = sum(pheromones.get((train_id, edge), 1) for train_id in train_queue)

    for train_id in train_queue:
        train = train_dict.get(train_id)
        if not train:
            print(f"Warning: Train {train_id} not found in train_objects list!")
            continue  

        pheromone = pheromones.get((train_id, edge), 1)

        # Apply rescheduling penalty to severely delayed trains
        delay_penalty = 0.5 if train.delay > 10 else 1.0  # Lower weight for highly delayed trains

        heuristic = (1 / (1 + train.delay)) * delay_penalty  # Adjust heuristic score
        
        train_type_weight = {
            "express": 1.5,
            "regional": 1.2,
            "local": 1.0
        }.get(train.type, 1.0)  

        probability = (pheromone ** alpha) * (heuristic ** beta) * (train_type_weight ** gamma)
        probabilities.append((train_id, probability))

    total_prob = sum(p for _, p in probabilities)

    if total_prob == 0:
        return random.choice(train_queue)  

    probabilities = [(train_id, p / total_prob) for train_id, p in probabilities]

    if all(p == 0 for _, p in probabilities):
        return random.choice(train_queue)

    chosen_train_id = random.choices(
        [train_id for train_id, _ in probabilities], 
        weights=[p for _, p in probabilities]
    )[0]

    return chosen_train_id  # Returns train ID






def update_pheromones(train_id, edge, pheromones):
    evaporation_rate = 0.1  # Prevents pheromones from accumulating too much
    pheromone_deposit = 1  # Amount of reinforcement for a good decision

    pheromones[(train_id, edge)] = pheromones.get((train_id, edge), 1) * (1 - evaporation_rate) + pheromone_deposit
    
    


def check_rescheduling_needed(train):
    """Checks if a train’s delay exceeds the rescheduling threshold."""
    return train.delay > 10  # Reschedule if delay exceeds 10 minutes

def reschedule_trains(train_queue, trains_dict):
    """
    Reorders the train queue based on excessive delays.
    `trains_dict` should be a dictionary where keys are train IDs and values are train objects.
    """
    
    for i in range(len(train_queue) - 1):
        print("IN LOOP")
        train_a_id = train_queue[i]
        train_b_id = train_queue[i + 1]

        # Retrieve train objects using train IDs
        train_a = trains_dict.get(train_a_id)
        train_b = trains_dict.get(train_b_id)

        # Ensure both train objects exist before attempting rescheduling
        if not train_a or not train_b:
            print(f"Warning: One of the trains {train_a_id}, {train_b_id} is missing in trains_dict!")
            continue

        # If train_a is significantly delayed, deprioritize it by swapping its order
        if check_rescheduling_needed(train_a):
            print(f"Rescheduling {train_a.id} due to excessive delay")

            # Lower its priority by temporarily placing it behind another train
            train_queue[i], train_queue[i + 1] = train_b.id, train_a.id  

            # Retain the original delay for final calculations
            train_a.original_delay = train_a.delay
        
    return train_queue  # Return updated queue order
