import sys
import json
import time
import os
import click
from colorama import init, Fore, Style
import csv
import random
from datetime import datetime

# Initialize colorama for Windows compatibility
init()

"""
My CS50P Final Project: Pomodoro Timer
By: Osal Wickremasinghe

I created this because I always had trouble focusing during my study sessions.
This timer helps me stay on track and take proper breaks.

Main Features:
- Work/Break timers
- Progress tracking
- Motivational quotes
- Session statistics

Note to self: Maybe add sound notifications in the future?
"""

# I found these quotes really helpful during my study sessions
class DailyQuote:
    def __init__(self):
        self.quotes_file = "quotes.csv"
        self.quotes = self._load_quotes()

    def _load_quotes(self):
        quotes = []
        try:
            # Read quotes from CSV - each line has a quote and author
            with open(self.quotes_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    quotes.append((row['Quote'], row['Author']))
        except FileNotFoundError:
            # Fallback quote if file is missing
            print(f"{Fore.RED}Couldn't find quotes.csv{Style.RESET_ALL}")
            return [("Keep pushing!", "Unknown")]
        return quotes
    
    def get_random_quote(self):
        quote, author = random.choice(self.quotes)
        return f'\n{Fore.CYAN}"{quote}"{Style.RESET_ALL}\n{Fore.YELLOW}- {author}{Style.RESET_ALL}'

class PomodoroTimer:
    def __init__(self):
        # File to keep track of my study sessions
        self.logfile = "logfile.json"
        self.session_count = 0
        
        # Standard Pomodoro times (in minutes)
        self.default_durations = {
            "work": 25,      # Standard Pomodoro session
            "short_break": 5, # Quick breather
            "long_break": 15  # Proper rest after 4 sessions
        }
        
        self.quote_generator = DailyQuote()

    def create_progress_bar(self, progress):
        # Simple progress bar with colors
        width = 50  # Looks good on most terminals
        filled = int(width * progress)
        bar = (Fore.GREEN + "█" * filled + 
               Style.RESET_ALL + Fore.WHITE + "-" * (width - filled) + 
               Style.RESET_ALL)
        return f"[{bar}] {Fore.CYAN}{progress*100:.1f}%{Style.RESET_ALL}"

    def display_time(self, minutes, seconds, duration_minutes, session_type):
        # Calculate progress for the bar
        total_seconds = duration_minutes * 60
        elapsed = (duration_minutes * 60) - (minutes * 60 + seconds)
        progress = elapsed / total_seconds

        # Create a nice looking display
        bar = self.create_progress_bar(progress)
        status = Fore.GREEN + "RUNNING" + Style.RESET_ALL
        type_color = Fore.BLUE if "break" in session_type.lower() else Fore.MAGENTA
        session = f"{type_color}{session_type.upper()}{Style.RESET_ALL}"

        # Update the display (overwrite previous line)
        print(f"\r{session} - {status}: {Fore.WHITE}{minutes:02d}:{seconds:02d}{Style.RESET_ALL} {bar}", end="")

    def timer_start(self, duration_minutes: int, session_type: str) -> bool:
        elapsed_time = 0
        click.clear()
        
        # Show a motivational quote to start
        print(self.quote_generator.get_random_quote())
        
        try:
            while elapsed_time < (duration_minutes * 60):
                remaining = (duration_minutes * 60) - elapsed_time
                mins, secs = divmod(int(remaining), 60)
                self.display_time(mins, secs, duration_minutes, session_type)
                time.sleep(1)
                elapsed_time += 1

            # Timer finished!
            print('\n\007')  # Terminal bell
            print(f"\n{Fore.GREEN}✓ {session_type.upper()} completed!{Style.RESET_ALL}")
            return True

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Timer stopped!{Style.RESET_ALL}")
            return False

    def save(self, session_type: str, duration: int, completed: bool) -> None:
        # Save session info for tracking progress
        session = {
            "timestamp": datetime.now().isoformat(),
            "type": session_type,
            "duration": duration,
            "completed": completed,
            "session_number": self.session_count
        }

        try:
            # Load existing sessions
            with open(self.logfile, 'r') as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        # Add new session and save
        logs.append(session)
        try:
            with open(self.logfile, 'w') as file:
                json.dump(logs, file, indent=2)
        except IOError as e:
            print(f"{Fore.RED}Couldn't save session: {e}{Style.RESET_ALL}")

    def get_stats(self) -> dict:
        try:
            with open(self.logfile, 'r') as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty stats if no log file
            return {
                "total_sessions": 0,
                "completed_sessions": 0,
                "total_minutes": 0,
                "work_sessions": 0,
                "break_sessions": 0
            }

        # Calculate some basic stats
        stats = {
            "total_sessions": len(logs),
            "completed_sessions": sum(1 for s in logs if s["completed"]),
            "total_minutes": sum(s["duration"] for s in logs if s["completed"]),
            "work_sessions": sum(1 for s in logs if s["type"] == "work" and s["completed"]),
            "break_sessions": sum(1 for s in logs if "break" in s["type"] and s["completed"])
        }

        return stats

    def run_session(self, session_type: str, duration: int = None) -> None:
        if not duration:
            duration = self.default_durations[session_type]

        self.session_count += 1
        completed = self.timer_start(duration, session_type)
        self.save(session_type, duration, completed)

        # Suggest breaks after work sessions
        if completed and session_type == "work":
            if self.session_count % 4 == 0:
                print(f"\n{Fore.GREEN}Great work! Time for a longer break!{Style.RESET_ALL}")
                if click.confirm("Start long break?", default=True):
                    self.run_session("long_break")
            else:
                print(f"\n{Fore.GREEN}Nice job! Quick break?{Style.RESET_ALL}")
                if click.confirm("Start short break?", default=True):
                    self.run_session("short_break")

def print_menu():
    # Simple menu display
    click.clear()
    print(f"\n{Fore.CYAN}=== STUDY TIMER ==={Style.RESET_ALL}")
    print(f"{Fore.WHITE}----------------{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Start Studying (25min)")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} Quick Break (5min)")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} Long Break (15min)")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Custom Timer")
    print(f"{Fore.MAGENTA}5.{Style.RESET_ALL} View Stats")
    print(f"{Fore.RED}6.{Style.RESET_ALL} Exit")

def main():
    timer = PomodoroTimer()

    while True:
        print_menu()
        choice = click.prompt("\nWhat would you like to do", type=str)

        if choice == "1":
            timer.run_session("work")
        elif choice == "2":
            timer.run_session("short_break")
        elif choice == "3":
            timer.run_session("long_break")
        elif choice == "4":
            try:
                mins = click.prompt("How many minutes", type=int)
                label = click.prompt("Session label", type=str)
                timer.run_session(label, mins)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
        elif choice == "5":
            stats = timer.get_stats()
            print(f"\n{Fore.CYAN}Your Progress:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}-------------{Style.RESET_ALL}")
            print(f"Total Sessions: {Fore.GREEN}{stats['total_sessions']}{Style.RESET_ALL}")
            print(f"Completed: {Fore.GREEN}{stats['completed_sessions']}{Style.RESET_ALL}")
            print(f"Total Minutes: {Fore.GREEN}{stats['total_minutes']}{Style.RESET_ALL}")
            print(f"Work Sessions: {Fore.MAGENTA}{stats['work_sessions']}{Style.RESET_ALL}")
            print(f"Break Sessions: {Fore.BLUE}{stats['break_sessions']}{Style.RESET_ALL}")
            click.pause()
        elif choice == "6":
            print(f"\n{Fore.GREEN}Thanks for studying! See you next time!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Oops! Invalid choice!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
