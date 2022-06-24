# © 2021-2022 Jacob Branch

import datetime
import keyboard
import mouse
import PySimpleGUI as gui


''' ButtonCalendar is a monthly calendar widget, with buttons for each date.

    Each calendar spans 6 weeks of dates, which are centered around a particular month and year.
    Buttons along the top can be used to change the selected month and year.
    These month/year buttons will also refresh the text (but not the key) of each button to reflect the new dates.
    
    Date Buttons are 'toggle-style', meaning they change color when clicked,
        and also add or remove their date string to this calendar's 'selected_dates' array.

    To the side of the row of dates is a Week Button, which toggles all Date Buttons in its same row.

    ButtonCalendar can be used either as an element within an existing PySimpleGUI window by using self.frame
        *(must call post_finalize() before event loop to get full functionality),
        or as a standalone widget by calling window()



    CONTROLS:

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
    
'''


class ButtonCalendar:
    gui.theme("LightBlue3")

    # 'm' is ordinal number of month (i.e. JAN == 1, DEC == 12)    
    month = lambda m: (
        'JAN',
        'FEB',
        'MAR',
        'APR',
        'MAY',
        'JUN',
        'JUL',
        'AUG',
        'SEP',
        'OCT',
        'NOV',
        'DEC',
    )[m - 1] # 'm-1' is its index in this tuple

    days = ('SUN',
            'MON',
            'TUE',
            'WED',
            'THU',
            'FRI',
            'SAT')

    def font(style="label_small"):
        fonts = {
            "label": ("consolas bold", 13),
            "label_small": ("consolas", 11),
            "calendar_button": ("consolas bold", 16),
        }
        return fonts[style]

    def get_palette():
        
        black = "#FFFFFF"
        white = "#000000"
        med_grey = "#AAAAAA"
        
        navy = "#183440"
        red_gold = "#f3c03f"
        gold = "#F4E04D"
        bright_gold = "#F9EE9F"
        
        colors = {
            "default": navy,
            "text_default": black,
            
            "selected": gold,
            "text_selected": white,
            
            "off_month": med_grey,
            
            "range_select_anchor": red_gold,
            "range_select_hover": bright_gold,
        }
        return colors

    palette = get_palette()

    def today():
        return datetime.datetime.today().strftime("%Y-%m-%d")

    def __init__(self, yyyy_mm_dd:str= None):
        if not yyyy_mm_dd:
            yyyy_mm_dd = ButtonCalendar.today()
        self.year, self.month, self.date = yyyy_mm_dd.split('-')
        
        self.year = int(self.year)
        self.month = int(self.month)
        self.date = int(self.date)
        
        self.today = yyyy_mm_dd
        
        self.range_select_mode = False
        self.range_select_anchor = None
        self.range_select_extent = None
        self.mouse_over = False

        self.set_next_and_last_month()

        self.date_list = self.build_date_list(self.year, self.month)
        self.button_array = []
        self.selected_dates = []

        self.top_button_text = self.refresh_top_buttons()

        ## build buttons

        self.back_year_btn = gui.Button(
            self.top_button_text['back_y'],
            key='back_year',
            size=(6, 1),
            font=ButtonCalendar.font('label'),
            button_color=(
                ButtonCalendar.palette['text_default'],
                ButtonCalendar.palette['default'],
            ),
        )
        self.back_month_btn = gui.Button(
            self.top_button_text['back_m'],
            key='back_month',
            size=(4, 1),
            font=ButtonCalendar.font('label'),
            button_color=(
                ButtonCalendar.palette['text_default'],
                ButtonCalendar.palette['default'],
            ),
        )
        self.month_and_year = gui.Text(
            self.top_button_text['m_and_y'], font=ButtonCalendar.font('calendar_button')
        )
        self.forward_month_btn = gui.Button(
            self.top_button_text['forward_m'],
            key='forward_month',
            size=(4, 1),
            font=ButtonCalendar.font('label'),
            button_color=(
                ButtonCalendar.palette['text_default'],
                ButtonCalendar.palette['default'],
            ),
        )
        self.forward_year_btn = gui.Button(
            self.top_button_text['forward_y'],
            key='forward_year',
            size=(6, 1),
            font=ButtonCalendar.font('label'),
            button_color=(
                ButtonCalendar.palette['text_default'],
                ButtonCalendar.palette['default'],
            ),
        )

        column_layout_array = []
        for d in ButtonCalendar.days:
            column_layout_array.append([[gui.Text(d, font=ButtonCalendar.font('label'))]])

        ## build date button array
        for ix, date in enumerate(self.date_list):

            btn = ButtonCalendar.Date_Button(date, self.month, ix, False)
            self.button_array.append(btn)

            ix = self.date_list.index(date) % 7
            column_layout_array[ix].append([btn])

        ## arrange all buttons into a frame

        frame_layout = [[]]
        for col in column_layout_array:
            new_column = gui.Column(
                col,
                element_justification='center',
                pad=(0, 0),
                vertical_alignment='bottom',
            )
            frame_layout[0].append(new_column)

        add_week_layout = [[gui.Text('WEEK', font=ButtonCalendar.font('label'))]]
        for week in range(6):
            btn = ButtonCalendar.Week_Button(week)
            add_week_layout.append([btn])
        add_week_column = gui.Column(
            add_week_layout,
            element_justification='center',
            pad=(2, 0),
            vertical_alignment='bottom',
        )

        frame_layout[0].append(add_week_column)

        spacer_frame = gui.Frame(
            '', frame_layout, pad=(10, 0), relief='flat', vertical_alignment='bottom'
        )
        c0 = gui.Column(
            [
                [gui.Text('', font=ButtonCalendar.font('label_small'))],
                [
                    self.back_year_btn,
                    self.back_month_btn,
                    self.month_and_year,
                    self.forward_month_btn,
                    self.forward_year_btn,
                ],
                [spacer_frame],
            ],
            element_justification='center',
##  metadata links are for debug only, not recommended for non-debug purposes
##            metadata= {
##                "ButtonCalendar_object": self,
##                "ButtonCalendar_class": ButtonCalendar,
##                }
        )

        self.layout = [[c0]]

        self.frame = gui.Frame(
            ' Select Dates: ',
            self.layout,
            font=ButtonCalendar.font('label'),
            element_justification='center',
            key= '-calendar-frame-',
        )
        
        
    # call after parent window is finalized or read
    def post_finalize(self):
        self.bind_mouse_over()
        self.bind_right_click_to_all_date_btns()
        self.select_today()

    def window(self):

        exit_events = (gui.WIN_CLOSED, 'Exit', 'Escape:27', 'F5:116')

        self.window = window = gui.Window(
            'Button Calendar',
            [[self.frame]],
            return_keyboard_events=True,
            finalize= True,
        )
        
        self.post_finalize()

        while True:
            event, values = window.read()
