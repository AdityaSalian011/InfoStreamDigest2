from news.news import NewsAPI
from weather.weather import WeatherAPI
from stock.stock import StockAPI
from gui.gui import userGUI
from html_email.html_email import HTMLEmail
from html_pdf.html_pdf import HTMLPdf
from gui.utils import show_error_message, show_success_message, store_user_data
from jinja2 import Environment, FileSystemLoader
import threading

class InfoStreamDigest:
    def __init__(self):
        """Initializing our class and imported modules."""
        self.gui = userGUI(file_name='dir/user_dir/userInfo.json')
        self.news_api = NewsAPI()
        self.weather_api = WeatherAPI()
        self.stock_api = StockAPI()
        self.html_email = HTMLEmail()
        self.html_pdf = HTMLPdf()

        self.unsaved_changes = False
        self.previous_data = self.gui.get_entry_data()

        self._bind_change_events()      ## handles changes made when program is running.

        self.gui.save_config_btn.config(command=self.save_config)
        self.gui.run_config_btn.config(command=self.run_now)
        self.gui.download_pdf_btn.config(command=self.download_pdf)

    def _get_entry_widgets(self):
        return [
            self.gui.name,
            self.gui.email,
            self.gui.news_api_key,
            self.gui.weather_api_key,
            self.gui.city,
            self.gui.news_topic
        ]

    def _show_loading(self, text='Loading..'):
        """Shows progression text"""
        self.gui.loading_label.config(text=text)
        self.gui.window.update_idletasks()
    
    def _hide_loading(self):
        """Hides progression text"""
        self.gui.loading_label.config(text='')
        self.gui.window.update_idletasks()

    def _bind_change_events(self):
        """Bind key and focus events on entry widgets to detect changes."""
        entry_widgets = self._get_entry_widgets()
        for widget in entry_widgets:
            if hasattr(widget, 'bind'):
                widget.bind('<KeyRelease>', self._on_entry_change)
                widget.bind('<FocusOut>', self._on_entry_change)

    def _on_entry_change(self, event=None):
        """Mark unsaved_changes=True if current data differs from previous."""
        current_data = self.gui.get_entry_data()
        if current_data != self.previous_data:
            self.unsaved_changes = True

    def _has_unsaved_changes(self):
        """Check if form data has changed since last save."""
        current_data = self.gui.get_entry_data()
        return current_data != self.previous_data
    
    def _save_config(self):
        """A helper function
            1. Retrieves user input data.
            2. Checks if data are valid, if not, an error is shown to user.
            3. Once every user field is valid, they are stored inside a json file.     
        """
        user_data = self.gui.get_entry_data()

        name = user_data['username']
        email = user_data['email']
        news_api_key = user_data['news api key']
        weather_api_key = user_data['weather api key']
        city = user_data['city']
        news_topic = user_data['news topic']

        invalid_data = self.gui.validate_username_email(name, email)
        if invalid_data:
            return invalid_data
        
        weather_error = self.weather_api.store_weather_info(api_key=weather_api_key, city_name=city, file_name='dir/weather_dir/weatherInfo.json')
        if weather_error:
            return weather_error 
            
        stock_error = self.stock_api.store_stock_data(period='5d', file_name='dir/stock_dir/stockInfo.json')
        if stock_error:
            return stock_error 
            
        if news_topic['error']:
            return news_topic['error']

        news_error = self.news_api.store_top_news(api_key=news_api_key, topic=news_topic['topic'], file_name='dir/news_dir/newsInfo.json')
        if news_error:
            return news_error
            
        store_user_data(user_data, file_name='dir/user_dir/userInfo.json')

        self.unsaved_changes = False    ## reseting everytime data is saved
        self.previous_data = user_data.copy()   ## previous data is now a copy of current user data.
        return

    def save_config(self):
        def task():
            self._show_loading('Saving data.. Please wait.')
            error = self._save_config()
            self._hide_loading()

            if error:
                show_error_message(error)
            else:
                show_success_message('✅ User Information Stored Successfully')
            
        threading.Thread(target=task, daemon=True).start()

    def run_now(self):
        def task():
            self._show_loading('Running now... Please wait')

            if self._has_unsaved_changes():     ## if unsaved_changes=True, we run save_config to save new user data
                save_error = self._save_config()

                if save_error:
                    self._hide_loading()
                    show_error_message(save_error)
                    return

            try:
                """Handling errors"""
                news_data, news_error = self.news_api.get_news_data_from_json(file_name='dir/news_dir/newsInfo.json')
                if news_error:
                    show_error_message(news_error)
                    return

                weather_data, weather_error = self.weather_api.get_weather_data_from_json(file_name='dir/weather_dir/weatherInfo.json')
                if weather_error:
                    show_error_message(weather_error)
                    return

                stock_data, stock_error = self.stock_api.get_stock_data_from_json(file_name='dir/stock_dir/stockInfo.json')
                if stock_error:
                    show_error_message(stock_error)
                    return 
                
            except Exception as exc:
                show_error_message(f'Error loading data\n{exc}')
                return
                    
            """Passing data to html file"""
            folder_name = 'templates'
            html_file = 'index.html'
                
            env = Environment(loader=FileSystemLoader(folder_name))
            template = env.get_template(html_file)

            rendered_html = template.render(
                data=news_data,
                weather_info=weather_data['weather_info'],
                weather_icon_url=weather_data['weather_icon_url'],
                stock_info=stock_data
            )

            user_data = self.gui.get_entry_data()
            if user_data and user_data.get('email'):
                try:
                    email_add = user_data['email']
                    news_topic = user_data['news topic']['topic']
                    _, email_error = self.html_email.send_html_content(email_add, rendered_html, news_topic)
                    if email_error:
                        self._hide_loading()
                        show_error_message(email_error)
                        return
                except Exception as exc:
                    self._hide_loading()
                    show_error_message(f"Unexpected error\n{exc}")
                    return
                else:
                    self._hide_loading()
                    show_success_message(f'We have sent you an email at {email_add}\nPlease check.')
                    return
            else:
                self._hide_loading()
                show_error_message('No user data found. Try saving data first!')
                return
        threading.Thread(target=task, daemon=True).start()

    def download_pdf(self):
        """A method to download pdf version of html file."""
        html_file_path = 'templates/rendered.html'

        pdf_success, pdf_error = self.html_pdf.html_to_pdf(html_file_path, 'output.pdf')
        if pdf_error:
            show_error_message(pdf_error)
            return
        
        show_success_message(pdf_success)
        return

if __name__=='__main__':
    info_sd = InfoStreamDigest()
    info_sd.gui.window.mainloop()