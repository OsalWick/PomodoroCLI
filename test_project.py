import pytest
from project import PomodoroTimer, DailyQuote
import json
import os
from datetime import datetime


"""
Changes Made
Vers. 1-> Timer could not get ahold of up the JsON File for the logs -> (typo) --> Fixed
Vers. 2 -> Successful Timers did not add up -> Adjusted the Stats functions --> (Fixed it)
Vers. 3 -> CSV Did not work for Daily Quote (Remade the CSV File) -> Fixed
Vers. 4 -> The Start Timer did not validate functions -> Fixed

12/01/2025 -> All Tests Pass


// Ignore this

Easy to Copy and Paste
"█" --> Symbol 

"""
"""
Test for the Timer Stuff

"""

# Test that new timer starts with session count of 0
def test_pomodoro_timer_starts_with_zero_sessions():
    timer = PomodoroTimer()
    assert timer.session_count == 0

# Test that work duration is set to 25 minutes
def test_pomodoro_timer_has_correct_work_duration():
    timer = PomodoroTimer()
    assert timer.default_durations["work"] == 25

# Test that short break duration is set to 5 minutes
def test_pomodoro_timer_has_correct_short_break_duration():
    timer = PomodoroTimer()
    assert timer.default_durations["short_break"] == 5

# Test that long break duration is set to 15 minutes
def test_pomodoro_timer_has_correct_long_break_duration():
    timer = PomodoroTimer()
    assert timer.default_durations["long_break"] == 15

# Test that progress bar shows both filled and empty sections at 50% progress
def test_progress_bar_shows_half_progress():
    timer = PomodoroTimer()
    progress_bar = timer.create_progress_bar(0.5)
    assert "█" in progress_bar
    assert "-" in progress_bar

# Test that progress bar shows mostly empty sections at 10% progress
def test_progress_bar_shows_minimal_progress():
    timer = PomodoroTimer()
    progress_bar = timer.create_progress_bar(0.1)
    assert "-" in progress_bar

# Test that full progress bar has more filled sections than half progress bar
def test_progress_bar_shows_full_vs_half_progress():
    timer = PomodoroTimer()
    full_bar = timer.create_progress_bar(1.0)
    half_bar = timer.create_progress_bar(0.5)
    assert full_bar.count("█") > half_bar.count("█")

# Test that saving a session creates a log file
def test_save_creates_logfile():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    timer.save("work", 25, True)
    assert os.path.exists(test_logfile)
    os.remove(test_logfile)

# Test that completed sessions are properly recorded in stats
def test_save_records_completed_session():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    timer.save("work", 25, True)
    stats = timer.get_stats()
    assert stats["completed_sessions"] == 1
    os.remove(test_logfile)
    

# Test that work sessions are properly recorded in stats
def test_save_records_work_session():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    timer.save("work", 25, True)
    stats = timer.get_stats()
    assert stats["work_sessions"] == 1
    os.remove(test_logfile)


# Test that session duration is properly recorded in stats
def test_save_records_session_duration():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    timer.save("work", 25, True)
    stats = timer.get_stats()
    assert stats["total_minutes"] == 25
    os.remove(test_logfile)

# Test that timer rejects zero duration
def test_timer_with_zero_duration():
    timer = PomodoroTimer()
    assert not timer.timer_start(0, "test")

# Test that timer rejects negative duration
def test_timer_with_negative_duration():
    timer = PomodoroTimer()
    assert not timer.timer_start(-1, "test")

# Test that total sessions is 0 when log file is missing
def test_stats_missing_logfile_total_sessions():
    timer = PomodoroTimer()
    timer.logfile = "nonexistent_file.json"
    stats = timer.get_stats()
    assert stats["total_sessions"] == 0



# Test that completed sessions is 0 when log file is missing
def test_stats_missing_logfile_completed_sessions():
    timer = PomodoroTimer()
    timer.logfile = "nonexistent_file.json"
    stats = timer.get_stats()
    assert stats["completed_sessions"] == 0

# Test that total minutes is 0 when log file is missing
def test_stats_missing_logfile_total_minutes():
    timer = PomodoroTimer()
    timer.logfile = "nonexistent_file.json"
    stats = timer.get_stats()
    assert stats["total_minutes"] == 0

# Test that work sessions count is 0 when log file is missing
def test_stats_missing_logfile_work_sessions():
    timer = PomodoroTimer()
    timer.logfile = "nonexistent_file.json"
    stats = timer.get_stats()
    assert stats["work_sessions"] == 0




# Test that break sessions count is 0 when log file is missing
def test_stats_missing_logfile_break_sessions():
    timer = PomodoroTimer()
    timer.logfile = "nonexistent_file.json"
    stats = timer.get_stats()
    assert stats["break_sessions"] == 0

    
"""
Tests for the Daily Quotes Stuff

"""

# Test that quotes are successfully loaded from CSV file
def test_daily_quote_loads_quotes():
    quote = DailyQuote()
    assert len(quote.quotes) > 0

# Test that random quote generator returns a valid string
def test_daily_quote_generates_random_quote():
    quote = DailyQuote()
    random_quote = quote.get_random_quote()
    assert isinstance(random_quote, str)
    assert len(random_quote) > 0
