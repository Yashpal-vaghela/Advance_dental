from jsmin import jsmin
import os
# js_files = [
#     'js/appointment-form.js',
#     'js/custom.js',
#     'js/comment-form.js',
#     'js/contact-form.js',
#     'js/hero-form.js',
#     'js/lazy.js',
#     'js/materialize.js',
#     'js/menu.js',
#     'js/sticky.js',
#     'js/swiper.js',
#     'js/timetable.js',
#     'js/wow.js'
# ]
js_files = [
    'js/contact-form.js'
]
for js_path in js_files:
    with open(js_path, 'r') as js_file:
        original_js = js_file.read()
    
    minified_js = jsmin(original_js)

    # Create output filename with .min.js
    base, ext = os.path.splitext(js_path)
    minified_path = f"{base}.min{ext}"

    # Save
    with open(minified_path, 'w') as minified_file:
        minified_file.write(minified_js)

    print(f" Minified {js_path} → {minified_path}")

print("All done!")
