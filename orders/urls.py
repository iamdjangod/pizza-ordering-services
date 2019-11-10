from django.urls import path

from orders import views

urlpatterns = [
    path(
        '',
        views.OrderCreateListView.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='create-list-orders'
    ),

    path(
        '<int:pk>',
        views.OrderRetrieveDeleteView.as_view({
            'get': 'retrieve',
            'delete': 'destroy'
        }),
        name='retrieve-delete-order'
    ),

    path(
        '<int:pk>/status',
        views.OrderRetrieveUpdateStatusView.as_view({
            'get': 'retrieve',
            'put': 'update'
        }),
        name='retrieve-update-order-status'
    ),

    path(
        'detail/<int:pk>',
        views.OrderDetailsUpdateView.as_view({
            'put': 'update'
        }),
        name='update-order-details'
    ),
]
