from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage, CoreImage
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton, MDFloatingActionButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import IconLeftWidget, TwoLineAvatarListItem, OneLineAvatarListItem
from kivymd.uix.card import MDCard
from filemanager import MDFileManager
from kivymd.toast import toast
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.spinner import MDSpinner
from kivy.storage.jsonstore import JsonStore
from kivy.loader import Loader
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
##############################
#Window.size = (390, 650)
#from concurrent.futures import ThreadPoolExecutor
import threading
import requests
import base64
import json
import os
import io
import shutil
import time
import csv
import webbrowser
from pyDes import *
from mutagen.mp4 import MP4, MP4Cover
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from contextlib import closing

if platform == 'android':
    import android
    from android.permissions import request_permissions, Permission, check_permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    from plyer import notification
    from jnius import autoclass
    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioManager = autoclass('android.media.AudioManager')

search_base_url = "https://www.jiosaavn.com/api.php?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query="
song_details_base_url = "https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids="
playlist_details_base_url = "https://www.jiosaavn.com/api.php?__call=webapi.get&token={}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
playlist_ids = {
  "Weekly Top JioTunes" : "znKA,YavndBuOxiEGmm6lQ__",
  "Hindi - Weekly Top Songs" : "8MT-LQlP35c_",
  "Hindi - Top JioTunes":"AZNZNH1EwNjfemJ68FuXsA__",
  "English Top Songs" : "LdbVc1Z5i9E_",
  "English - Top JioTunes" : "xXiMISqMjsrfemJ68FuXsA__",
  "Punjabi - Weekly Top Songs":"W6DUe-fP3X8_",
  "Punjabi - Top JioTunes":"mzDerWPsSwiO0eMLZZxqsA__",
  "Latest Punjabi Hits":"T,w3Z-u7t6A_",
  "VYRL Top 20":"zvYYPLOvojJFo9wdEAzFBA__",
  "Haryanvi - Weekly Top Songs" :"ar5lExlDmbwwkg5tVhI3fw__",
  "Haryanvi - Top JioTunes":"xgyTegenCljc1EngHtQQ2g__",
  }

playlist_images = {
    "8MT-LQlP35c_" : "http://c.saavncdn.com/editorial/wt15-49_20210101173527.jpg?bch=1609524330",
    "znKA,YavndBuOxiEGmm6lQ__" : "https://pli.saavncdn.com/44/90/101334490.jpg?bch=1486377541",
    "AZNZNH1EwNjfemJ68FuXsA__" : "https://c.saavncdn.com/editorial/TopJioTunesHindi_20200721161337.jpg?bch=1610064389",
    "LdbVc1Z5i9E_" : "http://c.saavncdn.com/editorial/wt15-7386899_20210101134203.jpg?bch=1609510327",
    "xXiMISqMjsrfemJ68FuXsA__" : "https://c.saavncdn.com/editorial/TopJioTunesEnglish_20181220070458.jpg",
    "W6DUe-fP3X8_" : "https://c.saavncdn.com/editorial/wt15-2676373_20201225140344.jpg?bch=1608935628",
    "mzDerWPsSwiO0eMLZZxqsA__" : "https://c.saavncdn.com/editorial/TopJioTunesPunjabi_20181220084041.jpg?bch=1610064899",
    "T,w3Z-u7t6A_" : "https://c.saavncdn.com/editorial/LatestPunjabiHits_20201128085206.jpg?bch=1606555342",
    "zvYYPLOvojJFo9wdEAzFBA__" : "https://c.saavncdn.com/editorial/VYRLTop20_20200929074344.jpg?bch=1605790299",
    "ar5lExlDmbwwkg5tVhI3fw__" : "https://c.saavncdn.com/editorial/wt15-157145953_20210101135104.jpg?bch=1609539668",
    "xgyTegenCljc1EngHtQQ2g__" : "https://c.saavncdn.com/editorial/TopJioTunesHaryanvi_20181220085019.jpg?bch=1610064088",
}

class Tab(FloatLayout, MDTabsBase):
    pass

class MyApp(MDApp):
    title = "Black Hole"
    __version__ = "0.7"
    status = True
    play_status = 'stop'
    last_screen = []
    win_size = min(Window.size)

