from tkinter import filedialog as _filedialog
import tkinter as _tk
from typing import Callable as _Callable
from simpleworkspace.utility import strings as _strings

class _TK_BaseDialog():
    _style_colors_background = "#E9ECED"
    _style_colors_foreground = "black"
    _style_colors_button_foreground = _style_colors_foreground
    _style_colors_button_background = "#CFD4D9"
    _style_fonts_helvetica_9 = "Helvetica 9"
    _style_fonts_helvetica_10 = "Helvetica 10"
    _style_fonts_paragraph = _style_fonts_helvetica_10
    _style_fonts_button = _style_fonts_helvetica_9

    def __init__(self):
        self._state_AppDestroyed = False
        self.Settings_Window_TopMost = False
        self.Settings_Window_Title:str = None
        self.root = _tk.Tk()

    def _Application_Mapper(self):
        if self.Settings_Window_TopMost:
            self.root.wm_attributes("-topmost", 1)
        if self.Settings_Window_Title:
            self.root.title(self.Settings_Window_Title)
        self.root.configure(background=self._style_colors_background)

        def OnDestroyed_Window(event:_tk.Event):
            self._state_AppDestroyed = True
        self.root.bind("<Destroy>", OnDestroyed_Window)  # it might get destroyed by tk itself when closing from taskbar etc

    def _Application_Run(self):
        self._Application_Mapper()
        self._CenterWindow()
        self.root.mainloop()

    def _CenterWindow(self):
        self.root.withdraw() # Remain invisible while we figure out the geometry
        self.root.update_idletasks() # Actualize geometry information

        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

        self.root.deiconify() # Become visible at the desired location

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if not self._state_AppDestroyed:
            self.root.destroy()

    def _AddEventHandler_OnLoad(self, widget: _tk.Widget, callback: _Callable[[_tk.Event], None]):
        def WrappedCallback(*args):
            callback(*args)
            widget.unbind('<Map>', eventId)

        eventId = widget.bind('<Map>', WrappedCallback, add='+')

class MessageBox(_TK_BaseDialog):
    def __init__(self):
        super().__init__()
        self.Settings_Message = ""
        self.Settings_Window_Title = "Information"
        self.Settings_Message_MaxLinesUntilScroll = 7

    def _Application_Mapper(self):
        super()._Application_Mapper()

        textbox_frame = _tk.Frame(self.root, bg=self._style_colors_background) #to later support scrollbar
        textbox = _tk.Text(
            textbox_frame,
            borderwidth=0,
            height=4,
            width=60,
            wrap=_tk.WORD,
            bg=self._style_colors_background,
            fg=self._style_colors_foreground,
            font=self._style_fonts_paragraph,
        )
    
        def OnLoad_Textbox(event: _tk.Event):
            widget: _tk.Text = event.widget

            widget.tag_configure("center", justify="center")
            widget.insert(_tk.INSERT, self.Settings_Message, "center")

            displayLines = widget.count("1.0", "end", "displaylines")[0]
            if displayLines > self.Settings_Message_MaxLinesUntilScroll:
                displayLines = self.Settings_Message_MaxLinesUntilScroll
                scrollbar = _tk.Scrollbar(widget.master)
                scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
                widget.configure(yscrollcommand=scrollbar.set)

            widget.configure(height=displayLines, state=_tk.DISABLED)
            return

        self._AddEventHandler_OnLoad(textbox, OnLoad_Textbox)
        if not (_strings.IsNullOrEmpty(self.Settings_Message)): #if empty message skip rendering message
            textbox.pack(side=_tk.LEFT, fill=_tk.BOTH, expand=True)
            textbox_frame.pack(fill=_tk.X, padx=10, pady=5)

        frame_belowMessage = _tk.Frame(self.root, bg=self._style_colors_background)
        self._LowerFrame_Mapper(frame_belowMessage)
        frame_belowMessage.pack(side=_tk.BOTTOM, fill=_tk.BOTH, expand=True, padx=10)

    def _LowerFrame_Mapper(self, frame: _tk.Frame):
        ok_button = _tk.Button(
            frame,
            text="OK",
            font=self._style_fonts_button,
            bg=self._style_colors_button_background,
            fg=self._style_colors_button_foreground,
            padx=35,
            command=self.root.destroy,
        )
        ok_button.pack(side=_tk.BOTTOM, pady=(5, 10))
        ok_button.focus()

    @classmethod
    def Show(cls, message: str, windowTitle: str = None, windowTopMost=False):
        with cls() as app:
            app.Settings_Message = message
            app.Settings_Window_Title = windowTitle
            app.Settings_Window_TopMost = windowTopMost
            app._Application_Run()

