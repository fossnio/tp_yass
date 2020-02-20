from .resources import (auth_user_factory,
                        admin_factory)

def includeme(config):
    config.add_static_view('static', 'tp_yass:themes/default/static', cache_max_age=3600)

    # frontend
    config.add_route('homepage', '/')
    config.add_route('news_list', '/news/list')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # backend
    config.add_route('backend_homepage', '/backend/', factory=auth_user_factory)
    config.add_route('backend_sys_config_edit', '/backend/sys/config/edit', factory=auth_user_factory)
    config.add_route('backend_navbar_list', '/backend/navbar/list', factory=admin_factory)
    config.add_route('backend_user_list', '/backend/user/list', factory=admin_factory)
    config.add_route('backend_user_group_list', '/backend/user/group/list', factory=admin_factory)
