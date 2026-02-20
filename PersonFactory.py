from Person import Person
import pandas as pd
import random as rand

class PersonFactory:
    def __init__(self):
        self.life_expectancy = {}
        self.first_names = {}
        self.last_names = {}
        self.marriage_rates = {}
        self.birth_rates = {}

    def read_files(self):
        """Read the files and store them in the corresponding dictionaries"""
        print("Reading files...")

        # Reading list expectancy data
        le = pd.read_csv('life_expectancy.csv')
        
        # Source: How to iterate pandas read csv output https://stackoverflow.com/questions/55091244/iterate-through-csv-rows-with-pandas-perform-selenium-action
        for index, row in le.iterrows():
            year = row["Year"]
            life_expectancy = row["Period life expectancy at birth"]
            self.life_expectancy[year] = life_expectancy

        # Reading first name data
        fn = pd.read_csv('first_names.csv')

        for index, row in fn.iterrows():
            decade = int(row['decade'].replace('s', ''))
            gender = row['gender']
            fname = row['name']
            freq = row['frequency']

            if decade not in self.first_names:
                self.first_names[decade] = {'male': [], "female": []}

            self.first_names[decade][gender].append((fname, freq))

        # Reading last name data
        ln = pd.read_csv('last_names.csv')
        rtp = pd.read_csv('rank_to_probability.csv', header=None)

        # Source: How to turn pandas read csv into a list https://stackoverflow.com/questions/71580700/creating-list-from-imported-csv-file-with-pandas
        rtp_list = rtp.values[0].tolist()

        for index, row in ln.iterrows():
            decade = int(row['Decade'].replace('s', ''))
            rank = row['Rank']
            lname = row['LastName']

            probability = rtp_list[rank - 1] # Subtract 1 because indexes start at 0 while ranks start at 1
            
            if decade not in self.last_names:
                self.last_names[decade] = []

            self.last_names[decade].append((lname, probability))

        # Reading birth and marriage rate data
        bmrates = pd.read_csv('birth_and_marriage_rates.csv')

        for index, row in bmrates.iterrows():
            decade = int(row['decade'].replace('s', ''))
            birth_rate = row['birth_rate']
            marriage_rate = row['marriage_rate']

            self.birth_rates[decade] = birth_rate
            self.marriage_rates[decade] = marriage_rate

    def get_life_expectancy(self, year_born):
        """Helper function: calculate life expectancy range and return a random number from the range"""
        life_expectancy = self.life_expectancy[year_born]

        middle = year_born + life_expectancy
        min_life_exp = int(middle - 10)
        max_life_exp = int(middle + 10)

        return rand.randint(min_life_exp, max_life_exp)

    def get_fname(self, year_born):
        """Helper function: choose a random first name based on decade and weights"""
        gender = rand.choice(['male', 'female'])

        # Find the decade by // 10 * 10
        decade = year_born // 10 * 10
        
        names_and_weights = self.first_names[decade][gender]

        names = []
        weights = []
        for n, w in names_and_weights:
            names.append(n)
            weights.append(w)

        return rand.choices(names, weights=weights, k = 1)[0]

    def get_lname(self, year_born):
        """Helper function: choose a random last name based on decade and weights"""
        decade = year_born // 10 * 10

        names_and_weights = self.last_names[decade]
        
        names = []
        weights = []
        for n, w in names_and_weights:
            names.append(n)
            weights.append(w)

        return rand.choices(names, weights=weights, k = 1)[0]

    def create_person(self, year_born):
        """Create person function: creates a person with a year born, year died, first name, and last name"""
        # Get year died
        year_died = self.get_life_expectancy(year_born)

        # Get first name
        first_name = self.get_fname(year_born)

        # Get last name
        last_name = self.get_lname(year_born)

        return Person(first_name, last_name, year_born, year_died)

    def create_spouse(self, person):
        """Create spouse function: creates a spouse with year born within +- 10 years of person passed through the argument"""
        # Calculate min and max birth year for the spouse, make sure max can't be after 2120
        min_birth_year = person.get_year_born() - 10
        max_birth_year = min(person.get_year_born() + 10, 2120)
        
        # If the range is valid (min < max) then calculate random number between the min and max, otherwise return None
        if min_birth_year <= max_birth_year:
            spouse_year = rand.randint(min_birth_year, max_birth_year)
        else:
            return None
        
        # Create the spouse as a new person
        spouse = self.create_person(spouse_year)
        
        person.set_spouse(spouse)
        spouse.set_spouse(person)

        return spouse

    def create_child(self, parent):
        """Create child function: creates a child with year born within +25 to +45 years of the parent(s)"""
        # Get the spouse of the parent
        spouse = parent.get_spouse()

        # Get the older parents birth year
        elder_parent_birth_year = parent.get_year_born()
        if spouse:
            elder_parent_birth_year = min(elder_parent_birth_year, spouse.get_year_born())
        
        # Calculate min and max birth year for the child, make sure max can't be after 2120
        min_birth_year = elder_parent_birth_year + 25
        max_birth_year = min(elder_parent_birth_year + 45, 2120)

        # If the range is valid (min < max) then calculate random number between the min and max, otherwise return None
        if min_birth_year <= max_birth_year:
            child_year_born = rand.randint(min_birth_year, max_birth_year)
        else:
            return None
        
        # Get a random first name
        first_name = self.get_fname(child_year_born)

        # Get the last name, if there is a spouse, choose random one between both parents, else just choose the single parent's last name
        if spouse:
            last_name = rand.choice([parent.get_last_name(), spouse.get_last_name()])
        else:
            last_name = parent.get_last_name()

        # Get year died
        year_died = self.get_life_expectancy(child_year_born)

        # Create the child
        child = Person(first_name, last_name, child_year_born, year_died)

        parent.add_child(child)
        if spouse:
            spouse.add_child(child)

        return child