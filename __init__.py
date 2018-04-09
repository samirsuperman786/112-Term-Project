from Listener import *
from tkinter import *
from Graphics.Word import *
from threading import Thread

#####
#MVC#
#####
def init(data):
    data.timerDelay= 10
    data.time = 0
    data.currentSentence=""
    data.words = []
    initializeListener()

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    data.time+=1
    if(phrases.empty()==False):
        data.currentSentence= phrases.get()
        words = data.currentSentence.split(" ")
        for i in range(len(words)):
            word = words[i]
            data.words.append(Word(data.width//2, data.height//2 - (i *100), getSoundVolume(), word))
    for word in data.words:
    	word.move((0, 1))
    	
def redrawAll(canvas, data):
    #canvas.create_text(data.width//2, data.height//2, text = data.currentWord, fill = "red")
    for word in data.words:
    	word.draw(canvas, data)

#####
#run#
#####
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#Creates different threads for the microphone
if __name__ == "__main__":
    mainThread = Thread(target = run, args = (1000, 600))
    mainThread.start()
    soundThread = Thread(target = initializeVolume)
    soundThread.start()
    soundThread.join()
    mainThread.join()