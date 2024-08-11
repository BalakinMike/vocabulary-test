import PySimpleGUI as sg
import json

def vocabulary_write(vocabulary, words):
   
   with open(vocabulary, 'w', encoding='utf-8') as voc:
      json.dump(words, voc, ensure_ascii=False, indent=4)

def vocabulary_read(vocabulary):
   with open('vocab.json', encoding='utf-8') as voc:
    data = json.load(voc)
    key_list = list(data.keys())
    return key_list[0], data[key_list[0]]

rightclick = ['&Edit', ['&Copy','&Paste']]
menu_def = [['&File', ['&Open', '&Save', 'E&xit', ]], ['Edit', ['Copy', 'Paste'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
left_column = sg.Column([[sg.Text('Creating dictionary', font='Any 18')],
                         [sg.Text("Open dictionary:"), sg.Input(size=(25, 1), enable_events=False, key="-UPFILE-"),
                            sg.FileBrowse('Browse'),],
                         [sg.Text("Create dictionary:"), sg.Input(size=(25, 1), enable_events=False, key="-CRFILE-"),
                            sg.Button('Create', key="-CRBUT-"), ],
                         [sg.Text('Input russian word'), sg.Input( key="-RUS-")], 
                         [sg.Text('Input english word'), sg.Input(key="-ENG-")],
                         [sg.Button('Confirm update dictionary', key='-CONFIRM-', expand_x=True)]])
right_column = sg.Column([[sg.Text('Run test', font='Any 18')],
                          [sg.Text("Searching dictionary:"),
                            sg.Input(size=(25, 1), enable_events=True, key="-FILE-"),
                            sg.FileBrowse('Browse'),],
                           [sg.Button('Generate', key='-GENERATE-', expand_x=True)],
                           [sg.Text('See RUSSIAN word'), 
                            sg.Multiline("", size=(25, 1), key='-WORD-', text_color='green', font=("BoldArial", 12),)], 
                           [sg.Text('Input ENGLISH translation'), sg.Input(size=(25, 1), enable_events=True, key='-TRANSLATE-')],
                           [sg.Button('Check', key='-CHECK-', expand_x=True)],
                           [sg.Text('Result'), 
                            sg.Multiline('', size=(30, 1), key='-RESULT-', text_color='red', font=("BoldArial", 12))]])
layout = [[left_column, sg.VerticalSeparator(), right_column],         
          
]

window = sg.Window("VOCABULARY TEST", layout, right_click_menu=rightclick, finalize=True)

while True:
   event, values = window.read()
    
   if event == "Exit" or event == sg.WIN_CLOSED:
      break
   print(values)
   if event == "-CRBUT-":
      print(values['-CRFILE-'])

   if event == "-FILE-":
      current_dict = list(values['-FILE-'].split('/'))[-1]
      
   if event == "-GENERATE-":
      word_with_translate = vocabulary_read(current_dict)
      window['-WORD-'].update(word_with_translate[0])
      check = word_with_translate[1]

   if event == "-TRANSLATE-":
       translate = values['-TRANSLATE-']  

   if event == "-CHECK-":
      try:
         if translate == check:
            window['-RESULT-'].update('ТЫ КРУТ!')
         else:
            window['-RESULT-'].update('ХРЕНЬ')
      except NameError:
         window['-RESULT-'].update('НУ, ВВЕДИ ХОТЬ ЧТО-ТО, ДРУГ!')
      
    
   
   