import tkinter as tk
from tkinter import ttk
import random

root = tk.Tk() # окно приложения
root.title('Программа нахождения кратчайших путей в графе') # название приложения
root.wm_attributes('-alpha', 1) # делаем окно поверх остальных окон и регулируем прохрачность
root.geometry('905x600+220+40') # размер окна и координаты
root.resizable(width=False, height=False) # настройки окна: невозможность изменения ширины и длины

# --------------------------ДАННЫЕ---------------------------
# обозначение состояний ребра
INF, HIMSELF, NOEDGE, ARROW, ARROWTEXT = 100000000, -1000000, -100000, -10000, -1000

# координаты
column1, column2, column3, column4 = 30, 240, 440, 605
row1, row2, row3, row4 = 5, 30, 55, 80

# цвета
lBlueC, blueC, dBlueC = '#5569a6', '#1b3faa', '#0d215c'
lRedC, redC, dRedC = '#cf4848', '#c71c1c', '#8c0a0a'
grayC, dGrayC = '#77767a', '#434245'
blackC = '#242424'

# данные
vertices = []
edges = []
pathVertices = []
verticesNums = []

# переменные для графических элементов
startVertice = tk.IntVar(value = 0)
finalVertice = tk.IntVar(value = 0)
edgeStartVertice = tk.IntVar(value = 0)
edgeFinalVertice = tk.IntVar(value = 0)
edgeSize = tk.IntVar(value = 0)
switchTurnNegativeNum = tk.IntVar(value = 0)
switchFaster = tk.IntVar(value = 0)
randomVerticeNum = tk.IntVar(value=2)
randomEdgeNum = tk.IntVar(value=0)
counterEdgeNum = 0

# стили кнопок и флажка
style = ttk.Style()
style.configure("r.TButton", foreground=redC)
style.configure("b.TButton", foreground="black")
style.configure("s.TCheckbutton", foreground=dGrayC)

# --------------------------ФУНКЦИИ--------------------------
# обновление интерфейса если поставлен флажок обновления
def update(): 
  if (switchFaster.get() == 0):
    root.update()

# проверка выбранных вершин на корректность
def checkStartFinalVertComboboxes(event):
  if startVertice.get() in list(range(1, len(vertices)+1)) and finalVertice.get() in list(range(1, len(vertices)+1)) and (startVertice.get() != 0 and finalVertice.get() != 0): buttonCalculatePath.configure(state = "normal")
  else: buttonCalculatePath.configure(state = "disabled")
def checkEdgesComboboxes(event):
  if edgeStartVertice.get() in list(range(1, len(vertices)+1)) and edgeFinalVertice.get() in list(range(1, len(vertices)+1)) and (edgeStartVertice.get() != 0 and edgeFinalVertice.get() != 0 and edgeStartVertice.get() != edgeFinalVertice.get()):
    spinboxEdgeSize.configure(state = "normal")
    buttonChangeEdge.configure(state = "normal")
  else:
    spinboxEdgeSize.configure(state = "disabled")
    buttonChangeEdge.configure(state = "disabled")
def checkRandomSpinboxes():
  if randomVerticeNum.get() in list(range(2, 301)) and randomEdgeNum.get() in list(range(0, 1501)):
    buttonRandom.configure(state = "normal")
  else:
    buttonRandom.configure(state = "disabled")
  
