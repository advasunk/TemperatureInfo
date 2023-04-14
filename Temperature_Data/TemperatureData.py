import errno
import math
import statistics
import pandas as pd


class TempDataset:
    """
    Class to store temperature data
    """
    num_TempDataset = 0

    def __init__(self):
        """
        To initialize everything
        """
        self._dataset_name = "Unnamed"
        self._data_set = None
        TempDataset.num_TempDataset = TempDataset.num_TempDataset + 1

    @property
    def name(self):
        """
        returns the name
        """
        return self._dataset_name

    @name.setter
    def name(self, new_name):
        """
        sets instance name to new name if amount if characters is in between 3-20,
        inclusive
        """
        if (len(new_name) >= 3) and (len(new_name) <= 20):
            self._dataset_name = new_name
        else:
            raise ValueError

    def process_file(self, filename):
        """
        Function to read the data and add it to _data_set
        """
        try:
            with open(filename) as f:
                self._data_set = []
                all_lines = f.readlines()
                for i in range(len(all_lines) - 1):
                    next_line = all_lines[i]
                    data_line = next_line.split(",")
                    if data_line[3] == "TEMP":
                        day = data_line[0]
                        # print(day)
                        time = data_line[1]
                        sensor = data_line[2]
                        temp = data_line[4]
                        day_int = int(day)
                        sensor_int = int(sensor)
                        temp_float = float(temp)
                        time_float = float(time)
                        timeOday = time_float * 24
                        timeofday = math.floor(timeOday)

                        temp_read = (day_int, timeofday, sensor_int, temp_float)
                        self._data_set.append(temp_read)

                return True

        except IOError as x:
            if x.errno == errno.ENOENT:
                return False

    def get_summary_statistics(self, filter_list, units):
        """
        Function to find and return the average, minimum, and maximum temperatures
        """
        new_list = [temp_data for temp_data in self._data_set if temp_data[2] in filter_list]
        temps = []
        for x in new_list:
            temperature = x[3]
            temps.append(temperature)

        average_temp = statistics.mean(temps)
        minimum_temp = min(temps)
        maximum_temp = max(temps)
        converted_min = convert_units(minimum_temp, units)
        converted_max = convert_units(maximum_temp, units)
        converted_avg = convert_units(average_temp, units)
        rounded_min = float(round(converted_min, 2))
        rounded_max = float(round(converted_max, 2))
        rounded_avg = float(round(converted_avg, 2))

        min_max_avg = (rounded_min, rounded_max, rounded_avg)
        return min_max_avg

    def get_avg_temperature_day_time(self, filter_list, day, time):
        """
        Function to return the average temperature of select days and times of certain rooms
        """
        if filter_list is None or len(filter_list) == 0 or self._data_set is None:
            return None
        else:
            # filter to filter temperature by selected day
            new_list = [temp_data for temp_data in self._data_set if temp_data[0] == day]
            # filter to filter temperature by selected time
            new_list = [temp_data for temp_data in new_list if temp_data[1] == time]
            # filter to filter temperature by active sensors
            new_list = [temp_data for temp_data in new_list if temp_data[2] in filter_list]
            temps = []
            for x in new_list:
                temperature = x[3]
                temps.append(temperature)
            average_temp = statistics.mean(temps)
            return average_temp

    def get_num_temps(self, active_sensors, lower_bound, upper_bound):
        if self._data_set is None:
            return None
        else:
            return 0

    def get_loaded_temps(self):
        """
        Function to return the length of the _data_set
        """
        if self._data_set is None:
            return None
        else:
            return len(self._data_set)

    @classmethod
    def get_num_objects(cls):
        """
        a class method that returns the number of times the class is initialized
        """
        return cls.num_TempDataset


def print_header():
    """
    Print header
    """
    print("STEM Center Temperature Project")
    print("Advaith Sunkara")


def convert_units(celsius_units, units):
    """
    Function to convert temperature from Celsius to Fahrenheit or Kelvin
    """
    if units == 0:
        cels = celsius_units
        return cels

    elif units == 1:
        fahr = (celsius_units * 1.8) + 32
        return fahr

    elif units == 2:
        kev = (celsius_units + 273.15)
        return kev

    else:
        return "*** Invalid Input, the conversion type must be 0, 1, 2):  You entered an illegal value"


