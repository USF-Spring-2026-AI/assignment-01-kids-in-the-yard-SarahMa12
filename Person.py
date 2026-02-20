class Person:
    def __init__(self, first_name, last_name, year_born, year_died):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.year_died = year_died
        self.spouse = None
        self.children = []

    def set_spouse(self, spouse):
        self.spouse = spouse

    def add_child(self, child):
        self.children.append(child)

    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_year_born(self):
        return self.year_born
    
    def get_year_died(self):
        return self.year_died
    
    def get_spouse(self):
        return self.spouse
    
    def get_year_died(self):
        return self.year_died
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}, Born: {self.year_born}, Died: {self.year_died}")