import argparse
import csv


from datetime import datetime

"""
print_red and print_cyan are used to output text on the console in their respective colors.
"""


def print_red(character): print("\033[91m {}\033[00m".format(character), end='')


def print_cyan(character): print("\033[96m {}\033[00m".format(character), end='')


"""
returns the number into int/float or returns None if str_num is "".
"""


def make_int(str_num):
    str_num = str_num.strip()
    return int(str_num) if str_num else None


def make_double(str_num):
    str_num = str_num.strip()
    return float(str_num) if str_num else None


class WeatherReading:
    """
    Data Structure used to store data from the file and convert it appropriately.
    """

    def __init__(self, record):
        if record != '':
            self.pkt, self.max_temp, self.mean_temp, self.min_temp, self.dew_point, self.mean_dew_point,\
                self.min_dew_point, self.max_humidity, self.mean_humidity, self.min_humidity, \
                self.max_sea_level_pressure, self.mean_sea_level_pressure, self.min_sea_level_pressure, \
                self.max_visibility, self.mean_visibility, self.min_visibility, self.max_wind_speed, \
                self.mean_wind_speed, self.max_gust_speed, self.precipitation, self.cloud_clover, self.event, \
                self.wind_dir_degrees = record[0], record[1], record[2], record[3], record[4], record[5], record[6], \
                record[7], record[8], record[9], record[10], record[11], record[12], \
                record[13], record[14], record[15], record[16], record[17], record[18], \
                record[19], record[20], record[21], record[22]

            self.pkt = datetime.strptime(self.pkt, '%Y-%m-%d')
            self.max_temp = make_int(self.max_temp)
            self.min_temp = make_int(self.min_temp)
            self.mean_temp = make_int(self.mean_temp)
            self.mean_humidity = make_int(self.mean_humidity)
            self.max_humidity = make_int(self.max_humidity)
            self.min_humidity = make_int(self.min_humidity)
            self.dew_point = make_int(self.dew_point)
            self.mean_dew_point = make_int(self.mean_dew_point)
            self.min_dew_point = make_int(self.min_dew_point)
            self.min_sea_level_pressure = make_double(self.min_sea_level_pressure)
            self.mean_sea_level_pressure = make_double(self.mean_sea_level_pressure)
            self.max_sea_level_pressure = make_double(self.max_sea_level_pressure)
            self.max_visibility = make_double(self.max_visibility)
            self.min_visibility = make_double(self.min_visibility)
            self.mean_visibility = make_double(self.mean_visibility)
            self.max_wind_speed = make_double(self.max_wind_speed)
            self.mean_wind_speed = make_double(self.mean_wind_speed)
            self.max_gust_speed = make_double(self.max_gust_speed)
            self.precipitation = make_double(self.precipitation)
            self.cloud_clover = make_double(self.cloud_clover)


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
filePath = "{0}/Murree_weather_{1}_{2}.txt"


class AnnualReport:
    """
    Class that stores the data about the Annual Report.
    """
    def __init__(self):
        self.max_temp = None
        self.max_date = None
        self.min_temp = None
        self.min_date = None
        self.most_humid = None
        self.humid_date = None
        self.report = "Highest: {0}C on {1} {2}\n" \
                      "Lowest: {3}C on {4} {5}\n" \
                      "Humidity: {6}% on {7} {8}"

    def display(self):
        """
        displays formatted report
        """
        self.report = self.report.format(self.max_temp, months[self.max_date.month - 1], self.max_date.day,
                                         self.min_temp, months[self.min_date.month - 1], self.min_date.day,
                                         self.most_humid, months[self.humid_date.month - 1], self.humid_date.day)
        print(self.report)


class MonthlyReport:
    """
    Class that stores the data about the Monthly Report.
    """
    def __init__(self):
        self.report = "Highest Average: {0}C\nLowest Average: {1}C\nAverage Mean Humidity: {2}%"
        self.max_mean_temp = None
        self.min_mean_temp = None
        self.mean_humid = None

    def display(self):
        """
        displays formatted report
        """
        self.report = self.report.format(self.max_mean_temp, self.min_mean_temp, round(self.mean_humid))
        print(self.report)


