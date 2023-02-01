import sys,os; sys.path.insert(0,os.path.join( os.path.dirname(__file__),".."))
from common import HClient
#################################################################################
from htag import Tag

class Stars(Tag.span): # it's a component ;-)
    def init(self,name,value=0):
        self.name=name
        self["class"]=name
        self["style"]="display:block"
        self.value=value
        self.bless = Tag.Button( self.name+"-", _onclick = lambda o: self.inc(-1) )
        self.bmore = Tag.Button( self.name+"+", _onclick = lambda o: self.inc(+1) )
    def inc(self,v):
        self.value+=v
    def render(self):
        self += self.bless + self.bmore + ("⭐"*self.value)
#------------------------------------------------------------

class App(Tag.div): # it's a component ;-)
    """ Using reactive component, in a reactive context
    """

    def init(self):
        # here we use the previous component "Stars"
        # in a a reactive way (with a render method)
        self.s1= Stars("a")
        self.s2= Stars("b",2)
        self.s3= Stars("c",4)
        self.reset= Tag.Button( "Reset", _onclick = self.clickreset )
        self.show = Tag.div()
        self.exiter = Tag.button("exit",_onclick = lambda o: self.exit())


    def render(self): # it's present -> it's used
        # so the rendering is managed by htag
        self <= self.s1+self.s2+self.s3+self.reset + self.show + self.exiter

        # and so, this div will be updated at reset !
        self.show.set("Values: %s,%s,%s" % (self.s1.value,self.s2.value,self.s3.value))

    def clickreset(self,o):
        # so, resetting values, will redraw this component (App) automatically
        self.s1.value=0
        self.s2.value=0
        self.s3.value=0


#################################################################################

def tests(client:HClient):
    assert "App" in client.title
    client.click('//button[text()="a+"]')
    client.click('//button[text()="a+"]')
    client.click('//button[text()="a+"]')
    client.click('//button[text()="a+"]')
    client.click('//button[text()="b+"]')
    client.click('//button[text()="b+"]')

    values=client.find('//div')[0]

    assert values.text == "Values: 4,4,4"
    assert client.find("//span[@class='a']")[0].text.count("⭐")==4
    assert client.find("//span[@class='b']")[0].text.count("⭐")==4
    assert client.find("//span[@class='c']")[0].text.count("⭐")==4

    client.click('//button[text()="Reset"]')

    values=client.find('//div')[0]
    assert values.text == "Values: 0,0,0"
    assert client.find("//span[@class='a']")[0].text.count("⭐")==0
    assert client.find("//span[@class='b']")[0].text.count("⭐")==0
    assert client.find("//span[@class='c']")[0].text.count("⭐")==0

    client.click('//button[text()="exit"]')

    return True



