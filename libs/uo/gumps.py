"""
gumpDefinition = { htmlgump 0 0 145 120 0 1 0 }{ text 43 5 0 1 }{ button 10 25 40019 40029 1 1 2 }{ text 30 28 80 2 }{ button 10 55 40019 40029 1 1 1 }{ text 30 58 80 3 }{ button 10 85 40019 40029 1 1 3 }{ text 30 88 80 4 }
gumpStrings = List[str](['', 'SOS Navigator', 'Stop Fishing', 'Refresh Markers', 'Select book'])

"""
from bigfish.libs import Observable
"""
Gumps.AddButton(gd,x,y,normalID,pressedID,buttonID,type,param)
#Gumps.SendGump(gumpid,serial,x,y,gumpDefinition,gumpStrings)
Gumps.AddCheck(gd,x,y,inactiveID,activeID,initialState,switchID)
Gumps.AddGroup(gd,group)
Gumps.AddImage(gd,x,y,gumpId)
Gumps.AddImageTiled(gd,x,y,width,height,gumpId)
Gumps.AddImageTiledButton(gd,x,y,normalID,pressedID,buttonID,type,param,itemID,hue,width,height)
Gumps.AddImageTiledButton(gd,x,y,normalID,pressedID,buttonID,type,param,itemID,hue,width,height,localizedTooltip)
Gumps.AddItem(gd,x,y,itemID)
Gumps.AddItem(gd,x,y,itemID,hue)
Gumps.AddLabel(gd,x,y,hue,text)
Gumps.AddLabel(gd,x,y,hue,textID)
Gumps.AddLabelCropped(gd,x,y,width,height,hue,text)
Gumps.AddLabelCropped(gd,x,y,width,height,hue,textID)
Gumps.AddPage(gd,page)
Gumps.AddRadio(gd,x,y,inactiveID,activeID,initialState,switchID)
Gumps.AddSpriteImage(gd,x,y,gumpId,spriteX,spriteY,spriteW,spriteH)
Gumps.AddTextEntry(gd,x,y,width,height,hue,entryID,initialText)
Gumps.AddTextEntry(gd,x,y,width,height,hue,entryID,initialTextID)
Gumps.AddTooltip(gd,cliloc,text)
Gumps.AddTooltip(gd,number)
Gumps.AddTooltip(gd,text)
Gumps.AddButton(gd,x,y,normalID,pressedID,buttonID,type,param)
"""

class GumpElement:
    def __init__(self, parent = None):
        self.parent = parent

    def render(self):
        raise NotImplementedError

class Html(GumpElement):
    def __init__(self, parent = None, x = 0, y = 0, width = 0, height = 0, text = "", background = True, scrollbar = False):
        super().__init__(parent)
        self.position = (x, y)
        self.size = (width, height)
        self.text = text
        self.background = background
        self.scrollbar = scrollbar

    """
    Gumps.AddHtml(gd,x,y,width,height,text,background,scrollbar)
    Gumps.AddHtml(gd,x,y,width,height,textID,background,scrollbar)
    Gumps.AddHtmlLocalized(gd,x,y,width,height,number,args,color,background,scrollbar)
    Gumps.AddHtmlLocalized(gd,x,y,width,height,number,background,scrollbar)
    Gumps.AddHtmlLocalized(gd,x,y,width,height,number,color,background,scrollbar)
    """
    def render(self):
        x, y = self.position
        width, height = self.size
        Gumps.AddHtml(self.parent.gumpData, x, y, width, height, self.text, self.background, self.scrollbar)

"""
Gumps.AddLabel(gd,x,y,hue,text)
Gumps.AddLabel(gd,x,y,hue,textID)
Gumps.AddLabelCropped(gd,x,y,width,height,hue,text)
Gumps.AddLabelCropped(gd,x,y,width,height,hue,textID)        
"""
class Label(GumpElement):
    def __init__(self, text, parent = None, x = 0, y = 0, color=80):
        super().__init__(parent)
        self.position = (x, y)
        self.text = text
        self.color = color

    def render(self):
        x, y = self.position
        Gumps.AddLabel(self.parent.gumpData, x, y, self.color, self.text)

class Button(GumpElement, Observable):
    def __init__(self, parent, btn_id, x = 0, y = 0, btn_type = 1, param = 0, normal_gid = 40019, pressed_id = 40029, on_click = None)
        super().__init__(parent)
        self.btn_id = btn_id
        self.position = (x, y)
        self.param = param
        self.normal_gid = normal_gid
        self.pressed_gid = pressed_id
        self.btn_type = btn_type
        self.on_click = on_click

    """
    Gumps.AddButton(gd,x,y,normalID,pressedID,buttonID,type,param)
    """
    def render(self):
        x, y = self.position
        Gumps.AddButton(self.parent, x, y, self.normal_gid, self.pressed_gid, self.btn_id, self.btn_type, self.param)

class Gump(GumpElement):
    def __init__(self, gump_id, x = 0, y = 0, on_open = None, on_close = None):
        super().__init__(None)
        self.position = (x, y)
        self.on_open = on_open
        self.on_close = on_close
        self.elements = []

    def add(self, element: GumpElement):
        element.parent = self
        self.elements.append(element)

    def render(self):
        for element in self.elements:
            element.render()

    def show(self):
        gump = Gumps.CreateGump(True, True)