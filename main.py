from src.services.Server import server

#Controllers
from src.controllers.UserEndpoints import *
from src.controllers.SDEndpoints import *
from src.controllers.GalleryEndpoints import *

#Models
from src.objects.UserModel import *
from src.objects.ImageModel import *
from src.objects.JobModel import *

if __name__ == '__main__':
    server.run()