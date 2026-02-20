from FamilyTree import FamilyTree

tree = FamilyTree()
tree.generate_tree()

while True:
    choice = input("Are you interested in:\n(T)otal number of people in the tree\nTotal number of people in the tree by (D)ecade\n(N)ames duplicated\n> ")
    if choice == 'T':
        tree.print_total_people()
    elif choice == 'D':
        tree.print_total_people_by_decade()
    elif choice == 'N':
        tree.print_duplicate_names()

