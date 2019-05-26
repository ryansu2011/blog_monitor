import sys
import os
import pathlib
import inspect

# must be direct call
if __name__ != '__main__':
    print(__name__, '__main__', (__name__ is not '__main__'))
    raise Exception("Run this config directly. Do not import.")

# go to root directory, add root to path
main_path_str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
main_path = pathlib.Path(main_path_str)
for i in range(10):
    if main_path.name != "blog_monitor":
        main_path = main_path.parent
if main_path.name != "blog_monitor":
    raise Exception("Error locating the root directory of 'blog_monitor' project.")
root_path_str = main_path.__str__()
os.chdir(root_path_str)
sys.path.insert(0, root_path_str)
print("Info: added root directory to path. ({})\n".format(root_path_str))

# make and go into temp folder
if not os.path.exists('./temp') or not os.path.isdir('./temp'):
    os.mkdir('./temp')
os.chdir('./temp')
print("Info: current working folder is ({})\n".format(os.getcwd()))

# get tested component
if sys.argv.__len__() <= 1:
    raise Exception("Add component name you want to test.")
component_name = sys.argv[1]

# start testing
if component_name == "notifier":
    import test.notifier as tst
elif component_name == "scraper":
    import test.scraper as tst
elif component_name == "timer":
    import test.timer as tst
else:
    raise Exception("Error: unrecogonized argument.")
tst.start_test()

