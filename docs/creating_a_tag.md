# Creating a Tag : the complete guide

If you come from [domonic](https://github.com/byteface/domonic) or [brython](https://brython.info/static_doc/fr/create.html) : htag borrows the best ideas from them.

## the basics

### at construction time
A Tag (htag's Tag) is a helper to let you build easily html representation of an object.

```python
from htag import Tag

print( Tag.div("hello world") )
```
Will generate `<div>hello world</div>` ... easy ;-)

If you want to set html attributs, prefix them with '_'

```python
print( Tag.div("hello world", _style="background:yellow") )
```
Will generate `<div style="background:yellow">hello world</div>` ;-)

It will work for every kind of html attributs, and events too

```python
print( Tag.div("hello world", _onclick="alert(42)") )
```
Will generate `<div onclick="alert(42)">hello world</div>` ;-)

You can construct whatever tag you want ...

```python
print( Tag.my_tag("hello world", _class="mine") )
```
Will generate `<my-tag class="mine">hello world</my-tag>` (notice that the `_` is replaced by `-` ;-)

```python
print( Tag.span("hello world", _val=12, _checked=True) )
```
Will generate `<span val="12" checked>hello world</span>` !

It's simple ;-)

But you can init some instance properties at construction time ...
```python
tag = Tag.span("hello world", value=12, _value=42 )
print( tag )
```
Will generate `<span value="42">hello world</span>`, but the instance var (here `tag`) will contain 12 ( tag.value==12 ) !
So `_value` is an html attribut ... whereas `value` is an instance property (on python side only). It's important to understand the difference.

take break, and medit on that ;-)

### post construction time

all this variables are usable/settable post construction time.
```python
tag = Tag.span("hello world", value=12, _value=42 )
assert tag["value"]=="42"
assert tag.value==12
```
html attributs are in the dictitem of the tag ! Whereas the instance properties are in the instance ;-)

So you can do that:
```python
tag = Tag.a("hello world")
tag["onclick"]="alert(42)"
```

easy, no ?
... TODO ...

## Inherit a Tag

It's the main purpose of Htag : create feature rich components on python side ...

... TODO ...