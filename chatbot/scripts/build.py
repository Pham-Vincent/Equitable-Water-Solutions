import os


# Creates File Structure For a Project
def buildProject(projectName: str = "Default"):
    projectName = "../projects/" + projectName
    os.mkdir(projectName)
    os.mkdir(projectName + "/data")
    os.mkdir(projectName + "/docs")
    os.mkdir(projectName + "/docs/unloaded")
    os.mkdir(projectName + "/docs/loaded")


buildProject("Salinity")
