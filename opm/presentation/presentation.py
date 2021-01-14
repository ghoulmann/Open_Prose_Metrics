class FrontEnd(object):
    def __init__(self):
        self.theme = "slate"
        self.logo = "" # path from static/
        self.app_name = "Open Prose Metrics"
        self.report_title = "Results"
        self.theme_cdn = self.bootswatch_url(self.theme)
    def bootswatch_url(self, label):
        if label == "cyborg":
            return "https://stackpath.bootstrapcdn.com/bootswatch/3.4.1/cyborg/bootstrap.min.css"
        elif label == "slate":
            return "https://stackpath.bootstrapcdn.com/bootswatch/3.4.1/slate/bootstrap.min.css"
        else:
            return ""

