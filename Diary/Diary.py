import Database
import kivy 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.core.window import Window
from kivy.properties import StringProperty
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex

Window.size =  (500, 600)
Window.minimum_width = 500
Window.minimum_height = 600
class MainScreen(Screen):
    pass
class Signup(Screen):
    username = ObjectProperty(None)
    invisible = ObjectProperty(None)
    invis = ObjectProperty(None)
   #----------------------------------- 
    passw = ObjectProperty(None)
    password = ObjectProperty(None)
    passwo = ObjectProperty(None) 
   #----------------------------------- 
    verify = ObjectProperty(None)
    verifying = ObjectProperty(None)
   #-----------------------------------
    exist = ObjectProperty(None)
    
    username_ok = False
    password_ok = False
    verify_ok = False
    
    def Username(self):
        if 0 < len(self.username.text) <= 2:
            self.invisible.opacity = 1
            self.invis.opacity = 0
            self.username_ok = False
        elif len(self.username.text) == 0:
            self.invisible.opacity = 0
            self.invis.opacity = 1
            self.username_ok = False
        else:
            self.invisible.opacity = 0
            self.invis.opacity = 0
            self.username_ok = True 
    def Password(self):
        if 0 < len(self.password.text) <= 7:
            self.passwo.opacity = 1
            self.passw.opacity= 0
            self.password_ok = False
        elif len(self.password.text) == 0:
            self.passwo.opacity = 0
            self.passw.opacity= 1
            self.password_ok = False
        else:
            self.passwo.opacity = 0
            self.passw.opacity= 0
            self.password_ok = True
    def VerifyPassword(self):
        if self.password.text != self.verify.text:
            self.verifying.opacity = 1
            self.verify_ok = False
        elif self.password.text == self.verify.text:
            self.verifying.opacity = 0
            self.verify_ok = True
    def GetStarted(self):
        self.Password()
        self.VerifyPassword()
        self.Username()
        existing = Database.get_user(self.username.text)
        if (self.verify_ok == True and
            self.username_ok == True and
            self.password_ok == True and 
            existing is None):
                self.manager.transition.direction = "left"
                self.manager.current = "DiaryScreen"

                for w in ["invisible", "invis", "passw", "passwo", "verifying"]:
                    self.ids[w].opacity = 0
                
                Database.add_user(self.username.text, self.password.text)
                new_user = Database.get_user(self.username.text)
                App.get_running_app().current_user_id = new_user[0]
                self.exist.opacity = 0
        elif existing != None:
            self.exist.opacity = 1
        else:
            return
            

class Signin(Screen):
    
    username = ObjectProperty(None)
    invisible1 = ObjectProperty(None)
    invis1 = ObjectProperty(None)
   #--------------------------------------
    password = ObjectProperty(None)
    passw1 = ObjectProperty(None)
    passwo1 = ObjectProperty(None)
   #--------------------------------------
    exist = ObjectProperty(None)
    passwordcheck = ObjectProperty(None)

    username_ok1 = False
    password_ok1 = False
    
    def Username(self):
        if 0 < len(self.username.text) <= 2:
            self.invisible1.opacity = 1
            self.invis1.opacity = 0
            self.username_ok1 = False
        elif len(self.username.text) == 0:
            self.invisible1.opacity = 0
            self.invis1.opacity = 1
            self.username_ok1 = False
        else:
            self.invisible1.opacity = 0
            self.invis1.opacity = 0
            self.username_ok1 = True 
    def Password(self):
        if 0 < len(self.password.text) <= 7:
            self.passwo1.opacity = 1
            self.passw1.opacity= 0
            self.password_ok1 = False
        elif len(self.password.text) == 0:
            self.passwo1.opacity = 0
            self.passw1.opacity= 1
            self.password_ok1 = False
        else:
            self.passwo1.opacity = 0
            self.passw1.opacity= 0
            self.password_ok1 = True
    def GetStarted(self):
        self.Password()
        self.Username()
        existing = Database.get_user(self.username.text)
        if (self.username_ok1 == True and
            self.password_ok1 == True and
            existing != None):
                for w in ["invisible1", "invis1", "passw1", "passwo1"]:
                    self.ids[w].opacity = 0
                self.exist.opacity = 0
                if existing[2] == self.password.text:
                    self.manager.transition.direction = "left"
                    self.manager.current = "DiaryScreen"
                    self.passwordcheck.opacity = 0
                    App.get_running_app().current_user_id = existing[0]
                elif (existing[2] != self.password.text and
                      not (0 < len(self.password.text) <= 7)and
                      len(self.password.text) != 0):
                    self.passwordcheck.opacity = 1
        elif  (existing == None and
               len(self.username.text) != 0 and
               not (0 < len(self.username.text) <= 2)):
            self.exist.opacity = 1
            return
        else:
            return
        
