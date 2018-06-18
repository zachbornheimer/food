#!/usr/bin/python
# food.py
# by Z. Bornheimer (ZYSYS)
# Purpose: help with food budgeting...once nutirition has been
#          figured out, now to make it financially sustainable!

import sys, getopt
import xml.etree.ElementTree as ET
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def usd(number):
    '''Takes an inputted number (float) and returns a
       version of it rounded to 2 decimal places, adds a
       $ infront and returns it as a string'''
    return "$" + str(float("{0:.2f}".format(number)))

def cost_per_meal(quantity, unit, price, meal_size, serving_measurement):
    '''Determines the cost per meal.  What that means is the amount of food
       on the plate is a portion of the total amount of food purchased.  How
       much does the food on the plate cost?  The food on the plate is the
       meal size and it is measured in serving_measurement units.  The amount
       we purchased is the quantity and it is measured in unit units.  It
       was purchased for price usd.'''
    pounds_to_grams = 453.592
    kg_to_pounds = 2.20462

    pounds_conversion = quantity

    # Step 1, convert quantity into serving_measurement ...we'll eventually need to add more conversions I suppose
    quantity_in_serving_type = quantity;
    if unit == "kilograms":
        pounds_conversion = float(kg_to_pounds) * float(quantity)
    elif unit == "pounds":
        pounds_conversion = quantity

    if serving_measurement == "grams":
        if unit in ("kilograms", "pounds"):
            quantity_in_serving_type = float(pounds_to_grams) * float(pounds_conversion)


    return (float(meal_size) / float(quantity_in_serving_type)) * float(price)


def store_updated_food_cost(food, price, quantity, unit):
    '''Given the food name, price, quantity, and unit, update the food.xml
       file with updated information for the food cost as supplied by the user.'''
    tree = ET.parse('food.xml')
    root = tree.getroot()
    costs = root.find('costs')
        
    for food_entry in root.find('costs'):
        if food_entry.get('name') == food:
            food_entry.set('price', price)
            food_entry.set('quantity', quantity)
            food_entry.set('unit', unit)

    tree.write('food.xml')

def get_meal_price(name, quantity, unit):
    '''Get the price for the quantity of food associated with the current meal.
       This function is necessary as it will extract the prices from the database and it
       is passed the informatin from the meal.'''
    tree = ET.parse('food.xml')
    root = tree.getroot()
    costs = root.find('costs')

    for food_entry in root.find('costs'):
        if food_entry.get('name') == name:
            return  cost_per_meal(float(food_entry.get('quantity')), food_entry.get('unit'), float(food_entry.get('price')), float(quantity), unit)



def print_overview():
    '''Prints an overview of the price per food item in each meal, the price for each meal, and the total daily food cost.'''
    tree = ET.parse('food.xml')
    root = tree.getroot()
    costs = root.find('costs')

    daily_food_cost = 0

    for meals_entry in root.find('meals'):
        meal_price = 0
        print bcolors.UNDERLINE + bcolors.HEADER + meals_entry.get('name').upper() + bcolors.ENDC

        for food_entry in meals_entry.findall('food'):
            meal_price += get_meal_price(food_entry.get('name'), food_entry.get('quantity'), food_entry.get('unit'))
            print '  Food: ', food_entry.get('name'), "price for meal: " + usd(get_meal_price(food_entry.get('name'), food_entry.get('quantity'), food_entry.get('unit')))

        print "Meal cost: " + usd(meal_price)
        print "="*17
        daily_food_cost += meal_price

    print bcolors.OKBLUE + "Total Daily Food Cost: " + usd(daily_food_cost) + bcolors.ENDC
 

