from django.urls import path

from sfacd.gis.views.IndexView import IndexView
from sfacd.gis.views.DashboardView import DashboardView
from sfacd.gis.views.MapsView import MapsView
from sfacd.gis.views.LargeMapsView import LargeMapsView
from sfacd.gis.views.ChartsView import ChartsView
from sfacd.gis.views.CalendarView import CalendarView
from sfacd.gis.views.CreateAttackListView import CreateAttackListView
from sfacd.gis.views.CreateCustomerMarkerView import CreateCustomerMarkerView
from sfacd.gis.views.GetEachStaffListView import GetEachStaffListView
from sfacd.gis.views.ReadLayerView import ReadLayerView
from sfacd.gis.views.DetailAttackListView import DetailAttackListView
from sfacd.gis.views.SearchCustomerView import SearchCustomerView
from sfacd.gis.views.CreateMyListMarkerView import CreateMyListMarkerView
from sfacd.gis.views.SearchAllCustomerView import SearchAllCustomerView
from sfacd.gis.views.CreateRouteCustomerView import CreateRouteCustomerView
from sfacd.gis.views.MainMapView import MainMapView
from sfacd.gis.views.RefineSearchCustomerView import RefineSearchCustomerView
from sfacd.gis.views.CreateMainMapMarkerView import CreateMainMapMarkerView
from sfacd.gis.views.CustomerListView import CustomerListView
from sfacd.gis.views.FavouriteListView import FavouriteListView
from sfacd.gis.views.CustomerDetailView import CustomerDetailView
from sfacd.gis.views.CreateAddMyListMarkerView import CreateAddMyListMarkerView
from sfacd.gis.views.ReadCsvView import ReadCsvView
from sfacd.gis.views.GetShopDetailDataView import GetShopDetailDataView
from sfacd.gis.views.GetShopLatLngView import GetShopLatLngView


app_name = "gis"
urlpatterns = [
    path("index", IndexView.as_view(), name="index"), #メインページ
    path("dashboard", DashboardView.as_view(), name="dashboard"), #活用なし
    path("maps", MapsView.as_view(), name="maps"), #活用なし
    path("large_maps", LargeMapsView.as_view(), name="large_maps"), #商圏分析
    path("large_maps/shop/detail", GetShopDetailDataView.as_view(), name="shop_detail"), #店舗詳細情報取得
    path("charts", ChartsView.as_view(), name="charts"), #活用なし
    path("calendar", CalendarView.as_view(), name="calendar"), #活用なし
    path("list/create", CreateAttackListView.as_view(), name="create_attack"), #活用なし
    path("list/ajax/search", SearchCustomerView.as_view(), name="search_customer"), #　営業支援側の顧客絞込機能
    path("ajax/create/customer", CreateCustomerMarkerView.as_view(), name="create_customer_marker"), #商圏分析マーカー絞込作成
    path("ajax/create/user", GetEachStaffListView.as_view(), name="create_user_list"), #商圏分析、店舗選択後の所属スタッフ表示の為
    path("ajax/get/shop/latlng", GetShopLatLngView.as_view(), name="get_shop_latlng"), #店舗検索し、マップ中央を変更するための特定1店舗の緯度経度を返す
    path("ajax/readLayer", ReadLayerView.as_view(), name="read_layer"), #レイヤーの標準偏差を求める際に使用
    path("list/detail", DetailAttackListView.as_view(), name="detail_attack"), #旧アタックリストの進捗確認ビュー
    path("list/detail/ajax/create/customer", CreateMyListMarkerView.as_view(), name="create_mylist_marker"), #マイリストに登録されている顧客を返す
    path("list/detail/ajax/search/allcustomer", SearchAllCustomerView.as_view(), name="search_all_customer"), #リスト作成
    path("list/detail/ajax/search/routecustomer", CreateRouteCustomerView.as_view(), name="get_route_customer"), #旧アタックリストのメイン訪問先のfeatureを作成する
    path("sales/main/map", MainMapView.as_view(), name="main_maps"), #営業メインマップ
    path("sales/refine/search", RefineSearchCustomerView.as_view(), name="refine_search"), #営業絞込検索
    path("sales/main/map/marker", CreateMainMapMarkerView.as_view(), name="main_maps_marker"), #営業マーカー作成
    path("sales/list", CustomerListView.as_view(), name="customer_list"), #営業顧客一覧
    path("sales/favourite", FavouriteListView.as_view(), name="favourite_list"), #営業お気に入り
    path("sales/customer/detail", CustomerDetailView.as_view(), name="customer_detail"), #営業顧客詳細画面
    path("sales/customer/list/marker", CreateAddMyListMarkerView.as_view(), name="add_mylist_marker"), #新営業支援ページのマイリストマーカーを返す処理
    path("index/csv", ReadCsvView.as_view(), name="read_csv"), #CSV読込、GisCustomer作成処理
]
