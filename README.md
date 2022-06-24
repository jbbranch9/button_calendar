# button_calendar
a PySimpleGUI calendar widget



ButtonCalendar is a monthly calendar widget, with buttons for each date.
Each calendar spans 6 weeks of dates, which are centered around a particular month and year.
Buttons along the top can be used to change the selected month and year.
These month/year buttons will also refresh the text (but not the key) of each button to reflect the new dates.

Date Buttons are 'toggle-style', meaning they change color when clicked,
    and also add or remove their date string to this calendar's 'selected_dates' array.
To the side of the row of dates is a Week Button, which toggles all Date Buttons in its same row.
ButtonCalendar can be used either as an element within an existing PySimpleGUI window by using self.frame
    *(must call post_finalize() before event loop to get full functionality),
    or as a standalone widget by calling window()
    
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
