# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import stock


def register():
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        stock.Move,
        module='sale_delivery_date', type_='model')