#    def on_start(self):
#        self.root.ids.tabs.add_widget(Tab(text='Local'))
#        self.root.ids.tabs.add_widget(Tab(text='Global'))
    #def on_start(self):
    #    self.trend_list = self.root.ids.trend_list
    #    self.trend_list.clear_widgets()
    #    add_trend_thread=threading.Thread(target=self.add_songs)
    #    add_trend_thread.start()

    def build(self):
        if self.user_data.exists('theme'):
            self.theme_cls.theme_style = self.user_data.get('theme')['mode']
        else:
            self.user_data.put('theme', mode='Light')
        if self.user_data.exists('accent'):
            self.theme_cls.primary_palette = self.user_data.get('accent')['color']
        if self.theme_cls.theme_style == "Dark":
            self.root.ids.dark_mode_switch.active = True
        #self.theme_cls.primary_hue = "A400"
        self.theme_cls.accent_palette = self.theme_cls.primary_palette
        Loader.loading_image = 'cover.jpg'
        #return Builder.load_string(main)
        # if self.user_data.exists('sync'):
        #     if int(time.time()) - int(self.user_data.get('sync')['time']) > 21600:
        #         sync_thread = threading.Thread(target=self.get_chart)
        #         sync_thread.start()
        #         self.user_data.put('sync', time=time.time())
        #     else:
        #         print('already synced')
        # else:
        #     sync_thread = threading.Thread(target=self.get_chart)
        #     sync_thread.start()

    def notify(self, title='', message='', app_name='', app_icon='', timeout=10, ticker='', toast=False):
        AndroidString = autoclass('java.lang.String')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        Context = autoclass('android.content.Context')
        Drawable = autoclass('org.test.notify.R$drawable')
        app_icon = Drawable.icon
        notification_builder = NotificationBuilder(PythonActivity.mActivity)
        notification_builder.setContentTitle(AndroidString(title.encode('utf-8')))
        notification_builder.setContentText(AndroidString(message.encode('utf-8')))
        notification_builder.setSmallIcon(app_icon)
        notification_builder.setAutoCancel(True)
        notification_service = notification_service = PythonActivity.mActivity.getSystemService(Context.NOTIFICATION_SERVICE)
        notification_service.notify(0,notification_builder.build())

    def tap_target_start(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data_path = os.path.join(self.user_data_dir, 'data.json')
        self.user_data = JsonStore(self.user_data_path)
        Window.bind(on_keyboard=self.events)
        if self.user_data.exists('download_path'):
            self.path = self.user_data.get('download_path')['path']
        else:
            self.path = os.path.join(os.getenv('EXTERNAL_STORAGE'), 'Songs')
        self.data_path = os.path.join(self.user_data_dir, 'cache')
        #self.user_data.put('accent', color='Blue')
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.file_manager.ext = [".m4a", ".mp3"]
        if os.path.exists(self.path):
            pass
        else:
            os.mkdir(self.path)
        if os.path.exists(self.data_path):
            pass
        else:
            os.mkdir(self.data_path)
        if not os.path.exists(self.user_data_path):
            self.user_data.put('theme', mode='Light')
            self.user_data.put('accent', color='Blue')

    def change_theme(self):
        if self.root.ids.dark_mode_switch.active == True:
            self.theme_cls.theme_style = "Dark"
            self.user_data.put('theme', mode='Dark')
        else:
            self.theme_cls.theme_style = "Light"
            self.user_data.put('theme', mode='Light')
    
    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        instance_tab.ids.label.text = tab_text

    def check_update(self):
        webbrowser.open_new('https://github.com/Sangwan5688/Black_Hole-music_downloader')

    def get_chart(self):
        with open('top_local_chart.csv', 'wb') as f:
            f.write(requests.get('https://spotifycharts.com/regional/in/daily/latest/download').content)
#        with open('top_global_chart.csv', 'wb') as f:
#            f.write(requests.get("https://spotifycharts.com/regional/global/daily/latest/download").content)
        self.user_data.put('sync', time=time.time())

    def add_top(self):
        self.top_list = self.root.ids.top_list
#        self.top_global_list = self.root.ids.top_global_list
        if self.top_list.children == []:
            Clock.schedule_once(self.thread_top)
            self.dia = MDDialog(text="Loading spotify top 200 chart", size_hint=(0.7,1))
            self.dia.open()
            
    def thread_top(self, *args):
        self.add_top_thread=threading.Thread(target=self.add_songs)
        self.add_top_thread.start()
    
    def add_trend(self):
        Clock.schedule_once(self.add_trend2)
        self.dia = MDDialog(text="Loading trending songs", size_hint=(0.7,1))
        self.dia.open()
    
    def add_trend2(self, *args):
        if self.root.ids.trend_grid.children == []:
            for key, values in playlist_ids.items():
                self.get_playlist(key, values)
        self.dia.dismiss()
        #for i in ["znKA,YavndBuOxiEGmm6lQ__", "8MT-LQlP35c_", "LdbVc1Z5i9E_", "xXiMISqMjsrfemJ68FuXsA__"]:
        #    executor.submit(self.get_playlist, i)
        #executor.shutdown()

    def add_songs(self):
        url = 'https://spotifycharts.com/regional/in/daily/latest/download'
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    pos = int(row[0])
                    song_name = row[1]
                    art_name = row[2]
                    lst = TwoLineAvatarListItem(text="{}. {}".format(pos, song_name), secondary_text=art_name, on_press=lambda x, y=song_name: self.select_spotify(y))
                    lst.add_widget(IconLeftWidget(icon='music-note-outline'))
                    self.top_list.add_widget(lst)
                except:
                   continue
        try:
            self.dia.dismiss()
        except:
            pass

    def select_spotify(self, song_name):
        self.dia = MDDialog(text="Loading..", size_hint=(0.7,1))
        self.dia.open()
        spoti = threading.Thread(target=self.spoti_thread, args=(song_name,))
        spoti.start()
    
    def spoti_thread(self, song_name):
        response = requests.get(search_base_url+song_name)
        result = response.content.decode()
        self.search_data = json.loads(result.replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"))['songs']['data']
        self.song_details(0)

    def push_notify(self, head):
        notification.notify(head, "Download complete")

    def download_list(self):
        self.down_list = self.root.ids.downloadlist
        self.down_list.clear_widgets()
        td = threading.Thread(target=self.add_songs_downlist)
        td.start()
    
    def add_songs_downlist(self):
        self.down_path_list = []
        for root, dirs, files in os.walk(os.getenv('EXTERNAL_STORAGE')):
            for filename in files:
                if os.path.splitext(filename)[1] in [".mp3", ".m4a", ".ogg", ".wav"]:
                    self.down_path_list.append((os.path.join(root, filename), filename))
        for i in range(len(self.down_path_list)):
            lst = OneLineAvatarListItem(text=self.down_path_list[i][1], on_press=lambda x, y=i: self.play_song(y))
            lst.add_widget(IconLeftWidget(icon='music-note-outline'))
            self.down_list.add_widget(lst)

    def show_data(self, query):
        close_btn = MDFlatButton(text="Close", on_release=self.close_dialog)
        if query == '':
            self.dia = MDDialog(title="Invalid Name", text="Please enter a song name", size_hint=(0.7,1), buttons=[close_btn])
            self.dia.open()
        
        else:
            self.change_screen('SongListScreen')
            self.dia = MDDialog(text="Searching for songs ...", size_hint=(0.7,1))
            self.list_view = self.root.ids.container
            self.list_view.clear_widgets()
            self.dia.open()
            req = UrlRequest(search_base_url+query.replace(' ','+'), self.show_list)

    def show_list(self, req, result):
        self.search_data = json.loads(result.replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"))['songs']['data']
        for i in range(len(self.search_data)):
            lst = TwoLineAvatarListItem(text=self.search_data[i]['title'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"), secondary_text=self.search_data[i]['more_info']['primary_artists'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"), on_press=lambda x,y=i: self.song_details(y))
            lst.add_widget(IconLeftWidget(icon='music-note-outline'))
            self.list_view.add_widget(lst)
        self.dia.dismiss()

    def fetch_details(self):
        print('started fetching details')
        self.song_data = json.loads(requests.get(song_details_base_url+self.song_id).text.replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"))[self.song_id]
        try:
            url = self.song_data['media_preview_url']
            url = url.replace("preview", "aac")
            if self.song_data['320kbps']=="true":
                url = url.replace("_96_p.mp4", "_320.mp4")
            else:
                url = url.replace("_96_p.mp4", "_160.mp4")
            self.song_dwn_url = url
        except KeyError or TypeError:
            self.song_data['media_url'] = self.decrypt_url(self.song_data['encrypted_media_url'])
            if self.song_data['320kbps']!="true":
                self.song_dwn_url = self.song_data['media_url'].replace("_320.mp4","_160.mp4")
        
        self.song_name = self.song_data['song']
        self.album = self.song_data['album']
        self.artist_name = self.song_data["primary_artists"]
        self.featured_artist = self.song_data["featured_artists"]
        self.year = self.song_data["year"]
        self.genre = (self.song_data["language"]).capitalize()
        self.prepare(self.song_dwn_url)
        self.root.ids.SongDetailsScreen.add_widget(MDLabel(text=self.convert_sec(self.sound.getDuration()), halign='right', theme_text_color='Secondary', padding_x='20dp', pos_hint={"top":0.725}))
        self.play_stamp = (MDLabel(text=self.convert_sec(self.sound.getCurrentPosition()), halign='left', theme_text_color='Secondary', padding_x='20dp', pos_hint={"top":0.725}))
        self.root.ids.SongDetailsScreen.add_widget(self.play_stamp)
        print('finished fetching details')
    
    def get_playlist(self, title, listId):
        image = AsyncImage(source=playlist_images[listId], size_hint=(1,1), pos_hint={'top':0.9}, allow_stretch=True)
        card = MDCard(orientation='vertical', border_radius= 15, radius= [0,0,15,15], pos_hint={"center_x":0.5, "center_y":0.5}, size_hint=(None, None), size=(self.win_size*0.3, self.win_size*0.3))
        card.add_widget(image)
        self.root.ids.trend_grid.add_widget(MDTextButton(text=title, pos_hint= {'center_x':0.5}, on_press=lambda x: self.show_top(title, listId)))
        self.root.ids.trend_grid.add_widget(card)
        self.root.ids.trend_grid.add_widget(MDLabel(text=''))
        self.root.ids.trend_grid.add_widget(MDLabel(text=''))
        self.root.ids.trend_grid.add_widget(MDLabel(text=''))
        self.root.ids.trend_grid.add_widget(MDLabel(text=''))
        
    def show_top(self, ttl, Id):
        self.dia = MDDialog(text="Loading {}".format(ttl), size_hint=(0.7,1))
        self.dia.open()
        t3 = threading.Thread(target=self.show_top2, args=(ttl,Id))
        t3.start()

    def show_top2(self, ttl, Id):
        self.tlist = self.root.ids.trend_list
        self.root.ids.trend_toolbar.title = ttl
        self.tlist.clear_widgets()
        try:
            response = requests.get(playlist_details_base_url.format(Id))
            if response.status_code == 200:
                songs_json = response.text.encode().decode()
                songs_json = json.loads(songs_json)
                self.search_data = songs_json['list']
                for i in range(int(len(songs_json['list']))):
                    #print(items['id'])
                    #print(i)
                    #print(songs_json['list'][i]['title'])
                    lst = TwoLineAvatarListItem(text=songs_json['list'][i]['title'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"), secondary_text=songs_json['list'][i]['subtitle'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'"), on_press=lambda x,y=i: self.song_details(y))
                    lst.add_widget(IconLeftWidget(icon='music-note-outline'))
                    self.tlist.add_widget(lst)
            self.change_screen('TrendListScreen')
        except Exception as e:
            print(e)
        self.dia.dismiss()

    def decrypt_url(url):
        des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
        enc_url = base64.b64decode(url.strip())
        dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
        dec_url = dec_url.replace("_96.mp4", "_320.mp4")
        return dec_url

    def song_details(self, i):
        self.s_manager = self.root.ids.screen_manager
        self.change_screen('SongDetailsScreen')
        self.details_screen = self.root.ids.SongDetailsScreen
        self.details_screen.clear_widgets()
        self.song_name = self.search_data[i]['title'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")
        self.song_id = self.search_data[i]['id']
        try:
            self.artist_name = self.search_data[i]['more_info']['primary_artists'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")
            self.album = self.search_data[i]['album'].replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")
        except:
            self.artist_name = self.search_data[i]['subtitle']
        self.image_url = self.search_data[i]['image'].replace('50x50', '500x500').replace('150x150', '500x500')
        self.image_path = os.path.join(self.data_path,self.song_id+'.jpg')
        self.fetch_thread = threading.Thread(target=self.fetch_details)
        self.fetch_thread.start()
        self.details_screen.add_widget(MDIconButton(icon='chevron-left', pos_hint={"center_x":0.05, "center_y":0.95}, on_press=lambda x: self.back_screen()))
        song_image = AsyncImage(source=self.image_url, pos_hint={"center_x":0.5, "center_y":0.5}, allow_stretch=True)
        card = MDCard(orientation='vertical', pos_hint={"center_x":0.5, "center_y":0.65}, size_hint=(None, None), size=(self.win_size*0.9, self.win_size*0.9))
        card.add_widget(song_image)
        self.details_screen.add_widget(card)
        self.details_screen.add_widget(MDLabel(text=self.song_name, halign='center', theme_text_color='Custom', text_color=self.theme_cls.primary_color, font_style='H4', bold=True, pos_hint={"top":0.84}))
        self.details_screen.add_widget(MDLabel(text=self.artist_name, halign='center', theme_text_color='Secondary', font_style='H6', pos_hint={"top":0.8}))
        self.spinner = MDSpinner(size_hint=(None, None), size=("50","50"), pos_hint={'center_x':0.5, "center_y":0.15}, active=True)
        #self.details_screen.add_widget(MDLabel(text=self.album, halign='center', theme_text_color='Hint', font_style='H6', pos_hint={"top":0.9}))
        self.heart_icon = MDIconButton(icon='heart-outline', user_font_size="30sp", theme_text_color= 'Secondary', pos_hint={"center_x":0.1, "center_y":0.15}, on_press=lambda x: self.add_fav())
        self.details_screen.add_widget(self.heart_icon)
        self.play_progress = MDProgressBar(pos_hint = {'center_x':0.5, 'center_y':0.25}, size_hint_x = 0.9, value = 0, color = self.theme_cls.primary_color)
        self.details_screen.add_widget(self.play_progress)
        self.tap_target_view = MDTapTargetView(
            widget=self.heart_icon,
            title_text="Add to Favorites",
            description_text="Feature currently under development",
            widget_position="left_bottom",
        )
        self.details_screen.add_widget(MDIconButton(icon="chevron-double-left", pos_hint={"center_x": .3, "center_y": .15}, user_font_size="50sp", on_release=lambda x: self.rewind()))
        self.details_screen.add_widget(MDIconButton(icon="chevron-double-right", pos_hint={"center_x": .7, "center_y": .15}, user_font_size="50sp", on_release=lambda x: self.forward()))
        self.play_btn = MDFloatingActionButton(icon='play', pos_hint={'center_x':0.5, "center_y":0.15}, user_font_size="50sp", md_bg_color=(1,1,1,1), elevation_normal=10, on_press=lambda x: self.play_song_online())
        self.details_screen.add_widget(self.play_btn)
        self.details_screen.add_widget(MDIconButton(icon='arrow-collapse-down', user_font_size="30sp", theme_text_color= 'Secondary', pos_hint={'center_x':0.9, "center_y":0.15}, on_press=lambda x: self.download_bar()))
        try:
            self.dia.dismiss()
        except:
            pass

    def add_fav(self):
        if self.heart_icon.icon == 'heart-outline':
            self.heart_icon.icon = 'heart'
            self.heart_icon.theme_text_color = "Custom"
            self.heart_icon.text_color = (1,0,0,1)
            self.tap_target_view.start()
            #toast("Feature under development")

        elif self.heart_icon.icon == 'heart':
            #self.heart_icon.icon = 'heart-broken'
            self.heart_icon.icon = 'heart-outline'
            self.heart_icon.theme_text_color = 'Secondary'
            #self.heart_icon.text_color = self.theme_cls.text_color
            toast("Removed from Favorites")

    def change_screen(self, screen, *args):
        if self.root.ids.screen_manager.current == 'SongDetailsScreen' or self.root.ids.screen_manager.current == 'PlayScreen':
            try:
                self.stop()
            except:
                pass
        if args:
            self.root.ids.screen_manager.transition.direction = args[0]
            if args[0] != 'right':
                self.last_screen.append(self.root.ids.screen_manager.current)
                
        else:
            self.root.ids.screen_manager.transition.direction = 'left'
            self.last_screen.append(self.root.ids.screen_manager.current)
        self.root.ids.screen_manager.current = screen
    
    def back_screen(self):
        if self.root.ids.screen_manager.current != 'MainScreen':
            self.change_screen(self.last_screen[-1], 'right')
            self.last_screen.pop(-1)
    
    def cancel(self):
        self.download_progress.color = 1, 0, 0, 1
        self.status = False
        t3=threading.Thread(target=self.cancel2)
        t3.start()
    
    def cancel2(self):
        time.sleep(0.5)
        try:
            os.remove("{}/{} - {}.m4a".format(self.data_path, self.song_name, self.artist_name))
            print('removed')
        except:
            print('failed to remove')
            pass
        self.dia.dismiss()
        self.status=True

    def download_bar(self):
        self.download_progress = MDProgressBar(pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint_x = 0.8, value = 0, color = self.theme_cls.primary_color)
        self.dia = MDDialog(text='Downloading', buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color, on_press=lambda x: self.cancel())])
        #self.dia.add_widget(IconLeftWidget(icon='download', pos_hint={'center_x': .1, 'center_y': .1}))
        self.dia.add_widget(self.download_progress)
        self.dia.open()
        t2 = threading.Thread(target=self.download_song)
        t2.start()

    def play_song_online(self):
        self.fetch_thread.join()
        if self.sound:
            #print("Sound found at %s" % self.sound.source)
            #print("Sound is %.3f seconds" % self.sound.length)
            if self.play_status == 'pause' or self.play_status == 'stop':
                self.play_btn.icon = 'pause'
                self.play()
                lnth = self.sound.getDuration()
                t2 = threading.Thread(target=self.online_play_bar, args=(lnth,))
                t2.start()
            elif self.play_status == 'play':
                self.play_btn.icon = 'play'
                self.pause()
        else:
            time.sleep(0.5)
            self.play_song_online
    
    def online_play_bar(self, length, *args):
        while True:
            if length != 0:
                self.play_progress.value = 100*(self.sound.getCurrentPosition())/length
            #print(self.progress.value)
            time.sleep(1)
            self.play_stamp.text = self.convert_sec(self.sound.getCurrentPosition())
            if self.play_status == 'stop':
                break
            if self.play_stamp.text == self.length_stamp.text:
                self.play_song(args[0]+1)

    def play_song(self, i):
        try:
            self.stop()
        except:
            pass
        link = self.down_path_list[i][0]
        if self.root.ids.screen_manager.current != 'PlayScreen':
            self.change_screen("PlayScreen")
        self.prepare(link)
        if link.endswith('.m4a'):
            self.audio = MP4(link)
            self.play_song_name = self.audio.get('\xa9nam', ['Unknown'])[0]
            #print(audio['\xa9alb'])
            self.play_art_name = self.audio.get('\xa9ART',['Unknown'])[0]
            #print(audio['\xa9day'])
            #print(audio['\xa9gen'])
            try:
                self.img_data = self.audio["covr"][0]
            except:
                with open('cover.jpg', 'rb') as f:
                    self.img_data = f.read()
        elif link.endswith('.mp3'):
            self.audio = MP3(link, ID3=EasyID3)
            self.audio_tags = ID3(link)
            self.play_song_name = self.audio.get('title', ['Unknown'])[0]
            self.play_art_name = self.audio.get('artist',['Unknown'])[0]
            try:
                self.img_data = self.audio_tags.get("APIC:").data
            except:
                with open('cover.jpg', 'rb') as f:
                    self.img_data = f.read()
        else:
            with open('cover.jpg', 'rb') as f:
                self.img_data = f.read()
                self.play_song_name = 'Unknown'
                self.play_art_name = 'Unknown'
        
        play_image_data = io.BytesIO(self.img_data)
        img=CoreImage(play_image_data, ext="jpg").texture
        song_image= Image(allow_stretch=True)
        song_image.texture= img
        self.root.ids.PlayScreen.clear_widgets()
        self.root.ids.PlayScreen.add_widget(MDIconButton(icon='chevron-left', pos_hint={"center_x":0.05, "center_y":0.95}, on_press=lambda x: self.back_screen()))
        card = MDCard(orientation='vertical', pos_hint={"center_x":0.5, "center_y":0.65}, size_hint=(None, None), size=(self.win_size*0.9, self.win_size*0.9))
        card.add_widget(song_image)
        self.root.ids.PlayScreen.add_widget(card)
        self.root.ids.PlayScreen.add_widget(MDLabel(text=self.play_song_name, halign='center', theme_text_color='Custom', text_color=self.theme_cls.primary_color, font_style='H4', bold=True, pos_hint={"top":0.84}))
        self.root.ids.PlayScreen.add_widget(MDLabel(text=self.play_art_name, halign='center', theme_text_color='Secondary', font_style='H6', pos_hint={"top":0.8}))
        self.play_progress = MDProgressBar(pos_hint = {'center_x':0.5, 'center_y':0.25}, size_hint_x = 0.9, value = 0, color = self.theme_cls.primary_color)
        self.root.ids.PlayScreen.add_widget(self.play_progress)
        self.root.ids.PlayScreen.add_widget(MDIconButton(icon="chevron-double-left", pos_hint={"center_x": .15, "center_y": .15}, user_font_size="40sp", on_release=lambda x: self.rewind()))
        self.root.ids.PlayScreen.add_widget(MDIconButton(icon="chevron-double-right", pos_hint={"center_x": .85, "center_y": .15}, user_font_size="40sp", on_release=lambda x: self.forward()))
        self.next_button = MDIconButton(icon="skip-next", pos_hint={"center_x": .65, "center_y": .15}, user_font_size="55sp", on_release=lambda x: self.play_song(i+1))
        self.root.ids.PlayScreen.add_widget(self.next_button)
        self.previous_button = (MDIconButton(icon="skip-previous", pos_hint={"center_x": .35, "center_y": .15}, user_font_size="55sp", on_release=lambda x: self.play_song(i-1)))
        self.root.ids.PlayScreen.add_widget(self.previous_button)
        self.play_btn = MDFloatingActionButton(icon='play', pos_hint={'center_x':0.5, "center_y":0.15}, user_font_size="50sp", md_bg_color=(1,1,1,1), elevation_normal=10, on_press=lambda x: self.play_song_offline(i))
        self.root.ids.PlayScreen.add_widget(self.play_btn)
        self.length_stamp = MDLabel(text=self.convert_sec(self.sound.getDuration()), halign='right', theme_text_color='Secondary', padding_x='20dp', pos_hint={"top":0.725})
        self.root.ids.PlayScreen.add_widget(self.length_stamp)
        self.play_stamp = (MDLabel(text=self.convert_sec(self.sound.getCurrentPosition()), halign='left', theme_text_color='Secondary', padding_x='20dp', pos_hint={"top":0.725}))
        self.root.ids.PlayScreen.add_widget(self.play_stamp)
        self.play_song_offline(i)

            
    def play_song_offline(self, i):
        if True:
            if self.play_status == 'pause' or self.play_status == 'stop':
                self.play_btn.icon = 'pause'
                self.play()
                lnth = self.sound.getDuration()
                t2 = threading.Thread(target=self.online_play_bar, args=(lnth,i))
                t2.start()
            elif self.play_status == 'play':
                self.play_btn.icon = 'play'
                self.pause()
        else:
            time.sleep(0.5)
            self.play_song_offline

    def convert_sec(self, lnth):
        lnth = lnth/1000
        try:
            if int(lnth-(60*(lnth//60))) < 10:
                return("{}:0{}".format(int(lnth//60), int(lnth-(60*(lnth//60)))))
            else:
                return("{}:{}".format(int(lnth//60), int(lnth-(60*(lnth//60)))))
        except:
            print('Error: Length is {}'.format(lnth))

    def prepare(self, link):
        print('preparing')
        try:
            self.sound = MediaPlayer()
            self.sound.setDataSource(link)
            self.sound.prepare()
            self.sound.setLooping(False)
        except Exception as e:
            print(e)
            time.sleep(0.25)
            self.prepare(link)
        print('prepared')
    def play(self):
        self.sound.start()
        self.play_status = 'play'
    def pause(self):
        self.sound.pause()
        self.play_status = 'pause'
    def stop(self):
        self.sound.stop()
        self.sound.release()
        self.play_status = 'stop'
    def forward(self):
        self.sound.seekTo(self.sound.getCurrentPosition() + 5000)
    def rewind(self):
        self.sound.seekTo(self.sound.getCurrentPosition() - 5000)
    
    def callback_for_about(self, *args):
        toast('Opening ' + args[0])
        webbrowser.open_new(args[0])
            
    def contact_us(self):
        bottom_sheet_menu = MDGridBottomSheet(radius=15,radius_from='top')
        data = [
            {"name":"Telegram", "icon":"telegram", "link":"https://t.me/sangwan5688"},
            {"name":"Instagram", "icon":"instagram", "link":"https://www.instagram.com/sangwan5688/"},
            {"name":"Twitter", "icon":"twitter", "link":"https://twitter.com/sangwan5688"},
            {"name":"Mail", "icon":"gmail", "link":"https://mail.google.com/mail/?view=cm&fs=1&to=blackholeyoucantescape@gmail.com&su=Regarding+Mobile+App"},
            {"name":"Facebook", "icon":"facebook", "link":"https://www.facebook.com/ankit.sangwan.5688"},
        ]
        for item in data:
            bottom_sheet_menu.add_item(
                item["name"],
                lambda x, y=item["link"]: self.callback_for_about(y),
                icon_src=item["icon"],
            )
        bottom_sheet_menu.open()

    def download_song(self):
        if self.status:
            print('started downloading song')
            fname = "{}/{} - {}.m4a".format(self.data_path, self.song_name, self.artist_name)
            #self.download_bar()
            with requests.get(self.song_dwn_url, stream=True) as r, open(fname, "wb") as f:
                file_size = int(r.headers['Content-Length'])
                total= int(file_size / 1024)
                self.dia.add_widget(MDLabel(text='{:.2f} MB'.format(file_size/(1024*1024)), halign='right'))
                for chunk in r.iter_content(chunk_size=1024):
                    if self.status:
                        f.write(chunk)
                        self.download_progress.value += 100/total
                    else:
                        #print('Download cancelled')
                        break
            print('finished downloading song')
        if self.status:
            self.save_metadata()

    def save_metadata(self):
        with open(self.image_path, 'wb') as f:
            f.write(requests.get(self.image_url).content)
        print('getting metadata')
        audio_path = os.path.join(self.data_path, "{} - {}.m4a".format(self.song_name, self.artist_name))
        audio = MP4(audio_path)
        audio['\xa9nam'] = self.song_name
        audio['\xa9alb'] = self.album
        audio['aART'] = self.artist_name
        if self.featured_artist != '':
            audio['\xa9ART'] = self.artist_name + ", " + self.featured_artist
        else:
            audio['\xa9ART'] = self.artist_name
        audio['\xa9day'] = self.year
        audio['\xa9gen'] = self.genre
        with open(os.path.join(self.data_path, self.song_id+'.jpg'), "rb") as f:
            audio["covr"] = [
                MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]
        audio.save()
        shutil.move(audio_path, audio_path.replace(self.data_path, self.path))
        print('finished getting metadata')
        #close_btn = MDFlatButton(text="OK", on_release=self.close_dialog)
        self.dia.dismiss()
        os.remove(os.path.join(self.data_path, self.song_id+'.jpg'))
        close_btn = MDIconButton(icon='checkbox-marked-circle-outline', theme_text_color="Custom", text_color=self.theme_cls.primary_color, on_release=self.close_dialog)
        self.dia = MDDialog(title="Download Complete", text="Song Downloaded Successfully!", size_hint=(0.7,1), buttons=[close_btn])
        self.dia.open()
        #notification.notify(self.song_name +' by '+ self.artist_name, "Download complete")
        #toast("Song Downloaded Successfully!")

    def set_nav_color(self, item):
        for child in self.root.ids.nav_list.children:
            #if child.text_color == self.theme_cls.primary_color:
            #    child.text_color = self.theme_cls.text_color
            #    break
            if child.text == item:
                child.text_color = self.theme_cls.primary_color
                break
                
        

    def file_manager_open(self):
        self.file_manager.show(self.path)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        if os.path.isdir(path):
            self.path = path
            toast("Songs will be downloaded to: "+path)
            self.user_data.put('download_path', path=self.path)
        else:
            toast("No directory selected")

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        #print(keyboard)
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
            else:
                self.back_screen()
        if keyboard == 13:
            if self.root.ids.screen_manager.current == 'MainScreen':
                self.show_data(self.root.ids.song_name.text)
            else:
                pass
        return True

    def close_dialog(self, obj):
        self.dia.dismiss()

if __name__ == '__main__':
    MyApp().run()
