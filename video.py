import uuid

class VideoEpisode:

    def __init__(self, video_id, title, description, subtitle, summary, author, image_url, published, keywords, media_url, media_size, media_duration, position):
        self.video_id = f"DOBR:{str(uuid.uuid4())}"
        # self.id11 = video_id

        self.title = title
        self.description = description
        self.subtitle = subtitle
        self.summary = summary
        
        self.author = author
        self.image_url = image_url
        self.published = published
        self.keywords = keywords

        self.position = position
        self.media_size = media_size
        self.media_duration = media_duration 
        self.media_url = media_url


    def __str__(self):
        return (f"""videoid: {self.video_id} \n""" 
                f"""title: {self.title} \n"""
                f"""description: {self.description} \n"""
                f"""title: {self.subtitle} \n"""
                f"""summary: {self.summary} \n"""
                f"""author: {self.author} \n"""
                f"""thumb: {self.image_url} \n"""
                f"""published: {self.published} \n"""
                f"""keywords: {self.keywords} \n"""

                f"""position: {self.position} \n"""
                f"""media_size: {self.media_size} \n"""
                f"""media_duration: {self.media_duration} \n"""
                f"""media_url: {self.media_url} \n"""

                # f"""rating: {self.rating}"""
                # f"""view count: {self.viewcount}"""
                # f"""likes: {self.likes}"""
                # f"""dislikes: {self.dislikes}"""

        )


    
    def __repr__(self):
        pass