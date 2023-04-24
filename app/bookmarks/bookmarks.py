from app.bookmarks import bookmarks

@bookmarks.route('/')
def register():
    return "Success"