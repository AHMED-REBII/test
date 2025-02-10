import base64
import re

import requests
from werkzeug import urls

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # -------------------------------------------------------------------------
    # CONSTRAINS METHODS
    # -------------------------------------------------------------------------

    @api.constrains("email")
    def _check_valid_email(self):
        """Validate the email format of the records."""
        email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        for rec in self:
            if rec.email and not re.match(email_regex, rec.email):
                raise ValidationError(
                    _("Invalid email address! Please provide a valid email.")
                )

    @api.constrains("website")
    def _check_valid_website(self):
        """Validate the website URL format of the records."""
        website_regex = (
            r"^(?:https?:\/\/)?(?:www\.)?(?!www\."
            r"[a-zA-Z0-9_-]+\.[a-zA-Z]{2,})(?:[a-zA-Z0-9_-]"
            r"+\.)+[a-zA-Z]{2,}(?:\/[a-zA-Z0-9_\-\/\.]*)?$"
        )
        for rec in self:
            if rec.website and not re.match(website_regex, rec.website):
                raise ValidationError(
                    _("Invalid website url! Please provide a valid website url.")
                )

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def _clean_website(self, website):
        url = urls.url_parse(website)
        if not url.scheme:
            if not url.netloc:
                url = url.replace(netloc=url.path, path="")
            # Start batch : add 'www.' if missing from hostname
            if "www." not in url.netloc:
                url = url.replace(netloc=f"www.{url.netloc}")
            # End batch
            website = url.replace(scheme="http").to_url()
        return website

    def _find_logo(self, param):
        url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_logo_finder_param", "https://logo.clearbit.com/")
        )
        url += param
        result = False
        try:
            response = requests.get(url, timeout=10)  # Adjust timeout as needed
            if response.status_code == 200:
                request_content = response.content
                url_base64 = base64.b64encode(request_content)
                result = url_base64
        except requests.exceptions.RequestException as e:
            raise ValidationError(_("Error fetching logo: %s") % e) from e
        return result

    def set_logo(self):
        result = False
        # find logo of partner by email
        if self.email:
            url = self.email.split("@", 1)[1]
            result = self._find_logo(url)
            if not result:
                raise ValidationError(
                    _("The company's logo could not be found from the email.")
                )
        # If the logo is not found by email, try by website
        if not result and self.website:
            website_format = self._clean_website(self.website)
            url = website_format.split("www.", 1)[1]
            result = self._find_logo(url)
            if not result:
                raise ValidationError(
                    _("The company's logo could not be found from the website.")
                )
        self.image_1920 = result
