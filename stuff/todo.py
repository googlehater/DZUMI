# # endpoints layer
# @Post('orders/order')  # rest
# def controller(@FromBody orderDto: { name, otherRequiredFields } as json):
#   ordersService = @Inject<OrdersService>()
#   orderDao = @Inject<OrdersDao>()
#   ordersService.createNewOrder(orderModel)


# class OrdersDao:  # как заполнить
#   def createModelBy(dto: dict, user: User):
#     model = Order.builder()
#       .set_id(UUIDv4::new)
#       .set_name(dto.name)
#       .set_created_at(UTC::now)
#       .set_user_id(user.id)
#       // other thigns
#     // or auto map all fields from dto to new model
#     return model

# class OrdersService:
#   def createNewOrder(orderDto: { name, otherRequiredFields } as json):
#     usersDao = @Inject<UsersDao>()
#     user = usersDao,.getCurrentLoggedInUser()
    
#     // validations
#     if (user.role != НАЧАЛЬНИК) raise ValidationError
    
#     orderDao = @Inject<OrdersDao>()
#     model = orderDao.createModelBy(orderDto, user)
#     orderDao.save(model)

from dao.orders_dao import OrderDAO
from models.order import Order
order_dao = OrderDAO
order = order_dao.get_by_id(order_id=1)
print(order.order_status)
