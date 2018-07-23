class JobOffer(object):
    """ A job offer contains the following properties:
        url: Url of the job offer
        position = A text explaining the offer
        company = The company offering the position
        date = Date of the offer
        tags = Some extra information in the form of tags
    """

    def __init__(self, url, position, description, company, date, tags):
        self.url = url
        self.position = position
        self.description = description
        self.company = company
        self.date = date
        self.tags = tags