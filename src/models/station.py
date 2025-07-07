class Station:
    def __init__(self, name, platforms_up=0, platforms_down=0, platforms_general=0, dwell_time=1):
        """
Represents a railway station with platform allocation for up, down, and general directions.

Args:
    name (str): Name of the station.
    platforms_up (int): Number of platforms for up-direction trains.
    platforms_down (int): Number of platforms for down-direction trains.
    platforms_general (int): Number of general-purpose platforms.
    dwell_time (int): Minimum time trains must spend at the station.

        """
        self.name = name
        self.platforms_up = platforms_up
        self.platforms_down = platforms_down
        self.platforms_general = platforms_general
        self.dwell_time = dwell_time
        self.schedule = []  # List of trains currently at the station

    def can_accommodate(self, train):
        platform_capacity = {
        'up': self.platform_up,
        'down': self.platform_down,
    }

        count = sum(1 for i in self.schedule if i.direction == train.direction)
        return count < platform_capacity.get(train.direction, 0) + self.platform_general

        
    def update_schedule(self, train):
        """
        Add a train to the station's schedule.

        :param train: The train to add.
        """
        if self.can_accommodate(train):
            self.schedule.append(train)
        else:
            raise ValueError(f"Cannot accommodate train {train.id} at {self.name}")

    def remove_train(self, train):
        """
        Remove a train from the station's schedule.

        :param train: The train to remove.
        """
        self.schedule.remove(train)