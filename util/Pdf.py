from fpdf import FPDF
from pandas import DataFrame

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        
        # self.image('assets/logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Monthly Report', 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    
    def print_df(self, df: DataFrame, font_size: int = 12):
        # table header
        self.set_font('Arial', 'B', font_size)
        
        columns = df.columns.to_list()
        df_length = len(df)
        for i in columns:
            if i != columns[-1]:
                self.cell(30, 10, i.capitalize(), 1, 0, align='C')
            else:
                self.cell(30, 10, i.capitalize(), 1, 1, align='C')
                
        # table content
        for i in range(df_length):
            for j in columns:
                text = str(df[j].iloc[i])
                if j != columns[-1]:
                    self.cell(30, 10, text, 1, 0, align='C')
                else:
                    self.cell(30, 10, text, 1, 1, align='C')
        