# алгоритм Беллмана-Форда
def bellmanFord():
  # проверка на существование вершин
  if ((startVertice.get() not in list(range(1, len(vertices)+1))) or (finalVertice.get() not in list(range(1, len(vertices)+1)))): giveError("Вы ввели вершину, которой не существует!"); return
  
  dist = [INF] * len(vertices) # длина от стартовой вершины до каждой вершины
  path = [INF] * len(vertices) # путь от каждой вершины до вершины, которая в конечном счете доведет до стартовой вершины
  dist[startVertice.get()-1] = 0
  path[startVertice.get()-1] = -1 
  pathVertices.clear() # очистка предыдущего неактуального кратчайшего пути


  # отрисовка
  for i in range(0, len(vertices)):
    canvas.itemconfig(vertices[i], fill = grayC)
  for u in range(0, len(edges)):
    for v in range(0, len(edges[i])):
      canvas.itemconfig(edges[u][v][1], fill = blackC)
  update() 

  # алгоритм
  for i in range(0, len(vertices) - 1): # |V|-1 итераций
    for u in range(0, len(edges)):
      for v in range(0, len(edges[u])):
        if (u != v and edges[u][v][0] != NOEDGE): # если ребро не от вершины до этой же вершины и если есть какое то ребро между вершинами
          # отрисовка
          if (switchFaster.get() == 0):
            canvas.itemconfig(edges[u][v][1], fill = lBlueC)
            canvas.itemconfig(vertices[u], fill = lBlueC)
            canvas.itemconfig(vertices[v], fill = lBlueC)
            update()

          # релаксация ребра
          if (dist[v] > dist[u] + edges[u][v][0]):
            dist[v] = dist[u] + edges[u][v][0]
            path[v] = u
            if (switchFaster.get() == 0):
              canvas.itemconfig(edges[u][v][1], fill = redC)
              canvas.itemconfig(vertices[u], fill = redC)
              canvas.itemconfig(vertices[v], fill = lRedC)
              update()
          
          # отрисовка
          if (switchFaster.get() == 0):
            canvas.itemconfig(edges[u][v][1], fill = blackC)
            canvas.itemconfig(vertices[u], fill = grayC)
            canvas.itemconfig(vertices[v], fill = grayC)
            update()

  # еще одна релаксация ребра для проверки графа на наличие отрицательного цикла
  for u in range(0, len(edges)):
    for v in range(0, len(edges[u])):
      if (u != v and edges[u][v][0] != NOEDGE) and (dist[v] > dist[u] + edges[u][v][0]):
        giveError("Отрицательный цикл! \n(Есть отрицательные ребра, мешающие построить путь)")
        return
  
  check = finalVertice.get()-1 # переменная для прохода от конечной вершины до стартовой
  
  # проверка, что вообще существует путь от стартовой вершины до конечной
  if (dist[check] == INF):
    infoAnswerVar.set(f"Длина пути: Неизвестно")
    infoPathVar.set(f"Путь: Нет ни одного подходящего пути")
    return


  # генерируем путь для отображения
  pathstr = "" # строка для отображения пути
  counter = 0 # счетчик для переноса строки "Путь:" для удобного отображения
  while (check != -1): # пока не дойдем до стартовой вершины
    counter += 1
    pathVertices.append(check) # сохраняем часть пути
    pathstr = f"{check + 1}(={dist[check]})"   + pathstr
    check = path[check]
    # работа со строкой для удобного отображения
    if (check != -1): 
      pathstr = " -> " + pathstr
      if counter >= 5:
        pathstr = "\n" + pathstr
        counter = 0
  infoAnswerVar.set(f"Длина пути: {dist[finalVertice.get()-1]}")
  infoPathVar.set(f"Путь: {pathstr}")

  # отрисовка кратчайшего пути
  for i in range(0, len(pathVertices)):
    if i == 0: canvas.itemconfig(vertices[pathVertices[i]], fill = dBlueC)
    elif i == len(pathVertices) - 1: canvas.itemconfig(vertices[pathVertices[i]], fill = lBlueC)
    else: canvas.itemconfig(vertices[pathVertices[i]], fill = blueC)
    canvas.tag_raise(vertices[pathVertices[i]])
    canvas.tag_raise(verticesNums[pathVertices[i]])
    if i != 0:
      canvas.itemconfig(edges[pathVertices[i]][pathVertices[i-1]][1], fill = blueC, width = 2)

