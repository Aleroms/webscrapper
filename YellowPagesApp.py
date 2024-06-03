from TKinterUserInterface import YellowpagesGUI
from YellowpagesWebscraper import YellowPagesScraper
from CsvData import PandasData


class YellowPagesApplication:
    def __init__(self):
        self.gui = YellowpagesGUI()
        self.pandasData = PandasData()

    def run(self):
        lead_criteria = self.gui.run()
        niche = lead_criteria["niche"].replace(" ", "")
        city = lead_criteria["city"].replace(" ", "")
        state = lead_criteria["state"].replace(" ", "")
        yp = YellowPagesScraper()
        raw_leads = yp.scrape(niche=lead_criteria["niche"], location=f"{city}, {state}")
        self.pandasData.writeToCsv(raw_leads, f"{niche}-{city}{state}")



