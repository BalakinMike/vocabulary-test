import PySimpleGUI as sg
import json

rightclick = ['&Edit', ['&Copy','&Paste']]
menu_def = [['&File', ['&Open', '&Save', 'E&xit', ]], ['Edit', ['Copy', 'Paste'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
left_column = sg.Column([[sg.Text('Creating dictionary', font='Any 18')],
                         [sg.Text("Open dictionary:"), sg.Input(size=(25, 1), enable_events=True, key="-UPFILE-"),
                            sg.FileBrowse('Browse'),],
                         [sg.Text("Create dictionary:"), sg.Input(size=(25, 1), enable_events=True, key="-CRFILE-"),
                            sg.Button('Create', key="-CRBUT-"), ],
                         [sg.Text('Input russian word'), sg.Input(),], 
                         [sg.Text('Input english word'), sg.Input(),]])
right_column = sg.Column([[sg.Text('Run test', font='Any 18')],
                          [sg.Text("Searching dictionary:"),
                            sg.Input(size=(25, 1), enable_events=True, key="-FILE-"),
                            sg.FileBrowse('Browse'),],
                            [sg.Text('See RUSSIAN word'), sg.Multiline("", key='-OUT-', text_color='red', font=("BoldArial", 14),)], 
                            [sg.Text('Input ENGLISH translation'), sg.Input(),],
                            [sg.Button('Check', key='-CHECK-', expand_x=True)],])
layout = [[left_column, sg.VerticalSeparator(), right_column],         
          
]

window = sg.Window("VOCABULARY TEST", layout, right_click_menu=rightclick, finalize=True)

while True:
   event, values = window.read()
    
   if event == "Exit" or event == sg.WIN_CLOSED:
      break

   print(values)
    
   
   