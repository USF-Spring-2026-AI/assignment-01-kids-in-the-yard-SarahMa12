from PersonFactory import PersonFactory
import random as rand
import math

class FamilyTree:
    def __init__(self):
        self.pf = PersonFactory()
        self.pf.read_files()

        self.people = set()


    def generate_root_people(self):
        """Helper function: generate two random people as the root"""
        p1 = self.pf.create_person(1950)
        p2 = self.pf.create_person(1950)

        p1.set_spouse(p2)
        p2.set_spouse(p1)

        self.people.add(p1)
        self.people.add(p2)

        return [p1, p2]

    def generate_tree(self):
        """Generate the family tree from the two root people. Also contains the logic for whether a person has a spouse and/or has children"""
        print("Generating family tree...")

        # Create the two root people born in 1950
        curr_gen = self.generate_root_people()
        
        # Save the children of the current generation
        next_gen = set()

        # While there are still people in the current generation
        while curr_gen:
            for p in curr_gen:
                decade = p.get_year_born() // 10 * 10

                # Check marriage probability for the person
                marriage_probability = self.pf.marriage_rates.get(decade)
                if p.get_spouse() is None and rand.random() <= marriage_probability:
                    spouse = self.pf.create_spouse(p)
                    self.people.add(spouse)

                # Determine number of children the person has
                birth_rate = self.pf.birth_rates.get(decade)

                # Min and max amount of children then randomly pick a number between (rounding up)
                min_children = birth_rate - 1.5
                max_children = birth_rate + 1.5
                num_children = math.ceil(rand.uniform(min_children, max_children))

                # For the number of chilren, create a child
                for _ in range(num_children):
                    child = self.pf.create_child(p)
                    # If the child was generated (wouldn't be generated if birth year is greater than 2120)
                    if child:
                        self.people.add(child)
                        next_gen.add(child)
                
            curr_gen = list(next_gen)
            next_gen = set()

    # Query functions
    def print_total_people(self):
        """Print total people in the tree"""
        print(f"The tree contains {len(self.people)} people total")
    
    def print_total_people_by_decade(self):
        """Print total people by decade"""
        counts = {}
        for p in self.people:
            decade = p.get_year_born() // 10 * 10
            counts[decade] = counts.get(decade, 0) + 1

        for decade in sorted(counts):
            print(f"{decade}: {counts[decade]}")

    def print_duplicate_names(self):
        """Print duplicate names"""
        name_counts = {}
        for p in self.people:
            full_name = f"{p.get_first_name()} {p.get_last_name()}"
            name_counts[full_name] = name_counts.get(full_name, 0) + 1

        duplicates = {}
        for name in name_counts:
            if name_counts[name] > 1:
                duplicates[name] = name_counts[name]
        
        if duplicates:
            print(f"There are {len(duplicates)} duplicate names in the tree:")
            for name in duplicates:
                print(f"* {name}")
        else:
            print("No duplicate names in the tree.")


            






