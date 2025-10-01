from gui.utils import *
from news.key import my_news_api_key
from weather.key import my_weather_api_key

class userGUI:
    def __init__(self, file_name):
        self.window = tk.Tk()
        self.window.state('zoomed')

        existing_data = get_user_data(file_name)

        frame_main = tk.Frame(self.window, bg='#2c2c2c')
        frame_main.grid(row=0, column=0, sticky='nsew', padx=40, pady=20)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        frame_main.grid_columnconfigure(0, weight=1)

        frame_user = tk.LabelFrame(frame_main, text='User Information', font=("Arial", 16, "bold"), bg="#2c2c2c", fg="white", padx=20, pady=20)
        frame_user.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        self.name = create_entry_windows(frame_user, field='username', user_data=existing_data, row=0)
        self.email = create_entry_windows(frame_user, field='email', user_data=existing_data, row=1)

        tk.Label(frame_user, fg='#ffcc00', bg='#2c2c2c', font=('Arial', 10), text='Optional: Leave blank to use the default News API key.').grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=(0,5))
        self.news_api_key = create_entry_windows(frame_user, field='news api key', user_data=existing_data, row=3)

        tk.Label(frame_user, fg='#ffcc00', bg='#2c2c2c', font=('Arial', 10), text='Optional: Leave blank to use the default Weather API key.').grid(row=4, column=0, columnspan=2, sticky='w', padx=5, pady=(0,5))
        self.weather_api_key = create_entry_windows(frame_user, field='weather api key', user_data=existing_data, row=5)

        self.city = create_entry_windows(frame_user, field='city', user_data=existing_data, row=6)
        
        self.loading_label = tk.Label(frame_main, text='', font=('Arial', 16, 'bold'), fg='#ffcc00', bg='#2c2c2c')
        self.loading_label.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

        frame_rb = tk.LabelFrame(frame_main, text='News Topics', font=('Arial', 16, 'bold'), bg='#2c2c2c', fg='white', padx=20, pady=20)
        frame_rb.grid(row=2, column=0, padx=20, pady=20, sticky='ew')

        self.news_topic = tk.StringVar()
        self.news_topic.set('trending')

        self.label, self.e_widget = create_entry_label_widgets(frame_rb, row=0, col=0)

        frame_rb_btns = tk.Frame(frame_rb, bg='#2c2c2c')
        frame_rb_btns.grid(row=1, column=0, pady=5, padx=10)

        create_radio_buttons(frame_rb_btns, self.e_widget, self.news_topic, row=0, col=0)

        ## colspan = 6 for 6 radio button (news topics).
        self.e_widget.grid(row=2, column=0, columnspan=6, sticky='ew', padx=10, pady=5)
        self.e_widget.grid_remove()

        frame_btns = tk.Frame(frame_main, bg='#2c2c2c')
        frame_btns.grid(row=3, column=0, pady=20, padx=20)

        self.save_config_btn = create_button(frame_btns, field='save config', col=0, row=0)
        self.run_config_btn = create_button(frame_btns, field='run config', col=1, row=0)
        self.download_pdf_btn = create_button(frame_btns, field='download pdf', col=2, row=0)

    def get_entry_data(self):
        """A helper function which returns information inputed by user"""
        news_topic, error = self.get_news_topic()

        return{
            'username': self.name.get(),
            'email': self.email.get(),
            'news api key': self.news_api_key.get() if self.news_api_key.get().strip() else my_news_api_key,    
            ## stores news api key inputed by user, if not uses default news api key.
            'weather api key': self.weather_api_key.get() if self.weather_api_key.get().strip() else my_weather_api_key,
            ## stores weather api key inputed by user, if not uses default weather api key.
            'city': self.city.get(),
            'news topic': {
                'topic': news_topic,
                'error': error
            }
        }
    
    def validate_username_email(self, username, email):
        is_valid_name = check_username_pattern(username)
        if not is_valid_name:
            return '❌ Invalid username pattern.'
        
        is_valid_email, error = check_email_pattern(email)
        if not is_valid_email:
            return '❌ '+str(error)
        
    def get_news_topic(self):
        """get the selected news topic, handling error"""
        return get_selected_topic(self.e_widget, self.news_topic)