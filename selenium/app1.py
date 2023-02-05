import sys,os; sys.path.insert(0,os.path.join( os.path.dirname(__file__),".."))
import hclient
#################################################################################
#<code>
from htag import Tag

class App(Tag.body):
    """ the base """
    def init(self):
        def say_hello(o):
            self <= Tag.li("hello")
        self<= Tag.button("click",_onclick = say_hello)
        self<= Tag.button("exit",_onclick = lambda o: self.exit())

#</code>
#################################################################################

def tests(client:hclient.HClient):
    assert "App" in client.title

    client.click('//button[text()="click"]')
    client.click('//button[text()="click"]')
    client.click('//button[text()="click"]')

    assert len(client.find('//li'))==3

    client.click('//button[text()="exit"]')
    return True

if __name__=="__main__":
    # hclient.run( App, "PyScript")
    # hclient.test( App, "BrowserHTTP", tests)
    hclient.test( App, "PyScript", tests)
    # hclient.test( App, "WebHTTP", tests)