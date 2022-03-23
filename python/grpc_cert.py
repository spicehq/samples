import os
from pathlib import Path
import ssl
import tempfile
import urllib.request


def get_grpc_cert():
    # Check for gRPC certificates
    if not (Path(Path.cwd().absolute().anchor) / 'usr' / 'share' / 'grpc' / 'roots.pem').exists():
        env_name = 'GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'
        if env_name not in os.environ or not Path(os.environ[env_name]).exists():
            tls_root_certs = Path(tempfile.gettempdir()) / 'roots.pem'
            if not Path(tls_root_certs).exists():
                print('Downloading gRPC certificates')
                ssl._create_default_https_context = ssl._create_unverified_context
                urllib.request.urlretrieve('https://pki.google.com/roots.pem', str(tls_root_certs))
            os.environ[env_name] = str(tls_root_certs)
