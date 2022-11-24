class Test:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    @property
    def nick_name(self):
        return self._nick_name

    @nick_name.setter
    def nick_name(self,name):
        self._nick_name=name

name = input().split()
obj1 = Test('dong han',19)
obj1.nick_name=name
print(obj1.nick_name)
obj1._nick_name = 'error'
print(obj1.nick_name,obj1._nick_name)