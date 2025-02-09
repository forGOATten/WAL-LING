import ttkbootstrap as ttk
from ttkbootstrap import scrolled
import tkinter as tk
from functools import partial
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 

MAXDEBRIS = 250
MAXPAYLOADS = 10

def UI_place_on_Grid(parent: ttk.Frame, layout: list, spadx:tuple=None):
    '''
    Some Overly Engineered Grid Placement
    Places UI elements from a layout list accordingly
        Parameter:
            parent (ttk.Frame): parent frame to have things placed
            layout (list[ttk.*]): list of ttk.* Widgets

        Example of layout list:
            self.Tabs2 =    [[SLabel, SCheck],
                            [SIpRadio],
                            [SIpAddLabel, SIpAddEntry, SIpConnect],
                            [SCOMRadio],
                            [None,SCOMButton]]

            * None will place nothing and move the following item in the next column
    '''

    WHITELIST_STICKY = [ttk.Label, ttk.LabelFrame, ttk.Notebook, ttk.Frame, ttk.Separator]
    WHITELIST_COLSPAN = [ttk.LabelFrame, ttk.Notebook, ttk.Frame]

    for row, elements in zip(range(len(layout)),layout):
        for column, element in zip(range(len(elements)), elements):
            # NOTE: Add whatever restrictions here
            sticky = tk.NSEW if type(element) in WHITELIST_STICKY else tk.NW
            columnspan = len(max(layout, key=len)) if type(element) in WHITELIST_COLSPAN or (column == len(elements)-1) else 1
            padx = (5,0) if column == 0 else (0,0)
            padx = (padx[1] + 5) if (column == len(elements)-1) else padx
            padx = spadx if spadx is not None else padx
            if element is not None:
                element.grid(row=row, column=column, columnspan = columnspan, sticky=sticky, padx=padx, pady=(5,5))

def WIN_Reconfigure(frame, orientation = "rc"):
    """
    Configures the frames col/row to be resizable @ weight 1
        Parameter:
            frame (ttk.Frame, ttk.Window): frame containing all the UI elements
            orientation (str): select orientation for reconfiguration
    """
    col, row = frame.size()
    if "r" in orientation or orientation is None:
        for r in range(row):
            frame.rowconfigure(r, weight=1)
    
    if "c" in orientation or orientation is None:
        for c in range(col):
            frame.columnconfigure(c, weight=1) 

def centerUIWindows(window):

    window.update()
    window.update_idletasks()
    s_width, s_height = window.winfo_screenwidth(), window.winfo_screenheight()
    app_width, app_height = window.winfo_width(), window.winfo_height()
    window.overrideredirect()
    window.geometry(f"+{int(1/2 * s_width - 1/2 * app_width)}+{int(1/2 * s_height - 1/2 * app_height)}")