def print_menu():
    """
    Print menu for user interface
    """
    print("Main Menu")
    print("---------")
    print("1 - Process a new data file")
    print("2 - Choose units")
    print("3 - Edit room filter")
    print("4 - Show summary statistics")
    print("5 - Show temperature by date and time")
    print("6 - Show histogram of temperatures")
    print("7 - Quit")
    print("")


def new_file(dataset):
    """
    Open a new file
    """
    file_name = input("Please enter the filename of the new dataset: ")
    if dataset.process_file(file_name) is False:
        print("Unable to load a file!")
    else:
        print("Loaded " + str(dataset.get_loaded_temps()) + " samples")
        valid_name = False
        while not valid_name:
            data_name = input("Please provide a 3 to 20 character name for the dataset My Data Set: ")
            try:
                dataset.name = data_name
                valid_name = True
            except ValueError:
                valid_name = False
                print("Name is invalid, please try again.")


def choose_units():
    """
    Function to choose units for conversion
    """
    global units_selected
    if units_selected is None:
        units_selected = 0
    print("Current units in " + str(UNITS[units_selected][0]))

    valid_option = False
    while valid_option is False:
        try:
            print("Choose new units: ")
            for x in UNITS:
                print(str(x) + " - " + (UNITS[x][0]))
            units_selected = int(input("Which unit? "))
            if units_selected not in UNITS:
                raise EOFError
            else:
                valid_option = True
        except ValueError:
            print("***Please enter a number only***")
        except EOFError:
            print("Please choose a unit from the list")


def change_filter(sensors, sensor_list, filter_list):
    """
    Changing filter's status (ACTIVE or not) based on user's room choice
    """
    print("")
    user_input = ""
    while user_input != "x":
        print_filter(sensor_list, filter_list)
        print("")
        user_input = input("Type the sensor to toggle (e.g. 4201) or x to end: ")
        print("")

        if user_input in sensors:
            if sensors[user_input][1] in filter_list:
                filter_list.remove(sensors[user_input][1])
            else:
                filter_list.append(sensors[user_input][1])
        else:
            if user_input != "x":
                print("Invalid Sensor")


def print_summary_statistics(dataset, active_sensors, units):
    """
    Print the maximum, minimum, and average temperatures
    """
    degrees = ""
    if units == 0:
        degrees = "C"
    elif units == 1:
        degrees = "F"
    elif units == 2:
        degrees = "K"
    summary_stats = dataset.get_summary_statistics(active_sensors, units)
    print("Minimum Temperature: " + str(summary_stats[0]) + " " + degrees)
    print("Maximum Temperature: " + str(summary_stats[1]) + " " + degrees)
    print("Average Temperature: " + str(summary_stats[2]) + " " + degrees)


def print_temp_by_the_day_time(dataset, active_sensors):
    """
    Print the average temp of every hour in each day as a DataFrame in pandas
    """
    dataset_status = dataset.get_loaded_temps()
    if dataset_status is None:
        print("Please load a file first")
        return
    avg_temp_by_day = {}
    for day in range(7):
        avg_temp_by_day_hour = []
        for hour in range(24):
            avg_hour_temp = dataset.get_avg_temperature_day_time(active_sensors, day, hour)
            if avg_hour_temp is not None:
                avg_hour_temp = convert_units(avg_hour_temp, 1)
                avg_hour_temp_rounded = round(avg_hour_temp, 1)
                avg_temp_by_day_hour.append(avg_hour_temp_rounded)
            else:
                avg_temp_by_day_hour.append("---")
        avg_temp_by_day[DAYS[day]] = avg_temp_by_day_hour
    avg_temp_dataframe = pd.DataFrame(data=avg_temp_by_day, index=HOURS.values(), columns=DAYS.values())
    print("Average Temperatures for " + dataset.name)
    print("Units are in Fahrenheit")
    print(avg_temp_dataframe)


