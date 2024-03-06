import customtkinter as ctk
from urllib.request import urlopen
from bs4 import BeautifulSoup 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GUI:
    def __init__(self):

        #Root
        self.root = ctk.CTk()
        self.root.geometry("700x450")
        self.root.title("Kalkulator jednostek")

        #Top Label
        self.toplabel = ctk.CTkLabel(master=self.root, text="Kalkulator jednostek", font=("Roboto", 30))
        self.toplabel.pack(padx=10, pady=10)

        #Main Frame
        self.frame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=2)
        self.frame.pack(padx=30, pady=15, fill="both", expand=True)

        #C Frame
        self.cframe = ctk.CTkFrame(master=self.frame)
        self.cframe.grid(row=0, column=0, padx=10, pady=10, sticky="news")

        self.clabel = ctk.CTkLabel(master=self.cframe, text="°C", font=("Roboto", 30))
        self.clabel.pack(padx=10, pady=10)

        self.centry = ctk.CTkEntry(master=self.cframe, font=("Roboto", 24), placeholder_text="")
        self.centry.pack(padx=10, pady=10)

        self.cbutton = ctk.CTkButton(master=self.cframe, text="Przelicz", font=("Roboto", 24), command=self.wylicz_f)
        self.cbutton.pack(padx=10, pady=40)

        #F Frame
        self.fframe = ctk.CTkFrame(master=self.frame)
        self.fframe.grid(row=0, column=1, padx=10, pady=10, sticky="news")

        self.flabel = ctk.CTkLabel(master=self.fframe, text="°F", font=("Roboto", 30))
        self.flabel.pack(padx=10, pady=10)

        self.fentry = ctk.CTkEntry(master=self.fframe, font=("Roboto", 24))
        self.fentry.pack(padx=10, pady=10)

        self.fbutton = ctk.CTkButton(master=self.fframe, text="Przelicz", font=("Roboto", 24), command=self.wylicz_c)
        self.fbutton.pack(padx=10, pady=40)

        #Bottomframe
        self.bottomframe = ctk.CTkFrame(master=self.frame)
        self.bottomframe.columnconfigure(0, weight=1)
        self.bottomframe.columnconfigure(1, weight=1)
        self.bottomframe.columnconfigure(2, weight=1)
        self.bottomframe.rowconfigure(0, weight=1)
        self.bottomframe.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="news")

        #Online data
        self.combobox = ctk.CTkComboBox(master=self.bottomframe, values=["pogoda.onet.pl","pogoda.wp.pl","weather.com"], font=("Roboto", 20))
        self.combobox.grid(row=0, column=0, padx=10, pady=20, sticky="we")

        self.checkstate = ctk.IntVar()
        self.checkbox = ctk.CTkCheckBox(master=self.bottomframe ,text="Odczuwalna", font=("Roboto", 16), variable=self.checkstate)
        self.checkbox.grid(row=0, column=1)

        self.download_button = ctk.CTkButton(master=self.bottomframe ,text="Pobierz dane", font=("Roboto", 20), command=self.download_data)
        self.download_button.grid(row=0, column=2, padx=10, pady=20)

        #MainLoop
        self.root.mainloop()

    #Metody
    def wylicz_f(self):
        cel = float(self.centry.get())
        far = round(cel*1.80+32,2)
        self.fentry.delete(0, ctk.END)
        self.fentry.insert(0, far)

    def wylicz_c(self):
        far = float(self.fentry.get())
        cel = round((far-32)/1.80,2)
        self.centry.delete(0, ctk.END)
        self.centry.insert(0, cel)

    def download_data(self):
        wybor = self.combobox.get()
        real = self.checkstate.get()

        self.centry.delete(0, ctk.END)

        if wybor == "pogoda.onet.pl":
            if real == 0:
                self.centry.insert(0, self.onet())
            else:
                self.centry.insert(0, self.onet_real())
        elif wybor == "pogoda.wp.pl":
            if real == 0:
                self.centry.insert(0, self.wp())
            else:
                self.centry.insert(0, self.wp_real())
        elif wybor == "weather.com":
            if real == 0:
                self.centry.insert(0, self.weather())
            else:
                self.centry.insert(0, self.weather_real())

        self.wylicz_f()

    #Webscraping
    def onet(self):
        url = "https://pogoda.onet.pl/prognoza-pogody/poznan-335979"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="temp").get_text()[0:-1]
        return float(temp)

    def onet_real(self):
        url = "https://pogoda.onet.pl/prognoza-pogody/poznan-335979"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="feelTempValue").get_text()[0:-2]
        return float(temp)
    
    def wp(self):
        url = "https://pogoda.wp.pl/pogoda-dlugoterminowa/poznan/696381"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="temp").get_text()
        return float(temp)
    
    def wp_real(self):
        url = "https://pogoda.wp.pl/pogoda-dlugoterminowa/poznan/696381"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="info").get_text()[11:-2]
        return float(temp)

    def weather(self):
        url = "https://weather.com/pl-PL/pogoda/dzisiaj/l/c997cf7ce4365a083341184a8a2ab4e91c93b8dc1fb7cd62ddbca12267daf9b0"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="CurrentConditions--tempValue--MHmYY").get_text()[0:-1]
        return float(temp)

    def weather_real(self):
        url = "https://weather.com/pl-PL/pogoda/dzisiaj/l/c997cf7ce4365a083341184a8a2ab4e91c93b8dc1fb7cd62ddbca12267daf9b0"
        html_code = urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html_code, "html.parser")
        temp = soup.find(class_="TodayDetailsCard--feelsLikeTempValue--2icPt").get_text()[0:-1]
        return float(temp)
        

GUI()