import time

from django.test import override_settings
from django.urls import path


from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


class BrowserEventDispatcher(Component):
    def mount(self):
        self.dispatch_browser_event("test", {"value": 123})

    def inline_template(self):
        return """
            <div>
                <div x-data>
                    <div x-on:test.window="console.log(`event called with payload: ${$event.detail.value}`)">Test</div>
                </div>
            </div>
        """


TestView = create_test_view(f"""
    {{% silica '{__name__}.BrowserEventDispatcher' %}}
    """)


urlpatterns = silica_urlpatterns + [
    path("dispatch-browser-events/", TestView.as_view()),
]


@override_settings(ROOT_URLCONF=__name__)
class DispatchBrowserEventTestCase(SilicaBrowserTestCase):

    def test_browser_event_received(self):
        self.selenium.get(self.live_server_url + '/dispatch-browser-events')
        time.sleep(0.4)
        console_log = self.get_console_log()
        self.assertTrue("event called with payload: 123" in console_log[0]['message'])
