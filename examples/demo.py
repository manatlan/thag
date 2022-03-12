from thag import Tag # the only thing you'll need ;-)


class Button(Tag):
    """ It's a button component, rendered as <button onclick=''>txt</button>"""

    # this Tag will be rendered as a <button>, so we set its attribut "tag" <- "button"
    tag="button"

    # this allow you to include statics in headers
    # (it will be included only once !!!)
    statics = [Tag.style("button.my {background:yellow; border:1px solid black; border-radius:4px}")]

    def __init__(self,txt, callback):
        super().__init__()

        # we set some html attributs
        self["class"]="my"                      # set @class to "my"
        self["onclick"]=self.bind.onclick()     # bind a js event on @onclick
                                                # "self.bind.<method>()" is the trick to generate a js interaction
                                                # binded to this component

        self <= txt                             # put a text into the button
                                                # it's a shortcut for "self.add( txt )"

        self.callback=callback                  # save the py callback for later use

    def onclick(self):
        # this is the event called by the @onclick
        # it will call the py callback
        self.callback()

class Star(Tag):
    """ This Star component display 2 buttons to decrease/increase a value
        (it displays nb x star according the value)
    """
    # it doesn't define its "tag" attribut, so it will be a <div> (the default)

    def __init__(self,value=0):
        super().__init__()
        self.nb=value

    def inc(self,v):
        self.nb+=v

    def __str__(self):
        # here, the representation is built lately
        # (during the __str__ rendering)

        # we clear all the contents of the tag
        self.clear()

        # we add our buttons, binded to its py method
        self <= Button( "-", lambda: self.inc(-1) )
        self <= Button( "+", lambda: self.inc(1) )

        # we draw the stars
        self <= "⭐"*self.nb

        return super().__str__()


class Page(Tag):
    """ This is the main Tag, it will be rendered as <body> by the thag/renderer """
    # it doesn't define its "tag" attribut
    # but as long as it's the main tag ...
    # it will be rendered as <body>

    def __init__(self):
        super().__init__()

        # here is a list of movies ;-)
        self.movies=[
            ("BatMan", Star(5)),
            ("Thor", Star(9)),
            ("Superman", Star(7)),
        ]

    def __str__(self):
        # here, the representation is built lately
        # (during the __str__ rendering)

        # we clear the content
        self.clear()

        # we put a title
        self <= Tag.h1("Best movies ;-)")   # here is shortcut to create "<h1>Best movies ;-)</h1>"
                                            # (it works for any html tag you want ;-)

        # and add our stuff, sorted by nb of stars
        for name,star in sorted( self.movies, key=lambda x: -x[1].nb ):
            self <= Tag.div( [name,star] )

        return super().__str__()

# instanciate the main component
obj=Page()

# and execute it in a pywebview instance
from thag.runners import *
PyWebWiew( obj ).run()

# here is another runner, in a simple browser (thru ajax calls)
# BrowserHTTP( obj ).run()
