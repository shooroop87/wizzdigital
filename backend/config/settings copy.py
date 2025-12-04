# config/settings.py - ИСПРАВЛЕНА СТРУКТУРА ШАБЛОНОВ
import io
import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "1insecure1-1default1")

# DEBUG
DEBUG = False

# ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split()

CSRF_TRUSTED_ORIGINS = [
    "https://*.wizzdigital.com",
    "https://wizzdigital.com",
    "http://localhost",
    "http://localhost:8000",
    "http://backend-1:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

# Приложения
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # 3rd party
    "easy_thumbnails",
    "filer",
    "mptt",
    "parler",
    "taggit",
    "meta",
    "tinymce",
    "core",
    "blog",
]
# Работает в связке с django.contrib.sites
# SITE_ID = 1

# Dev-only apps
if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",  # Основные шаблоны
            BASE_DIR / "blog" / "templates",  # Шаблоны блога
            BASE_DIR / "templates",  # Общие шаблоны
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "core.context_processors.default_schema",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "abroadtours"),
        "USER": os.getenv("POSTGRES_USER", "abroadtours_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": int(os.getenv("DB_PORT", 5432)),
    }
}

DEFAULT_CHARSET = "utf-8"
FILE_CHARSET = "utf-8"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "core" / "locale"]

# Static & media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_PERMISSIONS = 0o644  # rw-r--r--
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755  # rwxr-xr-x

# Создаем медиа-директорию если не существует
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Filer / thumbnails
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_QUALITY = 90
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Отключить строгий режи
# WHITENOISE_MANIFEST_STRICT = False

# Cache / static storages
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
else:
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

# НОВОЕ: Настройки для принуждения обновления браузерного кеша
# STATIC_CACHE_CONTROL = "public, max-age=3600"  # 1 час вместо года

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "your-smtp-server.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "your-email@domain.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "your-password")
DEFAULT_FROM_EMAIL = "Abroads Tours <noreply@wizzdigital.com>"
CONTACT_EMAIL = "abroadstour@gmail.com"

# Контакты
CONTACT_PHONE = "+39-339-2168555"
WHATSAPP_NUMBER = "393392168555"

