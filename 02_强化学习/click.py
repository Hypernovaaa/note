import pyautogui 

width, height = pyautogui.size()
for i in range(100):
    x = width - i * 10 
    y = height - i * 10 

    pyautogui.rightClick(x, y)