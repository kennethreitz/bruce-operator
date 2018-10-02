class App:
    def __init__(self, name):
        self.name = name
        self.auto_deploy_last_release = None
        self.repo = None

    @classmethod
    def from_info(kls, app_info):
        self = kls(name=app_info["metadata"]["name"])
        self.auto_deploy_last_release = app_info["spec"].get("auto_deploy_last_release")
        self.repo = app_info["spec"].get("repo")

        return self
