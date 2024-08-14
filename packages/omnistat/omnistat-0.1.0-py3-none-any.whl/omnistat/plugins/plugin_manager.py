class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin.register()

    def execute_plugins(self, *args, **kwargs):
        for plugin in self.plugins:
            plugin.execute(*args, **kwargs)