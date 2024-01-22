# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class InventoryLine(metaclass=PoolMeta):
    __name__ = 'stock.inventory.line'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.expected_quantity.states['invisible'] = False

    @staticmethod
    def _compute_expected_quantity(inventory, product, lot=None):
        pool = Pool()
        Inventory = pool.get('stock.inventory')
        Product = pool.get('product.product')
        try:
            Lot = pool.get('stock.lot')
        except KeyError:
            Lot = None

        if not product:
            return 0.0

        if isinstance(inventory, int):
            inventory = Inventory(inventory)
        if not inventory or not inventory.location:
            return 0.0

        grouping = Inventory.grouping()
        with Transaction().set_context(stock_date_end=inventory.date,
                inactive_lots=True):
            if Lot:
                grouping_filter = ([product],)
                pbl = Product.products_by_location([inventory.location.id],
                    grouping_filter=grouping_filter, grouping=grouping)
                return pbl[(inventory.location.id, product, lot)]
            pbl = Product.products_by_location([inventory.location.id],
                grouping=grouping)
            return pbl[(inventory.location.id, product)]

    @fields.depends('inventory', '_parent_inventory.date',
        '_parent_inventory.location', 'product')
    def on_change_with_expected_quantity(self, name=None):
        try:
            lot = self.lot
        except AttributeError:
            lot = None
        return self._compute_expected_quantity(
            self.inventory,
            self.product.id if self.product else None,
            lot.id if lot else None)

    @classmethod
    def create(cls, vlist):
        for values in vlist:
            if 'expected_quantity' not in values:
                values['expected_quantity'] = cls._compute_expected_quantity(
                    values.get('inventory'), values.get('product'),
                    values.get('lot'))

        return super(InventoryLine, cls).create(vlist)


class InventoryLineLot(metaclass=PoolMeta):
    __name__ = 'stock.inventory.line'

    @fields.depends('lot')
    def on_change_with_expected_quantity(self, name=None):
        return super().on_change_with_expected_quantity(name=name)
