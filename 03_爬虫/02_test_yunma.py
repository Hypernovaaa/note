import mouse, keyboard
events = []
mouse.hook(events.append)
keyboard.wait('esc')
mouse.unhook(events.append)
print(events)