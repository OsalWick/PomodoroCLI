import pytest
from project import PomodoroTimer, DailyQuote, print_menu
import json
import os
from datetime import datetime
from unittest.mock import patch

"""
Test file for project.py
Testing all functions and methods
"""

# Tests that timer starts correctly with valid/invalid durations and handles interrupts
def test_timer_start():
    timer = PomodoroTimer()
    
    # Test invalid durations
    assert not timer.timer_start(0, "test")
    assert not timer.timer_start(-1, "test")
    
    # Mock time.sleep to speed up tests
    with patch('time.sleep'):
        # Test valid duration
        assert timer.timer_start(1, "test")
        
        # Test keyboard interrupt
        with patch('time.sleep', side_effect=KeyboardInterrupt):
            assert not timer.timer_start(1, "test")

# Tests that progress bar displays correctly at different progress levels
def test_create_progress_bar():
    timer = PomodoroTimer()
    
    # Test different progress values
    assert len(timer.create_progress_bar(0)) > 0
    assert len(timer.create_progress_bar(0.5)) > 0
    assert len(timer.create_progress_bar(1)) > 0
    
    # Test progress bar components
    bar = timer.create_progress_bar(0.5)
    assert "[" in bar
    assert "]" in bar
    assert "%" in bar
    
    # Test progress bar fills correctly
    empty_bar = timer.create_progress_bar(0)
    half_bar = timer.create_progress_bar(0.5)
    full_bar = timer.create_progress_bar(1.0)
    
    assert empty_bar.count("█") == 0
    assert half_bar.count("█") == 25 # Half of width 50
    assert full_bar.count("█") == 50 # Full width

# Tests that time display shows correct format for different session types
def test_display_time():
    timer = PomodoroTimer()
    
    # Test different time displays
    with patch('builtins.print') as mock_print:
        timer.display_time(25, 0, 25, "work")
        mock_print.assert_called_once()
        
        timer.display_time(5, 30, 25, "break")
        timer.display_time(0, 0, 25, "custom")

# Tests that sessions are saved correctly to log file
def test_save():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    try:
        # Test log file creation
        timer.save("work", 25, True)
        assert os.path.exists(test_logfile)
        
        # Test saving multiple sessions
        timer.save("work", 25, True)
        timer.save("short_break", 5, True)
        timer.save("work", 25, True)
        
        with open(test_logfile) as f:
            logs = json.load(f)
            assert len(logs) == 4
            
            # Verify log structure
            for log in logs:
                assert "timestamp" in log
                assert "type" in log
                assert "duration" in log
                assert "completed" in log
                assert "session_number" in log
                
    finally:
        # Cleanup
        if os.path.exists(test_logfile):
            os.remove(test_logfile)

# Tests that statistics are calculated correctly from session logs
def test_get_stats():
    timer = PomodoroTimer()
    test_logfile = "test_logfile.json"
    timer.logfile = test_logfile
    
    try:
        # Test stats with sessions
        timer.save("work", 25, True)
        timer.save("short_break", 5, True)
        timer.save("work", 25, False) # Add incomplete session
        
        stats = timer.get_stats()
        assert stats["total_sessions"] == 3
        assert stats["completed_sessions"] == 2
        assert stats["total_minutes"] == 30 # Only completed sessions
        assert stats["work_sessions"] == 1
        assert stats["break_sessions"] == 1
        
        # Test stats with corrupted file
        with open(test_logfile, 'w') as f:
            f.write("invalid json")
            
        stats = timer.get_stats()
        assert stats["total_sessions"] == 0
        
        # Test stats with missing file
        os.remove(test_logfile)
        stats = timer.get_stats()
        assert stats["total_sessions"] == 0
        
    finally:
        # Cleanup
        if os.path.exists(test_logfile):
            os.remove(test_logfile)

# Tests that different session types run correctly
@patch('click.confirm', return_value=False)
def test_run_session(mock_confirm):
    timer = PomodoroTimer()
    
    with patch('project.PomodoroTimer.timer_start', return_value=True):
        # Test default durations
        timer.run_session("work")
        timer.run_session("short_break")
        timer.run_session("long_break")
        
        # Test custom duration
        timer.run_session("custom", 10)

# Tests that menu displays all required options
def test_print_menu(capsys):
    # Test menu display
    print_menu()
    captured = capsys.readouterr()
    
    required_items = [
        "STUDY TIMER",
        "Start Studying",
        "Quick Break", 
        "Long Break",
        "Custom Timer",
        "View Stats",
        "Exit"
    ]
    
    for item in required_items:
        assert item in captured.out

# Tests that quote system initializes with valid and missing quote files
def test_daily_quote_init():
    # Test with existing quotes file
    quote = DailyQuote()
    assert hasattr(quote, 'quotes_file')
    assert hasattr(quote, 'quotes')
    assert len(quote.quotes) > 0
    
    # Test with missing quotes file
    with patch('builtins.open', side_effect=FileNotFoundError):
        quote = DailyQuote()
        assert len(quote.quotes) == 1
        assert quote.quotes[0] == ("Keep pushing!", "Unknown")

# Tests that quotes are loaded correctly from file
def test_load_quotes():
    quote = DailyQuote()
    quotes = quote._load_quotes()
    
    assert isinstance(quotes, list)
    assert len(quotes) > 0
    assert isinstance(quotes[0], tuple)
    assert len(quotes[0]) == 2
    
    # Test quote format
    for q, author in quotes:
        assert isinstance(q, str)
        assert isinstance(author, str)
        assert len(q) > 0
        assert len(author) > 0

# Tests that random quotes are generated correctly and with variety
def test_get_random_quote():
    quote = DailyQuote()
    assert len(quote.quotes) > 0
    
    # Test multiple random quotes
    seen_quotes = set()
    for _ in range(10):
        random_quote = quote.get_random_quote()
        assert isinstance(random_quote, str)
        assert len(random_quote) > 0
        assert '"' in random_quote
        assert '-' in random_quote
        seen_quotes.add(random_quote)
    
    # Verify randomization
    assert len(seen_quotes) > 1
