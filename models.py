import hashlib


class JobOffer(object):
    """ A job offer contains the following properties:
        id = Unique id that identifies the job offer
        url = Url of the job offer
        position = A text explaining the offer
        company = The company offering the position
        date = Date of the offer
        tags = Some extra information in the form of tags
    """

    def __init__(self, url, position, description, company, date, tags):
        self.hash = generate_hash(url, position, description, company)
        self.url = url
        self.position = position
        self.description = description
        self.company = company
        self.date = date
        self.tags = tags


def generate_hash(url, position, description, company):
    hash_input = url + "#" + position + "#" + description + "#" + company
    encoded_hash_input = str.encode(hash_input)

    return hashlib.sha3_256(encoded_hash_input).hexdigest()
