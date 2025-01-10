# Osal's Study Timer 🍅

#### Video Demo: [URL HERE]

#### Description:

A feature-rich command-line Pomodoro Timer application designed to boost productivity through focused work sessions and structured breaks. This project was created as a final submission for Harvard's CS50P course (2023).

## Project Overview

This application implements the Pomodoro Technique, a time management method developed by Francesco Cirillo in the late 1980s. The technique uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. I chose to create this project because time management is a universal challenge for students and professionals alike, and I wanted to create a tool that would help users maintain focus while preventing burnout.

## File Descriptions

The project consists of several key files, each serving a specific purpose:

1. **project.py**: The main program file containing all core functionality. It includes several key functions:

   - `main()`: The primary function that handles the menu interface and program flow
   - `timer_start()`: Manages the timer functionality and display
   - `save()`: Handles session logging and data persistence
   - `get_stats()`: Processes and returns session statistics
     These functions are implemented at the root level as required by CS50P specifications.

2. **test_project.py**: Contains pytest test functions for the three main functions:

   - `test_timer_start()`: Validates timer functionality
   - `test_save()`: Ensures proper data logging
   - `test_get_stats()`: Verifies statistical calculations
     Each test function corresponds to a main function in project.py, following CS50P naming conventions.

3. **quotes.csv**: A database of inspirational quotes displayed before each session

   - Contains 50 carefully selected motivational quotes
   - Structured with Quote and Author columns

4. **logfile.json**: Stores session data in JSON format

   - Tracks session duration, type, and completion status
   - Enables long-term productivity analysis

5. **requirements.txt**: Lists all required Python packages:
   - click: For command-line interface
   - colorama: For cross-platform colored output
   - pytest: For running test suite

## Design Decisions

During development, I made several key design decisions that shaped the final product:

1. **Command-Line Interface**: I chose a CLI approach over a GUI for several reasons:

   - Minimizes distractions during work sessions
   - Faster interaction for power users
   - Easier integration with terminal workflows
   - Consistent with CS50P's focus on terminal-based applications
   - Study/Tasks within CS50P were mainly focused on CLI projects

2. **Data Storage Format**: I selected JSON for session logging because:

   - Human-readable format for easy debugging
   - Built-in Python support
   - Flexible schema for future feature additions
   - Efficient storage and retrieval

3. **Color Coding**: Implemented using colorama because:

   - Enhances user experience
   - Improves information hierarchy
   - Works consistently across different platforms
   - Helps distinguish between different timer states

4. **Progress Bar**: Added a visual progress indicator to:

   - Provide immediate feedback
   - Reduce anxiety about remaining time
   - Create a more engaging experience

5. **Motivational Quotes**: Included to:
   - Enhance user engagement
   - Provide positive reinforcement
   - Make each session unique

## Features

- 🎯 **Multiple Timer Options**

  - Work Sessions (25 minutes): Traditional Pomodoro work intervals
  - Short Breaks (5 minutes): Quick refreshment breaks
  - Long Breaks (15 minutes): Extended breaks after four sessions
  - Custom Timer durations: Flexible session lengths

- ✨ **Enhanced User Experience**

  - Colorized CLI output: Easy-to-read interface
  - Visual progress bar: Real-time tracking
  - Inspirational quotes: Session motivation
  - Session completion notifications
  - Intuitive menu system

- 📊 **Session Tracking**
  - Automatic logging
  - Statistical analysis
  - Session categorization
  - Completion rates
  - Time management insights

## Installation and Usage

1. Ensure Python 3.6+ is installed
2. Clone the repository
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python project.py`

## Testing

Run the test suite using pytest:

```bash
pytest test_project.py
```

## Author Information

- Name: N.N.G. Osal Wickremasinghe
- GitHub: OsalWick
- Student ID: 163292122
- Course: CS50P (2023)

## Contributing

While this project was developed as part of CS50P coursework, suggestions and improvements are welcome. Please feel free to fork the repository and submit pull requests.


