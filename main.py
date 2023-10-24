import os
import csv
import logging

from prettytable import PrettyTable

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

"""
Name, Description, Activity Dates (Individual), Scheduled Days, Scheduled Start Time, Scheduled End Time, 
Duration, Allocated Location Name, Allocated Staff Name, Zone Name
"""

class Timetable:
    def __init__(self):
        self.schedules = []

    # Load data from a CSV file
    def load_data(self, folder_path):
        self.schedules = []

        if not os.path.exists(folder_path):
            print("")
            logging.error("Input a valid path, rerun the program.\n".format(folder_path))
            exit(1)

        all_csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

        if not all_csv_files:
            print("")
            logging.error("No csv files found at [{}] path, rerun the program.\n".format(folder_path))
            exit(1)
        else:
            print("")
            print("Files are successfully loaded, proceeding further.")

        for _csv in all_csv_files:
            file_path = os.path.join(folder_path, _csv)
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['Scheduled Days'] != "Online Learning":
                        name_parts = row['Name'].split('_')
                        module_code = name_parts[1].strip()
                        course_type = name_parts[2].strip()
                        module_name = name_parts[3].strip()
                        session_name = name_parts[4].strip()
                        row['course_type'] = course_type
                        row['module_name'] = module_name
                        row['module_code'] = module_code
                        row['session_name'] = session_name
                        row['lecturer_name'] = row['Allocated Staff Name']
                        if row['']:
                            del row['']
                        self.schedules.append(row)

    def all_modules(self):
        module_name_with_code = {}
        for module in self.schedules:
            module_name_with_code[module['module_name']] = module['Description']
        return module_name_with_code


    def all_lecturers(self):
        raw_lecturer_names = []
        dedup_lecturer_name = []
        for lecturer in self.schedules:
            raw_lecturer_names.append(lecturer['lecturer_name'])
        for item in raw_lecturer_names:
            if item not in dedup_lecturer_name:
                dedup_lecturer_name.append(item)
        return dedup_lecturer_name


    def all_locations(self):
        raw_locations = []
        dedup_locations = []
        for loc in self.schedules:
            raw_locations.append(loc['Zone Name'])

        for item in raw_locations:
            if item not in dedup_locations:
                dedup_locations.append(item)
        return dedup_locations

    
    # List schedules based on user selection
    def list_schedules(self, filter_value):
        # Display the filtered and sorted data in a pretty table
        list_table = PrettyTable()
        column_order = [
            'module_name', 'Description', 'Activity Dates (Individual)', 'Scheduled Days', 'Scheduled Start Time',
            'Scheduled End Time',
            'Duration', 'Allocated Location Name', 'Planned Size', 'Allocated Staff Name', 'Zone Name'
        ]
        list_table.field_names = column_order
        filtered_schedules = [schedule for schedule in self.schedules for k,v in schedule.items() if v == filter_value]
        for row in filtered_schedules:
            list_table.add_row([row[column] for column in column_order])
        return list_table

# Main program
if __name__ == "__main__":
    timeTabler = Timetable()
    print("")
    print("  Welcome to \n")
    print("""  _______ _             _______    _     _   __      ___                        
 |__   __(_)           |__   __|  | |   | |  \ \    / (_)                       
    | |   _ _ __ ___   ___| | __ _| |__ | | __\ \  / / _  _____      _____ _ __ 
    | |  | | '_ ` _ \ / _ \ |/ _` | '_ \| |/ _ \ \/ / | |/ _ \ \ /\ / / _ \ '__|
    | |  | | | | | | |  __/ | (_| | |_) | |  __/\  /  | |  __/\ V  V /  __/ |   
    |_|  |_|_| |_| |_|\___|_|\__,_|_.__/|_|\___| \/   |_|\___| \_/\_/ \___|_| """)
    print("")
    folder_path = input("Enter the folder path with (.csv) files: ")

    timeTabler.load_data(folder_path)

    choices = {1: "List by Module",
               2: "List by Lecturer",
               3: "List by Location/Zone",
               4: "Exit"}
    all_mode = timeTabler.all_modules()
    all_lect = timeTabler.all_lecturers()
    all_zones = timeTabler.all_locations()

    while True:
        choice = ''
        print("\nInput from following Options:")
        print("")
        for k, v in choices.items():
            print("  {}: {}".format(k, v))

        try:
            print("")
            choice = int(input("Enter your choice: "))
            print("")
            if choice not in choices:
                logging.error("Please input from above options.")
                continue

            if choice == 1:
                print("Choose module code from folllowing list:")
                print("")
                for k, v in all_mode.items():
                    print(" {}: {}".format(k, v))
                print("")
                module_name = input("Enter module code from above: ")
                if module_name not in all_mode:
                    logging.error("Please input module code from above list")
                    continue
                filtered_schedules = timeTabler.list_schedules(module_name)
                print(filtered_schedules)
                continue
            if choice == 2:
                print("lecurer details names are as follows:")
                for lect in all_lect:
                    print(" {}".format(lect))
                lect_name = input("Enter Lecturer name from above: ")
                if lect_name not in all_lect:
                    logging.error("Please input lecturer name from above list")
                    continue
                filtered_schedules = timeTabler.list_schedules(lect_name)
                print(filtered_schedules)
                continue
            if choice == 3:
                print("Zone/Location names are as follows:")
                for loc in all_zones:
                    print(" {}".format(loc))
                loc_name = input("Enter Location name from above: ")
                if loc_name not in all_zones:
                    logging.error("Please input lecturer name from above list")
                    continue
                filtered_schedules = timeTabler.list_schedules(loc_name)
                print(filtered_schedules)
                continue
            elif choice == '4':
                print("Good Choice! Bye!!")
                break
        except ValueError:
            logging.error("Retry input from above options.")
            continue
        else:
            print("  Good Choice! Bye!!")
            print("")
            break
