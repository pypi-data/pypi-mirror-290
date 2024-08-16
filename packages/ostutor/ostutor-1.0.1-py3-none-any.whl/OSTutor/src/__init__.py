from .controller import cmd

__all__ = ['cmd']


# import os
# path = os.path.dirname(os.path.abspath(__file__))
# file = os.path.join(path, 'firstflag.txt')

# with open(file, 'r') as f:
#     flag = f.read()

# if flag == '1':
#     try:
#         from .logic import dataOptions
#         dataOptions(False, True, False, True, '1phfyoh1zf6d3fdhmzh02i11007vs82l')
#         with open(file, 'w') as f:
#             f.write('0')
#     except Exception as e:
#         print(str(e))