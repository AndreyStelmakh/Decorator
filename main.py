
from datetime import datetime


def decorator_logger(function):
    def new_function(*args, **kwargs):

        with open("log.txt", 'a', encoding='UTF-8') as f:
            f.write(f'{str(datetime.now())} {function.__name__} аргументы: {args} ')
            result = function(*args, **kwargs)
            f.write(f'результат: {result}\n')

        return result

    return new_function


def decorator_logger_path(log_file_name='log.txt'):
    def decorator_logger(function):
        def new_function(*args, **kwargs):

            with open(log_file_name, 'a', encoding='UTF-8') as f:
                f.write(f'{str(datetime.now())} {function.__name__} аргументы: {args} ')
                result = function(*args, **kwargs)
                f.write(f'результат: {result}\n')

            return result

        return new_function
    return decorator_logger


@decorator_logger_path('log.txt')
def func(name, len):
     return f'{name}: {len} {"*"*len}'


if __name__ == '__main__':
    func('звёздочки', 20)

    func('веб-скрапинг', 25)
