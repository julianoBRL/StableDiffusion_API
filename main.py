from src.services.Server import server

#Controllers
from src.controllers.UserEndpoints import *
from src.controllers.SDEndpoints import *
from src.controllers.GalleryEndpoints import *

#Models
from src.models.UserModel import *
from src.models.ImageModel import *
from src.models.JobModel import *

if __name__ == '__main__':
    server.run()