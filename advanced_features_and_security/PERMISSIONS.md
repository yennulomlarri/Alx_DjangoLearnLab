# Permission System Documentation

## Groups Created:
1. **Viewers**: can_view permission only
2. **Editors**: can_view, can_create, can_edit permissions
3. **Admins**: All permissions including can_delete

## Implementation Details:
- Custom permissions added to Book model Meta class
- Permission enforcement using @permission_required decorators
- Groups created and configured in Django admin
