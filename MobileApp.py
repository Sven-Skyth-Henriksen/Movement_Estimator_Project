from kivymd.app import MDApp 
from kivy.lang import Builder
from kivy.core.window import  Window
import os
from playsound import playsound

Window.size = (300,500) 



class FitnessApp(MDApp):
	def build(self):
		self.theme_cls.theme_style='Light'
		self.theme_cls.primary_palette = 'Orange'
		return Builder.load_file('MobileApp.kv')

	def load_shoulder_press(self):
		os.system('python shoulder_press.py')
		
	def load_curl(self):
		os.system('python curl.py')
	
	



if __name__ == '__main__':
	FitnessApp().run()
