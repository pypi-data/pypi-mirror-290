from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gsheet_api_handler",  # Reemplaza con el nombre de tu paquete
    version="0.1.3",  # Número de versión de tu paquete
    author="Fabrizzio Rutigliano",  # Tu nombre
    author_email="fabrizziorutigliano@gmail.com",  # Tu correo electrónico
    description="Paquete para la autenticación y lectura de datos desde Google Sheets con manejo de errores integrado pensado para Google Colab.",  # Breve descripción de lo que hace tu paquete
    long_description=open("README.md").read(),  # Usar el contenido de README.md como descripción larga
    long_description_content_type="text/markdown",  # Especifica que el README está en formato Markdown
    #url="https://github.com/tu_usuario/my_package",  # URL del repositorio del proyecto (GitHub, por ejemplo)
    packages=find_packages(),  # Encuentra y lista todos los paquetes automáticamente
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",  # Reemplaza con la licencia que estás usando
    #    "Operating System :: OS Independent",
    #],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    install_requires=[
        "gspread",  # Lista aquí las dependencias de tu paquete
        "google-auth"
    ],
    include_package_data=True,  # Incluye archivos adicionales especificados en MANIFEST.in
    package_data={
        # Incluir archivos adicionales dentro de los paquetes, si es necesario
        # "": ["*.txt", "*.md"],
    },
    entry_points={
        # Si tu paquete incluye scripts ejecutables
        # "console_scripts": [
        #     "nombre_comando=my_package.module:funcion_principal",
        # ],
    },
)
