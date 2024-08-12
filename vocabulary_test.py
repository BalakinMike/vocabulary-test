import PySimpleGUI as sg
import json
import random
words = {}
def vocabulary_write(vocabulary, words): # Функция заполнения словаря
   with open(vocabulary, encoding='utf-8') as voc: # Чтение словаря в промежуточную переменную "data"
      data = json.load(voc)
      data.update(words) # Объединение словаря и текущего словаря данной сессии "words"
      
   with open(vocabulary, 'w', encoding='utf-8') as voc: # Запись обновлённого словаря
      json.dump(data, voc, ensure_ascii=False, indent=4)

def vocabulary_read(vocabulary): # Чтение словаря 
   with open(vocabulary, encoding='utf-8') as voc:
    data = json.load(voc)
    key_list = list(data.keys())
    random.shuffle(key_list) # Перемешивает словарь для случайного выбора слова
    return key_list[0], data[key_list[0]] # Возврат пар "Слово - перевод"

rightclick = ['&Edit', ['&Copy','&Paste']]
menu_def = [['&File', ['&Open', '&Save', 'E&xit', ]], ['Edit', ['Copy', 'Paste'], ],  ['Help', 'About...'], ]

# ----- Full layout -----
left_column = sg.Column([[sg.Text('Creating dictionary', font='Any 18')],
                         [sg.Text("Open dictionary:"), sg.Input(size=(25, 1), enable_events=True, key="-UPFILE-"),
                            sg.FileBrowse('Browse', key='-UPBUT-'),],
                         [sg.Text("Create dictionary:"), sg.Input(size=(25, 1), enable_events=True, key="-CRFILE-"),
                            sg.Button('Create', key="-CRBUT-"), ],
                         [sg.Text('You work with dictionary:'), sg.Input(size=(25, 1), enable_events=True, key="-DICT-")],
                         [sg.Text('Input russian word'), sg.Input( key="-RUS-")], 
                         [sg.Text('Input english word'), sg.Input(key="-ENG-")],
                         [sg.Button('Confirm update dictionary', key='-CONFIRM-', expand_x=True)]])
right_column = sg.Column([[sg.Text('Run test', font='Any 18')],
                          [sg.Text("Searching dictionary:"),
                            sg.Input(size=(25, 1), enable_events=True, key="-FILE-"),
                            sg.FileBrowse('Browse'),],
                           [sg.Button('Generate', key='-GENERATE-', expand_x=True)],
                           [sg.Text('See RUSSIAN word'), 
                            sg.Input("", size=(25, 1), key='-WORD-', text_color='green', font=("BoldArial", 12),)], 
                           [sg.Text('Input ENGLISH translation'), sg.Input(size=(25, 1), enable_events=True, key='-TRANSLATE-')],
                           [sg.Button('Check', key='-CHECK-', expand_x=True)],
                           [sg.Text('HELP!!!'), sg.Input(size=(15,1), key='-CLUES-'), sg.Button('CLUE', key='-CLUE-')],
                           [sg.Text('Result'), 
                            sg.Input('', size=(30, 1), key='-RESULT-', text_color='red', 
                             font=("BoldArial", 12))]])

layout = [[left_column, sg.VerticalSeparator(), right_column]]

window = sg.Window("VOCABULARY TEST", layout, right_click_menu=rightclick, finalize=True)

while True:
   event, values = window.read()
    
   if event == "Exit" or event == sg.WIN_CLOSED:
      break
   print(values)
# Блок выбора существующего словаря
   if event == "-UPFILE-":
      flag = 'update'
      vocabulary = list(values['-UPFILE-'].split('/'))[-1] # Имя существующего словаря
      window['-DICT-'].update(vocabulary)
# Блок создания нового словаря
   if event == "-CRBUT-":
      flag = 'create'
      vocabulary = str(values['-CRFILE-'])+'.json' # Имя нового словаря
      window['-DICT-'].update(vocabulary)
# Блок заполнения словаря
   if event == '-CONFIRM-':
      window['-RUS-'].update('') # Очищение ячеек слов
      window['-ENG-'].update('')
      words[values['-RUS-']] = values['-ENG-'] # Промежуточный, заполняемый в данной сессии словарь, далее загружаемый в постоянный
      if flag == 'update': # Вызов функции заполнения существующего словаря
         vocabulary_write(vocabulary, words) 
      if flag == 'create': # Создание нового словаря
         with open(vocabulary, 'w', encoding='utf-8') as voc:
            json.dump(words, voc, ensure_ascii=False, indent=4)
      
# Блок выбора словаря для тестирования
   if event == "-FILE-":
      current_dict = list(values['-FILE-'].split('/'))[-1]
      attempt_counter = 0
      seccess_counter = 0
# Блок генерации слов      
   if event == "-GENERATE-":
      attempt_counter += 1
      word_with_translate = vocabulary_read(current_dict) # Вызов функции прочтения очередной пары "слово - перевод" из выбранного словаря
      window['-TRANSLATE-'].update('')
      window['-WORD-'].update(word_with_translate[0])
      check = word_with_translate[1]
# Блок вставки перевода (ответа пользователя на вопрос теста)
   if event == "-TRANSLATE-":
      translate = values['-TRANSLATE-']  
# Блок проверки совпадения слова и перевода
   if event == "-CHECK-":
      try: # Защита от пустого выбора
         if translate == check:
            seccess_counter +=1
            ball = (seccess_counter/attempt_counter)*100
            window['-RESULT-'].update(f'ТЫ КРУТ! - {ball} %')
         else:
            ball = (seccess_counter/attempt_counter)*100
            window['-RESULT-'].update(f'ХРЕНЬ - {ball} %')
      except NameError:
         window['-RESULT-'].update('НУ, ВВЕДИ ХОТЬ ЧТО-ТО, ДРУГ!')
   
   if event == "-CLUE-":
      attempt_counter += 1
      window['-CLUES-'].update(check)
    
   
   