##            print('Event: ', event)

            if event in exit_events:
                break

            self.handle_event(event, window)

##            print('Selected Dates: ', self.get_selected_dates())
        window.close()
        return self.get_selected_dates()

    # export copy of self.selected_dates
    def get_selected_dates(self):
        return tuple(self.selected_dates)

    # get a framed ButtonCalendar for use in another window
    def get_frame(self):
        del ButtonCalendar.window # disable window launcher
        return self.frame

    def __str__(self):
        return str(self.get_selected_dates())

    # ensures that certain actions (e.g. mouse wheel scroll) only affect calendar the when mouse is over the frame 
    def bind_mouse_over(self):
        self.frame.bind('<Enter>', '_mouse_enter_')
        self.frame.bind('<Leave>', '_mouse_exit_')

    # right click a date button to enter 'range select' mode
    def bind_right_click_to_all_date_btns(self):
        for btn in self.button_array:
            btn.bind('<Button-3>', '_right_click_')
            btn.bind('<Shift-Button-3>', '_control_right_click_')
            btn.bind('<Control-Button-3>', '_control_right_click_')
    
    # buttons can react to mouse hover when called. used when in 'range select' mode
    def bind_hover_to_all_date_btns(self):
        for btn in self.button_array:
            btn.bind('<Enter>', '_mouse_over_')
            
    # buttons can no longer react to mouse hover after called. used when exiting 'range select' mode
    def unbind_hover_from_all_date_btns(self):
        for btn in self.button_array:
            btn.unbind('<Enter>')

    # window-agnostic** handler for all events
    # **(i.e. it should be able to handle any events that originate inside or outside of the widget)
    def handle_event(self, event, window):
        
        if event == '-calendar-frame-_mouse_enter_':
            self.mouse_over = True
        elif event == '-calendar-frame-_mouse_exit_':
            self.mouse_over = False
        
        # interpret mouse wheel as +/- month
        if event == 'MouseWheel:Up' and self.mouse_over == True:
            event = 'back_month'
        if event == 'MouseWheel:Down' and self.mouse_over == True:
            event = 'forward_month'
        
        # if back/forward month/year buttons are pressed, update month and year
        if event in ['back_year', 'back_month', 'forward_year', 'forward_month']:
            self.refresh(event)
        # Date_Button() clicked (left click only)
        if event.startswith('date_btn_') and not event.endswith('_'):
            # if in 'range select mode', use left-click to select range
            if self.range_select_mode == True:
                self.select_range(window, select= True)
            # if not in 'range select mode', use left-click to select individual date
            else:
                btn = window[event]
                self.toggle_date_button(btn, not btn.metadata['selected'])
            
        # Date_Button() mouse over
        if self.range_select_mode == True and event.startswith('date_btn_') and event.endswith('_mouse_over_'):
            
            btn_name = event.replace('_mouse_over_', '')
            btn = window[btn_name]
            self.range_select_extent = btn.ix

            selection_range = self.get_selection_range()
            
            for btn in self.button_array:
                btn.update(
                    button_color=btn.get_button_color(
                        selected=btn.metadata['selected'],
                        is_range_select_anchor= btn.ix == self.range_select_anchor
                    )
                )
            
            for btn_ix in range(selection_range[0], selection_range[1]):
                btn = window['date_btn_'+str(btn_ix)]
                btn.on_range_select_mouse_over(self)
            
            
        # Date_Button() clicked (right click only)
        if event.startswith('date_btn_') and event.endswith('_right_click_'):

            event_is_ctrl_click = event.endswith('_control_right_click_')

            btn_key = event.replace('_right_click_', '')
            btn_key = btn_key.replace('_control', '')

            btn = window[btn_key]
            self.range_select_extent = btn.ix
            
            # not already in 'range_select_mode'
            if self.range_select_mode == False:
                self.bind_hover_to_all_date_btns()
                btn.set_to_range_select_anchor(self)
                self.range_select_mode = True
                
            else:
                self.select_range(window, select= not event_is_ctrl_click)

        # Week_Button() clicked
        if event.startswith('week_select_'):
            btn = window[event]
            dates = btn.metadata['date_range']
            self.toggle_week_button(dates)


        return self

    def select_range(self, window, select= True):
        selection_range = self.get_selection_range()
        for btn_ix in range(selection_range[0], selection_range[1]):
            btn = window['date_btn_'+str(btn_ix)]
            self.toggle_date_button(btn, select)
        self.unbind_hover_from_all_date_btns()
        self.range_select_mode = False

    def get_selection_range(self):
        selection_range = [self.range_select_anchor, self.range_select_extent]
        selection_range.sort()
        selection_range = (selection_range[0], selection_range[1]+1)
        return selection_range

    # auto-selects today's date_button. called after window is initiated, but before first .read() call
    def select_today(self):
        self.toggle_date_button(self.get_button(self.today), True)

    def sunday_before_first(self, year, month):

        first = datetime.datetime(year, month, 1)
        # get day of week from 'first' SUN=1 SAT=7
        dow = int(first.strftime('%w')) + 1

        # roll back one extra week if month starts on a Sunday
        if dow == 1:
            dow = 8

        #'last sunday' is 'first' minus the numerical day of week
        first_sun = first - datetime.timedelta(days=dow)
        return first_sun

    def get_new_month_and_year(self, event):

        if event == 'back_year':
            self.month = self.month
            self.year = self.year - 1

        elif event == 'back_month':
            self.month = self.last_month
            if self.month == 12:
                self.year = self.year - 1
            else:
                self.year = self.year

        elif event == 'forward_month':
            self.month = self.next_month
            if self.month == 1:
                self.year = self.year + 1
            else:
                self.year = self.year

        elif event == 'forward_year':
            mn = self.month
            self.year = self.year + 1

    def refresh_top_buttons(self):
        month = ButtonCalendar.month
        btn_text = {
            'back_y': '<<' + str(self.year - 1),
            'back_m': '<' + str(month(self.last_month)),
            'm_and_y': month(self.month) + '/' + str(self.year),
            'forward_m': str(month(self.next_month)) + '>',
            'forward_y': str(self.year + 1) + '>>',
        }

        return btn_text

    def update_top_buttons(self):
        btn_text = self.refresh_top_buttons()

        self.back_year_btn.update(text=btn_text['back_y'])
        self.back_month_btn.update(text=btn_text['back_m'])
        self.month_and_year.update(btn_text['m_and_y'])
        self.forward_month_btn.update(btn_text['forward_m'])
        self.forward_year_btn.update(btn_text['forward_y'])

    def toggle_date_button(self, button, select):
        date = button.metadata['date']
        if select:
            button.select()
            self.selected_dates.append(date)
            # remove duplicates
            self.selected_dates = list(set(self.selected_dates))
        else:
            button.deselect()
            if date in self.selected_dates:
                self.selected_dates.remove(date)
        # Sorting doesn't matter for saving the note. It's just for readability in the 'Saved to' popup (on window closure)
        self.selected_dates.sort()

    def toggle_week_button(self, date_range):
        # determine range
        begin = date_range[0]
        end = date_range[1]
        btns = self.button_array[begin:end]
        dates = self.date_list[begin:end]

        # assume all btns in week are selected,
        all_selected = True
        for btn in btns:
            # unless there exist one which isn't selected,
            if not btn.metadata['selected']:
                # in which case, deslect all:
                all_selected = False

        for ix, dt in enumerate(dates):
            btn = btns[ix]
            if all_selected:
                # deselect all btns in range
                self.toggle_date_button(btn, select=False)
            else:
                # select all btns in range
                self.toggle_date_button(btn, select=True)

    def set_next_and_last_month(self):
        if self.month == 1:
            self.last_month = 12
        else:
            self.last_month = self.month - 1

        if self.month == 12:
            self.next_month = 1
        else:
            self.next_month = self.month + 1

    def refresh(self, event):
        # get new date info
        self.get_new_month_and_year(event)
        self.date_list = self.build_date_list(self.year, self.month)

        # update month/year btns
        self.set_next_and_last_month()
        self.update_top_buttons()

        # update Date_Buttons
        for ix, new_date in enumerate(self.date_list):
            btn = self.button_array[ix]
            btn.metadata = btn.new_metadata(new_date, self.month)
            btn.update(text=btn.name(new_date))
            btn.update(button_color=btn.get_button_color())

        for btn in self.button_array:
            if btn.metadata['date'] in self.selected_dates:
                btn.select()
            else:
                btn.deselect()

    def get_button(self, date):
        dates = self.date_list
        ix = dates.index(date)
        btns = self.button_array
        btn = btns[ix]
        return btn

    def build_date_list(self, year, month):
        dates = []

        # start on the Sunday before the 1st of the month
        dt = self.sunday_before_first(year, month)

        for offset in range(42):
            dt += datetime.timedelta(days=1)

            dates.append(dt.strftime('%Y-%m-%d'))

        return dates

    class Week_Button(gui.Button):
        def __init__(self, week):
            date_range = [7 * week, 7 * week + 7]
            # P(date_range)
            super().__init__(
                '+/-',
                size=(3, 1),
                font=ButtonCalendar.font('calendar_button'),
                pad=(1, 1),
                auto_size_button=False,
                metadata={'date_range': date_range},
                key='week_select_' + str(week),
                button_color=(
                    ButtonCalendar.palette['text_default'],
                    ButtonCalendar.palette['default'],
                ),
            )

    class Date_Button(gui.Button):
        def __init__(self, date, parent_calendar_month, ix, selected=False):

            self.metadata = self.new_metadata(date, parent_calendar_month)
            
            self.ix = ix

            color = self.get_button_color(selected)

            super().__init__(
                self.name(date),
                key='date_btn_' + str(self.ix),
                size=(3, 1),
                pad=(1, 1),
                metadata=self.metadata,
                button_color=color,
                font=ButtonCalendar.font('calendar_button'),
            )

        def new_metadata(self, date, parent_calendar_month):
            return {
                'selected': False,
                'date': date,
                'button_month': self.get_button_month(date),
                'parent_month': parent_calendar_month,
            }

        def get_button_month(self, date):
            return int(date[5:7])

        def get_button_color(self, selected=False, is_range_select_anchor= False):
            if selected:
                color = (
                    ButtonCalendar.palette['text_selected'],
                    ButtonCalendar.palette['selected'],
                )

            elif is_range_select_anchor:
                color = (
                    ButtonCalendar.palette['text_selected'],
                    ButtonCalendar.palette['range_select_anchor'],
                )
            
            # unselected, within current month
            elif self.metadata['button_month'] == self.metadata['parent_month']:
                color = (
                    ButtonCalendar.palette['text_default'],
                    ButtonCalendar.palette['default'],
                )
                
            # unselected, outside of current month
            else:
                color = (
                    ButtonCalendar.palette['text_selected'],
                    ButtonCalendar.palette['off_month'],
                )

            return color

        def name(self, date):
            return str(date)[-2:]
        
        def toggle(self, select):
            self.metadata['selected'] = select
            self.update(button_color=self.get_button_color(selected= select))

        def select(self):
            self.toggle(select= True)

        def deselect(self):
            self.toggle(select= False)
            
        # right-click, init 'range select mode'
        def set_to_range_select_anchor(self, parent_calendar):
            parent_calendar.range_select_anchor = self.ix
            self.update(
                button_color=(
                    ButtonCalendar.palette['text_selected'],
                    ButtonCalendar.palette['range_select_anchor'],
                )
            )
            
        def on_range_select_mouse_over(self, parent_calendar):
            if parent_calendar.range_select_anchor != self.ix:
                self.update(
                    button_color=(
                        ButtonCalendar.palette['text_selected'],
                        ButtonCalendar.palette['range_select_hover'],
                    )
                )
                

def main():
    print(ButtonCalendar().window())
    print('Done.')

if __name__ == '__main__':
    main()
