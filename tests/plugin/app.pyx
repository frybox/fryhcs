from fryhcs import html, Element
from flask import Flask

app = Flask(__name__)
app.config['FRYHCS_PLUGINS'] = ['daisyui']

def App(props):
    initial_count = 20
    return <div>
             <h1 text-cyan-500 hover:text-cyan-600 text-center mt-100px>
               Hello FryHCS!
             </h1>
             <p text-indigo-600 text-center mt-9>
               Count:
               <span text-red-600>{initial_count}(count)</span>
             </p>
             <div flex w-full justify-center>
               <button btn btn-success
                 @click=(increment)>
                 Increment
               </button>
             </div>
           </div>
           <script initial={initial_count}>
              import {signal} from "fryhcs"

              count = signal(initial)

              function increment() {
                  count.value ++
              }
           </script>

@app.get('/')
def index():
    return html(App, "Hello")