# создание случайного графа
def rand():
  pathVertices.clear()
  v = randomVerticeNum.get()
  e = randomEdgeNum.get()
  sw = switchTurnNegativeNum.get()
  swf = switchFaster.get()
  if ((v < 2 or v > 300) or (e < 0 or e > 1500) or (v <= 1 and e != 0)): 
    giveError("Неправильное кол-во вершин или ребер \n(Кол-во вершин: от 2 до 300, \n Кол-во ребер: от 0 до 1500)")
    return

  clear()
  switchFaster.set(swf)
  for i in range(0, v):
    createVertice()
    update()
  if (len(vertices) >= 2):
    comboboxChooseFirstEdge.configure(state="normal")
    comboboxChooseSecondEdge.configure(state="normal")

  for i in range(0, e):
    edgeStartVertice.set(random.randint(1, v))
    edgeFinalVertice.set(random.randint(1, v))
    while (edgeStartVertice.get() == edgeFinalVertice.get()):
      edgeStartVertice.set(random.randint(1, v))
      edgeFinalVertice.set(random.randint(1, v))
    
    if (edgeStartVertice.get() != 0 and edgeFinalVertice.get() != 0 and edgeStartVertice.get() != edgeFinalVertice.get()):
      spinboxEdgeSize.configure(state = "normal")
      buttonChangeEdge.configure(state = "normal")
    else:
      spinboxEdgeSize.configure(state = "disabled")
      buttonChangeEdge.configure(state = "disabled")

    if (sw == 1): edgeSize.set(random.randint(-99, 99))
    else: edgeSize.set(random.randint(0, 99))
    
    update()
    createEdge()

# очистка интерфейса
def clear():
  vertices.clear()
  verticesNums.clear()
  edges.clear()
  canvas.delete("all")
  global counterEdgeNum
  counterEdgeNum = 0
  comboboxCreateVertice.configure(values=list(range(1, len(vertices)+1)))
  comboboxEndVertice.configure(values=list(range(1, len(vertices)+1)))
  comboboxChooseFirstEdge.configure(values=list(range(1, len(vertices)+1)))
  comboboxChooseSecondEdge.configure(values=list(range(1, len(vertices)+1)))
  infoVerticeSizeVar.set(f'Кол-во вершин: {len(vertices)}')
  infoEdgesSizeVar.set(f'Кол-во ребер: {len(edges)}')
  infoAnswerVar.set('Длина пути: Неизвестно')
  infoPathVar.set('Путь: Неизвестно')
  randomVerticeNum.set(2)
  randomEdgeNum.set(0)
  startVertice.set(0)
  finalVertice.set(0)
  edgeStartVertice.set(0)
  edgeFinalVertice.set(0)
  edgeSize.set(0)
  switchTurnNegativeNum.set(0)
  switchFaster.set(0)
  buttonDelete.configure(style="b.TButton")
  buttonCalculatePath.configure(state="disabled")
  buttonChangeEdge.configure(state="disabled")
  buttonCreateVertice.configure(state="normal")
  buttonRandom.configure(state="normal")
  comboboxChooseFirstEdge.configure(state="disabled")
  comboboxChooseSecondEdge.configure(state="disabled")
  comboboxCreateVertice.configure(state="disabled")
  comboboxEndVertice.configure(state="disabled")
  spinboxEdgeSize.configure(state="disabled")
  spinboxRandomEdgeSize.configure(state="normal")
  spinboxRandomVerticeSize.configure(state="normal")

# анимация при наведении и отведении мыши на вершину графа
def showVerticesEdges(event, a):
  canvas.itemconfig(vertices[a], fill = redC)
  for i in range(0, len(edges)):
    if (i == a): # ребра, отходящие от этой вершины
      for k in range(0, len(edges[i])):
        canvas.itemconfig(edges[i][k][2], state = "disabled")
        canvas.itemconfig(edges[i][k][1], fill = lRedC, width = 3)
        if (edges[i][k][0] != HIMSELF and edges[i][k][0] != NOEDGE):
          canvas.itemconfig(vertices[k], fill = lRedC)
    else:
      for k in range(0, len(edges[i])):
        if (k == a):  # ребра, приходящие в эту вершину
          canvas.itemconfig(edges[i][k][2], state = "disabled")
          canvas.itemconfig(edges[i][k][1], fill = dRedC, width = 3)
          if (edges[i][k][0] != HIMSELF and edges[i][k][0] != NOEDGE):
            canvas.itemconfig(vertices[i], fill = dRedC)
