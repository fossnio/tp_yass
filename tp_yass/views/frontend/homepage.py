from pyramid.view import view_config

from tp_yass.views.helper.navbar import generate_navbar_trees
from tp_yass.dal import DAL


@view_config(route_name='homepage', renderer='themes/default/frontend/homepage.jinja2')
def homepage_view(request):
    return {'news_list': DAL.get_latest_news(int(request.sys_config['site_homepage_news_quantity'])),
            'navbar_trees': generate_navbar_trees(visible_only=True)}
