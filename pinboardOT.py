import pinboard


pb = pinboard.Pinboard('lsanz_observatorio:CC8E7F9E71CC9B935378')

def obtener_posts():
    posts = pb.posts.recent(tag=["publishedOT", "d:201903"])
    #print(posts)
    for k,v in posts.items():
        print(k,v)