def hideVerticesEdges(event, a):
  if a in pathVertices: 
    if pathVertices.index(a) == 0: canvas.itemconfig(vertices[a], fill = dBlueC)
    elif pathVertices.index(a) == len(pathVertices) - 1: canvas.itemconfig(vertices[a], fill = lBlueC)
    else: canvas.itemconfig(vertices[a], fill = blueC)
  else: canvas.itemconfig(vertices[a], fill = grayC)

  for i in range(0, len(edges)):
    for k in range(0, len(edges[i])):
      canvas.itemconfig(edges[i][k][2], state = "hidden")
      
      if i in pathVertices and k in pathVertices and (pathVertices.index(i) - pathVertices.index(k)) == 1: canvas.itemconfig(edges[i][k][1], fill = blueC, width = 2)
      else: canvas.itemconfig(edges[i][k][1], fill = blackC, width = 1)
      
      if k in pathVertices:
        if pathVertices.index(k) == 0: canvas.itemconfig(vertices[k], fill = dBlueC)
        elif pathVertices.index(k) == len(pathVertices) - 1: canvas.itemconfig(vertices[k], fill = lBlueC)
        else: canvas.itemconfig(vertices[k], fill = blueC)
      else: canvas.itemconfig(vertices[k], fill = grayC)

# анимация при наведении и отведении мыши на ребро
def showEdgeSize(event, a, b):
  canvas.itemconfig(edges[a][b][2], state = "disabled")
  canvas.itemconfig(edges[a][b][1], fill = redC, width = 3)
  canvas.itemconfig(vertices[a], fill = redC)
  canvas.itemconfig(vertices[b], fill = lRedC)
def hideEdgeSize(event, a, b):
  canvas.itemconfig(edges[a][b][2], state = "hidden")
  if a in pathVertices and b in pathVertices and (pathVertices.index(a) - pathVertices.index(b)) == 1: canvas.itemconfig(edges[a][b][1], fill = blueC, width = 2)
  else: canvas.itemconfig(edges[a][b][1], fill = blackC, width = 1)

  if a in pathVertices:
    if pathVertices.index(a) == 0: canvas.itemconfig(vertices[a], fill = dBlueC)
    elif pathVertices.index(a) == len(pathVertices) - 1: canvas.itemconfig(vertices[a], fill = lBlueC)
    else: canvas.itemconfig(vertices[a], fill = blueC)
  else: canvas.itemconfig(vertices[a], fill = grayC)

  if b in pathVertices:
    if pathVertices.index(b) == 0: canvas.itemconfig(vertices[b], fill = dBlueC)
    elif pathVertices.index(b) == len(pathVertices) - 1: canvas.itemconfig(vertices[b], fill = lBlueC)
    else: canvas.itemconfig(vertices[b], fill = blueC)
  else: canvas.itemconfig(vertices[b], fill = grayC)

# создание вершины
def createVertice():
  # случайные координаты на окне графа 
  o1 = random.randint(5, 818)
  o2 = random.randint(5, 395)

  # создание новой вершины графически
  newVertice = canvas.create_oval(o1, o2, o1+40, o2+40, fill=grayC)
  vertices.append(newVertice)
  canvas.tag_raise(newVertice)
  
  # создание номера вершины графически
  numOfVertice = canvas.create_text(o1 + 20, o2 + 20, text = f"{len(vertices)}", state = "disabled")
  canvas.tag_raise(numOfVertice)
  verticesNums.append(numOfVertice)

  # заполнение ребер для новой вершины
  for i in range(len(edges)):
    edges[i].append([NOEDGE, ARROW, ARROWTEXT]) 
  edges.append([[NOEDGE, ARROW, ARROWTEXT]]*(len(edges)) + [[HIMSELF, ARROW, ARROWTEXT]])

  # коррекция элементов интерфейса
  comboboxCreateVertice.configure(values=list(range(1, len(vertices)+1)))
  comboboxEndVertice.configure(values=list(range(1, len(vertices)+1)))
  comboboxChooseFirstEdge.configure(values=list(range(1, len(vertices)+1)))
  comboboxChooseSecondEdge.configure(values=list(range(1, len(vertices)+1)))
  infoVerticeSizeVar.set(f'Кол-во вершин: {len(vertices)}')
  if (len(vertices) >= 2):
    comboboxChooseFirstEdge.configure(state="normal")
    comboboxChooseSecondEdge.configure(state="normal")
  elif (len(vertices) >= 1):
    comboboxCreateVertice.configure(state="normal")
    comboboxEndVertice.configure(state="normal")
  update()

  # присваивание функций для вершины при наведении и отведении
  canvas.tag_bind(newVertice, "<Enter>", lambda e, a = len(vertices)-1: showVerticesEdges(e, a))
  canvas.tag_bind(newVertice, "<Leave>", lambda e, a = len(vertices)-1: hideVerticesEdges(e, a))

