# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ValueMixin, fields
from trytond.pool import PoolMeta

default_country = fields.Many2One('country.country', 'Default Country')


class Configuration(metaclass=PoolMeta):
    __name__ = 'party.configuration'
    default_country = fields.MultiValue(default_country)


class ConfigurationCountry(ModelSQL, ValueMixin):
    'Party Configuration Country'
    __name__ = 'party.configuration.default_country'
    default_country = default_country
