from .api.spartaqube import Spartaqube as SpartaqubeAPI


class Spartaqube:

    def __init__(self, api_key=None):
        self = SpartaqubeAPI(api_key=api_key)

#END OF QUBE
