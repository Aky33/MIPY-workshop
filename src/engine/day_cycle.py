class DayCycle:
    def __init__(self, day_length_seconds=120):
<<<<<<< Updated upstream
        self.day_length = day_length_seconds
        # Start v 06:00 ⇒ odpovídá tomu, jako by uběhlo 6/24 = 0.25 cyklu
        self.time_elapsed = 0.25 * self.day_length
        self.time_of_day = "morning"  # Výchozí fáze

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed > self.day_length:
            self.time_elapsed -= self.day_length

        self._update_phase()

    def _update_phase(self):
        phase = self.time_elapsed / self.day_length
        if phase < 0.25:
            self.time_of_day = "morning"
        elif phase < 0.5:
            self.time_of_day = "afternoon"
        elif phase < 0.75:
=======
        self.day_length = day_length_seconds  # celková délka dne ve hře (v sekundách)
        self.time = 0                         # aktuální čas od začátku dne (v sekundách)
        self.time_of_day = "morning"          # výchozí čas dne

    def update(self, dt):
        self.time = (self.time + dt) % self.day_length
        self.update_time_of_day()

    def update_time_of_day(self):
        portion = self.time / self.day_length

        if portion < 0.25:
            self.time_of_day = "morning"
        elif portion < 0.5:
            self.time_of_day = "afternoon"
        elif portion < 0.75:
>>>>>>> Stashed changes
            self.time_of_day = "evening"
        else:
            self.time_of_day = "night"

    def get_overlay_color(self):
<<<<<<< Updated upstream
        colors = {
            "morning": (255, 255, 200, 40),
            "afternoon": (255, 255, 255, 0),
            "evening": (100, 100, 180, 60),
            "night": (30, 30, 80, 120),
        }
        return colors.get(self.time_of_day, (0, 0, 0, 0))

    def get_time_string(self):
        # Vrací čas ve formátu HH:MM (24h) podle aktuálního posunu
        total_minutes = int((self.time_elapsed / self.day_length) * 24 * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
=======
        # Vratíme barvu pro překrytí podle denní doby
        if self.time_of_day == "morning":
            return (255, 255, 224, 30)  # světlé žluté ráno
        elif self.time_of_day == "afternoon":
            return (255, 255, 255, 0)   # bez překrytí
        elif self.time_of_day == "evening":
            return (100, 100, 150, 60)  # modravý večer
        else:  # night
            return (0, 0, 40, 120)      # tmavá noc

    def get_time_hhmm(self):
        total_minutes = (self.time / self.day_length) * 24 * 60
        hours = int(total_minutes // 60) % 24
        minutes = int(total_minutes % 60)
>>>>>>> Stashed changes
        return f"{hours:02}:{minutes:02}"
