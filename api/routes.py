from django.urls import path,include
from .api import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("api/categories",CategoryView)
router.register("api/products",ProductsView)
router.register("api/orderitem",OrderItemView)
router.register("api/orders",OrderAdminView)


app_name = 'api'
urlpatterns = [
    path("api/users",UsersListView.as_view(),name="users"),
    path("",include(router.urls)),
    path("api/productslist",ProductListView.as_view(),name="prod-list"),
    path("api/authtoken",ObtainAuthTokenView.as_view(),name="authtoken"),
    path("api/productdetail/<int:pk>",ProductDetailView.as_view(),name="product-detail"),
    path("api/ordercreate",OrderCreateView.as_view(),name="order-create")
  

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
