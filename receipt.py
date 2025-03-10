from fpdf import FPDF
import datetime
import argparse
parser = argparse.ArgumentParser(description="receipt argument")

parser.add_argument('-d', '--description', type=str, default="TRADITIONAL SWEDISH MASSAGE", help='An service description')
parser.add_argument('-p','--price', type=int, default=85, help='An service price')
parser.add_argument('-t','--tip', type=int, default=85, help='An service tip')
parser.add_argument('-D','--Date', type=str, default=85, help='An service Date')
parser.add_argument('-s','--seed', type=int, default=85, help='random seed')

args = parser.parse_args()

description = args.description
price = args.price
tip = args.tip
date = datetime.datetime.strptime(args.Date, "%Y-%m-%d")
random_seed = args.seed


title_image = 'pink-lotus.jpg'
pdf_w=210
pdf_h=297
p = 10000000019
border = 0
receipt_number = "B{:09x}".format(pow(101,random_seed,p))

text = '''
Boston Wellness Massage & Skin Care
224 Clarendon Street
Suite 21 B, Boston, MA 02116
+1 (617)959-3901
cindywei@bostonwellnessmassage.com
'''
data = [['Description', 'Price', 'Quantity', 'Total']]
data.append([description,'{:5.2f}'.format(price),'1','{:5.2f}'.format(price)])


class Receipt_generator(FPDF):
    def header(self):
        epw = self.w - 2*self.l_margin
        self.image(title_image, x=self.l_margin, y=self.t_margin, w=100)
        self.set_font('Arial', 'B', 15)
        self.cell(epw, 10, 'Receipt #:' + ' ' + receipt_number, border = border, ln=0, align='R')
        self.ln(8)
        self.cell(epw, 10, 'Date :'+' '+'{}-{}-{}'.format(date.year,date.month,date.day), border = border, ln=0, align='R')
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
        self.cell(col_width, th, str('Tax:'), border=1, align='R')
        self.cell(col_width, th, str('{:5.2f}'.format(tip)), border=1, align='R')
        self.ln(th)

        self.set_font('Arial', 'B', 10)
        self.cell(col_width*5, th, '', border=0)
        self.cell(col_width, th, str('Grand Total:'), border=1, align='R')
        self.cell(col_width, th, str('{:5.2f}'.format(price + tip)), border=1, align='R')
        self.ln(th)


receipt = Receipt_generator(orientation='P', unit='mm', format='A4')
receipt.add_page()
receipt.body()
receipt.table()
receipt.subtotal()
receipt.output('receipt_'+receipt_number+'.pdf','F')
