from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_parameter_type


class LanguageAwareSchema(AutoSchema):
    def _get_global_language_parameters(self):
        return [
            build_parameter_type(
                name='Accept-Language',
                location='header',
                schema={'type': 'string', 'enum': ['ru', 'en', 'uz']},
                description='Response language. Defaults to ru.',
                required=False,
            ),
            build_parameter_type(
                name='lang',
                location='query',
                schema={'type': 'string', 'enum': ['ru', 'en', 'uz']},
                description='Override response language via query parameter.',
                required=False,
            ),
        ]

    def get_override_parameters(self):
        # merge parent params with our global ones
        params = super().get_override_parameters() or []
        return [*params, *self._get_global_language_parameters()]
