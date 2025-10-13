import datetime
from engi1020.arduino.api import *
from time import sleep

def get_assignments():
    """
    Collect assignment details with specific due dates and calculate remaining days.
    
    Returns:
    list: A sorted list of tuples containing (days_until_due, assignment name, due_date)
    """
    assignments = []
    print("Enter assignments (type 'done' to end): ")
    
    #get today's date
    today = datetime.date.today()
    
    while True:
        try:
            assignment = input("Assignment name: ").strip()
            if assignment.lower() == 'done':
                break
            
            #get due date
            while True:
                try:
                    due_date_str = input(f"When is {assignment} due? (YYYY-MM-DD): ").strip()
                    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    
                    #calculate days until due
                    days_until_due = (due_date - today).days
                    
                    if days_until_due < 0:
                        print("Warning: The due date is in the past. Please enter a future date.")
                        continue
                    
                    assignments.append((days_until_due, assignment, due_date))
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            break
    
    #sort assignments by days until due
    assignments.sort(key=lambda x: x[0])
    
    #display sorted assignments
    if assignments:
        print("\nUpcoming Assignments:")
        for days_until_due, assignment, due_date in assignments:
            print(f'{assignment} is due on {due_date} (in {days_until_due} days)')
    else:
        print("No assignments entered.")
    
    return assignments

def arduino_time_selection(assignment, days_until_due):
    """
    Select study time using Arduino rotary dial and button.
    
    Args:
    assignment (str): Name of the assignment
    days_until_due (int): Number of days until the assignment is due
    
    Returns:
    tuple: (selected hours, selected minutes)
    """
    print(f"\nSelecting study time for {assignment} (due in {days_until_due} days)")
    print("Select study time using the rotary dial.")
    print("Hours: First rotation")
    print("Minutes: Second rotation")
    print("Press the button to confirm each selection.")
    print("Maximum: 5 hours, 59 minutes")
    
    #short delay to allow user to read instructions
    sleep(3)
    
    #select hours
    print("\nSelect HOURS:")
    hours_selection = False
    selected_hours = 0
    
    while not hours_selection:
        #read analog value from rotary dial
        rotary_dial = analog_read(0)
        
        #scale rotary dial reading to hours (0 to 5 hours)
        hours = min(5, max(0, int(rotary_dial * 0.005 * 5)))
        
        print(f"\rSelected hours: {hours}   ", end='', flush=True)
        
        #check if button is pressed 
        if digital_read(6) == True:
            selected_hours = hours
            hours_selection = True
            sleep(0.5)  #debounce
    
    #select minutes
    print("\nSelect MINUTES:")
    minutes_selection = False
    selected_minutes = 0
    
    while not minutes_selection:
        #read analog value from rotary dial
        rotary_dial = analog_read(0)
        
        #scale rotary dial reading to minutes (0 to 59 minutes)
        minutes = min(59, max(0, int(rotary_dial * 0.005 * 59)))
        
        print(f"\rSelected minutes: {minutes}   ", end='', flush=True)
        
        #check if button is pressed
        if digital_read(6) == True:
            selected_minutes = minutes
            minutes_selection = True
            sleep(0.5)  #debounce
    
    print(f"\nYou have chosen {selected_hours} hour(s) and {selected_minutes} minute(s) for {assignment}!")
    return selected_hours, selected_minutes

def get_study_hours_for_assignment(assignment, days_until_due):
    """
    Collect study hours for the days leading up to an assignment using Arduino input.
    
    Args:
    assignment (str): Name of the assignment
    days_until_due (int): Number of days until the assignment is due
    
    Returns:
    dict: A dictionary with dates as keys and (hours, minutes) as values
    """
    study_time = {}
    today = datetime.date.today()
    
    #generate dates between today and the due date
    for i in range(days_until_due + 1):
        current_date = today + datetime.timedelta(days=i)
        day_name = current_date.strftime("%A")
        
        #get study time for this specific date using Arduino input
        hours, minutes = arduino_time_selection(f"{assignment} on {current_date} ({day_name})", days_until_due)
        
        #only add non-zero study time
        if hours > 0 or minutes > 0:
            study_time[current_date] = (hours, minutes)
    
    return study_time

