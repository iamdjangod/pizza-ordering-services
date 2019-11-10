from django.urls import path

from pizzas import views

urlpatterns = [
    path(
        '',
        views.PizzaCreateListView.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='create-list-pizzas'
    ),

    path(
        '<int:pk>',
        views.PizzaUpdateView.as_view({
            'put': 'update'
        }),
        name='update-pizzas'
    )
]
