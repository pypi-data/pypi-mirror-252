from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_navbar import Navbar, NavbarItem, site_navbars
from edc_review_dashboard.navbars import navbar_item as review_navbar_item

no_url_namespace = False  # True if settings.APP_NAME == "intecomm_dashboard" else False

navbar = Navbar(name="intecomm_dashboard")


navbar.append_item(
    NavbarItem(
        name="screen_group",
        title="Screen/Group",
        label="Screen/Group",
        fa_icon="fa-solid fa-user-plus",
        codename="edc_screening.view_screening_listboard",
        url_name="screen_group_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(
    NavbarItem(
        name="community_followup",
        title="Community",
        label="Community",
        fa_icon="fa-solid fa-users-between-lines",
        codename="edc_subject_dashboard.view_subject_listboard",
        url_name="followup_community_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(
    NavbarItem(
        name="facility_followup",
        title="Facility",
        label="Facility",
        fa_icon="fa-solid fa-user-circle",
        codename="edc_subject_dashboard.view_subject_listboard",
        url_name="followup_facility_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(review_navbar_item)
navbar.append_item(tmg_navbar_item)
navbar.append_item(ae_navbar_item)
navbar.append_item(dm_navbar_item)

site_navbars.register(navbar)
