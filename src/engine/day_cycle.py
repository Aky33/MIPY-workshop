class DayCycle:
    def __init__(self, day_length_seconds=120):
        self.day_length = day_length_seconds
        self.time = 0.25 * self.day_length  # start v 06:00
        self.time_of_day = "morning"

    def update(self, dt):
        self.time = (self.time + dt) % self.day_length
        self._update_time_of_day()

    def _update_time_of_day(self):
        # Přepočítá čas na skutečné HH:MM
        total_minutes = (self.time / self.day_length) * 24 * 60
        hour = int(total_minutes // 60) % 24

        if 6 <= hour < 11:
            self.time_of_day = "morning"
        elif 11 <= hour < 15:
            self.time_of_day = "noon"
        elif 15 <= hour < 21:
            self.time_of_day = "afternoon"
        else:
            self.time_of_day = "night"

    def get_overlay_color(self):
        if self.time_of_day == "morning":
            return (120, 120, 100, 80)     # tmavší rozbřesk
        elif self.time_of_day == "noon":
            return (255, 255, 255, 0)      # žádný filtr, plné světlo
        elif self.time_of_day == "afternoon":
            return (150, 130, 100, 50)     # teplé odpolední tóny
        else:  # night
            return (10, 10, 30, 130)       # velmi tmavá noc

    def get_time_string(self):
        total_minutes = (self.time / self.day_length) * 24 * 60
        hours = int(total_minutes // 60) % 24
        minutes = int(total_minutes % 60)
        return f"{hours:02}:{minutes:02}"

    def skip_to_morning(self):
        self.time = 0.25 * self.day_length  # 06:00
        self._update_time_of_day()

    def get_hour(self):
        total_minutes = (self.time / self.day_length) * 24 * 60
        hours = int(total_minutes // 60) % 24
        return hours
