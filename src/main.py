from models.station import Station
from models.train import Train
from simulation.graph_builder import build_graph, visualize_graph
import networkx as nx
from datetime import datetime, timedelta
from simulation.simulator import simulate_trains
from simulation.logger import log_event

def main(pheromones):
    # Create stations
    station_a = Station(name="York", platforms_general=11, dwell_time=2)
    station_b = Station(name="Ullskelf", platforms_up=1, platforms_down=1, dwell_time=1)
    station_c = Station(name="Church Fenton", platforms_up=2, platforms_down=1)
    station_d = Station(name="Micklefield", platforms_up=1, platforms_down=1)
    station_e = Station(name="East Garforth", platforms_up=1, platforms_down=1)
    station_f = Station(name="Garforth", platforms_up=1, platforms_down=1)
    station_g = Station(name="Cross Gates", platforms_up=1, platforms_down=1)
    station_h = Station(name="Leeds", platforms_general=18, dwell_time=2)
    station_i = Station(name="Cottingley", platforms_up=1, platforms_down=1)
    station_j = Station(name="Morley", platforms_up=1, platforms_down=1)
    station_k = Station(name="Batley", platforms_up=1, platforms_down=1)
    station_l = Station(name="Dewsbury", platforms_up=1, platforms_down=1)
    station_m = Station(name="Ravensthorpe", platforms_up=1, platforms_down=1)
    station_n = Station(name="Mirfield", platforms_up=1, platforms_down=1)
    station_o = Station(name="Deighton", platforms_up=1, platforms_down=1)
    station_p = Station(name="Huddersfield", platforms_general=8, dwell_time=2)
    station_q = Station(name="Slaithwaite", platforms_up=1, platforms_down=1)
    station_r = Station(name="Marsden", platforms_up=1, platforms_down=1)
    station_s = Station(name="Greenfield", platforms_up=1, platforms_down=1)
    station_t = Station(name="Mossley", platforms_up=1, platforms_down=1)
    station_u = Station(name="Stalybridge", platforms_up=1, platforms_general=1, platforms_down=1)
    station_v = Station(name="Ashton-Under-Lyne", platforms_up=1, platforms_down=1)
    station_w = Station(name="Manchester Victoria", platforms_general=4, dwell_time=2)

    
    
    
    
    
    #Always input the up direction, down will be added automatically. E.g Manchester to York
    edges = [
        ("Manchester Victoria", "Ashton-Under-Lyne", 6.30),
        ("Ashton-Under-Lyne", "Stalybridge", 1.21),
        ("Stalybridge", "Mossley",2.54),
        ("Mossley", "Greenfield", 2.43),
        ("Greenfield", "Marsden", 6.08),
        ("Marsden", "Slaithwaite", 2.66),
        ("Slaithwaite", "Huddersfield", 4.44),
        ("Huddersfield", "Deighton", 2.00),
        ("Deighton", "Mirfield", 2.69),
        ("Mirfield", "Ravensthorpe", 1.65),
        ("Ravensthorpe", "Dewsbury", 1.43),
        ("Dewsbury", "Batley", 1.34),
        ("Batley", "Morley", 3.18),
        ("Morley", "Cottingley", 2.08),
        ("Cottingley", "Leeds", 2.55),
        ("Leeds", "Cross Gates", 4.41),
        ("Cross Gates", "Garforth", 2.86),
        ("Garforth", "East Garforth", 0.59),
        ("East Garforth", "Micklefield", 1.43),
        ("Micklefield", "Church Fenton", 5.24),
        ("Church Fenton", "Ullskelf", 1.86),
        ("Ullskelf", "York", 8.88)
    ]

   # Build graph network
    graph = build_graph(
        stations=[station_a, station_b, station_c, station_d, station_e, station_f, station_g, station_g, station_h, station_i, station_j,station_k, station_l, station_m, station_n, station_o, station_p, station_q, station_r, station_s, station_t, station_u, station_v, station_w],  # Add all stations
        edges=edges
    )

    # Define trains with routes and schedules
    trains = [

        Train(id="TPX_York_MV_4",     route=["York", "Leeds", "Huddersfield", "Manchester Victoria", "Huddersfield", "Leeds", "York","Leeds", "Huddersfield", "Manchester Victoria", "Huddersfield", "Leeds", "York"],
              schedule=["08:00", "08:35", "09:01", "09:38", "10:15", "10:41", "11:20","11:55", "12:21", "12:58", "13:35", "14:01", "14:40"], speed=50,TrainType="express", TrainDis="LongDistance"),
            Train(id="TPX_MV_York_4", route=["Manchester Victoria", "Huddersfield", "Leeds", "York", "Leeds", "Huddersfield", "Manchester Victoria", "Huddersfield", "Leeds", "York", "Leeds", "Huddersfield", "Manchester Victoria"],
      schedule=["08:00", "08:36", "09:02", "09:38", "10:14", "10:40", "11:17", "11:53", "12:19", "12:55", "13:31", "13:57", "14:34"], speed=50, TrainType="express", TrainDis="LongDistance"),
        
        Train(id="TPX_York_MV_5", route=["York", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "York", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "York"],
      schedule=["08:20", "08:55", "09:10", "09:22", "09:59", "10:36", "10:49", "11:03", "11:39", "12:14", "12:29", "12:41", "13:18", "13:55", "14:08", "14:22", "14:58"], speed=50, TrainType="express", TrainDis="LongDistance"),

      Train(id="TPX_MV_York_5", route=["Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "York", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "York", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria"],
      schedule=["08:20", "08:55", "09:08", "09:22", "10:02", "10:41", "10:56", "11:08", "11:45", "12:20", "12:33", "12:47", "13:27", "14:06", "14:21", "14:33", "15:10"], speed=50, TrainType="express", TrainDis="LongDistance"),

        

        Train(id="TPX_York_MV_6", route=["York", "Garforth", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "Garforth", "York", "Garforth", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "Garforth", "York"],
      schedule=["08:40", "09:05", "09:16", "09:31", "09:43", "10:20", "10:57", "11:10", "11:24", "11:36", "12:01", "12:26", "12:37", "12:52", "13:04", "13:41", "14:18", "14:31", "14:45", "14:57", "15:22"], speed=50, TrainType="express", TrainDis="LongDistance"),

      Train(id="TPX_MV_York_6", route=["Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "Garforth", "York", "Garforth", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria", "Huddersfield", "Dewsbury", "Leeds", "Garforth", "York", "Garforth", "Leeds", "Dewsbury", "Huddersfield", "Manchester Victoria"],
            schedule=["08:40", "09:16", "09:29", "09:43", "09:55", "10:20", "10:46", "10:57", "11:12", "11:23", "12:01", "12:37", "12:50", "13:04", "13:16", "13:41", "14:07", "14:18", "14:33", "14:44", "15:22"], speed=50, TrainType="express", TrainDis="LongDistance"),


        
      Train(id="NOR_York_Leeds_5", route=["York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York"],
            schedule=["08:05", "08:27", "08:30", "08:32", "08:43", "08:55", "08:57", "09:00", "09:22", "09:45", "09:48", "09:50", "10:01", "10:13", "10:15", "10:18", "10:40", "11:03", "11:06", "11:08", "11:19", "11:31", "11:33", "11:36", "11:58", "12:21", "12:24", "12:26", "12:37", "12:49", "12:51", "12:54", "13:16", "13:39", "13:42", "13:44", "13:55", "14:07", "14:09", "14:12", "14:34"], speed=50, TrainType="express", TrainDis="ShortDistance"),

      Train(id="NOR_Leeds_York_5", route=["Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York", "Micklefield", "East Garforth", "Garforth", "Leeds", "Garforth", "East Garforth", "Micklefield", "York"],
            schedule=["08:05", "08:16", "08:18", "08:21", "08:43", "09:06", "09:09", "09:11", "09:22", "09:34", "09:36", "09:39", "10:01", "10:24", "10:27", "10:29", "10:40", "10:52", "10:54", "10:57", "11:19", "11:42", "11:45", "11:47", "11:58", "12:10", "12:12", "12:15", "12:37", "13:00", "13:03", "13:05", "13:16", "13:28", "13:30", "13:33", "13:55"], speed=50, TrainType="express", TrainDis="ShortDistance"),

      Train(id="TRX_Leeds_MV_4", route=["Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds"],
            schedule=["08:00", "08:25", "08:52", "09:03", "09:15", "09:41", "10:07", "10:33", "11:00", "11:11", "11:23", "11:49", "12:15", "12:41", "13:08", "13:19", "13:31", "13:57", "14:23"], speed=50, TrainType="express", TrainDis="ShortDistance"),

      Train(id="TRX_MV_Leeds_4", route=["Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria", "Stalybridge", "Huddersfield", "Leeds", "Huddersfield", "Stalybridge", "Manchester Victoria"],
            schedule=["08:00", "08:11", "08:37", "09:03", "09:29", "09:56", "10:07", "10:19", "10:45", "11:11", "11:37", "12:04", "12:15", "12:27", "12:53", "13:19", "13:45", "14:12", "14:23"], speed=50, TrainType="express", TrainDis="ShortDistance"),

      #CAN BE USED AS A TEST CASE
      Train(id="NOR_York_Leeds_7", route=["York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York"],
      schedule = ['08:10','08:28', '08:37', '08:41', '08:43', '08:49', '08:57', '09:06', '09:12', '09:14', '09:18', '09:27', '09:45', '10:04', '10:13', '10:17', '10:19', '10:25', '10:33', '10:42', '10:48', '10:50', '10:54', '11:03', '11:21', '11:40', '11:49', '11:53', '11:55', '12:01', '12:09', '12:18', '12:24', '12:26', '12:30', '12:39', '12:57', '13:16', '13:25', '13:29', '13:31', '13:37', '13:45', '13:54', '14:00', '14:02', '14:06', '14:15', '14:33', '14:52', '15:01', '15:05', '15:07', '15:13', '15:21', '15:30', '15:36', '15:38', '15:42', '15:51', '16:09']
,
      speed=40, TrainType="local", TrainDis='shortDistance'),
        Train(id="NOR_Leeds_York_7", route=["Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds", "Cross Gates", "Garforth", "East Garforth", "Micklefield", "Church Fenton", "York", "Church Fenton",  "Micklefield", "East Garforth", "Garforth", "Cross Gates", "Leeds"],
              schedule = ['08:10', '08:18', '08:24', '08:26', '08:30', '08:39', '08:57', '09:04', '09:06', '09:10', '09:19', '09:37', '09:56', '10:05', '10:09', '10:11', '10:17', '10:25', '10:34', '10:40', '10:42', '10:46', '10:55', '11:13', '11:32', '11:41', '11:45', '11:47', '11:53', '12:01', '12:10', '12:16', '12:18', '12:22', '12:31', '12:49', '13:08', '13:17', '13:21', '13:23', '13:29', '13:37']
            , speed=40, TrainType="local", TrainDis='shortDistance'),
      
        
         Train(id="TPX_Leeds_Huddersfield_9", route=["Leeds", "Cottingley", "Morley", "Batley", "Dewsbury", "Ravensthorpe", "Mirfield", "Deighton", "Huddersfield" , "Deighton", "Mirfield", "Ravensthorpe", "Dewsbury", "Batley", "Morley", "Cottingley", "Leeds", "Cottingley", "Morley", "Batley", "Dewsbury", "Ravensthorpe", "Mirfield", "Deighton", "Huddersfield" , "Deighton", "Mirfield", "Ravensthorpe", "Dewsbury", "Batley", "Morley", "Cottingley", "Leeds", "Cottingley", "Morley", "Batley", "Dewsbury", "Ravensthorpe", "Mirfield", "Deighton", "Huddersfield"],
               schedule = ['08:10','08:15', '08:20', '08:26', '08:30', '08:34', '08:38', '08:44', '08:48',
            '08:53', '08:59', '09:03', '09:07', '09:11', '09:17', '09:22', '09:27',
            '09:33', '09:38', '09:44', '09:48', '09:52', '09:56', '10:02', '10:06',
            '10:11', '10:17', '10:21', '10:25', '10:29', '10:35', '10:40', '10:45',
            '10:51', '10:56', '11:02', '11:06', '11:10', '11:14', '11:20', '11:24',
            '11:30', '11:36', '11:40', '11:44', '11:48', '11:54', '11:58', '12:03',
            '12:09', '12:13', '12:17', '12:21', '12:27', '12:32', '12:37', '12:43',
            '12:48', '12:54', '12:58', '13:02', '13:06', '13:12', '13:16', '13:21',
            '13:27', '13:31', '13:35', '13:39', '13:45', '13:50', '13:55', '14:01',
            '14:06', '14:12', '14:16', '14:20', '14:24', '14:30', '14:34']
, speed=40, TrainType="local", TrainDis="shortDistance"),
        
        Train(id="TPX_Huddersfield_Leeds_9", route=["Huddersfield" , "Deighton", "Mirfield", "Ravensthorpe", "Dewsbury", "Batley", "Morley", "Cottingley", "Leeds", "Cottingley", "Morley", "Batley", "Dewsbury", "Ravensthorpe", "Mirfield", "Deighton", "Huddersfield" , "Deighton", "Mirfield", "Ravensthorpe", "Dewsbury", "Batley", "Morley", "Cottingley", "Leeds", "Cottingley", "Morley", "Batley", "Dewsbury", "Ravensthorpe", "Mirfield", "Deighton", "Huddersfield", "Deighton", "Mirfield", "Ravensthorpe", "Dewsbury", "Batley", "Morley", "Cottingley", "Leeds"], 
               schedule = ['8:10','08:14', '08:20', '08:24', '08:28', '08:32', '08:38', '08:43', '08:48',
            '08:54', '08:59', '09:05', '09:09', '09:13', '09:17', '09:23', '09:27',
            '09:32', '09:38', '09:42', '09:46', '09:50', '09:56', '10:01', '10:06',
            '10:12', '10:17', '10:23', '10:27', '10:31', '10:35', '10:41', '10:45',
            '10:50', '10:56', '11:00', '11:04', '11:08', '11:14', '11:19', '11:24',
            '11:31', '11:35', '11:39', '11:43', '11:49', '11:54', '11:59', '12:05',
            '12:10', '12:16', '12:20', '12:24', '12:28', '12:34', '12:38', '12:43',
            '12:49', '12:53', '12:57', '13:01', '13:07', '13:12', '13:17', '13:23',
            '13:28', '13:34', '13:38', '13:42', '13:46', '13:52', '13:56', '14:01',
            '14:07', '14:11', '14:15', '14:19', '14:25', '14:30', '14:35']

 
 , speed=40, TrainType="local", TrainDis="shortDistance")]


        
    # Prompt user for simulation start time
    #start_time_str = input("Enter the simulation start time (HH:MM): ")
    start_time_str = "08:00"
    start_time = datetime.strptime(start_time_str, "%H:%M")
    #simulation_duration = int(input("Enter running duration (mm): "))
    simulation_duration = 500


    # Run the simulation for a defined duration (e.g., 90 minutes)
    simulate_trains(trains, graph, simulation_duration, pheromones,start_time=start_time)

if __name__ == "__main__":
    pheromones = {}  
    print(pheromones)
    for i in range(0,50):        
      main(pheromones)