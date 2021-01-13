import time
from PySide6.QtCore import QThread, QObject, Signal
import pandas as pd
from NaverLandScraper import NaverLandScraper

class Worker(QObject):
    finished = Signal()
    progress = Signal(float)
    def __init__(self, query, filter):
        super().__init__()
        self.query = query
        self.filter = filter

    def run(self):
        # """Long-running task."""
        # for i in range(100):
        #     time.sleep(1)
        #     self.progress.emit(i + 1)
        # self.finished.emit()

        app = NaverLandScraper(self.query, self.filter)
        columns=app.building_keys+app.article_keys
        df = pd.DataFrame({}, columns=columns)
        for item in app.item_list:
            self.progress.emit(float((app.item_list.index(item)+1)/len(app.item_list)*100))
            result = app.extract_building_detail(item)
            new_df = pd.DataFrame([result], columns=app.building_keys)
            if len(result["articles"]) != 0:
                building_df = pd.concat([new_df]*len(result["articles"]), ignore_index=True)
                article_df = pd.DataFrame(result["articles"], columns=app.article_keys)
                new_df = pd.concat([building_df, article_df], axis=1)
            df = df.append(new_df)
        df.to_csv(f'result/{app.query}.csv', encoding='utf-8-sig', index=False, header=app.fields)
        self.finished.emit()