# -*- coding: utf-8 -*-

import datetime
import logging
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, FileSystemLoader
from redtrics.core.filters import format_datetime
from redtrics.core.settings import email
from redtrics.metrics import registry
from redtrics.utils.decorators import catch_exceptions


class Runner(object):

    def __init__(self, base='master'):
        self.logger = logging.getLogger(__name__)
        self.base = base

    @catch_exceptions
    def run(self):
        self.logger.info("Running redtrics")

        self.today = datetime.datetime.now()
        results = {}

        for metric in registry.MetricRegistry.METRICS_LIST:
            results[metric.name] = metric.run(self.base)

        self._send_email(results)

        self.logger.info("Finished redtrics")

    def _get_template_loader(self):
        if os.path.exists('/opt/redtrics/templates/mail.html'):
            return FileSystemLoader('/opt/redtrics/templates')
        return PackageLoader('redtrics', 'templates')

    def _render_template(self, results):
        env = Environment(loader=self._get_template_loader())
        env.filters['format_datetime'] = format_datetime
        return env.get_template('mail.html').render(today=self.today, base=self.base, **results)

    def _send_email(self, results):
        mail = self._render_template(results)
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Tech Weekly Metrics - Week#%s' % format_datetime(self.today, "w")
        message['From'] = '%s <%s>' % (email['from_name'], email['from_email'])
        message['To'] = ', '.join(email['to'])
        message.attach(MIMEText(mail, 'html'))
        server = smtplib.SMTP(email['smtp_host'], email['smtp_port'])
        server.sendmail(email['from_email'], email['to'], message.as_string())
        server.quit()
        self.logger.info("Sent email to {}".format(email['to']))
