import spider.ticket.Before
import spider.ticket.later

def main_main(data):
    invoices=Before.invoice()
    confirm_numbers=later.confirm()
    json_pic_and_color=invoices.main(data)
    number=input()
    json_error_or_result=confirm_numbers.send_yz(invoices.browser,number)

