import pinboard


pb = pinboard.Pinboard('lsanz_observatorio:CC8E7F9E71CC9B935378')

def obtener_posts():
    posts = pb.posts.recent(tag=["starred", "pivotWeek"])