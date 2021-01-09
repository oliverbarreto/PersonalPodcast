class Channel:

    def __init__(self, name, description, website, explicit, 
        image, copyright, language, feed_url, category, authors, authors_email, owner, owner_email):


        self.name          = name
        self.description   = description
        self.website       = website
        self.explicit      = explicit
        self.image         = image

        self.copyright     = copyright
        self.language      = language
        self.feed_url      = feed_url
        self.category      = category
        
        # self.xslt        = xslt

        self.authors       = authors
        self.authors_email = authors_email
        self.owner         = owner
        self.owner_email   = owner_email
    
    @classmethod
    def defaultChannel(cls):

        return cls(name = "Oliver's Personal Podcast", 
        description     = "I publish interesting things i like to listen to!!!", 
        website         = "http://oliverbarreto.com/", 
        explicit        = True, 
        image           = "http://oliverbarreto.com/images/site-logo.png", 
        copyright       = "", 
        language        = "es-ES", 
        feed_url        = "https://raw.githubusercontent.com/oliverbarreto/PersonalPodcast/main/feed.xml",
        category        = "News", 
        authors         = "Oliver Barreto", 
        authors_email   = "oliver.barreto.online@gmail.com",
        owner           = "Oliver Barreto",
        owner_email     = "oliver.barreto.online@gmail.com"
    )

