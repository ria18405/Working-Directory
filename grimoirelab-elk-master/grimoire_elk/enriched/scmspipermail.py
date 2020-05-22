from .scmsmbox import ScmsMboxEnrich


class ScmsPipermailEnrich(ScmsMboxEnrich):
    def get_project_repository(self, eitem):
        return eitem['origin']
