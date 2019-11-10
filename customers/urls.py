from django.urls import path

from customers import views

urlpatterns = [
    path(
        '',
        views.CustomerCreateListView.as_view({
            'post': 'create',
            'get': 'list'
        }),
        name='create-list-customers'
    ),

    path(
        '<int:pk>',
        views.CustomerUpdateView.as_view({
            'put': 'update',
        }),
        name='update-customers'
    )
]
