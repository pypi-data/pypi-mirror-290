# jajucha/module.py


# function to do accomplished 
'''
    //control parts ->
    0. jajucha.control(0,0,0) // +-20 , +-50
    0. jajucha.get_speed()
    2. img = jajucha.get_img()
    3. jajucha.sendimg()
'''



class Jajucha:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"
