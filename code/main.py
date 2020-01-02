import protobuf

# import the library
file = open("tripUpdate.buf","r")
from appJar import gui
# create a GUI variable called app
app = gui()
# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", file.name)
app.setLabelBg("title", "red")
# start the GUI
app.go()