class CalculateResults:
    """
    Calculates the results from the given data and store them into their respective data structures or display
    them accordingly.
    """
    def __init__(self):
        self.directory = None
        self.year = None
        self.month = None

    def calculate_annual_report(self, directory, year):
        """
        opens files from specific year and calculates annual report data to be displayed
        """
        self.directory = directory
        self.year = year
        annual_report = AnnualReport()
        for month in months:
            try:
                with open(filePath.format(directory, year, month)) as file:
                    row_number = 0
                    file = csv.reader(file)

                    for row in file:

                        if row_number == 0:
                            row_number += 1
                            continue
                        weather_reading = WeatherReading(row)
                        if row_number == 1:
                            annual_report.max_temp = weather_reading.max_temp
                            annual_report.max_date = weather_reading.pkt
                            annual_report.min_temp = weather_reading.min_temp
                            annual_report.min_date = weather_reading.pkt
                            annual_report.most_humid = weather_reading.max_humidity
                            annual_report.humid_date = weather_reading.pkt
                            row_number += 1
                        else:
                            if weather_reading.max_temp is not None and annual_report.max_temp < \
                                    weather_reading.max_temp:
                                annual_report.max_temp = weather_reading.max_temp
                                annual_report.max_date = weather_reading.pkt
                            if weather_reading.min_temp is not None and annual_report.min_temp > \
                                    weather_reading.min_temp:
                                annual_report.min_temp = weather_reading.min_temp
                                annual_report.min_date = weather_reading.pkt
                            if weather_reading.max_humidity is not None and annual_report.most_humid < \
                                    weather_reading.max_humidity:
                                annual_report.most_humid = weather_reading.max_humidity
                                annual_report.humid_date = weather_reading.pkt
            except FileNotFoundError:
                continue
        return annual_report

    def calculate_monthly_report(self, directory, year, month):
        """
        opens files from specific year and month and calculates monthly report data to be displayed
        """
        self.directory = directory
        self.year = year
        self.month = month

        try:
            with open(filePath.format(directory, year, months[month - 1])) as file:
                row_number = 0
                file = csv.reader(file)
                monthly_report = MonthlyReport()

                for row in file:
                    if row_number == 0:
                        row_number += 1
                        continue
                    weather_reading = WeatherReading(row)
                    if row_number == 1:
                        monthly_report.max_mean_temp = weather_reading.mean_temp
                        monthly_report.min_mean_temp = weather_reading.mean_temp
                        monthly_report.mean_humid = weather_reading.mean_humidity
                        row_number += 1
                    if weather_reading.max_temp is not None and weather_reading.min_temp is not None:
                        if weather_reading.mean_temp is None:
                            weather_reading.mean_temp = (weather_reading.max_temp + weather_reading.min_temp) / 2
                        if monthly_report.max_mean_temp < weather_reading.mean_temp:
                            monthly_report.max_mean_temp = weather_reading.mean_temp
                        if monthly_report.min_mean_temp > weather_reading.mean_temp:
                            monthly_report.min_mean_temp = weather_reading.mean_temp
                        monthly_report.mean_humid += weather_reading.mean_humidity
                        row_number += 1
                monthly_report.mean_humid /= row_number

            return monthly_report

        except FileNotFoundError:
            print("File not found")

    def display_bars(self, directory, year, month, bars):
        """
        opens files from specific year and month and displays a horizontal bar chart representing two different colors,
        Cyan for minimum temperature and Red for maximum temperature
        """
        self.directory = directory
        self.year = year
        self.month = month
        try:
            with open(filePath.format(self.directory, self.year, months[self.month - 1])) as file:
                row_number = 0
                file = csv.reader(file)
                day = 1
                for row in file:
                    if row_number == 0:
                        row_number += 1
                        continue
                    weather_reading = WeatherReading(row)
                    if weather_reading.max_temp is not None and weather_reading.max_temp is not None:
                        if bars == 1:
                            min_temp_display = ("+" * weather_reading.min_temp)
                            max_temp_display = ("+" * weather_reading.max_temp) + " "
                            print("{:02d} ".format(day), end='')

                            print_cyan(min_temp_display)
                            print_red(max_temp_display)
                            print(weather_reading.min_temp, "C - ", weather_reading.max_temp, "C")
                        if bars == 2:
                            max_temp_display = ("+" * weather_reading.max_temp) + " " + str(weather_reading.max_temp) \
                                + "\n"
                            min_temp_display = ("+" * weather_reading.min_temp) + " " + str(weather_reading.min_temp) \
                                + "\n"
                            print("{:02d} ".format(day), end='')
                            print_red(max_temp_display)
                            print("{:02d} ".format(day), end='')
                            print_cyan(min_temp_display)
                        day += 1
        except FileNotFoundError:
            print("file not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--year", required=False, help="Annual Report")
    ap.add_argument("-a", "--month", required=False, help="Monthly Report")
    ap.add_argument("-c", "--horizontal", required=False, help="draw horizontal chart")
    ap.add_argument("-f", "--file", required=False, help="file(s) path")

    args = vars(ap.parse_args())

    calculator = CalculateResults()
    if args["year"] is not None:
        annual_report = calculator.calculate_annual_report(args["file"], args["year"])
        if annual_report is not None:
            annual_report.display()
    if args["month"] is not None:
        year, month = args["month"].split('/')
        monthly_report = calculator.calculate_monthly_report(args["file"], year, int(month))
        monthly_report.display()
    if args["horizontal"] is not None:
        year, month = args["horizontal"].split('/')
        calculator.display_bars(args["file"], year, int(month), 2)
        calculator.display_bars(args["file"], year, int(month), 1)


if __name__ == "__main__":
    main()
