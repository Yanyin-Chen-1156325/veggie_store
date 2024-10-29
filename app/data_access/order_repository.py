from sqlalchemy.orm import Session, aliased
from sqlalchemy import not_, union_all
from app.models.Order import *
from app.models.Product import *
from decimal import Decimal


class OrderRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_order_id(self):
        max_id = self.db_session.query(db.func.max(Order.orderNumber)).scalar()
        if max_id:
            next_id = int(max_id) + 1
        else:
            next_id = 1000000001
        return str(next_id)
    
    def generate_orderitem_id(self, order: Order, index):
        index_str = str(index).zfill(6)
        return order.orderNumber + index_str
    
    def get_Order(self, order_id=None, order_customer=None):
        if order_id:
            return self.db_session.query(Order).get(order_id)
        elif order_customer:
            return self.db_session.query(Order).filter_by(orderCustomer=order_customer).all()
        else:
            return self.db_session.query(Order).all()
    
    def place_order(self, order):
        try:       
            self.db_session.add(order)
            self.db_session.commit()
            return order
        except Exception as e:
            return str(e)

    def create_orderitem(self, orderitem):
        try:       
            self.db_session.add(orderitem)
            self.db_session.commit()
            return orderitem
        except Exception as e:
            return str(e)
    
    def update_order(self, order_id, status=None, payment=None):
        if status:
            order = self.db_session.query(Order).get(order_id)
            order.orderStatus = status
        elif payment:
            order = self.db_session.query(Order).get(order_id)
            order.paymentMethod = payment
        self.db_session.commit()
        return order
    
    def update_orderitem_product(self, orderitem_id, product):
        try:
            orderitem = self.db_session.query(OrderItem).get(orderitem_id)
            orderitem.product = product
            self.db_session.commit()
            return orderitem
        except Exception as e:
            return str(e)
        
    def update_order_orderitem(self, order_id, orderitems):
        try:
            order = self.db_session.query(Order).get(order_id)
            order.orderitems = orderitems
            self.db_session.commit()
            return order
        except Exception as e:
            return str(e)
        
    def get_sales(self, start_date, end_date):
        try:
            sales = db.session.query(
                    db.func.sum(Order.totalAmount).label('total_amount'),
                    db.func.count(Order.id).label('order_count')
                ).filter(
                    Order.orderDate.between(start_date, end_date),
                    not_(Order.orderStatus == OrderStatus.CANCELLED.value)
                ).all()
            
            return sales
        except Exception as e: 
            return str(e)
        
    # def get_top_products(self, limit=5):
    #     def create_weighted_query():
    #         # weightveggie
    #         VeggieW = aliased(Veggie, flat=True)
    #         WeightedVeggieA = aliased(WeightedVeggie, flat=True)
            
    #         return (
    #             db.session.query(
    #                 VeggieW.vegName.label('veg_name'),
    #                 WeightedVeggieA.weight.cast(db.Numeric(10, 2)).label('quantity')
    #             )
    #             .select_from(OrderItem)
    #             .join(Order, Order.id == OrderItem.order_id)
    #             .join(WeightedVeggieA, WeightedVeggieA.veggie_id == OrderItem.product_id)
    #             .join(VeggieW, VeggieW.product_id == WeightedVeggieA.veggie_id)
    #             .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
    #         )

    #     def create_pack_query():
    #         # packveggie
    #         VeggieP = aliased(Veggie, flat=True)
    #         PackVeggieA = aliased(PackVeggie, flat=True)
            
    #         return (
    #             db.session.query(
    #                 VeggieP.vegName.label('veg_name'),
    #                 PackVeggieA.numOfPack.cast(db.Numeric(10, 2)).label('quantity')
    #             )
    #             .select_from(OrderItem)
    #             .join(Order, Order.id == OrderItem.order_id)
    #             .join(PackVeggieA, PackVeggieA.veggie_id == OrderItem.product_id)
    #             .join(VeggieP, VeggieP.product_id == PackVeggieA.veggie_id)
    #             .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
    #         )

    #     def create_unit_query():
    #         # unitpriceveggie
    #         VeggieU = aliased(Veggie, flat=True)
    #         UnitPriceVeggieA = aliased(UnitPriceVeggie, flat=True)
            
    #         return (
    #             db.session.query(
    #                 VeggieU.vegName.label('veg_name'),
    #                 UnitPriceVeggieA.quantity.cast(db.Numeric(10, 2)).label('quantity')
    #             )
    #             .select_from(OrderItem)
    #             .join(Order, Order.id == OrderItem.order_id)
    #             .join(UnitPriceVeggieA, UnitPriceVeggieA.veggie_id == OrderItem.product_id)
    #             .join(VeggieU, VeggieU.product_id == UnitPriceVeggieA.veggie_id)
    #             .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
    #         )

    #     # combine
    #     union_query = union_all(
    #         create_weighted_query(),
    #         create_pack_query(),
    #         create_unit_query()
    #     ).select()

    #     # subquery
    #     subq = db.session.query(
    #         union_query.c.veg_name,
    #         union_query.c.quantity
    #     ).subquery()

    #     # final query
    #     final_query = (
    #         db.session.query(
    #             subq.c.veg_name,
    #             db.func.sum(subq.c.quantity).label('total_quantity')
    #         )
    #         .group_by(subq.c.veg_name)
    #         .order_by(db.func.sum(subq.c.quantity).desc())
    #         .limit(limit)
    #     )

    #     try:
    #         results = final_query.all()
    #         return [(veg_name, Decimal(str(quantity))) for veg_name, quantity in results]
    #     except Exception as e:
    #         return str(e)

    def get_top_products(self, limit=5):

        def create_weighted_query():
            # 為 WeightedVeggie 查詢創建別名
            VeggieW = aliased(Veggie, flat=True)
            WeightedVeggieA = aliased(WeightedVeggie, flat=True)
            ProductW = aliased(Product, flat=True)
            
            return (
                db.session.query(
                    VeggieW.vegName.label('veg_name'),
                    ProductW.type.label('veg_type'),
                    WeightedVeggieA.weight.cast(db.Numeric(10, 2)).label('quantity')
                )
                .select_from(OrderItem)
                .join(Order, Order.id == OrderItem.order_id)
                .join(WeightedVeggieA, WeightedVeggieA.veggie_id == OrderItem.product_id)
                .join(VeggieW, VeggieW.product_id == WeightedVeggieA.veggie_id)
                .join(ProductW, ProductW.id == VeggieW.product_id)
                .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
            )

        def create_pack_query():
            # 為 PackVeggie 查詢創建別名
            VeggieP = aliased(Veggie, flat=True)
            PackVeggieA = aliased(PackVeggie, flat=True)
            ProductP = aliased(Product, flat=True)
            
            return (
                db.session.query(
                    VeggieP.vegName.label('veg_name'),
                    ProductP.type.label('veg_type'),
                    PackVeggieA.numOfPack.cast(db.Numeric(10, 2)).label('quantity')
                )
                .select_from(OrderItem)
                .join(Order, Order.id == OrderItem.order_id)
                .join(PackVeggieA, PackVeggieA.veggie_id == OrderItem.product_id)
                .join(VeggieP, VeggieP.product_id == PackVeggieA.veggie_id)
                .join(ProductP, ProductP.id == VeggieP.product_id)
                .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
            )

        def create_unit_query():
            # 為 UnitPriceVeggie 查詢創建別名
            VeggieU = aliased(Veggie, flat=True)
            UnitPriceVeggieA = aliased(UnitPriceVeggie, flat=True)
            ProductU = aliased(Product, flat=True)
            
            return (
                db.session.query(
                    VeggieU.vegName.label('veg_name'),
                    ProductU.type.label('veg_type'),
                    UnitPriceVeggieA.quantity.cast(db.Numeric(10, 2)).label('quantity')
                )
                .select_from(OrderItem)
                .join(Order, Order.id == OrderItem.order_id)
                .join(UnitPriceVeggieA, UnitPriceVeggieA.veggie_id == OrderItem.product_id)
                .join(VeggieU, VeggieU.product_id == UnitPriceVeggieA.veggie_id)
                .join(ProductU, ProductU.id == VeggieU.product_id)
                .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
            )

        # 將三個查詢合併
        union_query = union_all(
            create_weighted_query(),
            create_pack_query(),
            create_unit_query()
        ).select()

        # 創建子查詢
        subq = db.session.query(
            union_query.c.veg_name,
            union_query.c.veg_type,
            union_query.c.quantity
        ).subquery()

        # 最終查詢
        final_query = (
            db.session.query(
                subq.c.veg_name,
                subq.c.veg_type,
                db.func.sum(subq.c.quantity).label('total_quantity')
            )
            .group_by(subq.c.veg_name, subq.c.veg_type)
            .order_by(db.func.sum(subq.c.quantity).desc())
            .limit(limit)
        )

        try:
            results = final_query.all()
            return [(veg_name, veg_type, Decimal(str(quantity))) 
                    for veg_name, veg_type, quantity in results]
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return []