# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool, If
from trytond.config import config


shipment_by_planned_date = config.getboolean('sale_delivery_date',
    'shipment_by_planned_date', default=True)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def process(cls, sales):
        pool = Pool()
        SaleLine = pool.get('sale.line')
        to_write = []
        super().process(sales)
        for sale in sales:
            for line in sale.lines:
                if (line.type == 'line'
                        and line.product
                        and not line.requested_delivery_date):
                    date = line.shipping_date
                    to_write.extend(([line], {
                        'requested_delivery_date': date,
                    }))
        if to_write:
            SaleLine.write(*to_write)

    def _group_shipment_key(self, moves, move):
        # Group shipments by move planned_date, so one shipment is created
        # for each planned_date
        grouping = super()._group_shipment_key(moves, move)
        if not shipment_by_planned_date:
            return grouping
        new_grouping = [('planned_date', move[1].planned_date)]
        for field, value in grouping:
            if field == 'planned_date':
                continue
            new_grouping.append((field, value))
        return tuple(new_grouping)


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    requested_delivery_date = fields.Date('Requested Delivery Date',
        states={
            'invisible': ((Eval('type') != 'line')
                | (If(Bool(Eval('quantity')), Eval('quantity', 0), 0) <= 0)),
        }, depends=['type', 'quantity'])

    @fields.depends('requested_delivery_date',
        methods=['on_change_with_shipping_date'])
    def on_change_with_requested_delivery_date(self, name=None):
        if self.requested_delivery_date:
            return self.requested_delivery_date
        return super().on_change_with_shipping_date(name='shipping_date')

    @fields.depends('requested_delivery_date')
    def on_change_with_shipping_date(self, name=None):
        if self.requested_delivery_date:
            return self.requested_delivery_date
        return super().on_change_with_shipping_date(name=name)

    def on_change_product(self):
        self.requested_delivery_date = None
        super().on_change_product()

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default.setdefault('requested_delivery_date')
        return super().copy(lines, default)

    @property
    @fields.depends('requested_delivery_date')
    def planned_shipping_date(self):
        if self.requested_delivery_date:
            return self.requested_delivery_date
        return super().planned_shipping_date
