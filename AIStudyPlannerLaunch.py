import tkinter as tk
from tkinter import messagebox
import AIStudyPlanner  

#graphical user interface window
root = tk.Tk()
root.title("AI Study Planner")
root.geometry("400x300")

assignments = []

#callback to run get_assignments()
def add_assignments_gui():
    global assignments
    new_assignments = AIStudyPlanner.get_assignments()
    assignments.extend(new_assignments)
    
    #remove any duplicate assignments
    assignments = list({a[1]: a for a in assignments}.values())
    messagebox.showinfo("Done", "Assignments added!")

#view assignments in a popup
def view_assignments_gui():
    if not assignments:
        messagebox.showinfo("Assignments", "No assignments found.")
        return

    popup = tk.Toplevel(root)
    popup.title("Upcoming Assignments")
    popup.geometry("350x250")
    
    tk.Label(popup, text="Assignments Due", font=('Helvetica', 12, 'bold')).pack(pady=5)

    sorted_list = sorted(assignments, key=lambda x: x[0])
    for days_left, name, due in sorted_list:
        tk.Label(popup, text=f"{name} - Due {due} ({days_left} days left)").pack(anchor='w', padx=10)

#create full plan (with rotary input)
def create_plan_gui():
    if not assignments:
        messagebox.showinfo("Missing Data", "Add assignments first.")
        return
    AIStudyPlanner.create_study_plan(assignments)

#start timer using rotary dial
def start_timer_gui():
    hours, minutes = AIStudyPlanner.select_study_duration_for_timer()
    if hours == 0 and minutes == 0:
        messagebox.showinfo("Timer", "Timer canceled. No time selected.")
    else:
        AIStudyPlanner.start_study_timer(hours, minutes)

#graphical user interface layout
        
tk.Label(root, text="📚 AI Study Planner", font=("Helvetica", 16)).pack(pady=15)

tk.Button(root, text="➕ Add Assignments", command=add_assignments_gui, width=25).pack(pady=5)
tk.Button(root, text="📋 View Assignments", command=view_assignments_gui, width=25).pack(pady=5)
tk.Button(root, text="🧠 Create Study Plan", command=create_plan_gui, width=25).pack(pady=5)
tk.Button(root, text="⏰ Start Study Timer", command=start_timer_gui, width=25).pack(pady=5)

tk.Button(root, text="❌ Exit", command=root.quit, width=25, fg="red").pack(pady=20)

root.mainloop()
