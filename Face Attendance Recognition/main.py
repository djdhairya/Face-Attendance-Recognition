import tkinter as tk
import os.path
import datetime
import pickle
from PIL import Image, ImageTk
import face_recognition
import cv2
import subprocess
import util



class App:
    def __init__(self):
        self.main_window=tk.Tk()
        self.main_window.geometry("1200x520+250+100")
        
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)       
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path="C:/Users/Dhairya Hindoriya/OneDrive/Desktop/Face Attendance Recognition/log.txt"    
        
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)
    
    def login(self):
        unknown_students_path = "C:/Users/Dhairya Hindoriya/OneDrive/Desktop/Face Attendance Recognition/db/tmp.jpg"       
        img = cv2.imread(unknown_students_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tmp_path = './db/tmp_rgb.jpg'
        cv2.imwrite(tmp_path, rgb_img)
        output=str(subprocess.check_output(['face_recognition',self.db_dir,unknown_students_path]))
        name=output.split(',')[1][:-3]
        if name in ['unknown_person','no_persons_found']:
            util.msg_box('Ups...','Unknown student.Pls register new user or Try Again')
        else:
            util.msg_box('Welcome Back!','Welcome,{}.'.format(name))
            with open(self.log_path, 'a') as f:
                try:
                    f.write('{},{}\n'.format(name, datetime.datetime.now()))
                    print(f"Log file created at: {os.path.abspath(self.log_path)}")
                except Exception as e:
                    print(f"Error writing to log file: {e}")    
    
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+270+20")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)
        self.register_new_user_capture = self.most_recent_capture_arr

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please,Input Username:')
        self.text_label_register_new_user.place(x=750, y=70)
    
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    
    def start(self):
        self.main_window.mainloop()    
    
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]
        file = open(os.path.join(self.db_dir, '{}.jpg'.format(name)), 'wb')
        pickle.dump(embeddings, file)
        util.msg_box('Success!', 'User was registered successfully !')
        self.register_new_user_window.destroy()                           
if __name__=="__main__":
    app=App()
    app.start()
        