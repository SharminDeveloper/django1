from rest_framework import permissions
class UserIsEqualToAuthor(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        name = view.model._meta.model_name.lower()
        if request.method == 'GET':
            request.user.has_perm(f'{name}s.view_{name}')
        elif request.method == 'POST':
            request.user.has_perm(f'{name}s.add_{name}')
        else:
            if view.pk:
                the_object = view.model.objects.get(id = view.pk)
                author = str(the_object.author) 
                if author != view.token_user:
                    return False
                request.user.has_perm(f'{name}s.change_{name}')
                request.user.has_perm(f'{name}s.delete_{name}')
        return True