class RootWindow(ttk.Window):
    def __init__(self):
        super().__init__()
        self.style.load_user_themes("theme.json")
        ttk.Style("starship")
        self.title("LINGLING")
        self.resizable(False, False)
        self.create_UI()

        self.parameters:dict = {
            "cargo": 0,
            "cargoMax": 0,
            "fuel": 0,
            "fuelMax": 0,
            "stationCoor": (0,0,0),
            "initial": {
                "nSpaceStations": 0,
                "nDebris": 0,
                "nPayloads": 0
            },
            "current": {
                "nSpaceStations": 0,
                "nDebris": 0,
                "nPayloads": 0
            }
        }
        self.set_MaxCapacity(100)
        self.set_MaxVolume(100)
        self.after(0, self.__regen)
        centerUIWindows(self)

    def create_Figure(self, master):
        self.fig = plt.figure(figsize = (10, 6), dpi = 100) 

        # adding the subplot 
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        self.canvas = FigureCanvasTkAgg(self.fig, master)   
        self.canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack() 
    
        # creating the Matplotlib toolbar 
        toolbar = NavigationToolbar2Tk(self.canvas, master) 
        toolbar.update() 
    
        # placing the toolbar on the Tkinter window 
        self.canvas.get_tk_widget().pack() 

    def add_scatter(self, *args, **kwargs):
        self.after(0, partial(self.ax.scatter, *args, **kwargs))
        self.update_Plot()
        
    def update_Plot(self):
        self.after(0,self.fig.canvas.draw())

    def __recycle(self):
        pass

    def __refuel(self):
        pass

    def __recon(self):
        pass

    def __random(self):
        pass

    def __regen(self):
        self.after(0, self.ax.clear)
        self.set_NDebris(np.random.randint(60, MAXDEBRIS)+1)
        self.set_NPayload(np.random.randint(3, MAXPAYLOADS))
        self.set_NStations(1)

        self.set_CargoValue(0)
        self.set_FuelValue(100)

        self.payloadArr = [
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nPayloads"])], 
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nPayloads"])], 
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nPayloads"])]
        ]
        self.debrisArr = [
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nDebris"]-1)], 
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nDebris"]-1)], 
            [a if np.random.randint(0,2) else -a for a in np.random.rand(self.parameters["initial"]["nDebris"]-1)]
        ]
        for i in range(len(self.debrisArr)):
            self.debrisArr[i].insert(0,0)
        
        self.add_scatter(self.payloadArr[0], self.payloadArr[1], self.payloadArr[2], 
            marker="p",
            linewidths=3,
            c = "#ffa620",
            label="Payload")
        self.add_scatter([0], [0], [0],
            marker="P",
            linewidths=10,
            c = "#00b976",
            label="Space Station")
        self.add_scatter(self.debrisArr[0], self.debrisArr[1], self.debrisArr[2],
            c = "#da524e",
            label="Debris")
        self.after(0, self.fig.legend)

    def create_UI(self):
        mainFrame = ttk.Frame(master=self)
        mainFrame.grid(column=0, row=0, sticky=tk.NSEW, padx=10)
        
        graphFrame = ttk.Frame(
            master=mainFrame            
        )
        graphFrame.grid(column=0, row=0, rowspan=3, sticky=tk.NSEW, padx=10, pady=10)

        statFrame = ttk.Frame(
            master=mainFrame
        )
        statFrame.grid(column=1, row=0, rowspan=2, sticky=tk.NSEW, padx=10, pady=10)

        logFrame = ttk.Frame(
            master=mainFrame 
        )
        logFrame.grid(column=1, row=2, sticky=tk.NSEW, padx=10, pady=10)

        # Statistics Layout
        statFrameTitle = ttk.Frame(statFrame)
        statFrameTitle.grid(column=0, row=0, columnspan=2, sticky=tk.EW)
        ttk.Label(statFrameTitle, justify="right", text="Statistics", font='-size 30 -weight bold').grid(row=0,column=0,sticky=tk.E)
        WIN_Reconfigure(statFrameTitle)

        statFrameMeters = ttk.Frame(statFrame)
        statFrameMeters.grid(column=0, row=1, rowspan=2, sticky=tk.NSEW)

        self.cargoMeter = ttk.Meter(
            master=statFrameMeters,
            metersize=220,
            meterthickness=25,
            stripethickness=5,
            amounttotal=100,
            amountused=34,
            metertype='full',
            textright="%",
            textfont='-size 27 -weight bold',
            subtext="Cargo Capacity",
            subtextfont='-size 12'
        )
        
        self.cargoMeter.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.fuelMeter = ttk.Meter(
            bootstyle="danger",
            master=statFrameMeters,
            metersize=220,
            meterthickness=25,
            stripethickness=5,
            amounttotal=100,
            amountused=76,
            metertype='full',
            textright="%",
            textfont='-size 27 -weight bold',
            subtext="Fuel Tank",
            subtextfont='-size 12'
        )

        self.fuelMeter.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.cargoValue = ttk.StringVar(value="N/A")
        self.fuelValue = ttk.StringVar(value="N/A")
        self.NSpaceStationValue = ttk.StringVar(value="N/A")
        self.NPayloadValue = ttk.StringVar(value="N/A")
        self.NDebrisValue = ttk.StringVar(value="N/A")

        self.XPos = ttk.StringVar(value="N/A")
        self.YPos = ttk.StringVar(value="N/A")
        self.ZPos = ttk.StringVar(value="N/A")

        statTextFrame = ttk.Frame(statFrame)
        statTextFrame.grid(column=1, row=1, sticky=tk.NSEW)
        statTextLayout = [[ttk.Label(statTextFrame, text="Cargo Capacity:"), ttk.Label(statTextFrame, textvariable=self.cargoValue)],
                          [ttk.Label(statTextFrame, text="Fuel Volume:"), ttk.Label(statTextFrame, textvariable=self.fuelValue)],
                          [ttk.Label(statTextFrame, text="Number of Space Stations:"), ttk.Label(statTextFrame, textvariable=self.NSpaceStationValue)],
                          [ttk.Label(statTextFrame, text="Number of Payload Objects:"), ttk.Label(statTextFrame, textvariable=self.NPayloadValue)]
                        ]
        UI_place_on_Grid(statTextFrame, statTextLayout, spadx=(5,5))
        WIN_Reconfigure(statTextFrame, 'c')
        
        statToolsFrame = ttk.Frame(statFrame)
        statToolsFrame.grid(column=1, row=2, sticky=tk.NSEW)
        self.debrisBar = ttk.Progressbar(statToolsFrame, style="danger", value=40)
        statButtonFrame = ttk.Frame(statToolsFrame)

        statToolsLayout = [[ttk.Label(statToolsFrame, text="Debris Remaining:"), ttk.Label(statToolsFrame, textvariable=self.NDebrisValue)],
                           [self.debrisBar],
                           [statButtonFrame]
                        ]
        UI_place_on_Grid(statToolsFrame, statToolsLayout, (5,5))

        statButtonLayout = [[
            ttk.Button(statButtonFrame, text="Recycle", command=self.__recycle),
            ttk.Button(statButtonFrame, text="Refuel", command=self.__refuel),
            ttk.Button(statButtonFrame, text="Recon", command=self.__recon),
            ttk.Button(statButtonFrame, text="Random", command=self.__random),
        ],[ttk.Button(statButtonFrame, text="Regen", command=self.__regen)]
        ]

        UI_place_on_Grid(statButtonFrame, statButtonLayout, (5,5))
        self.update()   # Mandatory to update the size of progressbar
        self.debrisBar.config(length=statToolsFrame.winfo_width())
        WIN_Reconfigure(statButtonFrame, 'c')
        WIN_Reconfigure(statToolsFrame, 'c')

        # Log Layout
        logTitleFrame = ttk.Frame(logFrame)
        logTitleFrame.grid(row=0, column=0, sticky=tk.EW)
        ttk.Label(logTitleFrame, justify="right", text="Log", font='-size 30 -weight bold').grid(row=0,column=0,sticky=tk.E)
        WIN_Reconfigure(logTitleFrame)

        self.logBox = scrolled.ScrolledFrame(logFrame, width=statFrame.winfo_width(), height=200)
        self.logBox.grid(row=1, column=0, sticky=tk.NSEW)
        self.logText = ttk.StringVar(value="N/A")
        ttk.Label(self.logBox,textvariable=self.logText).grid(row=0,column=0)

        # Graph Layout
        graphFrameTitle = ttk.Frame(graphFrame)
        graphFrameTitle.grid(row=0,column=0, sticky=tk.EW)
        ttk.Label(graphFrameTitle, justify="right", text="Space View", font='-size 30 -weight bold').grid(row=0,column=0,sticky=tk.E)
        WIN_Reconfigure(graphFrameTitle)

        graphPlotFrame = ttk.Frame(graphFrame, style="primary")
        graphPlotFrame.grid(row=1,column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.create_Figure(graphPlotFrame)
        WIN_Reconfigure(graphPlotFrame)

    def set_MaxCapacity(self, value: int | float):
        """
        ### Sets the cargoMax value for the UI and evaluates it in percentage as well before updating the UI
        """
        self.parameters["cargoMax"] = value
        if self.parameters["cargoMax"] >= self.parameters["cargo"]:
            self.after(0, self.cargoMeter.amountusedvar.set, int(self.parameters["cargo"]/self.parameters["cargoMax"] * 100))
            self.after(0, self.cargoValue.set, str(int(self.parameters['cargo'])))

    def set_CargoValue(self, value: int | float):
        """
        ### Sets the cargo value for the UI and evaluates it in percentage as well before updating the UI
        """
        self.parameters["cargo"] = value
        if self.parameters["cargoMax"] >= self.parameters["cargo"]:
            self.after(0, self.cargoMeter.amountusedvar.set, int(self.parameters["cargo"]/self.parameters["cargoMax"] * 100))
            self.after(0, self.cargoValue.set, str(int(self.parameters['cargo'])))

    def set_MaxVolume(self, value: int | float):
        """
        ### Sets the fuelMax value for the UI and evaluates it in percentage as well before updating the UI
        """
        self.parameters["fuelMax"] = value
        if self.parameters["fuelMax"] >= self.parameters["fuel"]:
            self.after(0, self.fuelMeter.amountusedvar.set, int(self.parameters["fuel"]/self.parameters["fuelMax"] * 100))
            self.after(0, self.fuelValue.set, str(int(self.parameters['fuel'])))

    def set_FuelValue(self, value: int | float):
        """
        ### Sets the fuel value for the UI and evaluates it in percentage as well before updating the UI
        """
        self.parameters["fuel"] = value
        if self.parameters["fuelMax"] >= self.parameters["fuel"]:
            self.after(0, self.fuelMeter.amountusedvar.set, int(self.parameters["fuel"]/self.parameters["fuelMax"] * 100))
            self.after(0, self.fuelValue.set, str(int(self.parameters['fuel'])))

    def set_NStations(self, value: int):
        """
        ### Sets the number of stations
        """
        self.parameters["initial"]["nSpaceStations"] = value
        self.parameters["current"]["nSpaceStations"] = value
        self.after(0, self.NSpaceStationValue.set, str(value))

    def set_NPayload(self, value: int):
        """
        ### Sets the number of payloads
        """
        self.parameters["initial"]["nPayloads"] = value
        self.parameters["current"]["nPayloads"] = value
        self.after(0, self.NPayloadValue.set, str(value))

    def set_NDebris(self, value: int):
        """
        ### Sets the number of debris
        """
        self.parameters["initial"]["nDebris"] = value
        self.parameters["current"]["nDebris"] = value
        self.after(0, self.NDebrisValue.set, str(value))
        self.after(0, partial(self.debrisBar.configure, value=100))

    def pop_NDebris(self):
        """
        ### Decrease the number of debris
        """
        self.parameters["current"]["nDebris"] -= 1
        self.after(0, self.NDebrisValue.set, str(self.parameters["current"]))
        self.after(0, partial(self.debrisBar.configure, value=int(self.parameters["current"]["nDebris"]/self.parameters["initial"]["nDebris"])))

    def clear_Log(self):
        self.after(0, self.logText.set, "")
    
    def add_LogEntry(self, value: str):
        prev = self.logText.get()
        self.after(0, self.logText.set, prev + "\n" + value)


if __name__ == "__main__":
    np.random.seed(datetime.now().second)
    root = RootWindow()
    root.mainloop()