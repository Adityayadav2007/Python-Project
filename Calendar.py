import datetime
from typing import Dict, Tuple, List

class PerpetualCalendar:
    def __init__(self):
        # Days of the week
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Months with their days (non-leap year)
        self.months = {
            1: ("January", 31),
            2: ("February", 28),
            3: ("March", 31),
            4: ("April", 30),
            5: ("May", 31),
            6: ("June", 30),
            7: ("July", 31),
            8: ("August", 31),
            9: ("September", 30),
            10: ("October", 31),
            11: ("November", 30),
            12: ("December", 31)
        }
        
        # Zeller's Congruence constants
        self.month_codes = {
            1: 11, 2: 12, 3: 1, 4: 2, 5: 3, 6: 4,
            7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10
        }

    def is_leap_year(self, year: int) -> bool:
        """Check if a year is a leap year."""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def get_days_in_month(self, year: int, month: int) -> int:
        """Get the number of days in a month for a given year."""
        if month == 2 and self.is_leap_year(year):
            return 29
        return self.months[month][1]

    def day_of_week_zeller(self, day: int, month: int, year: int) -> int:
        """
        Calculate day of the week using Zeller's Congruence.
        Returns: 0=Saturday, 1=Sunday, 2=Monday, ..., 6=Friday
        """
        if month < 3:
            month += 12
            year -= 1
        
        k = year % 100  # Year of the century
        j = year // 100  # Century
        
        h = (day + (13 * (month + 1)) // 5 + k + (k // 4) + (j // 4) - (2 * j)) % 7
        
        # Convert to our format: 0=Monday, 1=Tuesday, ..., 6=Sunday
        return (h + 5) % 7

    def day_of_week_datetime(self, day: int, month: int, year: int) -> int:
        """
        Calculate day of the week using datetime module.
        Returns: 0=Monday, 1=Tuesday, ..., 6=Sunday
        """
        date_obj = datetime.date(year, month, day)
        return date_obj.weekday()

    def get_day_name(self, day: int, month: int, year: int, method: str = 'datetime') -> str:
        """Get the name of the day for a given date."""
        if method == 'zeller':
            day_index = self.day_of_week_zeller(day, month, year)
        else:
            day_index = self.day_of_week_datetime(day, month, year)
        
        return self.days[day_index]

    def validate_date(self, day: int, month: int, year: int) -> bool:
        """Validate if a date is valid."""
        if year < 1 or year > 9999:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > self.get_days_in_month(year, month):
            return False
        return True

    def display_month_calendar(self, month: int, year: int):
        """Display a calendar for a specific month and year."""
        if not self.validate_date(1, month, year):
            print(f"Invalid date: {month}/{year}")
            return
        
        month_name = self.months[month][0]
        days_in_month = self.get_days_in_month(year, month)
        
        # Get the day of the week for the first day of the month
        first_day = self.day_of_week_datetime(1, month, year)
        
        print(f"\n{month_name} {year}")
        print("Mo Tu We Th Fr Sa Su")
        
        # Print leading spaces
        print("   " * first_day, end="")
        
        # Print the days
        for day in range(1, days_in_month + 1):
            print(f"{day:2} ", end="")
            if (day + first_day) % 7 == 0:
                print()
        
        # Add newline if the month doesn't end on Sunday
        if (days_in_month + first_day) % 7 != 0:
            print()

    def display_year_calendar(self, year: int):
        """Display calendar for an entire year."""
        print(f"\n{'=' * 50}")
        print(f"Calendar for {year}")
        print(f"{'=' * 50}")
        
        for month in range(1, 13):
            self.display_month_calendar(month, year)

    def get_date_info(self, day: int, month: int, year: int):
        """Get comprehensive information about a date."""
        if not self.validate_date(day, month, year):
            print(f"Invalid date: {day}/{month}/{year}")
            return
        
        day_name = self.get_day_name(day, month, year)
        month_name = self.months[month][0]
        is_leap = self.is_leap_year(year)
        
        print(f"\nDate Information for {day} {month_name} {year}:")
        print(f"Day of the week: {day_name}")
        print(f"Month: {month_name} ({self.get_days_in_month(year, month)} days)")
        print(f"Year: {year} ({'Leap year' if is_leap else 'Not a leap year'})")
        
        # Calculate day of the year
        day_of_year = day
        for m in range(1, month):
            day_of_year += self.get_days_in_month(year, m)
        print(f"Day of the year: {day_of_year}")
        print(f"Days remaining in year: {366 - day_of_year if is_leap else 365 - day_of_year}")

    def find_date_by_offset(self, start_day: int, start_month: int, start_year: int, 
                           offset_days: int) -> Tuple[int, int, int]:
        """Find date after adding/subtracting days from a given date."""
        if not self.validate_date(start_day, start_month, start_year):
            raise ValueError("Invalid start date")
        
        # Use datetime for easy date arithmetic
        start_date = datetime.date(start_year, start_month, start_day)
        target_date = start_date + datetime.timedelta(days=offset_days)
        
        return target_date.day, target_date.month, target_date.year

def main():
    calendar = PerpetualCalendar()
    
    while True:
        print("\n" + "=" * 50)
        print("PERPETUAL CALENDAR")
        print("=" * 50)
        print("1. Get day of the week for a date")
        print("2. Display month calendar")
        print("3. Display year calendar")
        print("4. Get date information")
        print("5. Find date by offset")
        print("6. Check if leap year")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            try:
                day = int(input("Enter day: "))
                month = int(input("Enter month: "))
                year = int(input("Enter year: "))
                
                if calendar.validate_date(day, month, year):
                    day_name = calendar.get_day_name(day, month, year)
                    print(f"\n{day}/{month}/{year} is a {day_name}")
                else:
                    print("Invalid date!")
                    
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '2':
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year: "))
                calendar.display_month_calendar(month, year)
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '3':
            try:
                year = int(input("Enter year: "))
                calendar.display_year_calendar(year)
            except ValueError:
                print("Please enter a valid year!")
                
        elif choice == '4':
            try:
                day = int(input("Enter day: "))
                month = int(input("Enter month: "))
                year = int(input("Enter year: "))
                calendar.get_date_info(day, month, year)
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '5':
            try:
                day = int(input("Enter start day: "))
                month = int(input("Enter start month: "))
                year = int(input("Enter start year: "))
                offset = int(input("Enter offset days (can be negative): "))
                
                new_day, new_month, new_year = calendar.find_date_by_offset(day, month, year, offset)
                day_name = calendar.get_day_name(new_day, new_month, new_year)
                print(f"\n{offset} days from {day}/{month}/{year} is {new_day}/{new_month}/{new_year} ({day_name})")
                
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '6':
            try:
                year = int(input("Enter year: "))
                is_leap = calendar.is_leap_year(year)
                print(f"\n{year} is {'a leap year' if is_leap else 'not a leap year'}")
            except ValueError:
                print("Please enter a valid year!")
                
        elif choice == '7':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()