class ConfirmationBox(MessageBox):
    def __init__(self):
        super().__init__()
        self.Settings_Window_Title = "Confirmation Dialog"
        self.dialogResult = False
        """defaults to false, is only true if yes button is pressed"""

    def _LowerFrame_Mapper(self, frame: _tk.Frame):
        def OnClick_AnswerBtn(answer: bool):
            self.dialogResult = answer
            self.root.destroy()

        yes_button = _tk.Button(
            frame,
            text="Yes",
            font=self._style_fonts_button,
            bg=self._style_colors_button_background,
            fg=self._style_colors_button_foreground,
            padx=35,
            command=lambda: OnClick_AnswerBtn(True),
        )
        no_button = _tk.Button(
            frame,
            text="No",
            font=self._style_fonts_button,
            bg=self._style_colors_button_background,
            fg=self._style_colors_button_foreground,
            padx=35,
            command=lambda: OnClick_AnswerBtn(False),
        )

        no_button.pack(side=_tk.LEFT, anchor=_tk.SE, expand=True, pady=(5, 10), padx=5)
        yes_button.pack(side=_tk.RIGHT, anchor=_tk.SW, expand=True, pady=(5, 10), padx=5)

    @classmethod
    def Show(cls, message: str, windowTitle: str = None, windowTopMost=False):
        '''Displays a messagebox containing a question with a yes or no button'''
        with cls() as app:
            app.Settings_Message = message
            app.Settings_Window_Title = windowTitle
            app.Settings_Window_TopMost = windowTopMost
            app._Application_Run()
            return app.dialogResult

class InputBox(MessageBox):
    def __init__(self):
        super().__init__()
        self.Settings_Window_Title = "Input Dialog"
        self.Settings_InitialValue = ''
        self.dialogResult: None | str = None

    def _LowerFrame_Mapper(self, frame: _tk.Frame):
        textBox = _tk.Entry(
            frame,
            font=self._style_fonts_paragraph
        )

        if self.Settings_InitialValue:
            textBox.insert(0, self.Settings_InitialValue)

        def OnClick_BtnOk(event:_tk.Event):
            self.dialogResult = textBox.get()
            self.root.destroy()

        btn_ok = _tk.Button(
            frame,
            text="Ok",
            font=self._style_fonts_helvetica_9,
            bg=self._style_colors_button_background,
            fg=self._style_colors_button_foreground,
            padx=35,
        )

        textBox.pack(side=_tk.LEFT, anchor=_tk.S, fill=_tk.X, expand=True, pady=(5, 13))
        btn_ok.pack(side=_tk.RIGHT, anchor=_tk.S, pady=(5, 10), padx=(5,0))
        textBox.focus()
        btn_ok.bind("<Button-1>", OnClick_BtnOk)
        textBox.bind("<Return>", OnClick_BtnOk)

    @classmethod
    def Show(cls, message: str, windowTitle: str = None, windowTopMost=False, initialValue:str = None):
        '''
        Asks user for a string input
        :param initalValue: A preentered default input text visible to user when prompt is displayed
        :returns: the input string, if window is closed then None
        '''
        with cls() as app:
            app.Settings_Message = message
            app.Settings_InitialValue = initialValue
            app.Settings_Window_Title = windowTitle
            app.Settings_Window_TopMost = windowTopMost
            app._Application_Run()
            return app.dialogResult

