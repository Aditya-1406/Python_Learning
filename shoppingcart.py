
class Cart:

    def __init__(self):
        self.items = {}
    
    def add_item(self, item_name, price, quantity=1):
        if item_name in self.items:
            self.items[item_name]['quantity'] += quantity
        else:
            self.items[item_name] = {'price': price, 'quantity': quantity}

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items:
            if quantity >= self.items[item_name]['quantity']:
                del self.items[item_name]
            else:
                self.items[item_name]['quantity'] -= quantity
        else:
            print("Item not found in cart.")
    
    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print("Items in your cart:")
        for item_name, details in self.items.items():
            print(f"{item_name}: ${details['price']} x {details['quantity']}")
    
    def total_price(self):
        total = 0
        for details in self.items.values():
            total += details['price'] * details['quantity']
        return total
    
def main():
    cart = Cart()
    while True:
        print("\nShopping Cart Menu:")
        print("1. View Cart")
        print("2. Add Item")
        print("3. Remove Item")
        print("4. View Total Price")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            cart.view_cart()
        elif choice == '2':
            item_name = input("Enter item name: ")
            try:
                price = float(input("Enter item price: "))
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Invalid input for price or quantity.")
                continue
            cart.add_item(item_name, price, quantity)
            print("Item added to cart.")
        elif choice == '3':
            item_name = input("Enter item name to remove: ")
            try:
                quantity = int(input("Enter quantity to remove: "))
            except ValueError:
                print("Invalid input for quantity.")
                continue
            cart.remove_item(item_name, quantity)
        elif choice == '4':
            print(f"Total price: ${cart.total_price():.2f}")
        elif choice == '5':
            print("Exiting the Shopping Cart application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()