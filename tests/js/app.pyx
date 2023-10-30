from fryhcs import Element, html
from flask import Flask

app = Flask(__name__)

def Sub2(v, create, **props):
    return (
    <div ref=(foo)>
      <p>Sub2: {v}</p>
      <p>Sub2: {v}(value)</p>
    </div>
    <script foo create={create}>
      const value = create(10);
      console.log(`sub2: ${foo}`);
    </script>)

def Sub1(bar, create, **props):
    return (
    <Sub2 v={bar} create={create}/>
    <script>
      console.log('sub1')
    </script>)

def App(**props):
    return (
    <Sub1 bar="from app" create=(create_signal)>
    </Sub1>
    <script>
      import {signal as create_signal} from 'fryhcs';
      console.log("app");
    </script>)


@app.get('/')
def index():
    return html(App, title="Test JS")
