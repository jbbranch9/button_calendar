# ButtonCalendar
a PySimpleGUI calendar widget with toggle buttons for each date.

# FEATURES

Each calendar screen spans 6 weeks, centered around the relevant month and year.

Multiple dates can be toggled. A tuple of toggled dates can be called/printed at any time. (see "SELECTED DATES")

DateButtons change color when toggled, and also add or remove their date string to the calendar's 'selected_dates' array.

WeekButtons on the side can toggle all DateButtons in its same row.

# APPLICATION:

ButtonCalendar has two modes, (A) self-windowed and (B) framed:

    (A) instantiate as a standalone window by calling 
        ButtonCalendar().window()
    
    -OR- 

    (B) use an element within an existing PySimpleGUI window by assigning 
        button_calendar_object = ButtonCalendar().get_frame()
        and adding button_calendar_object to the window's layout
        *NOTE: You must call post_finalize() AFTER the window is read or finalized, and/or BEFORE the window's event loop to enable full functionality.
    
# SELECTED DATES:

Calling button_calendar_object.get_selected_dates() will return an array of the 
currently selected dates formatted as ("YYYY-MM-DD", "YYYY-MM-DD", etc.)
This list can also be printed by casting the ButtonCalendar as a string.
In other words, print(button_calendar_object)* will print the selected dates as a string.

* or "ctrl-P" while in self-windowed mode
** ButtonCalendar().window() also returns the selected dates when the window is closed.


# CONTROLS:

while mouse is hovering over calendar:
    
    mouse_wheel:
        change month

while NOT in 'range selection mode':
    
    left-click:
        press button/select clicked date

    right-click:
        start 'range selection mode' from clicked date

while in 'range selection mode':

    left-click  
        -or-
    right-click:
        select all highlighted dates up to and including clicked date, exit 'range selection mode'

    ctrl-right-click  
        -or-
    shift-right-click:
        de-select all highlighted dates up to and including clicked date, exit 'range selection mode'
        
while in self-windowed mode:
    
    ctrl-P:
        print selected dates array
