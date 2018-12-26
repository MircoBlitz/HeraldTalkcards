from odf import text, teletype
from odf.opendocument import load
import time, shutil

class Pdfer:
    # Initializer / Instance Attributes
    def __init__(self, data, form):
        self.data = data
        self.format = form

    def gen_odt(self):
        for key in self.data:
            print("generating " + key + ".odt")
            shutil.copyfile("assets/a" + str(self.format) + ".odt", 'output/odt/' + key + '.odt')
            self.replace("#blockid", key, key, 14)
            self.replace("#day", "Day: " + self.data[key]["day"], key, 14)
            self.replace("#start", self.data[key]["start"] + "  -  " + self.data[key]["end"], key, 14)
            self.replace("#durat", self.data[key]["duration"], key, 14)
            self.replace("#DE", self.data[key]["language"].upper(), key, 14)
            self.replace("#title", self.data[key]["title"], key, 18)
            self.replace("#track", self.data[key]["track"], key, 12)
            self.replace("#room", self.data[key]["room"], key, 12)
            self.replace("#abstract", self.data[key]["abstract"], key, 8)
            self.replace("#speaker", self.data[key]["speaker"], key, 16)
            

    def replace(self, srch, rplz,filename, fontsize):
        odt = load('output/odt/' + filename + '.odt')
        textp = odt.getElementsByType(text.P)
        nump = len(textp)
        for i in range(nump):
            old_text = teletype.extractText(textp[i])
            if srch == old_text:
                new_text = old_text.replace(srch,rplz)
                new_S = text.P()
                new_S.setAttribute("stylename",textp[i].getAttribute("stylename"))
                new_S.addText(new_text)
                textp[i].parentNode.insertBefore(new_S,textp[i])
                textp[i].parentNode.removeChild(textp[i])
                odt.save('output/odt/' + filename + '.odt')

