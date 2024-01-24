# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import namedtuple
from html.parser import HTMLParser

from contrast.agent.settings import Settings
from contrast_vendor import structlog as logging
from contrast.utils.string_utils import ensure_string

logger = logging.getLogger("contrast")

Tag = namedtuple("Tag", ["type", "tag", "attrs"])


def analyze_response_rules(context):
    settings = Settings()

    response_rules = settings.enabled_response_rules()
    response = context.response
    if response is None or response.body is None:
        return

    body = ensure_string(response.body)

    if not response_rules or not body:
        return

    content_type = response.headers.get("content-type", "")

    status_code = response.status_code
    valid_response_rules = [
        rule for rule in response_rules if rule.is_valid(status_code, content_type)
    ]

    if not valid_response_rules:
        return

    form_tags, meta_tags = get_tags(body)

    for rule in valid_response_rules:
        violated, properties = rule.is_violated(
            response.headers, body, form_tags, meta_tags
        )
        if violated:
            rule.build_and_append_finding(properties, context)


def get_tags(body):
    form_tags, meta_tags = [], []

    class BodyParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "form":
                form_tags.append(
                    Tag(type="form", tag=self.get_starttag_text(), attrs=attrs)
                )
            if tag == "meta":
                meta_tags.append(
                    Tag(type="meta", tag=self.get_starttag_text(), attrs=attrs)
                )

    parser = BodyParser()
    parser.feed(body)

    return form_tags, meta_tags
