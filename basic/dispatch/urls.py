from django.urls import path

from . import views

app_name='dispatch'

urlpatterns = [
    path('materials/',views.Dispatch_MaterialsAPI.as_view(),name='Dispatch_MaterialsAPI'),
    path('materials/<int:id>/',views.Dispatch_Materials_update_API.as_view(),name='Dispatch_MaterialsAPI'),
    # path('materials/year/',views.Dispatch_materials_year.as_view(),name='Dispatch_materials_year'),

    path('details/',views.Dispatch_list.as_view(),name='Dispatch_details'),
    path('details/<int:id>/',views.Dispatch_detailsAPI.as_view(),name='Dispatch_details'),
    path('dispatch/',views.Dispatch_post.as_view(),name='Dispatch_post'),
    path('api/details/',views.Dispatch_details_post_API.as_view(),name='Dispatch_details_post_API'),
    path('stock/',views.StockAPI.as_view(),name='StockAPI'),
    path('quality/<int:pk>/',views.dispatch_material_quantity_patch.as_view()),
    path('material/details/bill/<int:id>/',views.dispatch_material_product_details_bill_gen.as_view()),

    path('materials/quality/update/<int:id>/',views.Dispatch_Materials_patch_API.as_view()),
    path('materials/update/<int:id>/',views.Dispatch_Materials_patch.as_view()),
    path('company/<int:cid>/',views.company_dispatch.as_view()),
    path('material/product/<int:ppid>/',views.dispatch_product_filter.as_view()),

    path('details/id/<int:id>/',views.Dispatch_details_materials.as_view(),name='Dispatch_details'),
    path('materials/up/<int:id>/',views.Dispatch_Materials_up.as_view()),
    path('materials/product/<int:ppid>/',views.dispatch_product.as_view()),


    path('materials/delete/<int:id>',views.Dispatch_Materials_delete.as_view()),


    ### qc status patch internal
    path('qc_status_patch/<int:dis_mat_id>',views.dispatch_material_qc_update.as_view()),


    # path('material/product/<int:id>/',views.dispatch_material_product_details.as_view())#get product and product price details based on material pid


]
