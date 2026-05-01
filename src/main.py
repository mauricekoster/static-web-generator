import sys
from utils import copy_static_assets, generate_pages_recursive


if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = '/'


copy_static_assets()

generate_pages_recursive('content', 'template.html', 'docs', basepath)