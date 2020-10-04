import pickle


from redis import Redis as _Redis
from pickle import UnpicklingError
from my_tt.config import REDIS

class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        '''带序列化处理的set方法'''
        pickled_data=pickle.dumps(value,pickle.HIGHEST_PROTOCOL)
        return super().set(name,pickled_data,ex,nx,xx)

    def get(self, name,default=None):
        '''带序列化处理的get方法'''
        pickle_data=super().get(name)
        if pickle_data is None:
            return default
        else:
            try:
                value=pickle.loads(pickle_data)
            except (KeyError,EOFError,UnpicklingError):
                return pickle_data
            return value
rds=Redis(**REDIS)