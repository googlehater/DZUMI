from sqlalchemy.orm import Session 
from dao.orders_dao import OrderDAO
from config import session



def show_orders(session: Session):
    order_dao = OrderDAO(session)

    try: 
        orders = order_dao.get_all(skip=2, limit=4)
 
        if not orders:
            print("\nЕщё нет заказов для отображения")
            return

        for order in orders:
            print('\n------------------------')
            print(f'ID: {order.id}')
            print(f'Object: {order.object.name}')
            print(f'User: {order.user.last_name, order.user.first_name, order.user.middle_name}')
            print(f'System Type: {order.system_type_id}')
            print(f'Status: {order.order_status}')
            print(f'Total price: {order.total_price}')
            print(f'Agreed?: {order.agreed}')
            print(f'Priority: {order.priority}')
            print(f'Description: {order.description}')
            print(f'Comment: {order.comment}')
            print(f'Decline_reason: {order.decline_reason}')
            print('------------------------')
    except Exception as e:
        print(f"\nПроизошла ошибка при получении заказов: {e}")


def manage_orders():

    while True:
        print("\n1. Поменять статус заявки")
        print("2. Создать заявку")
        print("3. Редактировать заявку")
        print("4. Удалить заявку")
        print("5. Показать заявки")
        print("0. Вернуться в главное меню")

        choice = input("Выберите: ")
        if choice == "1":
            change_status()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            show_orders(session)
        elif choice == "0":
            break 

    pass


def change_status():
    from dao.orders_dao import OrderDAO
    from models.order import Order


    order_dao = OrderDAO(session)
    order = order_dao.get_by_id(order_id=1)
    print(order.order_status)


def pay_order():
    pass


def add_smth():
    pass


def main_menu():
    with Session() as session:
        try:
            while True:
                print("\n===Главное меню===")
                print("1. Управление заявками")
                print("2. Оплатить заявку")
                print("3. Добавить...")
                print("0. Выход\n")

                choice = input("Выберите: ")

                if choice == "1":
                    manage_orders()
                elif choice == "2":
                    pay_order()
                elif choice == "3":
                    add_smth()
                elif choice == "0":
                    break
                
        except Exception as e:
            print(f"Произоша ошибка: {e}")

        finally:
            print('\nthe session is over')

main_menu()
