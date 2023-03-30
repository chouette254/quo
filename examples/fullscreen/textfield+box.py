from quo import container
from quo.box import Box
from quo.label import Label
 
# Layout for displaying hello world.
# (The box takes care of the margin/padding.)

label = Label("<style fg='red' bg='yellow'>Hello, world!!</style>")
 
content = Box(label, char="!")

container(content, bind=True, full_screen=True)