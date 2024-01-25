"""
    This is inheritance
"""
from inheritance.post import Review, Article


"""
    This is garden package, all the modules are imported from there.
"""
# importing modules from garden package
from garden_package.plants.tree import Tree
from garden_package.plants.flower import Flower
from garden_package.weather.weather import Weather


"""
    this portion is importing all stand alone modules form modules folder
"""
from modules.lights import LightsController
from modules.temperature import TemperatureController
from modules.security import SecuritySystem

"""
    Persistence from json
"""
from PersistenceJson.data import load_json

def main():
    """
        This is using inheritance 
    """
    
    print("\n-----------This is implemenation of Inheritance------------\n")
    
    article = Article("Python Inheritance", "Explaining inheritance in Python.", "Dr. Shelby", "Programming")
    article.display_article()

    # print("\n")

    review = Review("Movie Review", "A fantastic movie!", "Tommy Shelby", 5)
    review.display_review()

    """
    This is portion is using all modules from garden package.
    """

    print("\n-----------This is implemenation of package------------\n")
    # creating instace of classes/modules from garden package
    neem_tree = Tree("Neem", 7)
    rose = Flower("Rose", "red")
    cloudy_day = Weather("cloudy")
    
    neem_tree.grow()
    rose.bloom()
    cloudy_day.report()

    """
        This portion is using stand alone modules.
    """
    print("\n-----------This is implemenation of stand alone modules------------\n")
    
    living_room_lights = LightsController("living room")
    living_room_temp = TemperatureController("living room", 22)
    security_system = SecuritySystem()

    living_room_lights.toggle_lights()
    living_room_temp.adjust_temperature(25)
    security_system.arm()
    
    
    print("\n-----------This is implemenation of persistence from json------------\n")
    load_json()
    
if __name__ == "__main__":
    main()




