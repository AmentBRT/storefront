from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from . import views


router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = NestedSimpleRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = NestedSimpleRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-item')

urlpatterns = router.urls + products_router.urls + carts_router.urls