# Misc
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# stdout fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {asctime} {message}", "style": "{"},
        "detailed": {
            "format": "🐛 {levelname} [{asctime}] {name} {module}:{lineno} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "detailed",
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "debug.log",
            "formatter": "detailed",
        },
        "media_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "media.log",
            "formatter": "detailed",
        },
        "blog_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "blog.log",
            "formatter": "detailed",
        },
        "core_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "core.log",
            "formatter": "detailed",
        },
        "reviews_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "reviews.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "core.views": {
            "handlers": ["core_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "blog": {
            "handlers": ["blog_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "blog.models": {
            "handlers": ["blog_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.core.files": {
            "handlers": ["media_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "PIL": {
            "handlers": ["media_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "ckeditor": {
            "handlers": ["media_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file_debug", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {"handlers": ["file_debug"], "level": "INFO", "propagate": False},
        "services.multi_reviews_service": {
            "handlers": ["reviews_file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


# ===================== DJANGO TINYMCE =====================

# Базовые настройки TinyMCE
# TINYMCE_API_KEY = 'f80axcxfwy4juoux11elmrxusxzpkbrz85w43nyvug2yta1a'
# TINYMCE_JS_URL = f"https://cdn.tiny.cloud/1/{TINYMCE_API_KEY}/tinymce/6/tinymce.min.js"
TINYMCE_JS_URL = "/static/tinymce/tinymce.min.js"
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = False


# Основная конфигурация (аналог CKEditor 5 'default')
TINYMCE_DEFAULT_CONFIG = {
    "height": 800,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    # для встроенных плагинов TinyMCE
    "plugins": """
        tableofcontents accordion advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table code 
        help wordcount table lists emoticons template codesample nonbreaking toc pagebreak
    """,
    "toolbar": """
        undo redo | styles | bold italic | accordion underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist | tableofcontents | outdent indent | link image media swipergallery | 
        table | template | removeformat code fullscreen help
    """,
    # external_plugins - для кастомных плагинов
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js",
        "tableofcontents": "/static/tinymce/plugins/tableofcontents/plugin.js",
    },
    "license_key": "gpl",
    "templates": [
        {
            "title": "CTA Button",
            "description": "Centered button",
            "content": """
                <p class="mt-30" style="text-align:center">
                    <a href="#" class="button -md -dark-1 bg-accent-1 text-white" title="..." aria-label="...">
                        Call to Action
                    </a>
                </p>
            """,
        },
        {
            "title": "Highlight Box",
            "description": "Highlighted content block with border and background",
            "content": """
                <div style="border: 1.5px solid #f8ebde; background: #f8f5f1; padding: 15px 20px; border-radius: 8px; margin: 30px 0;">
                    <div class="ck-content">
                        <p>Your highlighted content here...</p>
                    </div>
                </div>
            """,
        },
    ],
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    "image_advtab": True,
    "image_caption": True,
    "image_class_list": [
        {"title": "None", "value": ""},
        {"title": "Float Left", "value": "img-float-left"},
        {"title": "Float Right", "value": "img-float-right"},
        {"title": "Center", "value": "img-center"},
    ],
    "image_title": True,
    "image_toolbar": "alignleft aligncenter alignright | image",
    "automatic_uploads": True,
    "file_picker_types": "image",
    "images_upload_url": "/tinymce/upload/",
    "images_reuse_filename": False,
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol",
    "table_appearance_options": True,
    "table_grid": True,
    "table_resize_bars": True,
    "table_default_attributes": {"border": "1"},
    "table_default_styles": {"border-collapse": "collapse", "width": "100%"},
    "content_css": [
        "/static/css/tinymce-content.css",
    ],
    "content_style": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            padding: 20px;
        }
        .table-of-contents {
            background: #f5f5f5;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #333;
        }
        .table-of-contents h2 {
            margin-top: 0;
        }
        .table-of-contents ul {
            list-style: none;
            padding-left: 20px;
        }
        .table-of-contents a {
            text-decoration: none;
            color: #333;
        }
    """,
    # Разрешенные элементы
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        br,
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style|aria-label|aria-*|title],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label],
        details[open|class|style|data-*|role|aria-*],
        summary[class|style|data-*|role|aria-*],
        ul[class|style|data-*],
        li[class|style|data-*],
        p[class|style|data-*|aria-*],
    """,
    "valid_elements": "+i[class|style|data-*],+span[class|style|data-*]",
    "valid_classes": {
        "div": (
            "table-responsive table-stack stack-item image-gallery gallery-grid gallery-item media accordion-panel "
            "accordion -simple row y-gap-20 mt-30 js-accordion "
            "col-12 accordion__item px-20 py-15 border-1 rounded-12 "
            "accordion__button d-flex items-center justify-between "
            "button text-16 text-dark-1 "
            "accordion__icon size-30 flex-center bg-light-2 rounded-full "
            "accordion__content pt-20 ck-content "
        ),
        "img": "gallery-image",
        "table": "compact striped lake-como-table table-normal",
        "span": (
            "stack-label stack-value stack-header "
            "icon-plus icon-minus text-13 "
            "text-accent-1 text-success text-warning "
            "badge tag"
        ),
        "i": ("icon-plus text-13 " "icon-minus text-13 "),
        "h2": "text-30 md:text-24",
        "p": "mt-20 mt-30 text-center",
        "ul": "list-disc mt-20",
        "ol": "numbered-list mt-20",
        "details": "accordion -simple row y-gap-20 mt-30 js-accordion",
        "summary": "button text-16 text-dark-1",
        "a": "cta-button cta-button-outline button -md -dark-1 bg-accent-1 text-white mt-30",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": False,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    # "contextmenu": "link image table",
    "contextmenu": False,
    "verify_html": False,
    # Сохранение переносов строк и пустых абзацев
    "forced_root_block": "p",
    "force_br_newlines": False,
    "force_p_newlines": True,
    "remove_trailing_brs": False,
    "remove_linebreaks": False,
    "convert_newlines_to_brs": False,
    "keep_styles": True,
    "entity_encoding": "raw",
    "allow_empty_tags": ["p", "br", "span", "div", "td", "th"],
    "pad_empty_with_br": True,
    "formats": {
        "alignleft": {
            "selector": "img",
            "styles": {"float": "left", "margin": "0 20px 10px 0"},
        },
        "alignright": {
            "selector": "img",
            "styles": {"float": "right", "margin": "0 0 10px 20px"},
        },
        "aligncenter": {
            "selector": "img",
            "styles": {
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        },
    },
}
TINYMCE_DEFAULT_CONFIG["valid_styles"] = {
    "*": "text-align,color,background-color,font-size,font-weight,text-decoration,margin,margin-left,margin-right,padding"
}
# Конфигурация для блога (аналог CKEditor 5 'blog')
TINYMCE_BLOG_CONFIG = {
    "height": 800,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    "license_key": "gpl",
    # для встроенных плагинов TinyMCE
    "plugins": """
        tableofcontents accordion advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table code 
        help wordcount table lists emoticons template codesample nonbreaking toc pagebreak
    """,
    "toolbar": """
        undo redo | styles | bold italic | accordion underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist | tableofcontents | outdent indent | link image media swipergallery | 
        table | template | removeformat code fullscreen help
    """,
    # external_plugins - для кастомных плагинов
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js",
        "tableofcontents": "/static/tinymce/plugins/tableofcontents/plugin.js",
    },
    "templates": [
        {
            "title": "CTA Button",
            "description": "Centered button",
            "content": """
                <div style="display:flex; justify-content:center; margin-top:30px;">
                    <a href="#" class="button -md -dark-1 bg-accent-1 text-white" style="width:350px; text-align:center;">
                        Call to Action
                    </a>
                </div>
            """,
        },
        {
            "title": "Highlight Box",
            "description": "Highlighted content block with border and background",
            "content": """
                <div style="border: 1.5px solid #f8ebde; background: #f8f5f1; padding: 15px 20px; border-radius: 8px; margin: 30px 0;">
                    <div class="ck-content">
                        <p>Your highlighted content here...</p>
                    </div>
                </div>
            """,
        },
    ],
    # Стили для блога
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "Numbered List (mt-20)",
            "selector": "ol",
            "classes": "numbered-list mt-20",
        },
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    # Специальные ссылки для блога (аналог link decorators в CKEditor)
    "link_class_list": [
        {"title": "Normal Link", "value": ""},
        {
            "title": "CTA Button",
            "value": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Button Outline",
            "value": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
        {
            "title": "WhatsApp Button",
            "value": "whatsapp-button button -md bg-success-1 text-white",
        },
    ],
    "link_default_target": "_self",
    "target_list": [
        {"title": "Same window", "value": "_self"},
        {"title": "New window", "value": "_blank"},
    ],
    # Цвета для блога
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    "image_advtab": True,
    "image_caption": True,
    "image_toolbar": "alignleft aligncenter alignright | image",
    "automatic_uploads": True,
    "images_upload_url": "/tinymce/upload/",
    "file_picker_types": "image",
    # Таблицы с расширенными настройками
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol | tablecellprops",
    "table_appearance_options": True,
    "table_advtab": True,
    "table_cell_advtab": True,
    "table_row_advtab": True,
    "table_class_list": [
        {"title": "Default", "value": ""},
        {"title": "Compact", "value": "compact"},
        {"title": "Striped", "value": "striped"},
        {"title": "Lake Como Table", "value": "lake-como-table"},
    ],
    # Медиа (аналог mediaEmbed в CKEditor)
    "media_live_embeds": True,
    "media_dimensions": True,
    "media_poster": True,
    # Контент CSS
    "content_css": "/static/css/ckeditor-content.css",
    "content_style": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            background: #fff;
            padding: 20px 24px;
        }
        .table-of-contents {
            background: #f5f5f5;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #333;
        }
        .table-of-contents h2 {
            margin-top: 0;
        }
        .table-of-contents ul {
            list-style: none;
            padding-left: 20px;
        }
        .table-of-contents a {
            text-decoration: none;
            color: #333;
        }
        p { margin: 0 0 1em 0; }
        p.mt-20 { margin-top: 20px; }
        h1, h2, h3, h4, h5, h6 {
            color: #23282d;
            font-weight: 600;
            margin: 1.5em 0 0.5em 0;
            line-height: 1.3;
        }
        h1 { font-size: 2.2em; margin-top: 1em; }
        h2 { font-size: 1.8em; }
        h2.text-30 { font-size: 1.875em; }
        h3 { font-size: 1.5em; }
        h4 { font-size: 1.25em; }
        h5 { font-size: 1.1em; }
        h6 { font-size: 1em; font-weight: 700; }
        a { color: #0073aa; text-decoration: none; }
        a:hover { color: #005177; text-decoration: underline; }
        blockquote {
            border-left: 4px solid #0073aa;
            margin: 1.5em 0;
            padding: 0 0 0 1em;
            font-style: italic;
            color: #666;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        table td, table th {
            border: 1px solid #e1e1e1;
            padding: 8px 12px;
            text-align: left;
        }
        table th {
            background: #f9f9f9;
            font-weight: 600;
            color: #23282d;
        }
        code {
            background: #f1f1f1;
            color: #d63384;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Monaco, Consolas, monospace;
            font-size: 0.9em;
        }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.5em 0; }
        .cta-button, .cta-button-outline, .whatsapp-button {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px auto;
            text-align: center;
        }
    """,
    # Разрешенные элементы
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        br,
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style|aria-label|aria-*|title],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label],
        details[open|class|style|data-*|role|aria-*],
        summary[class|style|data-*|role|aria-*],
        ul[class|style|data-*],
        li[class|style|data-*],
        p[class|style|data-*|aria-*],
    """,
    "valid_elements": "+i[class|style|data-*],+span[class|style|data-*]",
    "valid_classes": {
        "div": (
            "table-responsive table-stack stack-item image-gallery gallery-grid gallery-item media accordion-panel "
            "accordion -simple row y-gap-20 mt-30 js-accordion "
            "col-12 accordion__item px-20 py-15 border-1 rounded-12 "
            "accordion__button d-flex items-center justify-between "
            "button text-16 text-dark-1 "
            "accordion__icon size-30 flex-center bg-light-2 rounded-full "
            "accordion__content pt-20 ck-content "
        ),
        "img": "gallery-image",
        "table": "compact striped lake-como-table table-normal",
        "span": (
            "stack-label stack-value stack-header "
            "icon-plus icon-minus text-13 "
            "text-accent-1 text-success text-warning "
            "badge tag"
        ),
        "i": ("icon-plus text-13 " "icon-minus text-13 "),
        "h2": "text-30 md:text-24",
        "p": "mt-20 mt-30 text-center",
        "ul": "list-disc mt-20",
        "ol": "numbered-list mt-20",
        "details": "accordion -simple row y-gap-20 mt-30 js-accordion",
        "summary": "button text-16 text-dark-1",
        "a": "cta-button cta-button-outline button -md -dark-1 bg-accent-1 text-white mt-30",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": False,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    # "contextmenu": "link image table",
    "contextmenu": False,
    "verify_html": False,
    # Сохранение переносов строк и пустых абзацев
    "forced_root_block": "p",
    "force_br_newlines": False,
    "force_p_newlines": True,
    "remove_trailing_brs": False,
    "remove_linebreaks": False,
    "convert_newlines_to_brs": False,
    "keep_styles": True,
    "entity_encoding": "raw",
    "allow_empty_tags": ["p", "br", "span", "div", "td", "th"],
    "pad_empty_with_br": True,
    "formats": {
        "alignleft": {
            "selector": "img",
            "styles": {"float": "left", "margin": "0 20px 10px 0"},
        },
        "alignright": {
            "selector": "img",
            "styles": {"float": "right", "margin": "0 0 10px 20px"},
        },
        "aligncenter": {
            "selector": "img",
            "styles": {
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        },
    },
}

# Конфигурация для туров
TINYMCE_TOUR_CONFIG = {
    "height": 800,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    "license_key": "gpl",
    # для встроенных плагинов TinyMCE
    "plugins": """
        tableofcontents accordion advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table code 
        help wordcount table lists emoticons template codesample nonbreaking toc pagebreak
    """,
    "toolbar": """
        undo redo | styles | bold italic | accordion underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist | tableofcontents | outdent indent | link image media swipergallery | 
        table | template | removeformat code fullscreen help
    """,
    # external_plugins - для кастомных плагинов
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js",
        "tableofcontents": "/static/tinymce/plugins/tableofcontents/plugin.js",
    },
    "templates": [
        {
            "title": "CTA Button",
            "description": "Centered button",
            "content": """
                <div style="display:flex; justify-content:center; margin-top:30px;">
                    <a href="#" class="button -md -dark-1 bg-accent-1 text-white" style="width:350px; text-align:center;">
                        Call to Action
                    </a>
                </div>
            """,
        },
        {
            "title": "Highlight Box",
            "description": "Highlighted content block with border and background",
            "content": """
                <div style="border: 1.5px solid #f8ebde; background: #f8f5f1; padding: 15px 20px; border-radius: 8px; margin: 30px 0;">
                    <div class="ck-content">
                        <p>Your highlighted content here...</p>
                    </div>
                </div>
            """,
        },
    ],
    # Стили для блога
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "Numbered List (mt-20)",
            "selector": "ol",
            "classes": "numbered-list mt-20",
        },
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    # Специальные ссылки для блога (аналог link decorators в CKEditor)
    "link_class_list": [
        {"title": "Normal Link", "value": ""},
        {
            "title": "CTA Button",
            "value": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Button Outline",
            "value": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
        {
            "title": "WhatsApp Button",
            "value": "whatsapp-button button -md bg-success-1 text-white",
        },
    ],
    "link_default_target": "_self",
    "target_list": [
        {"title": "Same window", "value": "_self"},
        {"title": "New window", "value": "_blank"},
    ],
    # Цвета для блога
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    # Изображения
    "image_advtab": True,
    "image_caption": True,
    "image_toolbar": "alignleft aligncenter alignright | image",
    "automatic_uploads": True,
    "images_upload_url": "/tinymce/upload/",
    "file_picker_types": "image",
    # Таблицы с расширенными настройками
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol | tablecellprops",
    "table_appearance_options": True,
    "table_advtab": True,
    "table_cell_advtab": True,
    "table_row_advtab": True,
    "table_class_list": [
        {"title": "Default", "value": ""},
        {"title": "Compact", "value": "compact"},
        {"title": "Striped", "value": "striped"},
        {"title": "Lake Como Table", "value": "lake-como-table"},
    ],
    # Медиа
    "media_live_embeds": True,
    "media_dimensions": True,
    "media_poster": True,
    # Контент CSS
    "content_css": "/static/css/ckeditor-content.css",
    "content_style": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            background: #fff;
            padding: 20px 24px;
        }
        p { margin: 0 0 1em 0; }
        p.mt-20 { margin-top: 20px; }
        h1, h2, h3, h4, h5, h6 {
            color: #23282d;
            font-weight: 600;
            margin: 1.5em 0 0.5em 0;
            line-height: 1.3;
        }
        h1 { font-size: 2.2em; margin-top: 1em; }
        h2 { font-size: 1.8em; }
        h2.text-30 { font-size: 1.875em; }
        h3 { font-size: 1.5em; }
        h4 { font-size: 1.25em; }
        h5 { font-size: 1.1em; }
        h6 { font-size: 1em; font-weight: 700; }
        a { color: #0073aa; text-decoration: none; }
        a:hover { color: #005177; text-decoration: underline; }
        blockquote {
            border-left: 4px solid #0073aa;
            margin: 1.5em 0;
            padding: 0 0 0 1em;
            font-style: italic;
            color: #666;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        table td, table th {
            border: 1px solid #e1e1e1;
            padding: 8px 12px;
            text-align: left;
        }
        table th {
            background: #f9f9f9;
            font-weight: 600;
            color: #23282d;
        }
        code {
            background: #f1f1f1;
            color: #d63384;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Monaco, Consolas, monospace;
            font-size: 0.9em;
        }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.5em 0; }
        .cta-button, .cta-button-outline, .whatsapp-button {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px auto;
            text-align: center;
        }
    """,
    # Разрешенные элементы
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        br,
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style|aria-label|aria-*|title],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label],
        details[open|class|style|data-*|role|aria-*],
        summary[class|style|data-*|role|aria-*],
        ul[class|style|data-*],
        li[class|style|data-*],
        p[class|style|data-*|aria-*],
    """,
    "valid_elements": "+i[class|style|data-*],+span[class|style|data-*]",
    "valid_classes": {
        "div": (
            "table-responsive table-stack stack-item image-gallery gallery-grid gallery-item media accordion-panel "
            "accordion -simple row y-gap-20 mt-30 js-accordion "
            "col-12 accordion__item px-20 py-15 border-1 rounded-12 "
            "accordion__button d-flex items-center justify-between "
            "button text-16 text-dark-1 "
            "accordion__icon size-30 flex-center bg-light-2 rounded-full "
            "accordion__content pt-20 ck-content "
        ),
        "img": "gallery-image",
        "table": "compact striped lake-como-table table-normal",
        "span": (
            "stack-label stack-value stack-header "
            "icon-plus icon-minus text-13 "
            "text-accent-1 text-success text-warning "
            "badge tag"
        ),
        "i": ("icon-plus text-13 " "icon-minus text-13 "),
        "h2": "text-30 md:text-24",
        "p": "mt-20 mt-30 text-center",
        "ul": "list-disc mt-20",
        "ol": "numbered-list mt-20",
        "details": "accordion -simple row y-gap-20 mt-30 js-accordion",
        "summary": "button text-16 text-dark-1",
        "a": "cta-button cta-button-outline button -md -dark-1 bg-accent-1 text-white mt-30",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": False,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    # "contextmenu": "link image table",
    "contextmenu": False,
    "verify_html": False,
    # Сохранение переносов строк и пустых абзацев
    "forced_root_block": "p",
    "force_br_newlines": False,
    "force_p_newlines": True,
    "remove_trailing_brs": False,
    "remove_linebreaks": False,
    "convert_newlines_to_brs": False,
    "keep_styles": True,
    "entity_encoding": "raw",
    "allow_empty_tags": ["p", "br", "span", "div", "td", "th"],
    "pad_empty_with_br": True,
    "formats": {
        "alignleft": {
            "selector": "img",
            "styles": {"float": "left", "margin": "0 20px 10px 0"},
        },
        "alignright": {
            "selector": "img",
            "styles": {"float": "right", "margin": "0 0 10px 20px"},
        },
        "aligncenter": {
            "selector": "img",
            "styles": {
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        },
    },
}

# Настройки загрузки файлов (аналог CKEDITOR_5_UPLOAD_PATH)
TINYMCE_UPLOAD_PATH = "blog/content/"
TINYMCE_IMAGE_UPLOAD_ENABLED = True
TINYMCE_FILE_UPLOAD_ENABLED = True
TINYMCE_ALLOWED_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "webp", "pdf", "doc", "docx"]


# Теги / изображения / пагинация
TAGGIT_CASE_INSENSITIVE = True

THUMBNAIL_FORMAT = "WEBP"
THUMBNAIL_QUALITY = 85
THUMBNAIL_PRESERVE_FORMAT = False

PAGINATE_BY = 10

FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024  # 200MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024  # 200MB

# Для больших файлов
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
MAX_IMAGE_SIZE = 200 * 1024 * 1024  # 200MB (было 50MB)

IMAGE_QUALITY = 85
MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200

THUMBNAIL_ALIASES = {
    "": {
        # Hero и слайдеры главной
        "hero_mobile": {
            "size": (640, 360),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "hero_tablet": {
            "size": (1024, 576),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "hero_desktop": {
            "size": (1920, 1080),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        # Карточки туров
        "tour_card_mobile": {
            "size": (400, 280),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "tour_card_tablet": {
            "size": (600, 420),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "tour_card_desktop": {
            "size": (800, 560),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        # Детальная страница тура (галерея)
        "tour_gallery_mobile": {
            "size": (480, 320),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "tour_gallery_tablet": {
            "size": (768, 512),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "tour_gallery_desktop": {
            "size": (1200, 800),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        "blog_card_mobile": {
            "size": (400, 300),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "blog_card_tablet": {
            "size": (600, 450),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "blog_card_desktop": {
            "size": (800, 600),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        # Блог - детальная страница
        "blog_hero_mobile": {
            "size": (640, 400),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "blog_hero_tablet": {
            "size": (1024, 640),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "blog_hero_desktop": {
            "size": (1920, 1200),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        # Команда (About page)
        "team_mobile": {
            "size": (480, 480),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        "team_tablet": {
            "size": (768, 768),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "team_desktop": {
            "size": (1024, 1024),
            "crop": "smart",
            "quality": 90,
            "format": "WEBP",
        },
        # Отзывы (Reviews)
        "review_thumb": {
            "size": (60, 60),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        "review_avatar": {
            "size": (100, 100),
            "crop": "smart",
            "quality": 85,
            "format": "WEBP",
        },
        # Миниатюры для виджетов
        "widget_thumb": {
            "size": (80, 80),
            "crop": "smart",
            "quality": 80,
            "format": "WEBP",
        },
        # OG Image для соцсетей
        "og_image": {
            "size": (1200, 630),
            "crop": "smart",
            "quality": 90,
            "format": "JPEG",
        },
    }
}

# Включите кэш миниатюр
THUMBNAIL_CACHE_DIMENSIONS = True
THUMBNAIL_CACHE = "default"