# создание ребра
def createEdge():
  # получение вершин ребра и размера ребра
  u = edgeStartVertice.get()
  v = edgeFinalVertice.get()
  size = edgeSize.get()

  # проверка на корректность размера ребра
  if (u not in list(range(1, len(vertices)+1)) or v not in list(range(1, len(vertices)+1)) or size not in list(range(-100, 101))): giveError("Размер ребра должен быть \nв пределе от -100 до 100"); return

  # получение координат вершин ребра
  firstCoords = canvas.coords(vertices[u-1])
  secondCoords = canvas.coords(vertices[v-1])

  # работа с изменением ребра в edges
  if (edges[u-1][v-1][0] == NOEDGE): # если создаем новое ребро
    # отрисовка ребра
    # получаем середины вершин
    x1 = (firstCoords[0] + firstCoords[2]) / 2
    y1 = (firstCoords[1] + firstCoords[3]) / 2
    x2 = (secondCoords[0] + secondCoords[2]) / 2
    y2 = (secondCoords[1] + secondCoords[3]) / 2
    k = (((x2 - x1)**2 + (y2 - y1)**2)**0.5) / 25 # коэффициент, чтобы ребро располагалось не вплотную к вершинам
    # смещение ребра по координатам
    offsety = abs(x1-x2)/50 
    offsetx = abs(y1-y2)/50
    xtrue1 = (x2 - x1) / k + x1
    ytrue1 = (y2 - y1) / k + y1
    xtrue2 = (x1 - x2) / k + x2
    ytrue2 = (y1 - y2) / k + y2
    centerx = (xtrue2 + xtrue1) / 2
    centery = (ytrue2 + ytrue1) / 2
    c = 0
    if abs(x1-x2) + abs(y1-y2) < 100: c = 13
    elif abs(x1-x2) + abs(y1-y2) < 150: c = 9
    elif abs(x1-x2) + abs(y1-y2) < 200: c = 7
    elif abs(x1-x2) + abs(y1-y2) < 300: c = 6
    elif abs(x1-x2) + abs(y1-y2) < 400: c = 4
    elif abs(x1-x2) + abs(y1-y2) < 600: c = 3
    elif abs(x1-x2) + abs(y1-y2) < 900: c = 2
    elif abs(x1-x2) + abs(y1-y2) < 1200: c = 1.8
    else: c = 1.5
    if x1 < x2: offsety = -offsety
    ytrue1 += offsety
    ytrue2 += offsety
    centery += offsety * c
    if y1 > y2: offsetx = -offsetx
    xtrue1 += offsetx
    xtrue2 += offsetx
    centerx += offsetx * c

    # создание ребра графически 
    line = canvas.create_line(xtrue1, ytrue1, xtrue2, ytrue2, arrow=tk.LAST, fill=blackC, width = 1)
    canvas.tag_lower(line)
    
    # создание текста ребра графически
    lineText = canvas.create_text(centerx, centery, text=f"{size}", font='bold 14', state = "hidden", fill = "#e80000")
    canvas.tag_raise(lineText)
    
    # обновление ребра в массиве edges
    edges[u-1][v-1] = [size, line, lineText]

    # присваивание функций для ребра при наведении и отведении
    canvas.tag_bind(line, "<Enter>", lambda e, a = u-1, b=v-1: showEdgeSize(e, a, b))
    canvas.tag_bind(line, "<Leave>", lambda e, a = u-1, b=v-1: hideEdgeSize(e, a, b))

    # увеличение числа ребер и отрисовка
    global counterEdgeNum; counterEdgeNum += 1
    infoEdgesSizeVar.set(f'Кол-во ребер: {counterEdgeNum}')
  elif (edges[u-1][v-1][0] == HIMSELF): # если меняется ребро, ведущая от вершины на эту же вершину, возвращаем ошибку
    giveError("Смотрим на ребро \nвершины, ведущий на само себя"); return
  else: # если меняем существующее ребро
    # обновляем существующее ребро
    edges[u-1][v-1][0] = size
    
    # меняем графический текст существующего ребра
    canvas.itemconfig(edges[u-1][v-1][2], text=f"{size}")

