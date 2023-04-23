class BaseArtifact:
    def __init__(self, main_stat, main_stat_value):
        self.main_stat = main_stat
        self.main_stat_value = main_stat_value

class Artifact:
    def __init__(self, main_stat, sub_stats):
        self.main_stat = main_stat
        self.sub_stats = sub_stats