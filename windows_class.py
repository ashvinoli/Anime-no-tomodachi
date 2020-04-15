from tkinter import *
from tkinter import messagebox

class windows:
    def __init__(self,title="Unnamed Window",geometry="800x800"):
        self.window = Tk()
        windowWidth = self.window.winfo_reqwidth()
        windowHeight = self.window.winfo_reqheight()
        positionRight = int(self.window.winfo_screenwidth()/2 - windowWidth*2)
        positionDown = int(self.window.winfo_screenheight()/2 - windowHeight)
        self.window.geometry("+{}+{}".format(positionRight, positionDown))
        self.window.title(title)
        self.window.geometry(geometry)
        self.threads = {}
        self.define_widgets()
        self.pack_widgets()
        self.assign_functions()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

        
    def define_widgets(self):
        self.define_frames()
        self.define_labels()
        self.define_buttons()
        self.define_entries()
        self.define_radio_buttons()
        self.define_sliders()
        self.define_check_buttons()
        self.define_drop_down_boxes()
        self.define_list_boxes()
        self.define_scroll_bars()
        
    def pack_widgets(self):
        self.pack_frames()
        self.pack_buttons()
        self.pack_labels()
        self.pack_entries()
        self.pack_radio_buttons()
        self.pack_sliders()
        self.pack_check_buttons()
        self.pack_drop_down_boxes()
        self.pack_list_boxes()
        self.pack_scroll_bars()

    def on_closing(self):
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #   self.window.destroy()
        self.window.destroy()
        
    def assign_functions(self):
        pass
    
    #Widgets definition
    ##########################################################################
    
    #Advantages of Frames: You can PACK things in your main window and GRID in your frames
    def define_frames(self):
        pass

    def pack_frames(self):
        pass
    
    def define_labels(self):
        pass

    def pack_labels(self):
        pass
    
    def define_buttons(self):
        pass

    def pack_buttons(self):
        pass

    def define_entries(self):
        pass

    def pack_entries(self):
        pass

    #In python radio_buttons are associated with variables. Clicking a particular radio-button changes the value of that variable. The value is assigned during radio button definition. For all radio buttons which share the same variables only one of them can be checked which makes sense.
    def define_radio_buttons(self):
        pass

    def pack_radio_buttons(self):
        pass

    #Sliders are actually "Scale" in Tkinter
    def define_sliders(self):
        pass
    
    def pack_sliders(self):
        pass

    def define_scroll_bars(self):
        pass
    
    def pack_scroll_bars(self):
        pass
    

    def define_check_buttons(self):
        pass
    
    def pack_check_buttons(self):
        pass    

    #Drop down boxes are "OptionMenu" in tkinter
    def define_drop_down_boxes(self):
        pass
    
    def pack_drop_down_boxes(self):
        pass    

    #Listboxes are "Listbox" in tkinter
    def define_list_boxes(self):
        pass

    def pack_list_boxes(self):
        pass
