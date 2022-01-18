from fpdf import FPDF
import datetime

title_image = 'pink-lotus.jpg'
pdf_w=210
pdf_h=297
p = 10000000019
border = 0
random_seed = 103
receipt_number = "B{:09x}".format(pow(101,random_seed,p))
data_today = datetime.datetime.now()

text = '''
Boston Wellness Massage & Skin Care
224 Clarendon Street
Suite 21 B, Boston, MA 02116
+1 (617)959-3901
cindywei@bostonwellnessmassage.com
'''
price = 95
tip = 25
data = [['Description', 'Price', 'Quantity','Tax 6.25%', 'Total']]
data.append(['TRADITIONAL SWEDISH MASSAGE','{:5.2f}'.format(price/1.0625),'1','{:5.2f}'.format(price - 95/1.0625),'{:5.2f}'.format(price)])


class Receipt_generator(FPDF):
    def header(self):
        epw = self.w - 2*self.l_margin
        self.image(title_image, x=self.l_margin, y=self.t_margin, w=100)
        self.set_font('Arial', 'B', 15)
        self.cell(epw, 10, 'Receipt #:' + ' ' + receipt_number, border = border, ln=0, align='R')
        self.ln(8)
        self.cell(epw, 10, 'Date :'+' '+'{}-{}-{}'.format(data_today.year,data_today.month,data_today.day), border = border, ln=0, align='R')
        self.ln(40)

    def body(self):
        epw = self.w - 2*self.l_margin
        self.set_font('Arial', 'B', 15)
        local_margin = 6
        # self.cell(epw, 10, 'Boston Wellness Massage & Skin Care', border = border, ln=0, align='L')
        # self.ln(local_margin)
        self.set_font('Arial', '', 15)
        self.cell(epw, 10, '224 Clarendon Street', border = border, ln=0, align='L')
        self.ln(local_margin)
        self.cell(epw, 10, 'Suite 21 B, Boston, MA 02116', border = border, ln=0, align='L')
        self.ln(local_margin)
        self.cell(epw, 10, '+1 (617)959-3901', border = border, ln=0, align='L')
        self.ln(local_margin)
        self.cell(epw, 10, 'cindywei@bostonwellnessmassage.com', border = border, ln=0, align='L')
        self.ln(40)

    def table(self):
        epw = self.w - 2*self.l_margin
        col_width = epw/7
        self.set_font('Arial', '', 10)
        th = self.font_size*1.5
        for row in data:
            self.cell(col_width*3, th, str(row[0]), border=1)
            self.cell(col_width, th, str(row[1]), border=1)
            self.cell(col_width, th, str(row[2]), border=1)
            self.cell(col_width, th, str(row[3]), border=1)
            self.cell(col_width, th, str(row[4]), border=1)
            self.ln(th)
        self.ln(20)

    def subtotal(self):
        epw = self.w - 2*self.l_margin
        col_width = epw/7
        self.set_font('Arial', '', 10)
        th = self.font_size*1.5
        self.cell(col_width*5, th, '', border=0)
        self.cell(col_width, th, str('Subtotal:'), border=1, align='R')
        self.cell(col_width, th, str('{:5.2f}'.format(price)), border=1, align='R')
        self.ln(th)

        self.cell(col_width*5, th, '', border=0)
        self.cell(col_width, th, str('Tip:'), border=1, align='R')
        self.cell(col_width, th, str('{:5.2f}'.format(tip)), border=1, align='R')
        self.ln(th)

        self.set_font('Arial', 'B', 10)
        self.cell(col_width*5, th, '', border=0)
        self.cell(col_width, th, str('Total:'), border=1, align='R')
        self.cell(col_width, th, str('{:5.2f}'.format(price + tip)), border=1, align='R')
        self.ln(th)


receipt = Receipt_generator(orientation='P', unit='mm', format='A4')
receipt.add_page()
receipt.body()
receipt.table()
receipt.subtotal()
receipt.output('receipt_'+receipt_number+'.pdf','F')
