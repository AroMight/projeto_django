from .environment import BASE_DIR

STATICFILES_DIRS = [
    BASE_DIR / 'global_static',
]  # Outros caminhos pro Django procurar arquivos estáticos

STATIC_URL = 'static/'  # url em que os arquivos estáticos serão servidos
# onde os arquivos estáticos serão armazenados. Obs: Comando COLLECTSTATIC
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'  # url em que os arquivos de mídia serão servidos
MEDIA_ROOT = BASE_DIR / 'media'  # onde os arquivos de midia serão armazenados.
