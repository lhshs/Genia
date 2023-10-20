# 1. 일반  클래스 ================================
#
# class Student:
#     pass
#
# a = Student()
# b = Student()
# print(id(a), id(b))
# print(a is b)          # False, 두개의 클래스는 다른 변수에 저장됨
# exit()


# =============================================
# 2. 일반  클래스 (객체가 생성될 때 불리는 함수 표현)
#
# 우리는 클래스 선언시에 __init__ 만 많이 작성하지만
# 실제로 클래스 객체를 생성하는 함수는 __new__ 이고
# 그 뒤에 __init__ 이 호출되서 클래스 변수를 세팅합니다.
# __new__ 를 선언 안해주면 자동으로 __new__를 호출하기 때문에
# 대부분 선언하지 않는 것
#
# class Foo(object):
#
#     # 구현되어 있는 default 객체 생성 함수
#     # 객체를 생성해서 리턴하는 instance 라는 변수가 self 변수가 아니라
#     # 그냥 없어지는 변수임
#     def __new__(cls, *args, **kwargs):
#         print("__new__ is called\n")
#         instance = super().__new__(cls)
#         return instance
#
#     def __init__(self):
#
#         self.a = "test"
#         print(f"__init__ is called : {self.a}\n")

# 그래서 생성 될 때 instance 생성하고 return (s1)
# s1 = Foo()
# 그래서 생성 될 때 instance 생성하고 return (s2)
# s2 = Foo()
# s1, s2 같은 함수를  호출할 때마다 독립 변수가 메모리에 할당됨
# 메모리 낭비!
# print(s1)
# print(s2)
# print(s1 is s2)


# =============================================
# 2. 싱글톤 구현
#
# 거창한 게 아니라 default __new__ 함수에 약간 기법을 추가해 준 것
# cls(self 랑 비슷한 거라고 봐도 됨, 객체가 생성 되지 않고 클래스 일때의 내부 변수)
# 클래스 객체가 최초 생성될 때
# _instance 를 클래스 내부에 변수를 만들고 객체를 저장해 둠
class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # Foo 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self):
        print("__init__ is called\n")             # __init__ 으로 초기화하는 것 같지만 이것은 변수 세팅
                                                  # 실제로는 __new__ 로 클래스 객체가 생성됨

# 그래서 최초 객체 생성 이후에
s1 = Singleton()
# 또 다시 객체를 생성할 때 클래스 내부에 _instance 가 있으면
# 또 다른 변수를 생성하지 않고 이미 메모리에 있는 객체를 리턴함
s2 = Singleton()
print(s1)
print(s2)
# 그래서 s1, s2 는 변수는 다르지만 같은 메모리에 클래스 객체를 참조하고 있음
print(s1 is s2)   # True
exit()


# =============================================
# 3. 실제 내 클래스에 적용
#
# 내가 구현한 클래스에 싱글톤 __new__ 함수 갖다 두면 됨니다
# 문법이 아니기 때문에 사람들이 비슷비슷하게 구현해둔 것
# 동작만 잘 하면 굿 !


# 적용 예시)
import os
import shutil


class Files(object):

    # 짜잔
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super(Files, self).__init__()
        self.name = "Files"

    def print_class(self,):
        print(f"this class name is {self.name}")

    @staticmethod
    def exists(target):
        return os.path.exists(target)

    @staticmethod
    def rm(target):
        if os.path.isdir(target):
            return shutil.rmtree(target)
        if os.path.isfile(target):
            return os.remove(target)
        if os.path.islink(target):
            return os.unlink(target)

    def mkdir(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self.mkdir(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def cp(source, target):
        if os.path.isdir(source):
            return shutil.copytree(source, target)
        return shutil.copy(source, target)