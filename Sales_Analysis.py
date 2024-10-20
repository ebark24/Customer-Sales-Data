import firebase_admin
from firebase_admin import credentials, firestore

# Use the service account key file
cred = credentials.Certificate("C:\\Users\\eliba\\OneDrive\\Documents\\FirestoreJson\\sales-analysis-58113-firebase-adminsdk-ccv64-3ee7a1407c.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Function to display all products
def display_products():
    print("\nCurrent Products:\n")
    docs = products_ref.stream()
    for doc in docs:
        product_data = doc.to_dict()
        print(f'{product_data["Product ID"]}. {product_data["Name"]} - Price: ${product_data["Price"]}, Inventory: {product_data["Inventory"]}')

# Function to add a product
def add_product():
    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    price = float(input("Enter Product Price: "))
    inventory = int(input("Enter Product Inventory: "))
    
    # Add product to Firestore
    products_ref.document(name).set({
        'Product ID': product_id,
        'Name': name,
        'Price': price,
        'Inventory': inventory
    })
    print(f"Product {name} added successfully!")

# Function to remove a product
def remove_product():
    product_id = str(input("Enter the Product ID to remove: "))
    
    # Find product by Product ID and delete
    product_query = products_ref.where('`Product ID`', '==', product_id).stream()
    
    found = False
    for product in product_query:
        found = True
        product_ref = products_ref.document(product.id)
        product_ref.delete()
        print(f"Product {product.id} removed successfully.")
    
    if not found:
        print("Product not found.")

# Function to reduce inventory after purchase
def reduce_inventory(product_id, purchase_quantity):
    product_ref = products_ref.where('`Product ID`', '==', product_id).stream()
    for product in product_ref:
        product_data = product.to_dict()
        new_inventory = product_data['Inventory'] - purchase_quantity
        
        if new_inventory < 0:
            print("Not enough inventory to complete the purchase.")
        else:
            # Update inventory in Firestore
            products_ref.document(product.id).update({'Inventory': new_inventory})
            print(f"Purchase successful. New inventory for {product_data['Name']}: {new_inventory}")

# Main menu
def main():
    while True:
        print("\nSelect an option:")
        print("1. Display Products")
        print("2. Buy a Product")
        print("3. Add a Product")
        print("4. Remove a Product")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            display_products()
        
        elif choice == '2':
            # Display products first
            display_products()
            
            # Get the product ID and quantity from the user
            Purchase_ID = str(input('What Product Number would you like to buy? '))
            Purchase_Quantity = int(input('How many would you like to buy? '))

            # Query Firestore to get the product with the matching 'Product ID'
            product_query = products_ref.where('`Product ID`', '==', Purchase_ID).stream()

            # Get the first matching product from the query
            selected_product = None
            for product in product_query:
                selected_product = product
                break

            if selected_product:
                selected_product_data = selected_product.to_dict()

                # Retrieve the price and inventory of the queried product
                product_price = selected_product_data['Price']
                inventory = selected_product_data['Inventory']

                if Purchase_Quantity > inventory:
                    print(f"Sorry, we only have {inventory} left in stock.")
                else:
                    # Calculate total price (quantity * price)
                    total_price = Purchase_Quantity * product_price

                    # Print the total price to the user
                    print(f'Your final price is: ${total_price:.2f}')  # Format to two decimal places

                    # Reduce inventory after purchase
                    reduce_inventory(Purchase_ID, Purchase_Quantity)
            else:
                print("Product not found.")
        
        elif choice == '3':
            add_product()
        
        elif choice == '4':
            remove_product()
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid option, please try again.")

# Initialize Products collection reference
products_ref = db.collection('Products')

# Run the main program
main()
