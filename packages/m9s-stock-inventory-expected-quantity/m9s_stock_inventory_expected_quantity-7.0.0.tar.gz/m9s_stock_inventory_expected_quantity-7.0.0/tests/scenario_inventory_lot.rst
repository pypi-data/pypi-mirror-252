===================================================
Stock Inventory Expected Quantity With Lot Scenario
===================================================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date.today()


Install stock_inventory_expected_quantity Module::

    >>> config = activate_modules(['stock_inventory_expected_quantity',
    ...     'stock_lot'])


Create company::

    >>> _ = create_company()
    >>> company = get_company()
    >>> party = company.party

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])

Create products::

    >>> ProductUom = Model.get('product.uom')
    >>> ProductTemplate = Model.get('product.template')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal('300')
    >>> template.cost_price_method = 'average'
    >>> template.save()
    >>> product, = template.products

Create a lot for product::

    >>> Lot = Model.get('stock.lot')
    >>> lot = Lot(number='01', product=product)
    >>> lot.save()
    >>> second_lot = Lot(number='02', product=product)
    >>> second_lot.save()

Create an inventory::

    >>> Inventory = Model.get('stock.inventory')
    >>> inventory = Inventory()
    >>> inventory.location = storage_loc
    >>> line = inventory.lines.new()
    >>> line.product = product
    >>> line.expected_quantity == 0.0
    True
    >>> line.lot = lot
    >>> line.expected_quantity == 0.0
    True

Fill storage: Two moves with lots and quantity 1::

    >>> StockMove = Model.get('stock.move')
    >>> incoming_move = StockMove()
    >>> incoming_move.currency = company.currency
    >>> incoming_move.product = product
    >>> incoming_move.lot = lot
    >>> incoming_move.unit = unit
    >>> incoming_move.quantity = 1
    >>> incoming_move.from_location = supplier_loc
    >>> incoming_move.to_location = storage_loc
    >>> incoming_move.planned_date = today
    >>> incoming_move.effective_date = today
    >>> incoming_move.unit_price = Decimal('100')
    >>> incoming_move.click('do')
    >>> incoming_move = StockMove()
    >>> incoming_move.currency = company.currency
    >>> incoming_move.product = product
    >>> incoming_move.lot = second_lot
    >>> incoming_move.unit = unit
    >>> incoming_move.quantity = 1
    >>> incoming_move.from_location = supplier_loc
    >>> incoming_move.to_location = storage_loc
    >>> incoming_move.planned_date = today
    >>> incoming_move.effective_date = today
    >>> incoming_move.unit_price = Decimal('100')
    >>> incoming_move.click('do')

Fill storage: One move without lot and quantity 10::

    >>> incoming_move = StockMove()
    >>> incoming_move.currency = company.currency
    >>> incoming_move.product = product
    >>> incoming_move.unit = unit
    >>> incoming_move.quantity = 10
    >>> incoming_move.from_location = supplier_loc
    >>> incoming_move.to_location = storage_loc
    >>> incoming_move.planned_date = today
    >>> incoming_move.effective_date = today
    >>> incoming_move.unit_price = Decimal('100')
    >>> incoming_move.click('do')

Create an inventory and check expected quantity is computed::

    >>> inventory = Inventory()
    >>> inventory.location = storage_loc
    >>> inventory.empty_quantity = 'keep'
    >>> line = inventory.lines.new()
    >>> line.product = product
    >>> line.expected_quantity
    10.0
    >>> line.lot = lot
    >>> line.expected_quantity
    1.0

Save the inventory and check if the result of expected quantity remains the same::

    >>> inventory.save()
    >>> line, = inventory.lines
    >>> line.expected_quantity
    1.0
    >>> line.quantity = 0.0
    >>> inventory.save()
    >>> line, = inventory.lines
    >>> line.expected_quantity
    1.0
    >>> line.quantity
    0.0
