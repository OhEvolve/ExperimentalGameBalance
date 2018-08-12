
from win32com.client import Dispatch

app = GetActiveObject("Illustrator.Application")
docRef = app.Documents.Add()
rectRef = docRef.PathItems.Rectangle(700, 50, 100, 100)
areaTextRef = docRef.TextFrames.AreaText(rectRef)
areaTextRef.Contents = "Hello World!"
