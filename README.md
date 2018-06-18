# food.py
=======
LICENSE: GPLv3
By Z. Bornheimer (ZYSYS)
Purpose: deal with a food budget intelligently!

## SETUP
* Define your meals in food.xml including names of food, serving sizes, and
  measurement units
* Add your foodnames to the food.xml file costs section.  The program cannot
  yet automatically create new foods, but it will update units, sizes, etc, so
  that info doesn't need to be accurate.  
* Take your most recent grocery receipt and enter in prices into the program
* Check the food.xml database to confirm that everything looks okay!

## FOOD.XML
This file is the main database of the program.
It's divided into 2 sections:
* `costs`
* `meals`

### `costs`

The costs section consists of food entries and are measured how you purchase
the item.  For example, if you buy a 25 pound bag of jasmine rice, the entry in
the costs section would look something like:

`<food name="jasmine-rice" price="49.99" quantity="25" unit="pounds" />`

### `meals`

You can define meals however.  Each meal is named and food and portions.
Consider the portion how much food goes in your stomach!  If you have 50 grams
of jasmine rice at lunch, you might have an entry in the meals section, under
lunch that looks like:

`<food name="jasmine-rice" quantity="50" unit="grams" />`

### NOTE

NOTE: As of now, the software doesn't really mess too heavily with the
database.  It is not a total interface.  I decided that, for me, it would be
enough to define the API to the DB in a pragmatic way...if I need something,
write it on the fly.  I don't need a way to add new foods, so, it's not here!


## USAGE:

`food.py - A food price database system
	by Z. Bornheimer (ZYSYS)

USAGE: food.py <TYPE> <PROPERTIES>
  <TYPE> = [--overview|-o] [--store|-s] [--check|-c]
	NOTE: --overview is assumed.  If --overview or -o is supplied and another <TYPE> is also supplied, overview will exit after report is displayed.
	--check has priority over --store.  After --check runs, the program will exit.
  <PROPERTIES> = (-f=<foodname>||--food=<foodname>) (-u=<unit>||--unit=<unit>) (-q=<quantity>||--quantity=<quantity>) (-p=<price>||--price=<price>) [<PROPERTIES_FOR_CHECK>]
  <PROPERTIES_FOR_CHECK> = (--ss=<serving_size>||--serving-size=<serving_size>) (--sm=<serving_measurement_unit>||--serving-measurement=<serving_measurement_unit>)
		NOTE: --ss AND --sm have two hyphens
	NOTE: All 4 properties must be supplied with --check or with --store.

--check requires additional parameters --serving-size (or -ss) AND --serving-measurement (or -sm).
	For example, to check the price of 50lbs of oatmeal with a meal being 80g, use:
		python food.py --check --food=oatmeal --unit=pounds --quantity=50 --price=74.99 --serving-size=80 --serving-measurement=grams

--overview prints details about food costs.
--check yields the price per serving.  This helps with bulk price comparison.
--store updates the database of food prices so that calculations in --overview are accurate.  Run this after food shopping.  Include tax+shipping if applicable.`

## ORIGIN/HOW I USE:

So why this program?  Well, my trainer gave me a diet that is really working
for me.  I've been on it (pretty much) for the last few months and love it.  I
feel like it's my default food system now, so I wanted to get it straight
financially - because the hard part was already fixed!

The idea was to be able to compare the prices of different oatmeal!  I wanted
to know how much oatmeal was gonna cost me every day if I had one serving.
Originally, I started using a REPL script just so I could do the conversion
between grams and pounds, so I decided to just make a script.  Then that turned
into storing all of my food and then optimizing it from there!

My personal goal was to spend less than $7 a day on food.  This helped me get
to about $5 because I could try out different options using the --check
feature.  Because of the --overview feature, I was able to determine that
protein powder was my biggest expense, much to my surprise, so I was able to
figure out a way to reduce that cost.  I hope it's as helpful to you as it was
to me.  If you create new conversion systems or API's to the DB, please submit
a pull request!


## EXAMPLES:

1) Compare 50lb pound of oatmeal that's 74.99 to a 25kg of oatmeal that 43.99

`python food.py --check --food=oatmeal --serving-size=80 --serving-measurement=grams --quantity=50 --price=74.99 --unit=pounds`
`python food.py --check --food=oatmeal --serving-size=80 --serving-measurement=grams --quantity=25 --price=43.99 --unit=kilograms`

2) You saved $3 in yogurt this cycle (was 12.99, now 9.99).  You want to update
that price.  You buy 16 pre-packaged cups at once.

`python food.py --store --food=yogurt --price=9.99 --quantity=16 --unit=servings`

3) You want to see a report on your food-plan

`python food.py --overview`
