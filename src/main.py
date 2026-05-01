
from utils import copy_static_assets, generate_pages_recursive


copy_static_assets()

generate_pages_recursive('content', 'template.html', 'public')