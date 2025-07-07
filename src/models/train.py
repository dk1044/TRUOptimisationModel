from datetime import datetime

class Train:
    def __init__(self, id, route, schedule, speed, TrainType, TrainDis):
        self.id = id
        self.route = route
        self.original_route = route.copy()
        self.schedule = schedule
        self.orginal_schedule = schedule.copy()
        self.speed = speed
        self.delay = 0
        self.completed = False
        self.dwell_time = 0
        self.current_edge = None
        self.remaining_travel_time = 0
        self.dwell_time = 0
        self.direction = None
        self.Arrived = False
        self.type = TrainType
        self.TrainDis = TrainDis
        
    def set_dwell_time(self, dwell_time):
        self.dwell_time = dwell_time
    

    def reduce_dwell(self):
        if self.dwell_time > 0:
            self.dwell_time -= 1  
        
        
    def add_dwell(self, dwell):
        self.dwell_time += dwell
        
    def reduce_dwell(self):
        self.dwell_time -= 1

    def calculate_travel_time(self, graph, from_station, to_station):
        distance = graph[from_station][to_station]['weight']
        return (distance / self.speed) * 60  # Return travel time in minutes
