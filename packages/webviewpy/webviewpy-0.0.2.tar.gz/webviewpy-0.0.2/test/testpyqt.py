import sys 
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QApplication, QWidget
from webviewpy import Webview

app = QApplication(sys.argv)
class _QW(QWidget):
    def resizeEvent(self, a0: QResizeEvent) -> None:  
        self.wv.set_geo(10,10,a0.size().width()-20,a0.size().height()-20) 
        
         
window = _QW()
window.resize(1000,500)  

wv=Webview(False,int((window.winId())))

window.wv=wv  
wv.set_title('basic') 
wv.navigate('https://www.baidu.com')
  
window.show()
sys.exit(app.exec_())