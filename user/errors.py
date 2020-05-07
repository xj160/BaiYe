class NullError(Exception):
    def __init__(self, *args):
        self.args = args
class lengthError(Exception):
    def __init__(self,code=None,message='长度错误！',args=('长度错误！',)):
        self.args = args
        self.code = code
        self.message = message

class naneNullError(NullError):
    def __init__(self,code = 1300, message = '昵称为空', args = ('昵称为空',)):
        self.args = args
        self.code = code
        self.message = message
