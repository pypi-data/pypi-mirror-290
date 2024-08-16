from setuptools import setup, find_packages

setup(
    name="artifact-lab-3-package-2387cbf7", #Nombre de tu paquete
    version="0.1.1",  # Versión de tu paquete
    packages=find_packages(),  # Encuentra automáticamente las subcarpetas que contienen código Python
    install_requires=[  # Lista de dependencias de tu paquete
        "requests",  # Especifica que tu paquete depende de requests
    ],
    entry_points={  # Define puntos de entrada para ejecutar tu código como un script
        'console_scripts': [
            'send-env=your_module_name:send_env_variables',  # 'send-env' será el comando ejecutable
        ],
    },
    author="Tu Nombre",  # Tu nombre como autor del paquete
    author_email="tuemail@example.com",  # Tu correo electrónico
    description="A package to send environment variables to a specified URL.",  # Descripción del paquete
    url="https://github.com/tuusuario/env_sender",  # URL del proyecto (puede ser un repo en GitHub, por ejemplo)
    classifiers=[  # Clasificadores que ayudan a otros a encontrar tu proyecto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
