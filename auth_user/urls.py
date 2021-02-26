from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            )

from auth_user.views import (
    APIAuthCodeRequestViewSet,
    APIAuthConfirm,
    APIUserProfileViewSet,
)

users_router = DefaultRouter()
users_router.register('users', APIUserProfileViewSet, basename='users')

urlpatterns = [
    path('auth/email/',
         APIAuthCodeRequestViewSet.as_view({'post': 'create'})),

    path('auth/token/', APIAuthConfirm.as_view({'post': 'create'})),


    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns += [
    path('v1/', include(users_router.urls)),
]