def print_histogram(dataset, active_sensors):
    """
    Print histogram
    """
    print("Print Histogram Function Called")


def recursive_sort(list_to_sort, key=0):
    """
    Sorting the values using bubble sort
    """
    order_list = []
    item_swapped = False
    if key == 0:
        for y in range(len(list_to_sort) - 1):
            z = list_to_sort[y]
            if z[0] > list_to_sort[y + 1][0]:
                list_to_sort[y] = list_to_sort[y + 1]
                list_to_sort[y + 1] = z
                item_swapped = True
    elif key == 1:
        for y in range(len(list_to_sort) - 1):
            z = list_to_sort[y]
            if z[1] > list_to_sort[y + 1][1]:
                list_to_sort[y] = list_to_sort[y + 1]
                list_to_sort[y + 1] = z
                item_swapped = True
    last = list_to_sort.pop(-1)
    order_list.insert(0, last)

    if item_swapped:
        order_list = recursive_sort(list_to_sort, key) + order_list
    else:
        order_list = list_to_sort + order_list
    return order_list


def print_filter(sensor_list, filter_list):
    """
    Prints the updated list of filters
    """
    for x in sensor_list:
        status = ""
        if x[2] in filter_list:
            status = "[ACTIVE]"
        print(x[0] + ": " + x[1] + " " + status)


UNITS = {
    0: ("Celsius", "C"),
    1: ("Fahrenheit", "F"),
    2: ("Kelvin", "K")
}
units_selected = 0

DAYS = {
    0: "SUN",
    1: "MON",
    2: "TUE",
    3: "WED",
    4: "THU",
    5: "FRI",
    6: "SAT"
}

HOURS = {
    0: "Mid-1AM  ",
    1: "1AM-2AM  ",
    2: "2AM-3AM  ",
    3: "3AM-4AM  ",
    4: "4AM-5AM  ",
    5: "5AM-6AM  ",
    6: "6AM-7AM  ",
    7: "7AM-8AM  ",
    8: "8AM-9AM  ",
    9: "9AM-10AM ",
    10: "10AM-11AM",
    11: "11AM-NOON",
    12: "NOON-1PM ",
    13: "1PM-2PM  ",
    14: "2PM-3PM  ",
    15: "3PM-4PM  ",
    16: "4PM-5PM  ",
    17: "5PM-6PM  ",
    18: "6PM-7PM  ",
    19: "7PM-8PM  ",
    20: "8PM-9PM  ",
    21: "9PM-10PM ",
    22: "10PM-11PM",
    23: "11PM-MID ",
}


def main():
    """
    Main function with the menu function, the filter function, the head function, and the sorting function
    """
    global units_selected
    print_header()
    sensors = {"4213": ("STEM Center", 0),
               "4201": ("Foundation Lab", 1),
               "4204": ("CS Lab", 2),
               "4218": ("Workshop Room", 3),
               "4205": ("Tiled Room", 4),
               "Out": ("Outside", 5)}

    sensor_list = [((key,) + sensors[key]) for key in sensors.keys()]

    filter_list = [(sensors[key][1]) for key in sensors.keys()]
    sensor_list = recursive_sort(sensor_list)
    current_set = TempDataset()
    while True:
        print_menu()
        try:
            user_input = int(input("What is your choice? "))
            print("")
            if user_input == 1:
                new_file(current_set)
            elif user_input == 2:
                choose_units()
            elif user_input == 3:
                change_filter(sensors, sensor_list, filter_list)
            elif user_input == 4:
                try:
                    print_summary_statistics(current_set, filter_list, units_selected)
                except TypeError:
                    print("Please load data file and make sure at least one sensor is active")
            elif user_input == 5:
                print_temp_by_the_day_time(current_set, filter_list)
            elif user_input == 6:
                print_histogram(current_set, current_set)
            elif user_input == 7:
                print("Thank you for using the STEM Center Temperature Project")
                break
            else:
                print("Invalid Choice, please enter an integer between 1 and 7.")
        except ValueError:
            print("*** Please enter a number only ***")
        print("")


main()