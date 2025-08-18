from rcssmin import cssmin
import os

# Always resolve relative to this script’s location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

css_files = [
    'css/animate.css',
    'css/adImplant1.css',
    'css/responsive.css',
    'css/banner.css',
    'css/blog.css',
    'css/magnific-popup.css',
    'css/menu.css',
    'css/product.css',
    'css/style.css',
    'css/timetable.css',
    'css/web_story.css',
    'css/zir.css',
    'css/bootstrap1.min.css'
]
# css_files = [
#     'css/style.css'
# ]
for css_path in css_files:
    full_css_path = os.path.join(BASE_DIR, css_path)

    if not os.path.exists(full_css_path):
        print(f" File not found: {full_css_path}")
        continue

    with open(full_css_path, 'r') as css_file:
        original_css = css_file.read()

    minified_css = cssmin(original_css)

    minified_path = full_css_path

    with open(minified_path, 'w') as minified_file:
        minified_file.write(minified_css)

    print(f"Overwrote with minified: {css_path}")

print("All CSS minified!")
