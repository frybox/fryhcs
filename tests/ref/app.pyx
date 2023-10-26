from fryhcs import Element, html
from flask import Flask

app = Flask(__name__)

@app.get('/')
def index():
    return html(RefApp, title="test ref")

def RefApp(props):
    return (
    <div w-full h-100vh flex flex-col gap-y-10 justify-center items-center>
      <p ref=(foo) text-indigo-600 text-6xl transition-transform duration-1500>
        Hello World!
      </p>
      <p ref=(bar) text-cyan-600 text-6xl transition-transform duration-1500>
        Hello FryHCS!
      </p>
    </div>
    <script foo bar>
      setTimeout(()=>{
        foo.style.transform = "skewY(180deg)";
      }, 1000);
      setTimeout(()=>{
        bar.style.transform = "skewY(180deg)";
      }, 2500);
    </script>)

if __name__ == '__main__':
    print(html(RefApp))
