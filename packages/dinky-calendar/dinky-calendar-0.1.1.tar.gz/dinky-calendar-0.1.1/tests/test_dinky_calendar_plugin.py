from dinky_calendar import DinkyCalendarPlugin

def test_dinky_calendar_plugin_init():
    plugin = DinkyCalendarPlugin('url', 'username', 'password', 'timezone')
    assert plugin.url == 'url'
    assert plugin.username == 'username'
    assert plugin.password == 'password'
    assert plugin.timezone == 'timezone'