class InputBoxLarge(InputBox):
    def _LowerFrame_Mapper(self, frame: _tk.Frame):
        textbox_frame = _tk.Frame(self.root, bg=self._style_colors_background) #to support scrollbar
        xScrollbar = _tk.Scrollbar(textbox_frame, orient=_tk.HORIZONTAL) 
        yScrollbar = _tk.Scrollbar(textbox_frame, orient=_tk.VERTICAL)
        textBox = _tk.Text(
            textbox_frame,
            font=self._style_fonts_paragraph,
            xscrollcommand=xScrollbar.set,
            yscrollcommand=yScrollbar.set,
            wrap=_tk.NONE
        )

        if self.Settings_InitialValue:
            textBox.insert(_tk.INSERT, self.Settings_InitialValue)

        xScrollbar.pack(side=_tk.BOTTOM, fill=_tk.X)
        yScrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
        textBox.pack(side=_tk.LEFT, fill=_tk.BOTH, expand=True, pady=5)
        textbox_frame.pack(fill=_tk.X)

        def OnClick_BtnOk(*args):
            self.dialogResult = textBox.get("1.0",'end-1c')
            self.root.destroy()

        btn_ok = _tk.Button(
            frame,
            text="Ok",
            font=self._style_fonts_helvetica_9,
            bg=self._style_colors_button_background,
            fg=self._style_colors_button_foreground,
            padx=35,
            command=OnClick_BtnOk,
        )

        btn_ok.pack(side=_tk.BOTTOM,pady=(5, 10), padx=(5,0))
        textBox.focus()
        textBox.bind("<Return>", OnClick_BtnOk)

class ButtonPanel(MessageBox):
    def __init__(self, buttonMappings: dict[str, _Callable[[_tk.Event], None]]):
        super().__init__()
        self._Settings_Buttons = {}
        self.Settings_Window_Title = "Menu"
        self.Settings_Grid_MaxItemsPerRow = 4
        self.Settings_CloseWindowAfterAction = True
        self.Settings_ButtonMappings = buttonMappings

    def _LowerFrame_Mapper(self, frame: _tk.Frame):
        subFrame = _tk.Frame(frame, bg=self._style_colors_background)
        row, col = 0, 0
        for btnName, action in self.Settings_ButtonMappings.items():
            btn = _tk.Button(
                subFrame,
                text=btnName,
                font=self._style_fonts_button,
                bg=self._style_colors_button_background,
                fg=self._style_colors_button_foreground,
                padx=25,
                pady=10
            )
            def WrappedCallback(event, action=action): #capture current instance of btnOptions
                action(event)
                if(self.Settings_CloseWindowAfterAction):
                    self.root.destroy()
            btn.bind('<Button-1>', WrappedCallback)
            btn.grid(row=row, column=col, pady=5, padx=5)
            
            subFrame.columnconfigure(col, weight=1)
            col += 1
            if(col % self.Settings_Grid_MaxItemsPerRow == 0):
                subFrame.rowconfigure(row, weight=1)
                col = 0
                row += 1
        subFrame.pack(fill=_tk.BOTH,expand=True, padx=20, pady=20)

    @classmethod
    def Show(cls, buttonMappings:dict[str, _Callable[[_tk.Event], None]], message: str = "", windowTitle: str = None, windowTopMost=False):
        '''
        Asks user for a string input
        :param initalValue: A preentered default input text visible to user when prompt is displayed
        :returns: the input string, if window is closed then None
        '''
        with cls(buttonMappings) as app:
            app.Settings_Message = message
            app.Settings_Window_Title = windowTitle
            app.Settings_Window_TopMost = windowTopMost
            app._Application_Run()
        
#only reason to use parent as custom tkdialog is to add icon to taskbar and being able to set topmost attribute
class FileDialog:
    @staticmethod
    def Show(multiple=False, initialDir:str=None, windowTitle:str=None, windowTopMost=False):
        with _TK_BaseDialog() as app:
            app.Settings_Window_TopMost = windowTopMost
            app.root.attributes('-alpha', 0.0)  #makes the root windows invisible if it were to be reopened
            app.root.iconify()                  #minimizes the root windows
            if(multiple):
                res = tuple(_filedialog.askopenfilenames(initialdir=initialDir, title=windowTitle, parent=app.root))
            else:
                res = _filedialog.askopenfilename(initialdir=initialDir, title=windowTitle, parent=app.root)
            return res if res != '' else None

class DirectoryDialog:
    @staticmethod
    def Show(initialDir:str=None, windowTitle:str=None, windowTopMost=False):
        with _TK_BaseDialog() as app:
            app.Settings_Window_TopMost = windowTopMost
            app.root.attributes('-alpha', 0.0)  #makes the root windows invisible if it were to be reopened
            app.root.iconify()                  #minimizes the root windows
            res = _filedialog.askdirectory(initialdir=initialDir, title=windowTitle, parent=app.root)
            return res if res != '' else None
