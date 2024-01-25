class Constant:
    #################App para
    app_name = ""

    def get_verbose_name(self, table_name, verbose_name=app_name):
        return verbose_name + "." + table_name