# сообщение об ошибке
def giveError(message):
  # деактивируем все графические элементы, кроме кнопки "Очистить"
  buttonDelete.configure(style = "r.TButton")
  infoPathVar.set(f"Ошибка: {message}")
  buttonCalculatePath.configure(state="disabled")
  buttonChangeEdge.configure(state="disabled")
  buttonCreateVertice.configure(state="disabled")
  buttonRandom.configure(state="disabled")
  comboboxChooseFirstEdge.configure(state="disabled")
  comboboxChooseSecondEdge.configure(state="disabled")
  comboboxCreateVertice.configure(state="disabled")
  comboboxEndVertice.configure(state="disabled")
  spinboxEdgeSize.configure(state="disabled")
  spinboxRandomEdgeSize.configure(state="disabled")
  spinboxRandomVerticeSize.configure(state="disabled")

# ---------------------ГРАФИЧЕСКИЕ-ЭЛЕМЕНТЫ------------------
# Раздел: Вычисления
titleCalculating = tk.Label(root, text= 'ВЫЧИСЛЕНИЕ', fg = blueC, font=("Times New Roman", 8))
titleCalculating.pack()
titleCalculating.place(x = column1, y = row1)

comboboxCreateVertice = ttk.Combobox(root, textvariable = startVertice, values = list(range(1, len(vertices)+1)), width = 5, state = "disabled")
comboboxCreateVertice.pack()
comboboxCreateVertice.place(x = column1 + 130, y = row2)
comboboxCreateVertice.bind("<<ComboboxSelected>>", checkStartFinalVertComboboxes)

comboboxEndVertice = ttk.Combobox(root, textvariable = finalVertice, values = list(range(1, len(vertices)+1)), width = 5, state = "disabled")
comboboxEndVertice.pack()
comboboxEndVertice.place(x = column1 + 130, y = row3)
comboboxEndVertice.bind("<<ComboboxSelected>>", checkStartFinalVertComboboxes)

labelStartVertice = tk.Label(root, text= 'Стартовая вершина', fg = dGrayC)
labelStartVertice.pack()
labelStartVertice.place(x = column1, y = row2)

labelEndVertice = tk.Label(root, text= 'Конечная вершина', fg = dGrayC)
labelEndVertice.pack()
labelEndVertice.place(x = column1, y = row3)

buttonCalculatePath = ttk.Button(root, text = 'Вычислить путь', command = bellmanFord, state = "disabled")
buttonCalculatePath.pack()
buttonCalculatePath.place(x = column1, y = row4)

buttonDelete = ttk.Button(root, text = 'Очистить', command = clear)
buttonDelete.pack()
buttonDelete.place(x = column1 + 108, y = row4)

checkButtonFaster = ttk.Checkbutton(root, text='Быстрее (без анимации)', variable=switchFaster, style = "s.TCheckbutton")
checkButtonFaster.pack()
checkButtonFaster.place(x = column1, y = row4 + 25)


# Раздел: Генерация
titleAnother = tk.Label(root, text= 'ГЕНЕРАЦИЯ', fg = blueC, font=("Times New Roman", 8))
titleAnother.pack()
titleAnother.place(x = column2, y = row1)

buttonRandom = ttk.Button(root, text = 'Рандом', command = rand)
buttonRandom.pack()
buttonRandom.place(x = column2, y = row4 + 25)

labelRandomVerticeSize = tk.Label(root, text= 'Кол-во вершин:', fg = dGrayC)
labelRandomVerticeSize.pack()
labelRandomVerticeSize.place(x = column2, y = row2)

labelRandomEdgeSize = tk.Label(root, text= 'Кол-во рёбер:', fg = dGrayC)
labelRandomEdgeSize.pack()
labelRandomEdgeSize.place(x = column2, y = row3)

checkButtonRandomNegativeNumbersSwitcher = ttk.Checkbutton(root, text='Включить рёбра c минусом', variable=switchTurnNegativeNum, style = "s.TCheckbutton")
checkButtonRandomNegativeNumbersSwitcher.pack()
checkButtonRandomNegativeNumbersSwitcher.place(x = column2, y = row4)

