Profile assets
==============

Edit .github/profile/profile-content.json to change the three typing lines,
LinkedIn URL, project names, descriptions, categories, or tags.

Regenerate on Windows with Python, Pillow and NumPy:
  python -m pip install pillow numpy
  python .github/profile/build_profile.py

The script rebuilds the local GIF, SVG assets, and README. It uses local Windows
fonts and does not depend on an external badge or animation service.

The four cards are a curated snapshot of the most recently updated public
projects. They do not automatically modify or synchronize GitHub's pinned list.
The LinkedIn button is intentionally unlinked while its URL is unset.
