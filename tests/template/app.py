# fry e8f245a7bd0ecda5470b27f7ef2d3e721bad688d
# Generated by fryweb, DO NOT EDIT THIS FILE!
from fryweb import Element, html
from flask import Flask

app = Flask(__name__)

@app.get('/')
def index():
    return html(RefApp, title="test template", autoreload=False)

def Log(value=''):
    prefix = ''
    return Element("div", {"call-client-script": ["app_Log", [("prefix", prefix)]], "children": [Element("p", {":log": Element.ClientRef("log"), "children": [(value)]})]})

def RefApp():
    count = 0
    return Element("div", {"call-client-script": ["app_RefApp", [("count", count)]], "w-full": True, "h-100vh": True, "flex": True, "flex-col": True, "gap-y-10": True, "items-center": True, "children": [Element("p", {":foo": Element.ClientRef("foo"), "text-primary-tx": True, "text-6xl": True, "transition-transform": True, "duration-1500": True, "children": [Element("span", {"*": Element.ClientEmbed(0), "children": [f"{count}"]})]}), Element("button", {"type": "button", "@click": Element.ClientEmbed(1), "border": True, "rounded": True, "bg-primary": True, "w-3/4": True, "children": ["点我"]}), Element("div", {":logger": Element.ClientRef("logger"), "children": [Element(Log, {"frytemplate": True, ":logline": Element.ClientRef("logline")})]})]})


if __name__ == '__main__':
    print(html(RefApp))
