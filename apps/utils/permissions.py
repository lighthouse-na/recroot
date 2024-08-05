from guardian.shortcuts import get_objects_for_user


def has_permission(self, request, obj, action):
    opts = self.opts
    code_name = f"{action}_{opts.model_name}"
    if obj:
        return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
    else:
        return self.get_model_objects(request).exists()


def get_model_objects(self, request, action=None, klass=None):
    opts = self.opts
    actions = [action] if action else ["view"]
    klass = klass if klass else opts.model
    model_name = klass._meta.model_name
    return get_objects_for_user(
        user=request.user,
        perms=[f"{perm}_{model_name}" for perm in actions],
        klass=klass,
        any_perm=True,
    )
