import os
import json

CAR_INVENTORY_FILE = 'car_inventory.json'

def clr_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def model(n):
    return n.get('model')

def year(n):
    return int(n.get('year'))

def color(n):
    return n.get('color')

def price(n):
    return float(n.get('price'))

def sort_func(cars:list):
    clr_screen()
    sort_option = input('Sort by (model/year/color/price): ').lower()
    order = input('In ascending(a) or descending(d) order: ').lower()
    sort_model = model
    sort_year = year
    sort_color = color
    sort_price = price
    sort_key = {
        'model' : sort_model,
        'year' : sort_year,
        'color' : sort_color,
        'price' : sort_price
    }

    if sort_option in sort_key:
        cars.sort(key= sort_key[sort_option], reverse  = True if order == 'd' else False)
    return

def rendering(cars:list):
    model_len = 0
    year_len = 4
    color_len = 0

    for car in cars: 
        if len(car.get('model')) > model_len:
            model_len = len(car.get('model'))  
        else:
            model_len = model_len

    for car in cars:
        if len(car.get('color')) > color_len:
            color_len = len(car.get('color'))  
        else:
            color_len = color_len

    return [model_len, year_len, color_len,]
    

def load_inventory():
    if os.path.exists(CAR_INVENTORY_FILE):
        with open(CAR_INVENTORY_FILE, 'r') as file:
            return json.load(file)
    return []


def save_inventory(cars:list):
    with open(CAR_INVENTORY_FILE, 'w') as file:
        json.dump(cars, file)


def get_car_details(cars:list, key, value):
    value = str(value)
    value.lower()
    result = [car for car in cars if value in str(car.get(key, '')).lower()]
    if result:
        print('\nMatching Cars')
        print(f'{'Model'.rjust(8)}  {'Year'.rjust(rendering(cars)[0] - 5 + 4)}  {'Color'}  {'Price'.rjust(rendering(cars)[2] - 5 + 5)}')
        for index,search in enumerate(result):
           print(f'{index + 1}. {search['model']}  {str(search['year']).rjust(rendering(cars)[0] - len(search['model']) + 4)}  {search['color']}  {str(search['price']).rjust(rendering(cars)[2] - len(search['color']) + len(str(search['price'])))}')
        input('\nPress enter to continue...')
    else:
        input("No matching car found. \nPress enter to continue..")


def add_new_car(cars:list):
    while True:
        clr_screen()
        try:
            new_car_model = input('Enter car model: ').capitalize()
            new_car_year = input('Enter car year: ')
            if len(new_car_year) > 4:
                clr_screen()
                input('incorrect year ')
                return
            new_car_color = input('Enter car color: ').lower()
            new_car_price = input('Enter car price: ')
            new_car_model.format(' ',)
            new_car_color.format(' ',)
            new_car = {
                'model': new_car_model,
                'year': int(new_car_year),
                'color': new_car_color,
                'price': float(new_car_price)
            }
            if cars.__sizeof__() < 10000:
                cars.append(new_car) 
            else:
                print('\nStorage is FULL!')
                return
            input(f'\n{new_car_model} added successfully!\nEnter..')
            option = input('\nDo you want to add a new car (yes/no): ').lower()
            if option == 'yes':
                continue
            else:
                break
        except ValueError:
            print('Invalid value. Enter to try again...')
            return
        

def view_all_cars(cars:list):
    clr_screen()
    print('Current Inventory:')
    if not cars:
        print('No cars available.')
    else:
        print(f'{'Model'.rjust(8)}  {'Year'.rjust(rendering(cars)[0] - 5 + 4)}  {'Color'}  {'Price'.rjust(rendering(cars)[2] - 5 + 5)}')
        for index, car in enumerate(cars):
            print(f'{index + 1}. {car['model']}  {str(car['year']).rjust(rendering(cars)[0] - len(car['model']) + 4)}  {car['color']}  {str(car['price']).rjust(rendering(cars)[2] - len(car['color']) + len(str(car['price'])))}')
        print(f'{str(cars.__len__()).rjust(46)}/500')
        option = input('Do you want to sort the list (yes/no): ').lower()
        if option == 'yes':
            sort_func(cars)
        else:
            return
    input('Press Enter to continue...')


def search_for_car(cars:list):
    clr_screen()
    search_opt = input('Search by (model/year/color): ')
    if search_opt.lower() == 'model':
        car_model = input('Enter model: ')
        get_car_details(cars, 'model', car_model)
    elif search_opt.lower() == 'year':
        car_year = input('Enter year: ')
        get_car_details(cars, 'year', car_year)
    elif search_opt.lower() == 'color':
        car_color = input('Enter color: ')
        get_car_details(cars, 'color', car_color)


def delete_car(cars:list):
    try:
        view_all_cars(cars)
        option = int(input("Choose car's number to delete: "))- 1
        print(f'{cars[option]['model']} has been deleted')
        cars.pop(option)
        input('\nPress enter to continue...')
    except ValueError:
        input('invalid option. Enter to continue. ')
        return
        
def clear_cars(cars:list):
    try:
        option = input('Do you want to clear all cars in inventory? (yes/no): ').lower()
        if  option == 'no':
            return
        cars.clear()
        input('Cars has been cleared. Press Enter to continue... ')
    except ValueError:
        input('invalid option. Enter to continue. ')
        return

def update_car(cars:list):
    view_all_cars(cars)
    car_index = int(input('\nChoose car to edit details')) - 1
    options = {"model": "Model", "year": "Year", "color": "Color", "price": "Price"}
    option = input("Update car's (model/year/color/price): ").lower()
    if option in options:
        new_value = input(f"Enter new {options[option]}: ")
        cars[car_index][option] = int(new_value) if option == "year" else float(new_value) if option == "price" else new_value
        input(f"{options[option]} updated successfully!")


def main_menu():
    cars = load_inventory()
    while True:
        try:
            clr_screen()
            print('Car Inventory Management System')
            print('1. Add a New Car')
            print('2. View all Cars')
            print('3. Search for a Car')
            print('4. Delete a Car')
            print('5. Update Car Details')
            print('6. Clear all Cars')
            print('7. Exit')
            option = int(input('Enter you choice: '))
            if option == 1:
                add_new_car(cars)
            if option == 2:
                view_all_cars(cars)
            if option == 3:
                search_for_car(cars)
            if option == 4:
                delete_car(cars)
            if option == 5:
                update_car(cars)
            if option == 6:
                clear_cars(cars)
            if option == 7:
                clr_screen()
                exit_option = input('Are you sure you want to EXIT (yes/no)? ')
                if exit_option.lower() != 'no':
                    print('Exiting..')
                    save_inventory(cars)
                    break
        except ValueError:
            input('Invalid value'
            '\nPress enter to continue..')
            continue
        

if __name__ == "__main__":
    main_menu()
