import csv
import random
import math

class Person:
    """Stores details for each simulated person in the tree."""
    def __init__(self, first_name, last_name, year_born, gender, year_died):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.gender = gender
        self.year_died = year_died
        self.partner = None
        self.children = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PersonFactory:
    """Handles data loading and random generation of Person attributes."""
    def __init__(self):
        self.life_expectancy = {}
        self.first_names = {}  # decade -> gender -> list of (name, freq)
        self.last_names = []   # list of last names
        self.rank_probs = []   # list of probabilities from rank_to_probability.csv
        self.birth_marriage_rates = {}

    def read_files(self):
        """Reads all required CSV files from the current directory."""
        # 1. Life Expectancy
        with open('life_expectancy.csv', mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.life_expectancy[int(row['Year'])] = float(row['Period life expectancy at birth'])

        # 2. First Names
        with open('first_names.csv', mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dec = row['decade']
                gen = row['gender']
                if dec not in self.first_names:
                    self.first_names[dec] = {'male': [], 'female': []}
                self.first_names[dec][gen].append((row['name'], float(row['frequency'])))

        # 3. Last Names
        with open('last_names.csv', mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['LastName'].strip()
                if name:
                    self.last_names.append(name)

        # 4. Rank to Probability
        with open('rank_to_probability.csv', mode='r') as f:
            # Cleans up commas/newlines to ensure a clean list of floats
            content = f.read().replace(',', ' ').strip()
            self.rank_probs = [float(x) for x in content.split() if x]

        # 5. Birth and Marriage Rates
        with open('birth_and_marriage_rates.csv', mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.birth_marriage_rates[row['decade']] = (
                    float(row['birth_rate']), 
                    float(row['marriage_rate'])
                )

    def get_decade_string(self, year):
        """Helper to convert a year (1955) to a decade string ('1950s')."""
        return f"{(year // 10) * 10}s"

    def get_person(self, year_born, gender=None, last_name=None):
        """Generates a new Person object based on statistical data."""
        if gender is None:
            gender = random.choice(['male', 'female'])
        
        decade = self.get_decade_string(year_born)
        lookup_dec = decade if decade in self.first_names else "1950s"
        
        # Determine First Name using weighted frequency
        names_data = self.first_names[lookup_dec][gender]
        f_names = [n[0] for n in names_data]
        f_weights = [n[1] for n in names_data]
        f_name = random.choices(f_names, weights=f_weights, k=1)[0]
        
        # Determine Last Name (Rule: use rank probabilities if not inherited)
        if last_name is None:
            # ZIP ensures population and weights are identical length
            # Pairing Name #1 with Prob #1, Name #2 with Prob #2...
            valid_pairs = list(zip(self.last_names, self.rank_probs))
            pop = [p[0] for p in valid_pairs]
            weights = [p[1] for p in valid_pairs]
            
            if not pop:
                last_name = "Jones"  # Absolute fallback
            else:
                last_name = random.choices(pop, weights=weights, k=1)[0]
            
        # Determine Year Died (Life expectancy +/- 10 years)
        expectancy = self.life_expectancy.get(year_born, 72.0)
        year_died = year_born + int(expectancy + random.uniform(-10, 10))
        
        return Person(f_name, last_name, year_born, gender, year_died)

class FamilyTree:
    """The main simulation engine for building and querying the family tree."""
    def __init__(self):
        self.factory = PersonFactory()
        self.all_people = []

    def generate(self):
        print("Reading files...")
        self.factory.read_files()
        print("Generating family tree...")

        # Founder pair (Desmond and Molly Jones)
        p1 = Person("Desmond", "Jones", 1950, "male", 1950 + 72)
        p2 = Person("Molly", "Jones", 1950, "female", 1950 + 75)
        p1.partner, p2.partner = p2, p1
        self.all_people.extend([p1, p2])
        
        # Use a queue for breadth-first generation processing
        queue = [p1, p2]
        processed_pairs = set()

        while queue:
            parent = queue.pop(0)
            
            # Use unique IDs to ensure we don't process a couple twice
            pair_id = tuple(sorted([id(parent), id(parent.partner) if parent.partner else 0]))
            if pair_id in processed_pairs:
                continue
            processed_pairs.add(pair_id)

            decade = self.factory.get_decade_string(parent.year_born)
            # Default fallback if decade is missing in file
            b_rate, m_rate = self.factory.birth_marriage_rates.get(decade, (1.8, 0.4))
            
            # Calculation: Birth rate +/- 1.5, rounded up
            num_children = math.ceil(b_rate + random.uniform(-1.5, 1.5))
            for _ in range(max(0, num_children)):
                # Child birth year: Parent birth + 25 to 45
                child_year = parent.year_born + random.randint(25, 45)
                
                # Termination condition: No children after 2120
                if child_year > 2120: 
                    continue
                
                # Rule: Child directly descended keeps parent's last name
                child = self.factory.get_person(child_year, last_name=parent.last_name)
                parent.children.append(child)
                self.all_people.append(child)

                # Determine if child has a partner (Marriage Rate probability)
                if random.random() < m_rate:
                    p_year = child_year + random.randint(-10, 10)
                    partner = self.factory.get_person(p_year) # Partner gets random last name
                    child.partner, partner.partner = partner, child
                    self.all_people.append(partner)
                    queue.append(child) 
                else:
                    queue.append(child)

    def run_menu(self):
        """Interactive terminal menu for reporting."""
        while True:
            print("\nAre you interested in:")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("(Q)uit")
            choice = input("> ").upper()

            if choice == 'T':
                print(f"The tree contains {len(self.all_people)} people total")
            elif choice == 'D':
                counts = {}
                for p in self.all_people:
                    d = (p.year_born // 10) * 10
                    counts[d] = counts.get(d, 0) + 1
                for d in sorted(counts.keys()):
                    print(f"{d}: {counts[d]}")
            elif choice == 'N':
                name_map = {}
                for p in self.all_people:
                    full = f"{p.first_name} {p.last_name}"
                    name_map[full] = name_map.get(full, 0) + 1
                dupes = [name for name, count in name_map.items() if count > 1]
                print(f"There are {len(dupes)} duplicate names in the tree:")
                for d in dupes: print(f"* {d}")
            elif choice == 'Q':
                break

if __name__ == "__main__":
    ft = FamilyTree()
    ft.generate()
    ft.run_menu()