spinboxRandomVerticeSize = ttk.Spinbox(root, from_ = 2, to = 300, textvariable = randomVerticeNum, width = 5, command = checkRandomSpinboxes)
spinboxRandomVerticeSize.pack()
spinboxRandomVerticeSize.place(x = column2 + 126, y = row2)

spinboxRandomEdgeSize = ttk.Spinbox(root, from_ = 0, to = 1500, textvariable = randomEdgeNum, width = 5, command = checkRandomSpinboxes)
spinboxRandomEdgeSize.pack()
spinboxRandomEdgeSize.place(x = column2 + 126, y = row3)


# Раздел: Информация
titleInfo = tk.Label(root, text= 'ИНФОРМАЦИЯ', fg = blueC, font=("Times New Roman", 8))
titleInfo.pack()
titleInfo.place(x = column3, y = row1)

infoVerticeSizeVar = tk.StringVar(value=f'Кол-во вершин: {len(vertices)}')
infoVerticeSize = tk.Label(root, textvariable = infoVerticeSizeVar, fg = dGrayC)
infoVerticeSize.pack()
infoVerticeSize.place(x = column3, y = row2)

infoEdgesSizeVar = tk.StringVar(value='Кол-во ребер: 0')
infoEdgesSize = tk.Label(root, textvariable = infoEdgesSizeVar, fg = dGrayC)
infoEdgesSize.pack()
infoEdgesSize.place(x = column3, y = row3-8)

infoAnswerVar = tk.StringVar(value='Длина пути: Неизвестно')
infoAnswer = tk.Label(root, textvariable = infoAnswerVar, fg = dGrayC)
infoAnswer.pack()
infoAnswer.place(x = column3, y = row3+10)

infoPathVar = tk.StringVar(value='Путь: Неизвестно')
infoPath = tk.Label(root, textvariable = infoPathVar, fg = dGrayC, justify = "left")
infoPath.pack()
infoPath.place(x = column3, y = row4+2)


# Раздел: Создание
titleChange = tk.Label(root, text= 'СОЗДАНИЕ', fg = blueC, font=("Times New Roman", 8))
titleChange.pack()
titleChange.place(x = column4, y = row1)

labelChangeEdge = tk.Label(root, text= 'Ребро от                      до                      = ', fg = dGrayC)
labelChangeEdge.pack()
labelChangeEdge.place(x = column4, y = row2)

comboboxChooseFirstEdge = ttk.Combobox(root, textvariable = edgeStartVertice, values = list(range(1, len(vertices)+1)), width = 5, state = "disabled")
comboboxChooseFirstEdge.pack()
comboboxChooseFirstEdge.place(x = column4 + 58, y = row2)
comboboxChooseFirstEdge.bind("<<ComboboxSelected>>", checkEdgesComboboxes)

comboboxChooseSecondEdge = ttk.Combobox(root, textvariable = edgeFinalVertice, values = list(range(1, len(vertices)+1)), width = 5, state = "disabled")
comboboxChooseSecondEdge.pack()
comboboxChooseSecondEdge.place(x = column4 + 137, y = row2)
comboboxChooseSecondEdge.bind("<<ComboboxSelected>>", checkEdgesComboboxes)

spinboxEdgeSize = ttk.Spinbox(root, from_ = -100, to = 100, textvariable = edgeSize, width= 6, state = "disabled")
spinboxEdgeSize.pack()
spinboxEdgeSize.place(x = column4 + 213, y = row2 + 1)

buttonChangeEdge = ttk.Button(root, text = 'Создать/Изменить ребро', command = createEdge, state = "disabled")
buttonChangeEdge.pack()
buttonChangeEdge.place(x = column4, y = row3)

buttonCreateVertice = ttk.Button(root, text = 'Создать вершину', command = createVertice)
buttonCreateVertice.pack()
buttonCreateVertice.place(x = column4 + 163, y = row3)


# Окно графа
canvas = tk.Canvas(root, height = 435, width = 860, bg = '#e6e6e6')
canvas.pack()
canvas.place(x = 20, y = 140)

# Запуск программы
root.mainloop()
