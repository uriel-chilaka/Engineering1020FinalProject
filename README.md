# Engineering1020FinalProject
The AI Study Planner is an interactive Python-based tool designed for students to manage assignments and plan study sessions efficiently. Built as part of the Engineering 1020 Final Project, this system combines AI-inspired scheduling logic with Arduino hardware integration to create a hands-on study management experience.

It allows users to:
- Input and track assignments with deadlines
- Use an Arduino rotary dial and button to select study times interactively
- Generate a personalized study plan leading up to each due date
- Launch a study timer with LED and buzzer alerts to stay on task
- Access both a command-line interface (CLI) and a graphical user interface (GUI) via Tkinter


Features:
- Assignment Management: Add and view upcoming assignments with due dates.
- Arduino Integration: Use analog and digital inputs (rotary dial, button, LED, and buzzer) for study time selection and alerts.
- Study Plan Generator: Automatically distribute study time between the current day and the assignment’s due date.
- Study Timer: Countdown timer with LED and buzzer notifications during the last five minutes.
- GUI Launcher: Simple and accessible Tkinter interface for quick navigation.

Hardware Requirements: 
- Arduino with:
- Rotary potentiometer (for time selection)
- Push button (for confirmation)
- LED (for visual alerts)
- Buzzer (for auditory alerts)
