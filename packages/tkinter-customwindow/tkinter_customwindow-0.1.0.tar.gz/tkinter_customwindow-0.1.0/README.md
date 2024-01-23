# tkinter-titlebar

在`Windows`平台上自定义窗口，代码大部分借鉴自[CustomTkinterTitlebar](https://pypi.org/project/CustomTkinterTitlebar/)项目，采用`ctypes`与`win32`兼并使用。

## 使用
```Python
from tkcustomwindow import CustomWindow
from tkinter import Tk, Frame

root = Tk()

frame = Frame(root, width=100, height=25, background="grey")
frame.pack(fill="x", side="top")

customwindow = CustomWindow(root)
customwindow.bind_drag(frame)

root.mainloop()

```