def create_study_plan(assignments):
    """
    Create a comprehensive study plan for all assignments.
    
    Args:
    assignments (list): List of assignments with their due dates
    """
    if not assignments:
        print("No assignments to create a study plan for.")
        return
    
    comprehensive_study_plan = {}
    
    print("\n--- Study Plan Creation ---")
    for days_until_due, assignment, due_date in assignments:
        print(f"\nPlanning study time for {assignment}")
        assignment_study_time = get_study_hours_for_assignment(assignment, days_until_due)
        
        #store the study time for this assignment
        comprehensive_study_plan[assignment] = {
            'due_date': due_date,
            'days_until_due': days_until_due,
            'study_time': assignment_study_time
        }
    
    #display the comprehensive study plan
    print("\n--- Comprehensive Study Plan ---")
    for assignment, details in comprehensive_study_plan.items():
        print(f"\n{assignment} (Due: {details['due_date']}):")
        if details['study_time']:
            total_hours = 0
            total_minutes = 0
            print("Study Schedule:")
            for date, (hours, minutes) in details['study_time'].items():
                total_hours += hours
                total_minutes += minutes
                print(f"  {date}: {hours} hours {minutes} minutes")
            
            #convert total minutes to hours and remaining minutes
            total_hours += total_minutes // 60
            total_minutes %= 60
            
            print(f"\nTotal study time: {total_hours} hours {total_minutes} minutes")
        else:
            print("No study time allocated.")

def start_study_timer(hours, minutes):
    """
    Start a study timer with LED and buzzer alerts.
    
    Args:
    hours (int): Number of study hours
    minutes (int): Number of study minutes
    """
    total_seconds = (hours * 3600) + (minutes * 60)
    
    #set up LED and buzzer pins
    buzzer_pin = 5
    led_pin = 4
    button_pin = 6
    
    print(f"\nStudy Timer Started: {hours} hours {minutes} minutes")
    print("Press the button to stop the timer early.")
    
    for remaining in range(total_seconds, 0, -1):
        #calculate hours, minutes, seconds
        current_hours, remainder = divmod(remaining, 3600)
        current_minutes, current_seconds = divmod(remainder, 60)
        
        #display remaining time
        print(f"\rTime Remaining: {current_hours:02d}:{current_minutes:02d}:{current_seconds:02d}", end='', flush=True)
        
        #activate LED and buzzer during last 5 minutes (300 seconds)
        if remaining <= 300:
            #alternate LED on/off every second
            if remaining % 2 == 0:
                digital_write(led_pin, True)# Turn LED on
                oled_clear()
                oled_print("Time is almost up!")
            else:
                digital_write(led_pin, False)  # Turn LED off
            
            #buzzer alert every 2 seconds during last 5 minutes
            if remaining % 2 == 0:
                buzzer_frequency(buzzer_pin, 1000)  # Sound buzzer at 1000 Hz
            else:
                #turn buzzer off
                buzzer_stop(5)
        #check if button is pressed to stop timer early
        if digital_read(button_pin) == True:
            print("\nTimer Stopped Early!")
            #ensure LED and buzzer are turned off when timer is stopped
            digital_write(led_pin, False)
            #digital_write(buzzer_pin, False)
            buzzer_stop(5)
            break
        
        #small delay to prevent overwhelming the system
        sleep(1)
    
    #timer complete
    if remaining == 0:
        print("\nStudy Timer Complete!")
        #final alert sequence
        for _ in range(3):
            digital_write(led_pin, True)
            buzzer_frequency(buzzer_pin, 1500)  #higher pitch to signify completion
            sleep(0.5)
            digital_write(led_pin, False)
            digital_write(buzzer_pin, False)
            sleep(0.5)
            
            
def select_study_duration_for_timer():
    """
    Select total study duration using rotary dial (hours + minutes).
    
    Returns:
    tuple: (hours, minutes)
    """
    print("\n--- Select Timer Duration ---")
    return arduino_time_selection("Study Session Timer", days_until_due=0)


def view_assignments(assignments):
    """
    Display the current list of assignments with due dates.
    """
    if not assignments:
        print("⚠️ No assignments added yet.")
    else:
        print("\n📅 Current Assignments:")
        assignments.sort(key=lambda x: x[0])  #sort by due date
        for days_left, name, due in assignments:
            print(f"  - {name} → Due: {due} (in {days_left} days)")

        
def main():
    """
    Interactive main menu for the AI Study Planner.
    """
    assignments = []  # store assignments across menu options

    while True:
        print("\n📚 AI Study Planner Menu")
        print("1. Add Assignments")
        print("2. Create/View Study Plan")
        print("3. Start a Study Timer")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            #add new assignments (appends to the list)
            new_assignments = get_assignments()
            assignments.extend(new_assignments)
            #remove duplicates based on assignment name
            assignments = list({a[1]: a for a in assignments}.values())
        
        elif choice == "2":	
            view_assignments(assignments)

        elif choice == "3":
            print("\n🎯 Use the rotary dial + button to select study time.")
            hours, minutes = select_study_duration_for_timer()
            if hours == 0 and minutes == 0:
                print("Timer cancelled. No time selected.")
            else:
                start_study_timer(hours, minutes)

        elif choice == "4":
            print("👋 Exiting AI Study Planner. Good luck with your studies!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()