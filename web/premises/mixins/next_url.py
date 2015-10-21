class NextURLMixin(object):
    # todo: find a proper way to handle this and remove this mixin
    def get_view_name(self):
        view = self.request.GET.get("view")
        return view if view in ["tree", "list"] else ""

    def get_next_parameter(self):
        if self.get_view_name() == "list":
            return "?view=list"
        return ""