def main(argv):
    convert = ''
    store = ''
    quantity = ''
    unit = ''
    food = ''
    price = ''
    serving_size = ''
    serving_measurement = ''
    overview = 1
    try:
        opts, args = getopt.getopt(argv,"hscof:u:q:p:", ["ss=", "sm=", "help", "store", "check", "overview", "food=", "unit=", "quantity=", "price=", "serving-size=", "serving-measurement="])
    except getopt.GetoptError:
        help_man()
        sys.exit(2);
    for opt, arg in opts:
        if opt in ('--help', '-h'):
            help_man()
            sys.exit()
        elif opt in ('-o', "--overview"):
            overview = 1
        elif opt in ("-c", '--check'):
            convert = 1
            overview = 0
        elif opt in ("-s", '--store'):
            store = 1
            overview = 0
        elif opt in ('-q', "--quantity"):
            quantity = re.sub(r'^=*', r'', arg)
        elif opt in ('-p', "--price"):
            price = re.sub(r'^=*', r'', arg)
            price = re.sub(r'\$', r'', price)
        elif opt in ('-u', "--unit"):
            unit = re.sub(r'^=*', r'', arg)
            if unit in ("pounds", "lbs"):
                unit = "pounds"
            if unit in ("kilograms", "kg"):
                unit = "kilograms"
            if unit in ("grams", "g"):
                unit = "grams"
        elif opt in ('-f', "--food"):
            food = re.sub(r'^=*', r'', arg)
        elif opt in ('--ss', "--serving-size"):
            serving_size = re.sub(r'^=*', r'', arg)
        elif opt in ('--sm', "--serving-measurement"):
            serving_measurement = re.sub(r'^=*', r'', arg)



    if overview:
        print_overview()
        sys.exit(0)
    if convert:
        if (None in [quantity, price, unit, food, serving_measurement, serving_size] or '' in [quantity, price, unit, food, serving_measurement, serving_size]):
            if (None == quantity or '' == quantity):
                print '--quantity has not been supplied' 
            if (None == price or '' == price):
                print '--price has not been supplied' 
            if (None == unit or '' == unit):
                print '--unit has not been supplied' 
            if (None == food or '' == food):
                print '--food has not been supplied' 
            if (None == serving_size or '' == serving_size):
                print '--serving-size has not been supplied' 
            if (None == serving_measurement or '' == serving_measurement):
                print '--serving-measurement has not been supplied' 
            sys.exit(2)
        #print food, " quantity: ", quantity, ", price: $", price, ", cost per meal: ", cost_per_meal(quantity, unit, price, serving_size, serving_measurement)
        print 'food cost for ' + food + ' at ' + usd(float(price)) + ' for ' + quantity + ' ' + unit + "... cost per meal: " +  usd(cost_per_meal(quantity, unit, price, serving_size, serving_measurement))

        sys.exit(0)
    if store:
        if (None in [quantity, price, unit, food] or '' in [quantity, price, unit, food]):
            if (None == quantity or '' == quantity):
                print '--quantity has not been supplied' 
            if (None == price or '' == price):
                print '--price has not been supplied' 
            if (None == unit or '' == unit):
                print '--unit has not been supplied' 
            if (None == food or '' == food):
                print '--food has not been supplied' 
            sys.exit(2)
        print 'storing updated food cost for ' + food + ' at ' + usd(float(price)) + ' for ' + quantity + ' ' + unit
        store_updated_food_cost(food, price, quantity, unit)
        sys.exit(0)



def help_man():
    print 'food.py - A food price database system'
    print '\tby Z. Bornheimer (ZYSYS)'
    print ''
    print 'USAGE: food.py <TYPE> <PROPERTIES>'
    print '  <TYPE> = [--overview|-o] [--store|-s] [--check|-c]'
    print '\tNOTE: --overview is assumed.  If --overview or -o is supplied and another <TYPE> is also supplied, overview will exit after report is displayed.'
    print '\t--check has priority over --store.  After --check runs, the program will exit.'
    print '  <PROPERTIES> = (-f=<foodname>||--food=<foodname>) (-u=<unit>||--unit=<unit>) (-q=<quantity>||--quantity=<quantity>) (-p=<price>||--price=<price>) [<PROPERTIES_FOR_CHECK>]'
    print '  <PROPERTIES_FOR_CHECK> = (--ss=<serving_size>||--serving-size=<serving_size>) (--sm=<serving_measurement_unit>||--serving-measurement=<serving_measurement_unit>)'
    print '\t\tNOTE: --ss AND --sm have two hyphens'
    print '\tNOTE: All 4 properties must be supplied with --check or with --store.'
    print ''
    print '--check requires additional parameters --serving-size (or -ss) AND --serving-measurement (or -sm).'
    print '\tFor example, to check the price of 50lbs of oatmeal with a meal being 80g, use:'
    print '\t\tpython food.py --check --food=oatmeal --unit=pounds --quantity=50 --price=74.99 --serving-size=80 --serving-measurement=grams'
    print ''
    print '--overview prints details about food costs.'
    print '--check yields the price per serving.  This helps with bulk price comparison.'
    print '--store updates the database of food prices so that calculations in --overview are accurate.  Run this after food shopping.  Include tax+shipping if applicable.'
    print ''

if __name__ == "__main__":
    main(sys.argv[1:])
