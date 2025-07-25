
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style
import logging 
from datetime import datetime  

#Set the default time for work and break intervals
WORK_TIME = 25 * 60  # 25 minutes in seconds
SHORTBREAK_TIME = 5 * 60   # 5 minutes in seconds
LONGBREAK_TIME = 15 * 60  # 15 minutes in seconds
class PomodoroTimer:    
    def __init__(self):
        # Setup logging 
          

        logging.basicConfig(
            filename='pomodoro_activity.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
            )
        
        self.logger = logging.getLogger(__name__)

        # Initialize the main window    
        self.root = tk.Tk()
        self.root.geometry("400x200")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme='simplex')
        self.style.theme_use('simplex')

        self.timer_label = tk.Label(self.root, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)
        
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.work_time, self.break_time = WORK_TIME, SHORTBREAK_TIME

        self.is_work_time, self.pomodoro_completed, self.is_running = True, 0, False

        self.root.mainloop()
    

   
    
    def start_timer(self):
        #Logging the start of the session
        logging.info(f"Started {'work' if self.is_work_time else 'break'} session")

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL) 
        self.is_running = True
        self.update_timer() 

    def stop_timer(self):
        #Logging the stop of the session
        logging.info(f"Stopped {'work' if self.is_work_time else 'break'} session")
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False 

    def update_timer(self):
        if self.is_running: #Only proceed if timer is running
            
            if self.work_time: #Check if still in work time (work_time > 0)
                self.work_time -= 1 # Decrease work time by 1 second

                if self.work_time == 0: #  When work time reaches 0
                    self.is_work_time = False # Switch to break mode
                    self.pomodoro_completed += 1 #Increment completed pomodoros counter
                    self.break_time = LONGBREAK_TIME if self.pomodoro_completed % 4 == 0 else SHORTBREAK_TIME
                    
                    messagebox.showinfo("Great job!" if self.pomodoro_completed % 4 == 0 
                                        else "Good job" , "Take a break and rest your mind."
                                        if self.pomodoro_completed % 4 == 0 
                                        else "Take a short break and strech your legs.")
            else: # If not in work time (must be break time)
                self.break_time-= 1 # Decrease break time by 1 second            
                if self.break_time == 0: 
                    self.is_work_time, self.work_time = True, WORK_TIME
                    messagebox.showinfo("Time's up!", "Back to work!")
            
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
   

PomodoroTimer()