class DiaryScreen(Screen):
    page_number = ObjectProperty(None)
    
    def on_enter(self):

        manager = self.ids.pagemanager
        user_id = App.get_running_app().current_user_id
        if manager.screen_names:
            return  
        pages = Database.get_pages(user_id)

        if pages:
            for i, (date, text) in enumerate(pages, start=1):
                page = DiaryPage(
                    name=f"page_{i}",
                    date=date,
                    content=text
                )
                manager.add_widget(page)

            manager.current = f"page_{i}"
            self.page_number.text = f"Page: {i}"

        else:
            today = datetime.now().strftime("%d/%m/%Y")
            first_page = DiaryPage(
                name="page_1",
                date=today,
                content=""
            )
            manager.add_widget(first_page)
            manager.current = "page_1"
            self.page_number.text = "Page: 1"

    def save_and_nextpage(self):
        manager = self.ids.pagemanager
        current = manager.current_screen
        current_name = manager.current

        current_num = int(current_name.split("_")[1])
        total_num = len(manager.screen_names)
        if current_num < total_num:
            manager.transition.direction = "left"
            manager.current = f"page_{current_num + 1}"
            self.page_number.text = f"Page: {current_num + 1}"
            return
        else:
            today = datetime.now().strftime("%d/%m/%Y")
            new_name = f"page_{total_num + 1}" 

            self.page_number.text = f"Page: {total_num + 1}"

            new_page = DiaryPage(
                name=new_name,
                date=today,
                content=""
            )
            manager.add_widget(new_page)
            manager.transition.direction = "left"
            manager.current = new_name

    def previous_page(self):
        manager = self.ids.pagemanager
        current_name = manager.current
        current_num = int(current_name.split("_")[1])
        if not current_name.startswith("page_"):
            return
        number = int(current_name.split("_")[1])
        if number <= 1:
            return
        self.page_number.text = f"Page: {current_num - 1}"
        prev_name = f"page_{number - 1}"
        manager.transition.direction = "right"
        manager.current = prev_name
    def save_the_page(self):
    
        manager = self.ids.pagemanager
        current_page = manager.current_screen

        user_id = App.get_running_app().current_user_id   
        content = current_page.content
        date = current_page.date
        page_number = int(manager.current.split("_")[1])

        exists = Database.page_exists(user_id, page_number)

        try:
            if exists is None:
                Database.add_data(user_id, content, date)
                print("New Page Added (INSERT).")
            else:
                Database.update_page(user_id, page_number, content, date)
                print("Current Page Updated (UPDATE).")
        except Exception as e:
            print("An Error Occured While Trying To Save:", e)
    def logout(self):
        app = App.get_running_app()
        app.current_user_id = None
        diary_screen = self.manager.get_screen("DiaryScreen")
        diary_screen.ids.pagemanager.clear_widgets()
       #---------------------------------------------
        signin = self.manager.get_screen("Signin")
        signin.username.text = ""
        signin.password.text = ""
       #---------------------------------------------
        signup = self.manager.get_screen("Signup")
        signup.username.text = ""
        signup.password.text = ""
        signup.verify.text = ""

class GoToPagePopup(Popup):
    def go_to_page(self, num):
        app = App.get_running_app()
        manager = app.root  
        manager.go_to_page(num)
        self.dismiss()
class DiaryPage(Screen):
    date = StringProperty("")
    content = StringProperty("")
    def open_popup(self):
        GoToPagePopup().open()
class DiaryManager(ScreenManager):
     def go_to_page(self, num):
        try:
            num = int(num)
        except:
            return
        diary_screen = self.get_screen("DiaryScreen")
        manager = diary_screen.ids.pagemanager
        pages = manager.screen_names  
        if num < 1 or num > len(pages):
            return  
        target = pages[num - 1] 
        manager.transition.direction = "left"
        manager.current = target
        diary_screen.page_number.text = f"Page: {num}"
class Diary(App):
    def build(self):
        return Builder.load_file("Notes.kv")
    
    
if __name__ == '__main__':
    Diary().run()