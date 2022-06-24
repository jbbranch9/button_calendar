# button_calendar
a PySimpleGUI calendar widget

# OVERVIEW:

ButtonCalendar is a monthly calendar widget, with toggle buttons for each date.

# FEATURES

Each calendar screen spans 6 weeks, centered around the relevant month and year.

DateButtons change color when toggled, and also add or remove their date string to the calendar's 'selected_dates' array.

WeekButtons on the side can toggle all DateButtons in its same row.

# APPLICATION:

ButtonCalendar either can be:

    instantiated as a standalone window by calling 
        ButtonCalendar().window()
    
    -OR- 

    used an element within an existing PySimpleGUI window by assigning 
        button_calendar_object = ButtonCalendar().get_frame()
    and adding button_calendar_object to the window's layout
        *NOTE: You must call post_finalize() AFTER the window is read or finalized, and/or BEFORE the window's event loop to enable full functionality
    
# CONTROLS:

at all times:
    
    mouse_wheel:
        change month

while NOT in 'range selection mode':
    
    left-click:
        press button/select clicked date

    right-click:
        start 'range selection mode' from clicked date

while in 'range selection mode':

    left-click OR
    right-click:
        select all highlighted dates up to and including clicked date, exit 'range selection mode'

    ctrl-right-click OR
    shift-right-click:
        de-select all highlighted dates up to and including clicked date, exit 'range selection mode'
